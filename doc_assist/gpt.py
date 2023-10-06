import openai


def gpt_request(system, prompt):
    try:
        # time.sleep(SLEEP_TIME)
        messages = [
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

        reply = chat.choices[0].message.content
        return reply
    except Exception as e:
        print(f'Hit issue with Open AI API: {e}')
        print('Trying again...')
        return gpt_request(system, prompt)
