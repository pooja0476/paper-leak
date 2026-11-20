import json
import pymupdf
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uuid
from datetime import datetime
def extract_questions(pdf_name):
    pdf = pymupdf.open(pdf_name)
    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    questions = re.findall(
    r'(?im)^\s*(?:Q(?:uestion)?\s*\.?\s*\d+|\d+\s*[.)])\s*(.*?)(?=^\s*(?:Q(?:uestion)?\s*\.?\s*\d+|\d+\s*[.)])\s*|$)',
    text,
    re.S
)

    return [q.strip().replace("\n", " ") for q in questions if q.strip()]


reference_questions = extract_questions("sample.pdf")
suspicious_questions = extract_questions("suspicious.pdf")

print("REFERENCE QUESTIONS:", reference_questions)
print("\nQUESTION MATCHING RESULTS\n")

vectorizer = TfidfVectorizer(stop_words="english")

all_questions = reference_questions + suspicious_questions
tfidf_matrix = vectorizer.fit_transform(all_questions)

results = []
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

    print("Suspicious Question:", suspicious)
    print("Closest Reference Question:", best_match)
    print("Similarity:", round(best_score, 2), "%")

    if best_score >= 70:
        status = "Possible match - Manual review required"
        alert_id = f"ALERT-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:8].upper()}"
    else:
        status = "No strong match"
        alert_id = None

    print("Status:", status)

    results.append({
    "Alert ID": alert_id,
    "Reference PDF": "sample.pdf",
    "Suspicious PDF": "suspicious.pdf",
    "Evidence Type": "PDF document comparison",
    "Suspicious Question": suspicious,
    "Closest Reference Question": best_match,
    "Similarity": round(best_score, 2),
    "Status": status
})

    print("-" * 50)
with open("matching_results.txt", "w", encoding="utf-8") as file:
    for result in results:
        file.write(str(result) + "\n\n")

print("\nMatching results saved successfully!")
with open("matching_results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print("JSON results saved successfully!")