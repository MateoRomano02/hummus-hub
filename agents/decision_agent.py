import os
import json
import anthropic
from agents.base_agent import run_with_retry
from config.supabase_client import supabase

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_decisions_internal(client_id: str, text: str, campaign_id: str = None):
    """
    Core logic for decision extraction.
    """
    # 1. Read system prompt
    with open("config/prompts/decision_system.txt", "r") as f:
        system_prompt = f.read()

    # 2. Call Anthropic
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"Extract decisions from this text:\n\n{text}"}
        ]
    )

    # 3. Parse response
    content = message.content[0].text
    try:
        if "[" in content:
            content = content[content.find("["):content.rfind("]")+1]
        decisions = json.loads(content)
        
        # 4. Save to Supabase
        for dec in decisions:
            supabase.table("decisions").insert({
                "agency_id": os.getenv("DEFAULT_AGENCY_ID"),
                "client_id": client_id,
                "campaign_id": campaign_id,
                "content": dec["content"],
                "context": dec.get("context"),
                "is_reversal": dec.get("is_reversal", False),
                "source": "Decision Agent"
            }).execute()
            
        return {"extracted_count": len(decisions)}
    except Exception as e:
        print(f"Failed to parse or save decisions: {content}")
        raise e

def extract_decisions(client_id: str, text: str, campaign_id: str = None):
    """
    Public method wrapped with retry and logging.
    """
    return run_with_retry(
        extract_decisions_internal,
        "decision",
        client_id,
        text=text,
        campaign_id=campaign_id
    )

if __name__ == "__main__":
    # Test run
    TEST_CLIENT_ID = "61ed6000-7354-4f26-a5bd-5c679f521326"
    sample_text = "En la reunión de hoy decidimos que el presupuesto para Meta Ads será de $1000 por mes y que el target será mujeres de 25 a 40 años."
    res = extract_decisions(TEST_CLIENT_ID, sample_text)
    print(res)
