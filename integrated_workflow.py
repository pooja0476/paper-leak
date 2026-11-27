
import os
import re
import json
import uuid
from datetime import datetime

import cv2
import numpy as np
import pymupdf
import pytesseract

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# TESSERACT OCR LOCATION
# --------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# --------------------------------------------------
# EXTRACT TEXT FROM AN IMAGE
# --------------------------------------------------

def extract_image_text(image_path):

    image = Image.open(image_path).convert("RGB")

    image = ImageOps.grayscale(image)
    image_array = np.array(image)

    # Detect text angle
    _, thresh = cv2.threshold(
        image_array,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    coords = np.column_stack(np.where(thresh > 0))

    if len(coords) > 0:

        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        h, w = image_array.shape
        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0
        )

        image_array = cv2.warpAffine(
            image_array,
            matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=255
        )

    image = Image.fromarray(image_array)

    # Improve image quality
    image = ImageOps.autocontrast(image)

    image = image.resize(
        (image.width * 3, image.height * 3),
        Image.Resampling.LANCZOS
    )

    image = image.filter(
        ImageFilter.MedianFilter(size=3)
    )

    image = ImageEnhance.Sharpness(image).enhance(2)

    # OCR extraction
    text = pytesseract.image_to_string(
        image,
        config="--oem 3 --psm 11"
    )

    return text


# --------------------------------------------------
# EXTRACT TEXT FROM A PDF
# --------------------------------------------------

def extract_pdf_text(pdf_path):

    pdf = pymupdf.open(pdf_path)
    text = ""

    try:

        for page in pdf:

            page_text = page.get_text()

            if page_text.strip():

                text += page_text + "\n"

            else:

                # Convert scanned PDF page into image
                pix = page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2)
                )

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                page_text = pytesseract.image_to_string(
                    image,
                    config="--oem 3 --psm 6"
                )

                text += page_text + "\n"

    finally:
        pdf.close()

    return text


# --------------------------------------------------
# EXTRACT TEXT BASED ON FILE TYPE
# --------------------------------------------------

def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension in [".png", ".jpg", ".jpeg"]:

        return extract_image_text(file_path)

    elif extension == ".pdf":

        return extract_pdf_text(file_path)

    else:

        raise ValueError("Unsupported file format")


# --------------------------------------------------
# EXTRACT INDIVIDUAL QUESTIONS
# --------------------------------------------------

def extract_questions_from_text(text):

    pattern = (
        r'(?m)^\s*'
        r'(?:Q(?:uestion)?\s*#?\s*\d+\s*[.):\-]?|\d+\s*[.)])'
        r'\s*(.+?)'
        r'(?=^\s*(?:Q(?:uestion)?\s*#?\s*\d+\s*[.):\-]?|\d+\s*[.)])'
        r'\s*|\Z)'
    )

    matches = re.findall(pattern, text, re.S)

    questions = []

    for question in matches:

        question = re.sub(r'\s+', ' ', question).strip()

        if len(question) >= 10:
            questions.append(question)

    return questions


# --------------------------------------------------
# COMPARE QUESTIONS USING TF-IDF
# --------------------------------------------------

def compare_questions(
    reference_questions,
    suspicious_questions,
    reference_file,
    suspicious_file
):

    if not reference_questions:
        raise ValueError("No reference questions found.")

    if not suspicious_questions:
        raise ValueError("No suspicious questions found.")

    # Prepare comparison data
    all_questions = (
        reference_questions + suspicious_questions
    )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(all_questions)

    results = []
    alerts = []

    for i, suspicious in enumerate(suspicious_questions):

        suspicious_vector = tfidf_matrix[
            len(reference_questions) + i
        ]

        best_score = 0
        best_match = ""

        for j, reference in enumerate(reference_questions):

            reference_vector = tfidf_matrix[j]

            score = cosine_similarity(
                suspicious_vector,
                reference_vector
            )[0][0] * 100

            if score > best_score:

                best_score = score
                best_match = reference

        # Alert threshold
        if best_score >= 70:

            status = "Possible match - Manual review required"

            alert_id = (
                f"ALERT-{datetime.now():%Y%m%d}-"
                f"{uuid.uuid4().hex[:8].upper()}"
            )

        else:

            status = "No strong match"
            alert_id = None

        result = {

            "Reference File": reference_file,
            "Suspicious File": suspicious_file,
            "Detection Time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Alert ID": alert_id,
            "Suspicious Question": suspicious,
            "Closest Reference Question": best_match,
            "Similarity": float(round(best_score, 2)),
            "Status": status

        }

        results.append(result)

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


# --------------------------------------------------
# MAIN INTEGRATED WORKFLOW
# --------------------------------------------------

def run_workflow():

    print("\n===================================")
    print("PAPER-LEAK SENTINEL")
    print("OCR AND QUESTION MATCHING")
    print("===================================")

    reference_file = input(
        "\nEnter reference PDF filename: "
    ).strip().strip('"')

    suspicious_file = input(
        "Enter suspicious image/PDF filename: "
    ).strip().strip('"')

    if not os.path.isfile(reference_file):

        print("Reference file not found!")
        return

    if not os.path.isfile(suspicious_file):

        print("Suspicious file not found!")
        return

    allowed_formats = [
        ".pdf", ".png", ".jpg", ".jpeg"
    ]

    if os.path.splitext(reference_file)[1].lower() not in allowed_formats:

        print("Unsupported reference file format!")
        return

    if os.path.splitext(suspicious_file)[1].lower() not in allowed_formats:

        print("Unsupported suspicious file format!")
        return

    try:

        print("\nExtracting text...")

        reference_text = extract_text(reference_file)
        suspicious_text = extract_text(suspicious_file)

    except Exception as error:

        print("Error while processing files:", error)
        return

    if not reference_text.strip():

        print("No readable text in reference file!")
        return

    if not suspicious_text.strip():

        print("No readable text in suspicious file!")
        return

    print("Text extraction completed!")

    reference_questions = extract_questions_from_text(
        reference_text
    )

    suspicious_questions = extract_questions_from_text(
        suspicious_text
    )

    print(
        "\nReference questions found:",
        len(reference_questions)
    )

    print(
        "Suspicious questions found:",
        len(suspicious_questions)
    )

    if not reference_questions:

        print("No reference questions detected.")
        return

    if not suspicious_questions:

        print("No valid suspicious questions detected.")
        return

    try:

        results, alerts = compare_questions(
            reference_questions,
            suspicious_questions,
            reference_file,
            suspicious_file
        )

    except ValueError as error:

        print("Comparison error:", error)
        return

    print("\n===================================")
    print("COMPARISON RESULTS")
    print("===================================")

    for result in results:

        print("\nSuspicious Question:")
        print(result["Suspicious Question"])

        print(
            "Closest Reference:",
            result["Closest Reference Question"]
        )

        print(
            "Similarity:",
            result["Similarity"],
            "%"
        )

        print("Status:", result["Status"])

    # Save results
    with open(
        "integrated_results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    with open(
        "integrated_alerts.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            alerts,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n===================================")
    print("WORKFLOW SUMMARY")
    print("===================================")

    print("Questions compared:", len(results))
    print("Possible matches:", len(alerts))

    print("\nResults saved: integrated_results.json")
    print("Alerts saved: integrated_alerts.json")

    print("\nManual review is required for possible matches.")


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    run_workflow()
