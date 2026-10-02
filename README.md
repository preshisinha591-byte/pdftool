# pdftool

Convert Word documents and many other formats to PDF — via web UI or CLI.

**Supported:** `.doc .docx .odt .rtf .xls .xlsx .ods .ppt .pptx .odp .csv .txt .md .html .json .xml`, code files, and images (`.png .jpg .gif .bmp .tiff .webp`).

## Setup
```bash
pip install -r requirements.txt
# Recommended for best fidelity & legacy formats (.doc, .ppt, .rtf, .odt ...):
sudo apt install libreoffice     # or install LibreOffice on Windows/macOS
```
If LibreOffice is installed it's used automatically; otherwise built-in Python converters handle `.docx`, `.xlsx`, `.csv`, `.html`, text and images.

## Use
- Web: `python app.py` → open http://localhost:5000, drop files, download PDF (multiple files → ZIP).
- CLI: `python converter.py report.docx data.xlsx photo.jpg`
