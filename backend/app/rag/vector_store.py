import os

from langchain_community.vectorstores import FAISS
import shutil


class VectorStore:

    def save(

        self,

        bidder_id,

        texts,

        embedding

    ):

        db = FAISS.from_texts(

            texts=texts,

            embedding=embedding

        )

        folder = f"vector_db/{bidder_id}"

        os.makedirs(folder, exist_ok=True)

        db.save_local(folder)

    def load(

        self,

        bidder_id,

        embedding

    ):

        folder = f"vector_db/{bidder_id}"

        return FAISS.load_local(

            folder,

            embedding,

            allow_dangerous_deserialization=True

        )
    
    def delete(
    self,
    bidder_id
):

        folder = f"vector_db/{bidder_id}"

        if os.path.exists(folder):

            shutil.rmtree(folder)    