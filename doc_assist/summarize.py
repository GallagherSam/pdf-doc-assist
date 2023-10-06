from doc_assist.gpt import gpt_request


def summarize(pdf, page):
    system_summary_prompt = "Summarize the following prompt by writing a 3 sentence paragraph. Write it in new words, without referring to prompt."
    page_content = pdf.pages[page - 1].extract_text().replace("\n", "")
    summary = gpt_request(system_summary_prompt, page_content)
    return summary
