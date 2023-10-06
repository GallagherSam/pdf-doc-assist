# AI Assisted PDF Reader

This is a small Python utility that empowers users to read, summarize, and ask questions about PDF documents using Open AI Apis.

Here is a short video demonstrating loading, batch_summarizing, vectorizing, and asking questions about a PDF document.

[![asciicast](https://asciinema.org/a/zOOwLsk01fWDBqfMSN4NH86PX.svg)](https://asciinema.org/a/zOOwLsk01fWDBqfMSN4NH86PX)

## Usage Guide

To use this tool you must have an Open AI Api key, as that is the model used for both text generation and embeddings.

The environment variable `OPENAI_API_KEY` must be set to your API key for this tool to work.

1. Clone down the repository locally.
2. (Optional, but recommended) Setup a virtual python environment. `virtualenv venv && source venv/bin/activate`
3. Install the Python requirements with `pip install -r requirements.txt`.
4. Drop a PDF you want to read in the same directory. (Can be anywhere on your filesystem, but local is easier)
5. Run the tool `python doc_assist.py`

After these steps you will have a prompt called `doc assist:` you can use to interact with your documents.

## Tool Commands

### load

`doc assist: load <path_to_pdf_file>`

This loads the PDF file into memory and is the required first step.

### read

`doc assist: read <page_num>`

This reads the text of a given page of the PDF document, and is useful to quickly inspect pages on the fly.

### summarize

`doc assist: summarize <page_num>`

Generates a short summary for a specific page.

### batch_summarize

`doc assist: batch_summarize <start_page> <end_page>`

`start_page` and `end_page` are optional. If not specified the entire document is used.

This uses a MapReduce system to iteratively generate summaries of each page, and then generate holistic summaries from there.

### vectorize

`doc assist: vectorize`

This creates a ChromaDB collection for the PDF document, creates embeddings for the document pages, and persists the content for later use.

### ask

`doc assist: ask <query>`

Ask questions about the content of the PDF document. `vectorize` must be run first.
