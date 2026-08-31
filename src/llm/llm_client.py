import ollama


MODEL_NAME = "granite4.2:3b"


def generate_response(question, context):
    prompt = f"""
You are answering a question based only on the provided context.

Context:
{context}

Question:
{question}

Answer the question using the context.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]