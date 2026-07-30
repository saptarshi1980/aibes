from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


class RAGRetriever:

    def __init__(self):

        self.embedding = EmbeddingService()

        self.vector = VectorStore()
        
    def delete_embeddings(
    self,
    bidder_id
):

        self.vector.delete(
            bidder_id
        )    

    def retrieve(
        self,
        bidder_id,
        criterion,
        k=5
    ):

        embedding = self.embedding.get()

        db = self.vector.load(
            bidder_id,
            embedding
        )

        query = f"""
Title:
{criterion.title}

Description:
{criterion.description}

Evidence Required:
{criterion.evidence_required}
"""

        docs = db.similarity_search(
            query,
            k=k
        )

        return "\n\n".join(
            doc.page_content
            for doc in docs
        )