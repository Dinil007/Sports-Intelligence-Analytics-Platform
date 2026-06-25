import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_results(question: str, dataframe_text: str):
    prompt = f"""
User Question:
{question}

Database Results:
{dataframe_text}

Explain these results in simple football language.
Keep the answer short and clear.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def generate_scouting_verdict(player1: str, player2: str, dataframe_text: str) -> str:
    prompt = f"""
You are an expert football scout. You have been given statistics for two players: {player1} and {player2}.

Player Statistics:
{dataframe_text}

Based strictly on the data provided, produce a structured scouting verdict in EXACTLY this format
(replace the bracketed placeholders, keep the emoji labels and headings):

🏆 Better Finisher: [player name]
🎯 Better Creator: [player name]
👟 Better Ball Carrier: [player name]
🛡️ Better Defender: [player name]

**Final Recommendation:**
For an attacking system, [player name] is the stronger option because [one sentence reason].
For a defensive setup, [player name] provides more defensive value because [one sentence reason].

Rules:
- Use only the player names "{player1}" or "{player2}" — no invented names.
- Base every verdict on the numbers in the data.
- Keep each reason to one concise sentence.
- Do NOT add any extra sections, bullet points, or commentary outside this format.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content