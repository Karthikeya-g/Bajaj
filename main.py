from fastapi import FastAPI, HTTPException
from schemas import BillExtractionRequest, BillExtractionResponse
from extractor import process_bill_with_gemini
import uvicorn

app = FastAPI(title="Bajaj Health Datathon API")

@app.post("/extract-bill-data", response_model=BillExtractionResponse)
async def extract_bill_data(request: BillExtractionRequest):
    """
    Accepts a document URL and returns extracted bill line items.
    """
    if not request.document:
        raise HTTPException(status_code=400, detail="Document URL is mandatory")
    
    # Process the document
    result = process_bill_with_gemini(request.document)
    
    if not result.is_success:
        # Log the error internally here if needed
        # We return 200 OK even on logical failure, but is_success=False (as per common API patterns)
        # OR you can raise 500 if strict HTTP codes are preferred.
        return result
        
    return result

if __name__ == "__main__":
    # Host 0.0.0.0 is important for deployment (e.g. Docker/Render)
    uvicorn.run(app, host="0.0.0.0", port=8000)
