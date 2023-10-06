from doc_assist.gpt import gpt_request


def batch_summarize(pdf, batch_size, start_page, end_page):
    # Summarize each page
    system_summary_prompt = "Summarize the following prompt by writing a 3 sentence paragraph. Write it in new words, without referring to prompt."
    summaries = []
    for page in pdf.pages[start_page:end_page]:
        page_text = page.extract_text().replace("\n", "")
        summaries.append(
            gpt_request(system_summary_prompt, page_text)
        )

    # Initial summary reduce
    summary_batches = create_batches(summaries, batch_size)
    system_batch_summary_prompt = "Summarize the following prompt by writing a 5 sentence paragraph. Write it in new words, without referring to prompt."
    next_summaries = []
    for batch in summary_batches:
        summary_text = "\n".join(batch)
        next_summary = gpt_request(system_batch_summary_prompt, summary_text)
        next_summaries.append(next_summary)

    print('Finished individual page summaries...')

    flag = True
    n_summaries = next_summaries
    while flag:
        if len(n_summaries) == 1:
            flag = False
            break

        n_1_summaries = []
        batches = create_batches(n_summaries, batch_size)
        for batch in batches:
            summary_text = "\n".join(batch)
            next_summary = gpt_request(
                system_batch_summary_prompt, summary_text)
            n_1_summaries.append(next_summary)

        n_summaries = n_1_summaries

    return n_summaries[0]


def create_batches(list, batch_size):
    batches = []
    for i in range(0, len(list), batch_size):
        batch = list[i:i+batch_size]
        batches.append(batch)
    return batches
