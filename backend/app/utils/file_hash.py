import hashlib
from pathlib import Path


class FileHash:

    @staticmethod
    def sha256(file_path: Path) -> str:

        sha = hashlib.sha256()

        with open(file_path, "rb") as f:

            while True:

                chunk = f.read(8192)

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()