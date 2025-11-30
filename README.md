# Bajaj Health Datathon - Bill Extraction Pipeline

## Problem Solved
This solution implements an AI-powered pipeline to extract line items from complex medical invoices. It addresses the challenge of "Double Counting" by utilizing a Multimodal LLM (Gemini 1.5 Flash) to classify pages into "Bill Details" vs "Final Summaries" and extracts structured data accordingly.

## Architecture
- **Framework:** FastAPI (Python)
- **AI Model:** Google Gemini 1.5 Flash (Multimodal)
- **Schema Validation:** Pydantic

## Setup Instructions
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with `GEMINI_API_KEY=...`
4. Run the server: `python main.py`

## API Usage
**Endpoint:** `POST /extract-bill-data`
**Body:** `{"document": "url_to_pdf_or_image"}`
