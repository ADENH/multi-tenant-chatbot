import openai
import os
from app.database import mongo_db

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_ai(tenant_id, message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": f"You are a chatbot for Tenant {tenant_id}"},
                  {"role": "user", "content": message}]
    )
    chat_response = response["choices"][0]["message"]["content"]
    
    # Save chat log
    mongo_db.chats.insert_one({
        "tenant_id": tenant_id,
        "message": message,
        "response": chat_response
    })
    
    return chat_response
