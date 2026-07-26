from pathlib import Path
import shutil

UPLOAD_FOLDER = Path("uploads")


class DocumentService:

    @staticmethod
    def save_document(file):

        UPLOAD_FOLDER.mkdir(exist_ok=True)

        file_path = UPLOAD_FOLDER / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "filename": file.filename,
            "size": file_path.stat().st_size
        }