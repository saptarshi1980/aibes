from app.rag.document_loader import DocumentLoader
from app.rag.chunker import Chunker
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


class IndexService:

    def __init__(self):

        self.loader = DocumentLoader()

        self.chunker = Chunker()

        self.embedding = EmbeddingService()

        self.vector = VectorStore()

    def build_index(

            self,

            bidder_id,

            file_path

    ):

        print("Loading document...")

        text = self.loader.load(file_path)

        print("Characters:", len(text))

        chunks = self.chunker.split(text)

        print("Chunks:", len(chunks))

        embedding = self.embedding.get()

        print("Creating embeddings...")

        self.vector.save(

            bidder_id,

            chunks,

            embedding

        )

        print("Vector DB created successfully.")