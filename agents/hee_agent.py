import os
import json
import anthropic
from agents.base_agent import run_with_retry
from config.supabase_client import supabase

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_email_internal(client_id: str, objective: str):
    """
    Core logic for email generation.
    """
    # 1. Fetch client data from Supabase
    client_res = supabase.table("clients").select("*").eq("id", client_id).single().execute()
    if not client_res.data:
        raise ValueError(f"Client {client_id} not found")
    
    client_data = client_res.data
    
    # 2. Read system prompt
    with open("config/prompts/hee_system.txt", "r") as f:
        system_prompt = f.read().format(
            industry=client_data.get("industry", "Agency"),
            target_audience=client_data.get("target_audience", "Business owners"),
            brand_voice=client_data.get("brand_voice", "Professional and friendly"),
            objective=objective
        )

    # 3. Call Anthropic
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"Generate a {objective} email for {client_data['name']}. Return ONLY JSON."}
        ]
    )

    # 4. Parse response
    content = message.content[0].text
    try:
        # Try to find JSON in the response if it's not pure
        if "{" in content:
            content = content[content.find("{"):content.rfind("}")+1]
        return json.loads(content)
    except Exception as e:
        print(f"Failed to parse JSON: {content}")
        raise e

def generate_email(client_id: str, objective: str):
    """
    Public method wrapped with retry and logging.
    """
    return run_with_retry(
        generate_email_internal,
        "hee",
        client_id,
        objective=objective
    )

if __name__ == "__main__":
    # Test run
    # Replace with a real client ID from your Supabase
    TEST_CLIENT_ID = "61ed6000-7354-4f26-a5bd-5c679f521326"
    res = generate_email(TEST_CLIENT_ID, "Welcome sequence")
    print(json.dumps(res, indent=2))
