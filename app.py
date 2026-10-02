import io, os, tempfile, zipfile
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from converter import convert, SUPPORTED

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024


@app.get("/")
def index():
    return render_template("index.html", exts=", ".join(sorted(SUPPORTED)))


@app.post("/convert")
def do_convert():
    files = [f for f in request.files.getlist("files") if f.filename]
    if not files:
        return jsonify(error="No files uploaded"), 400
    with tempfile.TemporaryDirectory() as d:
        results, errors = [], []
        for f in files:
            name = secure_filename(f.filename) or "file"
            src = Path(d) / name
            f.save(src)
            try: results.append(convert(src, Path(d) / (src.stem + ".pdf")))
            except Exception as e: errors.append(f"{f.filename}: {e}")
        if not results:
            return jsonify(error="; ".join(errors)), 400
        if len(results) == 1:
            data = io.BytesIO(results[0].read_bytes())
            return send_file(data, mimetype="application/pdf",
                             as_attachment=True, download_name=results[0].name)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            for r in results: z.write(r, r.name)
        buf.seek(0)
        return send_file(buf, mimetype="application/zip", as_attachment=True,
                         download_name="converted_pdfs.zip")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
