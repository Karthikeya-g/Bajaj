import os
import requests
import google.generativeai as genai
import tempfile
import json
from schemas import BillExtractionResponse, TokenUsage, ExtractionData, PageLineItems
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def download_file(url: str) -> str:
    """Downloads the document from the provided URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Determine extension or default to .pdf
        ext = ".pdf"
        if ".jpg" in url.lower() or ".jpeg" in url.lower(): ext = ".jpg"
        if ".png" in url.lower(): ext = ".png"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            for chunk in response.iter_content(chunk_size=8192):
                tmp.write(chunk)
            return tmp.name
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")

def process_bill_with_gemini(document_url: str) -> BillExtractionResponse:
    file_path = None
    try:
        # 1. Download File
        file_path = download_file(document_url)
        
        # 2. Upload to Gemini
        # Gemini 1.5 Flash is efficient for document extraction
        model = genai.GenerativeModel('gemini-1.5-flash')
        uploaded_file = genai.upload_file(path=file_path, display_name="Invoice")
        
        # 3. The Prompt (Critical for Double Counting Logic)
        prompt = """
        You are an expert medical bill auditor. Extract line items from this invoice document into JSON format.

        CRITICAL EXTRACTION RULES:
        1. **Identify Page Type**: Classify each page as 'Bill Detail', 'Final Bill' (Summary), or 'Pharmacy'.
        2. **No Double Counting**: 
           - Do NOT extract "Total", "Subtotal", "Balance Due", or "Amount Paid" lines as bill items.
           - Only extract the individual services/medicines listed.
        3. **Data Precision**:
           - item_amount: Must be the NET amount (after discount, before tax if split).
           - item_quantity: If missing, default to 1.0.
           - item_rate: If missing, infer from amount/quantity.

        OUTPUT FORMAT (Strict JSON):
        {
          "pagewise_line_items": [
            {
              "page_no": "1",
              "page_type": "Bill Detail",
              "bill_items": [
                {
                  "item_name": "Bed Charges",
                  "item_amount": 500.0,
                  "item_rate": 500.0,
                  "item_quantity": 1.0
                }
              ]
            }
          ]
        }
        """

        # 4. Generate Content (Force JSON mode)
        response = model.generate_content(
            [uploaded_file, prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        
        # 5. Parse Output
        try:
            parsed_json = json.loads(response.text)
        except json.JSONDecodeError:
            raise Exception("AI model returned invalid JSON")

        # 6. Post-Processing & Total Calculation
        pagewise_items = parsed_json.get("pagewise_line_items", [])
        total_count = sum(len(page.get("bill_items", [])) for page in pagewise_items)

        # 7. Construct Response
        usage = response.usage_metadata
        
        return BillExtractionResponse(
            is_success=True,
            token_usage=TokenUsage(
                total_tokens=usage.total_token_count,
                input_tokens=usage.prompt_token_count,
                output_tokens=usage.candidates_token_count
            ),
            data=ExtractionData(
                pagewise_line_items=pagewise_items,
                total_item_count=total_count
            )
        )

    except Exception as e:
        # Error Handling
        return BillExtractionResponse(
            is_success=False,
            token_usage=TokenUsage(total_tokens=0, input_tokens=0, output_tokens=0),
            error_message=str(e)
        )
    finally:
        # Cleanup temp file
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
