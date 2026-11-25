# Paper-Leak Sentinel

**An Intelligent Examination Paper Leak Detection and Monitoring System**

Paper-Leak Sentinel is a prototype system designed to help identify potential examination paper leaks and unusual examination performance patterns. It combines Telegram monitoring, digital evidence collection, OCR-based text extraction, question similarity analysis, machine learning, and an administrative dashboard.

The system generates alerts for further investigation. An alert is an indication for human review, not proof of examination malpractice.

## 1. Problem Statement

Examination paper leaks can affect the fairness and credibility of examinations. Manually monitoring online sources and identifying suspicious examination patterns can be difficult and time-consuming.

Paper-Leak Sentinel aims to support this process by collecting digital evidence, comparing extracted question content, and identifying unusual score patterns across examination centres.

## 2. Key Features

- **Telegram Monitoring:** Monitors configured Telegram channels and collects messages and shared media.
- **Digital Evidence Collection:** Stores message details and downloaded files with SHA-256 hash verification.
- **OCR Processing:** Extracts text from images and PDF documents.
- **Question Similarity Detection:** Compares extracted questions with reference examination papers using TF-IDF and cosine similarity.
- **Anomaly Detection:** Uses Isolation Forest to identify unusual centre-wise examination performance.
- **Historical Analysis:** Compares current and historical examination results.
- **Admin Dashboard:** Displays alerts, investigations, centre analysis, historical comparisons, and system status.
- **Human Review:** Supports investigation of potential matches and unusual patterns.

## 3. System Architecture

```text
             TELEGRAM CHANNELS
                     |
                     v
        MEMBER 1: TELEGRAM MONITORING
                     |
          Messages and Media Files
                     |
                     v
          SQLite Evidence Database
                     |
              SHA-256 Hashing
                     |
                     v
        MEMBER 2: OCR AND TEXT MATCHING
                     |
          Text Extraction from Files
                     |
          Question Similarity Analysis
                     |
                     v
              Alert Results
                     |
                     |
                     v
MEMBER 3: MACHINE LEARNING       MEMBER 4: DASHBOARD
        |                              ^
        v                              |
 Centre-wise Analysis                 |
        |                              |
 Isolation Forest                     |
        |                              |
 Historical Comparison                |
        |                              |
        v                              |
   CSV Output Files                    |
        |                              |
        +----------+-------------------+
                   |
                   v
             FLASK BACKEND
                   |
                   v
          REACT ADMIN DASHBOARD
```

The Telegram-to-OCR integration currently processes collected evidence in a batch workflow. The Flask API reads generated JSON and CSV output files for dashboard display.

## 4. Technologies Used

| Component | Technologies |
|---|---|
| Programming | Python |
| Telegram Monitoring | Telethon |
| Evidence Storage | SQLite |
| File Integrity | SHA-256 |
| OCR | Tesseract OCR |
| Text Processing | TF-IDF, cosine similarity |
| Machine Learning | Scikit-learn, Isolation Forest |
| Data Processing | Pandas |
| Backend | Flask, Flask-CORS |
| Frontend | React, Vite |
| Icons | Lucide React |

## 5. Project Structure

```text
paper-leak/
|
|-- backend/
|   |-- app.py
|
|-- member1/
|   |-- database/
|   |-- src/
|   |   |-- telegram_monitor.py
|   |   |-- verify_evidence.py
|   |-- channels.txt
|   |-- README.md
|
|-- member3/
|   |-- data/
|   |   |-- current_scores.csv
|   |   |-- historical_scores.csv
|   |-- outputs/
|   |-- src/
|   |-- README.md
|
|-- Member4/
|   |-- src/
|   |   |-- main.jsx
|   |   |-- style.css
|   |-- package.json
|   |-- package-lock.json
|   |-- index.html
|
|-- integrated_workflow.py
|-- telegram_ocr_integration.py
|-- question_matching.py
|-- read_image.py
|-- read_pdf.py
|-- text_matching.py
|-- README.md
|-- .gitignore
```

## 6. Team Responsibilities

### Member 1 – Telegram Monitoring and Evidence Collection
- Telegram authentication and channel monitoring using Telethon.
- Collection of existing and newly received messages.
- Downloading image and PDF attachments.
- Storing evidence metadata in SQLite.
- Generating SHA-256 hashes and verifying file integrity.

### Member 2 – OCR and Question Similarity Detection
- Extracting text from images and PDFs.
- Processing scanned documents using OCR.
- Extracting examination questions.
- Comparing questions against reference papers using TF-IDF and cosine similarity.
- Generating possible-match results for manual review.

### Member 3 – Machine Learning and Historical Analysis
- Cleaning and validating examination datasets.
- Calculating centre-wise performance metrics.
- Detecting unusual patterns using Isolation Forest.
- Comparing current and historical examination results.
- Identifying repeated unusual patterns.

### Member 4 – Admin Dashboard
- Developing the React-based administrative dashboard.
- Displaying possible leak alerts and investigation details.
- Presenting centre-wise anomaly results.
- Displaying historical examination comparisons.
- Showing system and module status.

### Backend Integration
- Providing Flask API endpoints.
- Reading generated JSON and CSV analysis results.
- Supplying data to the React dashboard.

## 7. How to Run the Project

### Prerequisites

- Python
- Node.js and npm
- Tesseract OCR
- Git

### Step 1: Open the project

Open PowerShell in the project root directory.

### Step 2: Activate the Python environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Run the Flask backend

Open the first terminal:

```powershell
python backend\app.py
```

The backend runs at:

`http://127.0.0.1:5000`

Health endpoint:

`http://127.0.0.1:5000/api/health`

### Step 4: Run the React dashboard

Open a second terminal:

```powershell
cd Member4
npm install
npm run dev
```

Open the local URL displayed by Vite, usually:

`http://localhost:5173`

### Step 5: Run the machine learning analysis

From the project root:

```powershell
python member3\src\run_all.py
```

This generates the centre analysis CSV output files.

### Step 6: Run the OCR and integration workflows

From the project root:

```powershell
python integrated_workflow.py
```

To process collected Telegram evidence:

```powershell
python telegram_ocr_integration.py
```

These workflows generate result files used by the backend and dashboard.

### Step 7: Run Telegram monitoring

Configure Telegram API credentials in `member1/.env` and channel names in `member1/channels.txt`.

Run:

```powershell
python member1/src/telegram_monitor.py
```

Press `Ctrl + C` to stop monitoring.

To verify downloaded evidence integrity:

```powershell
python member1/src/verify_evidence.py
```

Refer to `member1/README.md` for module-specific setup instructions.

## 8. Backend API Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Backend status |
| `/api/health` | Health check |
| `/api/alerts` | Telegram and OCR results |
| `/api/centers` | Centre-wise anomaly and historical analysis |

## 9. Sample Testing and Results

The project has been tested using sample examination documents and fictional examination datasets.

- Telegram evidence integrity test: 9 files verified successfully with 0 hash failures in the recorded test.
- OCR and question matching: An exact sample question match of 100% was detected in a test comparison.
- Centre analysis: Five sample examination centres were analysed.
- Historical comparison: Centre C004 showed a sample average of 96.67 compared with its historical average of 76.00, an increase of 20.67 marks.
- Dashboard: Integrated with the local Flask API to display alert and centre analysis results.

These are prototype test results, not findings of an actual examination leak.

## 10. Limitations

- Telegram evidence-to-OCR processing currently uses a batch workflow rather than a fully automated continuous pipeline.
- The Flask backend reads generated JSON and CSV files rather than using a shared production database.
- Dashboard login is a prototype and is not production-grade authentication.
- Machine learning results depend on the quality and quantity of available examination data.
- Sample examination datasets are fictional and intended for testing.
- Similarity matches and anomaly flags require verification by authorised personnel.

## 11. Future Enhancements

- Automated continuous Telegram-to-OCR processing.
- Integration with a central database.
- Secure role-based authentication.
- Improved OCR accuracy for different document formats.
- Larger real-world datasets for model validation.
- Advanced investigation and evidence management features.
- Deployment to a secure production environment.

## 12. Security and Responsible Use

- Never upload Telegram API credentials or `.env` files to GitHub.
- Keep Telegram session files, databases, and collected evidence private.
- Use SHA-256 hashes to check whether stored evidence files have changed.
- Restrict access to sensitive examination material.
- Treat system-generated alerts as leads requiring human verification.

---

**Paper-Leak Sentinel**  
*Supporting examination integrity through intelligent monitoring, evidence analysis, and anomaly detection.*