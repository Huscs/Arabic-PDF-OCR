import os
import re
import arabic_reshaper
from bidi.algorithm import get_display
from pdf2image import convert_from_path
import pytesseract
import warnings
import logging
import sys

# Suppress PDFMiner and other warnings/log messages
logging.getLogger("pdfminer").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

def extract_arabic_text_from_pdf_via_ocr(pdf_path, min_line_length=8, psm_mode=6, dpi=300, debug=False):
    """
    Extracts Arabic text from any PDF using OCR, fixes RTL and shaping.
    Returns (txt_text, html_text): processed for TXT, raw for HTML/Markdown.
    """
    txt_lines = []
    html_lines = []
    print(f"Converting PDF pages to images (DPI={dpi})...")
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return "", ""
    print(f"OCR extracting {len(images)} pages...")
    tesseract_config = f'--psm {psm_mode}'
    for idx, img in enumerate(images, 1):
        ocr_text = pytesseract.image_to_string(img, lang='ara', config=tesseract_config)
        if debug:
            print(f"\n--- RAW OCR PAGE {idx} ---\n{ocr_text}\n----------------------\n")
        lines = ocr_text.splitlines()
        for line in lines:
            line = line.strip()
            if len(line) >= min_line_length:
                # For TXT: reshape + bidi
                reshaped = arabic_reshaper.reshape(line)
                bidi_line = get_display(reshaped)
                txt_lines.append(bidi_line)
                # For HTML/MD: use raw line
                html_lines.append(line)
            else:
                txt_lines.append("")
                html_lines.append("")
        txt_lines.append("")  # Page separator
        html_lines.append("")
        print(f"Processed page {idx}/{len(images)}")
    return '\n'.join(txt_lines), '\n'.join(html_lines)

def collapse_blank_lines(text):
    """Replace 2+ blank lines with just one."""
    return re.sub(r'\n{2,}', '\n\n', text)

def remove_bidi_marks(text):
    """Remove all Unicode BiDi control characters for pure reading."""
    return re.sub(r'[\u200e\u200f\u202a\u202b\u202c\u202d\u202e]', '', text)

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def save_to_markdown(content, filename, title="Arabic OCR Output"):
    md = f"""<div dir="rtl" style="font-family:'Amiri','Noto Naskh Arabic','Arial',sans-serif;font-size:1.1em;line-height:2; white-space:pre-wrap">

# {title}

{content}

</div>
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md)

def save_to_html(content, filename, title="Arabic OCR Output"):
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Amiri&family=Noto+Naskh+Arabic&display=swap" rel="stylesheet">
    <style>
        body {{
            direction: rtl;
            font-family: 'Amiri', 'Noto Naskh Arabic', 'Arial', 'Tahoma', sans-serif;
            background: #f5f5f5;
            color: #222;
            margin: 2em auto;
            max-width: 900px;
            line-height: 2;
            font-size: 1.25em;
            padding: 2em;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        }}
        .arabic-content {{
            direction: rtl;
            unicode-bidi: plaintext;
            white-space: pre-wrap;
            word-break: break-word;
            text-align: initial;
            background: #fff;
            padding: 1em;
            border-radius: 6px;
            border: 1px solid #ccc;
            font-family: inherit;
            font-variant-numeric: arabic-indic;
            line-height: 2;
        }}
        h1, h2, h3, h4 {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
<h1>{title}</h1>
<div class="arabic-content">
{content}
</div>
</body>
</html>"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

def main(pdf_path, debug=False):
    title = os.path.splitext(os.path.basename(pdf_path))[0]
    txt_text, html_text = extract_arabic_text_from_pdf_via_ocr(pdf_path, min_line_length=8, psm_mode=6, dpi=300, debug=debug)
    if not txt_text.strip():
        print("No text extracted. Exiting.")
        return
    txt_text = collapse_blank_lines(txt_text)
    html_text = collapse_blank_lines(html_text)
    base = os.path.splitext(pdf_path)[0]
    # Save RAW OCR lines to TXT for normal reading
    save_to_file(html_text, base + "_processing.txt")
    save_to_file(html_text, base + "_reading.txt")
    # Optionally, also save the reshaped/BiDi version for rare legacy environments
    save_to_file(txt_text, base + "_legacy_terminal.txt")
    # Markdown and HTML use the raw OCR (not bidi, not reshaped)
    save_to_markdown(html_text, base + ".md", title=title)
    save_to_html(html_text, base + ".html", title=title)
    print(f"\nDone! Files saved as:\n  {base}_processing.txt (raw)\n  {base}_reading.txt (raw)\n  {base}_legacy_terminal.txt (reshaped/bidi)\n  {base}.md\n  {base}.html\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        debug = "--debug" in sys.argv
    else:
        pdf_path = "MYPDF.pdf"  # Default
        debug = False
    main(pdf_path, debug=debug)