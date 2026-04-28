import anthropic
from config.schemas.brief_schema import BriefSchema

def process_brief_email(email_text: str) -> BriefSchema:
    client = anthropic.Anthropic()
    
    with open('config/prompts/intake_system.txt', 'r') as f:
        system_prompt = f.read()

    response = client.messages.create(
        model='claude-3-5-haiku-latest',
        max_tokens=2000,
        system=system_prompt,
        messages=[{
            'role': 'user',
            'content': f'Extraé los campos de este brief:\n\n{email_text}'
        }],
        tools=[{
            'name': 'save_brief',
            'description': 'Guarda el brief estructurado del cliente',
            'input_schema': BriefSchema.model_json_schema()
        }],
        tool_choice={'type': 'tool', 'name': 'save_brief'}
    )
    
    raw = response.content[0].input
    return BriefSchema(**raw)
