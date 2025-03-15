import openai
from app.models.tenant import get_tenant_config

def get_ai_response(tenant_id, user_message):
    """Generate AI response based on tenant-specific settings."""
    tenant_config = get_tenant_config(tenant_id)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": tenant_config["ai_prompt"]},
                  {"role": "user", "content": user_message}]
    )
    
    return response["choices"][0]["message"]["content"]
