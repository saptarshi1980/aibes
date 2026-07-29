from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:

    def __init__(self):

        self.embedding = HuggingFaceEmbeddings(

            model_name="BAAI/bge-large-en-v1.5",

            model_kwargs={
                "device": "cpu"
            },

            encode_kwargs={
                "normalize_embeddings": True
            }
        )

    def get(self):

        return self.embedding