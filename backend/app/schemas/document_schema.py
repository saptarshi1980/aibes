from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    filename: str
    size: int