import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read reference PDF
reference_pdf = fitz.open("sample.pdf")
reference_text = ""

for page in reference_pdf:
    reference_text += page.get_text()

reference_pdf.close()

# Read suspicious PDF
suspicious_pdf = fitz.open("suspicious.pdf")
suspicious_text = ""

for page in suspicious_pdf:
    suspicious_text += page.get_text()

suspicious_pdf.close()

# Compare both documents
documents = [reference_text, suspicious_text]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

similarity = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[1:2]
)

score = similarity[0][0] * 100

print("Reference Paper Text:\n", reference_text)
print("\nSuspicious Paper Text:\n", suspicious_text)

print("\nText Similarity Score:", round(score, 2), "%")

if score >= 50:
    print("Possible match detected. Requires manual review.")
else:
    print("Low similarity detected.")