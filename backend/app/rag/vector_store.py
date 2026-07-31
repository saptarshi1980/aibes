import os
import shutil
import time

from langchain_community.vectorstores import FAISS


class VectorStore:

    def save(
        self,
        bidder_id,
        texts,
        embedding
    ):

        print("Starting FAISS.from_texts()")

        t1 = time.time()

        db = FAISS.from_texts(
            texts=texts,
            embedding=embedding
        )

        print(
            "Embedding completed in",
            round(time.time() - t1, 2),
            "seconds"
        )

        folder = f"vector_db/{bidder_id}"

        os.makedirs(folder, exist_ok=True)

        t2 = time.time()

        db.save_local(folder)

        print(
            "FAISS save completed in",
            round(time.time() - t2, 2),
            "seconds"
        )
        
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