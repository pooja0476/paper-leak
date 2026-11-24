import fitz

pdf = fitz.open("sample.pdf")

print("Extracted PDF Text:\n")

for page in pdf:
    text = page.get_text()
    print(text)

pdf.close()