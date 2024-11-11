import openai
from secrets import api_key

client = openai.OpenAI(
    # This is the default and can be omitted
    api_key=api_key
)

def get_posnegs_gpt(titles):
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": (
                    " "
                )
            },
            {
                "role": "user", 
                "content": (
                    " "
                )
            }
        ]
    )

    gpt_answer = chat_completion.choices[0].message.content
    text = gpt_answer.split('\n')

    return text