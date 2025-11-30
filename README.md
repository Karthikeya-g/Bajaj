# 🧾 AI Medical Bill Extractor (Bajaj Health Datathon)

An intelligent API pipeline that extracts line-item details from complex, multi-page medical invoices. 
It uses **Google Gemini 1.5 Flash (Multimodal)** to "read" the documents and strictly handles the **Double-Counting Problem** by distinguishing between *Bill Details*, *Pharmacy*, and *Final Summaries*.

---

## 🚀 Key Features
* **Multimodal Extraction:** Uses Vision-Language Models (VLM) to understand layout context, not just text.
* **Double-Counting Prevention:** Implements logic to classify pages as `Final Bill` (Summary) vs `Bill Detail`. Summary pages are processed for context but excluded from the final line-item sum to ensure 100% accuracy.
* **Standardized Output:** Returns data in the strict JSON schema required by the problem statement.
* **Token Usage Tracking:** accurately calculates and returns input/output token counts for cost estimation.

---

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python)
* **AI Model:** Google Gemini 1.5 Flash
* **Validation:** Pydantic
* **Deployment:** Ready for Docker/Cloud Run

---

## ⚙️ Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/bajaj-bill-extractor.git](https://github.com/YOUR_USERNAME/bajaj-bill-extractor.git)
    cd bajaj-bill-extractor
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```ini
    GEMINI_API_KEY=your_google_api_key_here
    ```

4.  **Run the Server**
    ```bash
    python main.py
    ```
    *Server will start at `http://0.0.0.0:8000`*

---

## 🔌 API Documentation

### Extract Bill Data
**Endpoint:** `POST /extract-bill-data`

**Request Body:**
```json
{
  "document": "[https://hackrx.blob.core.windows.net/sample_2.png](https://hackrx.blob.core.windows.net/sample_2.png)"
}
