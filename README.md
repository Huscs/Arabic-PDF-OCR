```markdown
# PDF Arabic OCR to Text/Markdown/HTML

Extract clean, line-preserved, right-to-left Arabic text from scanned PDFs — ready for search, LLM/NLP, or beautiful reading in Markdown/HTML!

## Features

- **Robust OCR**: Uses Tesseract to extract Arabic from any scanned PDF.
- **Automatic shaping and BiDi handling**: Ensures Arabic text displays correctly in all formats.
- **Multiple Outputs**:
  - `*_processing.txt`: Raw, clean Arabic text (for LLMs or further processing)
  - `*_reading.txt`: Same as above (for easy reading)
  - `.md`: Ready-to-use Markdown, with preserved formatting and RTL display
  - `.html`: Styled HTML, beautiful in browsers and ready for sharing
- **No more broken, reversed, or disconnected Arabic** in your outputs!
- **Optimized for macOS** (works on Linux/Windows with compatible dependencies)

---


## Install

1. **Python 3.8+** (recommended: Python 3.10+)
2. **Tesseract** with Arabic language pack:
   ```sh
   brew install tesseract
   brew install tesseract-lang
   ```
   Or for Ubuntu:
   ```sh
   sudo apt install tesseract-ocr tesseract-ocr-ara
   ```
3. **Python dependencies**:
   ```sh
   pip install pytesseract pdf2image arabic_reshaper python-bidi
   ```
4. **Poppler** (for `pdf2image` PDF conversion):
   - macOS: `brew install poppler`
   - Ubuntu: `sudo apt install poppler-utils`

---

## Usage

1. Place your PDF (e.g. `book.pdf`) in the project folder.
2. Run the script:
   ```sh
   python3 app.py book.pdf
   ```
   - Add `--debug` to see raw OCR output for troubleshooting.

3. **Output files**:
   - `book_processing.txt` : Clean text for processing/LLMs
   - `book_reading.txt`    : Clean text for reading
   - `book.md`             : Markdown (with proper RTL block)
   - `book.html`           : Beautiful HTML

---

## Output Examples

**HTML/Markdown preview:**

```html
<div dir="rtl" style="font-family:'Amiri','Noto Naskh Arabic','Arial',sans-serif;font-size:1.1em;line-height:2;white-space:pre-wrap">
هذا نص عربي مستخرج من PDF!
مع الحفاظ على الاتجاه والتشكيل والسطر.
</div>
```

**TXT preview:**
```
هذا نص عربي مستخرج من PDF!
مع الحفاظ على الاتجاه والتشكيل والسطر.
```

---

## How does it work?

- Converts each PDF page to image (`pdf2image`)
- Runs Tesseract OCR in Arabic mode
- For TXT: outputs raw lines for modern editors (no reshaping needed)
- For HTML/Markdown: outputs raw lines, styled for RTL and Arabic fonts
- Optionally, can output a legacy-compatible reshaped/BiDi TXT for old terminals

---

## Customization

- **Tesseract config**: You can adjust `psm` mode or DPI in `extract_arabic_text_from_pdf_via_ocr`.
- **Styling**: Edit the HTML/Markdown CSS for your own look.
- **Multi-language**: Add more Tesseract languages as needed.

---

## Troubleshooting

- **Disconnected/broken Arabic in HTML/MD?**  
  Make sure you’re using the *raw* OCR output, not reshaped or BiDi-processed.
- **Tesseract not found?**  
  Ensure it’s installed and accessible in your system PATH.
- **PDF2Image errors?**  
  Check that `poppler` is installed.

---

## License

MIT License

---

## Credits

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pdf2image](https://github.com/Belval/pdf2image)
- [arabic_reshaper](https://github.com/mpcabd/python-arabic-reshaper)
- [python-bidi](https://github.com/MeirKriheli/python-bidi)

---

## Contributing

Pull requests and issues are welcome!

---
```
## Author

- [Hussam](https://github.com/Huscs)

```
