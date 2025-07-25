import fitz  # PyMuPDF
import json
import os

def extract_pdf_headings(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = set()
    raw_headings = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_sizes.add(span["size"])

    font_sizes = sorted(list(font_sizes), reverse=True)
    h1_threshold = font_sizes[0] - 1
    h2_threshold = font_sizes[1] - 1 if len(font_sizes) > 1 else h1_threshold - 2
    h3_threshold = font_sizes[2] - 1 if len(font_sizes) > 2 else h2_threshold - 2

    seen_headings = set()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        size = span["size"]

                        if not text or len(text) < 2:
                            continue

                        if size >= h1_threshold:
                            level = "H1"
                        elif size >= h2_threshold:
                            level = "H2"
                        elif size >= h3_threshold:
                            level = "H3"
                        else:
                            continue

                        heading_key = (text.lower(), level)
                        if heading_key in seen_headings:
                            continue
                        seen_headings.add(heading_key)

                        raw_headings.append({
                            "level": level,
                            "text": text,
                            "page": page_num + 1
                        })

    result = {
        "title": raw_headings[0]["text"] if raw_headings else "Untitled",
        "outline": raw_headings
    }

    return result


# MAIN: loop over all PDFs
input_dir = "/app/input"
output_dir = "/app/output"

for file in os.listdir(input_dir):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file.replace(".pdf", ".json"))

        print(f"📄 Processing: {file}")
        result = extract_pdf_headings(pdf_path)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved: {output_path}")
