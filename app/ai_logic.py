import os
import openai
from transformers import pipeline

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_with_openai(tenant_id: str, message: str) -> str:
    """
    Generate a response using OpenAI's Chat Completion API.
    """
    try:
        # Define the conversation messages
        messages = [
            {"role": "system", "content": f"You are a helpful assistant for tenant {tenant_id}."},
            {"role": "user", "content": message},
        ]

        # Call the OpenAI Chat Completion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the desired model (e.g., gpt-3.5-turbo or gpt-4)
            messages=messages,
            max_tokens=150,  # Limit the response length
            temperature=0.7,  # Control randomness (0.0 to 1.0)
        )

        # Extract the generated text from the assistant's response
        ai_response = response.choices[0].message["content"].strip()
        return ai_response
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {str(e)}")