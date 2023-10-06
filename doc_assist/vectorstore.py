import os

import chromadb
from chromadb.utils import embedding_functions

from doc_assist.gpt import gpt_request
from doc_assist.pdf import read_page, get_title


class VectorStore:
    char_batch_size = 300

    def __init__(self):
        # Load the persistent ChromaDB store
        self.client = chromadb.PersistentClient("./chroma")
        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction()

        # Check for chroma directory
        if not os.path.exists("chroma"):
            os.makedirs("chroma")

    def vectorize(self, pdf, pdf_file_path):
        pdf_title = get_title(pdf, pdf_file_path)

        # Does the collection already exist
        existing_collections = self.client.list_collections()
        if pdf_title in [i.name for i in existing_collections]:
            print(
                f"Vectorstore collection for {pdf_title} already exists. Skipping create.")
            return

        # Create the collection
        collection = self.client.create_collection(
            pdf_title, embedding_function=self.openai_ef)

        # Chunk the data and add to the collection
        chunked_data = self._chunk_pdf(pdf)
        collection.add(
            documents=chunked_data,
            ids=[f'{i}' for i in list(range(0, len(chunked_data)))]
        )

    def query(self, pdf, pdf_file_path, prompt, num_documents=8):
        pdf_title = get_title(pdf, pdf_file_path)

        # Does the collection already exist
        existing_collections = self.client.list_collections()
        if pdf_title not in [i.name for i in existing_collections]:
            print(
                f"Vectorstore collection for document not found, did you `vectorize` first?")
            return

        # Run the query
        collection = self.client.get_collection(
            pdf_title, embedding_function=self.openai_ef)
        results = collection.query(
            query_texts=[prompt],
            n_results=num_documents
        )

        # Create context and run query
        context = "\n".join(results["documents"][0])
        system_prompt = f"Use the following as context to answer the following prompt.\n{context}"
        return gpt_request(system_prompt, prompt)

    def _chunk_pdf(self, pdf):
        content = []
        for page in pdf.pages:
            content.append(page.extract_text().replace("\n", ""))

        all_pages = "\n".join(content)

        return [all_pages[i:i+self.char_batch_size] for i in range(0, len(all_pages), self.char_batch_size)]
