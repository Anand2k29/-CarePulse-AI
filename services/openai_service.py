from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_explanation(disease, precautions, risk):
    prompt = f"""
    Explain the disease {disease} in simple language.
    Risk level: {risk}.
    Precautions: {precautions}.
    Include a disclaimer.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content