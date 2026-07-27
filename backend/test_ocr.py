from app.ocr.ocr_processor import OCRProcessor

result = OCRProcessor.extract_text(r"C:/Users/user/Downloads/promotionlist.pdf")

print(result["pages"])
print(result["text"][:1000])