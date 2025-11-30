from pydantic import BaseModel
from typing import List, Optional, Literal

# 1. Structure for a single line item
class BillItem(BaseModel):
    item_name: str
    item_amount: float
    item_rate: float
    item_quantity: float

# 2. Structure for Page-wise breakdown
class PageLineItems(BaseModel):
    page_no: str
    page_type: Literal["Bill Detail", "Final Bill", "Pharmacy", "Other"]
    bill_items: List[BillItem]

# 3. Structure for the 'data' field
class ExtractionData(BaseModel):
    pagewise_line_items: List[PageLineItems]
    total_item_count: int

# 4. Structure for Token Usage
class TokenUsage(BaseModel):
    total_tokens: int
    input_tokens: int
    output_tokens: int

# 5. The Main Response Wrapper
class BillExtractionResponse(BaseModel):
    is_success: bool
    token_usage: TokenUsage
    data: Optional[ExtractionData] = None
    error_message: Optional[str] = None

# 6. The Input Request
class BillExtractionRequest(BaseModel):
    document: str
