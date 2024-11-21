import openai
from qwerasvadf import api_key

client = openai.OpenAI(
    # This is the default and can be omitted
    api_key=api_key
)

def get_diagnosis_gpt(vci=80, wmi=70, pri=75, psi=90):
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are an assistant who tells you how to diagnose ADHD and what additional games are needed through multiple cognitive indicators of the user."
                )
            },
            {
                "role": "user", 
                "content": (
                    f"VCI: {vci}, WMI: {wmi}, PRI: {pri}, PSI: {psi}, "
                    f"Average Interaction Time: 4.2 sec\n"
                    "Diagnose ADHD according to the data."
                    "Say in 30 words."
                )
            }
        ]
    )

    gpt_answer = chat_completion.choices[0].message.content
    text = gpt_answer

    return text

if __name__ == "__main__":
    print(get_diagnosis_gpt())