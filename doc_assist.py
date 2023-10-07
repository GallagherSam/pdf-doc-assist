import cmd
import os

from doc_assist.batch_summarize import batch_summarize
from doc_assist.summarize import summarize
from doc_assist.pdf import load_pdf, read_page
from doc_assist.vectorstore import VectorStore


class DocAssist(cmd.Cmd):
    prompt = "doc assist: "
    intro = "REPL for ai assistance with documents."

    vectorstore = VectorStore()
    pdf_file_path = None
    pdf_data = None
    batch_size = 4

    # Ask questions about the document
    def do_ask(self, line):
        if self.pdf_data is not None and line:
            reply = self.vectorstore.query(
                self.pdf_data, self.pdf_file_path, line)
            print(f'\n{reply}\n')
        else:
            print(
                'Make sure to `load` the pdf document first, vectorize it, and follow `ask` with a query.')

    # Store the data into a vectorstore DB for future queries
    def do_vectorize(self, line):
        if self.pdf_data is not None:
            self.vectorstore.vectorize(self.pdf_data, self.pdf_file_path)
            print("Vectorized pdf.")
        else:
            print('Please `load` a pdf document first.')

    def help_vectorize(self):
        print('\n'.join([
            'vectorize',
            'Create embeddings and persist documents in a vectorstore for later QA analysis.'
        ]))

    # Read a specific page
    def do_read(self, page_num):
        if self.pdf_data is not None:
            if page_num:
                content = read_page(self.pdf_data, int(page_num))
                print(f'\n{content}\n')
            else:
                print("Specify a page_num to read.")
        else:
            print("Please `load` a pdf document first.")

    def help_read(self):
        print('\n'.join([
            'read [page_num]',
            'Read a given page from the pdf document. Pages start at 1.'
        ]))

    # Perform a batch summarize on the loaded pdf
    def do_batch_summarize(self, line):
        if " " in line:
            args = line.split(" ")
            start_page = args[0]
            end_page = args[1]
        else:
            start_page = None
            end_page = None

        if start_page is None:
            start_page = 1
        if end_page is None:
            end_page = len(self.pdf_data.pages)

        start_page = int(start_page) - 1
        end_page = int(end_page) - 1

        # Ensure a pdf is loaded
        if self.pdf_data is not None:
            # Check Open AI API Key
            if os.environ.get("OPENAI_API_KEY") != "":
                summary = batch_summarize(
                    self.pdf_data, self.batch_size, start_page, end_page)
                print(f'\n{summary}\n')
            else:
                print("Please set OPENAI_API_KEY environment variable.")
        else:
            print("Please `load` a pdf document first.")

    def help_batch_summarize(self):
        print('\n'.join([
            'batch_summarize [start_page] [end_page]',
            'Create a holistic summary of the document using a MapReduce algorithm. This summarizes each page independently, then generates a holistic summaries from the independent page summaries.',
            'start_page and end_page are optional. If not specified all pages are used.'
        ]))

    # Single page summary
    def do_summary(self, page):
        if self.pdf_data is not None:
            if page:
                summary = summarize(self.pdf_data, int(page))
                print(f'\n{summary}\n')
            else:
                print("Please specify a page number to summarize")
        else:
            print("Please `load` a pdf document first.")

    def help_summary(self):
        print('\n'.join([
            'summary [page_num]',
            'Generate a summary from a given page.'
        ]))

    # Load a PDF document
    def do_load(self, file_path):
        if file_path:
            # Ensure the file exists
            if os.path.exists(file_path):
                # Load the PDF
                self.pdf_file_path = file_path
                self.pdf_data = load_pdf(file_path)
                print(f"Loaded {len(self.pdf_data.pages)} pages.")
            else:
                print(f"{file_path} not found.")
        else:
            print("Specify a file path to load a PDF document.")

    def help_load(self):
        print('\n'.join([
            'load [file_path]',
            'Load the PDF document from the specified path.'
        ]))

    def do_EOF(self, line):
        return True


if __name__ == "__main__":
    DocAssist().cmdloop()
