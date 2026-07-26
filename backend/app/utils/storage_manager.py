from pathlib import Path
from uuid import UUID


class StorageManager:

    STORAGE_ROOT = Path("storage")
    TENDER_ROOT = STORAGE_ROOT / "tenders"

    @classmethod
    def get_tender_folder_name(cls, tender_id: UUID, tender_number: str):

        tender_number = (
            tender_number
            .replace("/", "_")
            .replace("\\", "_")
            .replace(" ", "_")
        )

        return f"{tender_id}_{tender_number}"

    @classmethod
    def create_tender_folder(cls, tender_id: UUID, tender_number: str):

        folder_name = cls.get_tender_folder_name(
            tender_id,
            tender_number
        )

        tender_path = cls.TENDER_ROOT / folder_name

        (tender_path / "tender_documents").mkdir(parents=True, exist_ok=True)
        (tender_path / "bidders").mkdir(parents=True, exist_ok=True)
        (tender_path / "criteria").mkdir(parents=True, exist_ok=True)
        (tender_path / "reports").mkdir(parents=True, exist_ok=True)
        (tender_path / "logs").mkdir(parents=True, exist_ok=True)

        return tender_path

    @classmethod
    def find_tender_folder(cls, tender_id: UUID):

        for folder in cls.TENDER_ROOT.iterdir():

            if folder.is_dir() and folder.name.startswith(str(tender_id)):
                return folder

        return None

    @classmethod
    def get_tender_documents_path(cls, tender_id: UUID):

        tender_folder = cls.find_tender_folder(tender_id)

        if tender_folder is None:
            raise FileNotFoundError("Tender folder not found.")

        return tender_folder / "tender_documents"