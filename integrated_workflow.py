import os
import re
import json
import uuid
from datetime import datetime

import pymupdf
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Tesseract OCR location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# Extract text from an image
def extract_image_text(image_path):
    image = Image.open(image_path)
    image = image.resize((image.width * 2, image.height * 2))

    # Convert image to grayscale
    image = ImageOps.grayscale(image)

    # Improve contrast
    image = ImageEnhance.Contrast(image).enhance(2)

    # Sharpen the image
    image = image.filter(ImageFilter.SHARPEN)

    # Extract text using OCR
    text = pytesseract.image_to_string(image, config="--oem 3 --psm 6")

    return text


# Extract text from a PDF
def extract_pdf_text(pdf_path):
    pdf = pymupdf.open(pdf_path)
    text = ""

    for page in pdf:
        text += page.get_text() + "\n"

    pdf.close()
    return text


# Extract text based on file type
def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension in [".png", ".jpg", ".jpeg"]:
        return extract_image_text(file_path)

    elif extension == ".pdf":
        return extract_pdf_text(file_path)

    else:
        raise ValueError("Unsupported file format")
        # Extract individual questions from text
def extract_questions_from_text(text):

    questions = re.findall(
        r'(?m)^\s*(?:Q(?:uestion)?\s*\.?\s*\d+|\d+\s*[.)])\s*(.*?)(?=^\s*(?:Q(?:uestion)?\s*\.?\s*\d+|\d+\s*[.)])\s*|\Z)',
        text,
        re.S
    )

    return [
        re.sub(r'\s+', ' ', q).strip()
        for q in questions if q.strip()
    ]
    
    # Compare suspicious questions with reference questions
def compare_questions(reference_questions, suspicious_questions, reference_file, suspicious_file):

    if not reference_questions:
        raise ValueError("No reference questions found.")

    if not suspicious_questions:
        raise ValueError("No suspicious questions found.")

    vectorizer = TfidfVectorizer(stop_words="english")

    all_questions = reference_questions + suspicious_questions
    tfidf_matrix = vectorizer.fit_transform(all_questions)

    results = []
    alerts = []

    for i, suspicious in enumerate(suspicious_questions):

        suspicious_vector = tfidf_matrix[len(reference_questions) + i]

        best_score = 0
        best_match = ""

        for j, reference in enumerate(reference_questions):

            reference_vector = tfidf_matrix[j]

            score = cosine_similarity(
                suspicious_vector, reference_vector
            )[0][0] * 100

            if score > best_score:
                best_score = score
                best_match = reference

        if best_score >= 70:
            status = "Possible match - Manual review required"
            alert_id = (
                f"ALERT-{datetime.now():%Y%m%d}-"
                f"{uuid.uuid4().hex[:8].upper()}"
            )
        else:
            status = "No strong match"
            alert_id = None

        results.append({
            "Reference File": reference_file,
            "Suspicious File": suspicious_file,
            "Detection Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Alert ID": alert_id,
            "Suspicious Question": suspicious,
            "Closest Reference Question": best_match,
            "Similarity": float(round(best_score, 2)),
            "Status": status
        })
        if alert_id is not None:
            alerts.append({
            "Alert ID": alert_id,
            "Reference File": reference_file,
            "Suspicious File": suspicious_file,
            "Suspicious Question": suspicious,
            "Closest Reference Question": best_match,
            "Similarity": float(round(best_score, 2)),
            "Status": status
        })

    return results, alerts
    # Main integrated workflow
def run_workflow():

    reference_file = input("Enter reference PDF filename: ")
    suspicious_file = input("Enter suspicious image/PDF filename: ")
    reference_file = reference_file.strip().strip('"')
    suspicious_file = suspicious_file.strip().strip('"')

    if not os.path.isfile(reference_file):
        print("Reference file not found! Please check the file path.")
        return

    if not os.path.isfile(suspicious_file):
        print("Suspicious file not found! Please check the file path.")
        return
    allowed_formats = [".pdf", ".png", ".jpg", ".jpeg"]

    if os.path.splitext(reference_file)[1].lower() not in allowed_formats:
        print("Unsupported reference file format!")
        return

    if os.path.splitext(suspicious_file)[1].lower() not in allowed_formats:
        print("Unsupported suspicious file format!")
        return

    try:
        reference_text = extract_text(reference_file)
        suspicious_text = extract_text(suspicious_file)

    except Exception as e:
        print("Error while processing files:", e)
        return
    
    if not reference_text.strip():
        print("No readable text found in reference file!")
        return

    if not suspicious_text.strip():
        print("No readable text found in suspicious file!")
        return
        print("\nText extraction completed!")
       
    # Extract individual questions
    reference_questions = extract_questions_from_text(reference_text)
    suspicious_questions = extract_questions_from_text(suspicious_text)
    

    print("\nReference questions found:", len(reference_questions))
    print("Suspicious questions found:", len(suspicious_questions))

    # Compare questions
    results, alerts = compare_questions(
    reference_questions,
    suspicious_questions,
    reference_file,
    suspicious_file
)

    # Display results
    for result in results:
        print("\n", result)

    # Save results
    with open("integrated_results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)
    with open("integrated_alerts.json", "w", encoding="utf-8") as file:
        json.dump(alerts, file, indent=4)

    print("\nResults saved successfully in integrated_results.json")


if __name__ == "__main__":
    run_workflow()