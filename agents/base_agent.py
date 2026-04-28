import time
import hashlib
import anthropic
from functools import wraps

MAX_RETRIES = 3
RETRY_DELAYS = [2, 5, 15]

from config.supabase_client import supabase
import os

def log_agent(agent_type: str, client_id: str, kwargs: dict, result, prompt_hash: str, duration: int, status: str, error: str = None):
    """
    Logs agent activity to Supabase agent_logs table.
    """
    agency_id = os.getenv("DEFAULT_AGENCY_ID")
    
    # Extract token usage if available in result (assuming Anthropic response format)
    tokens_in = getattr(result, 'usage', {}).input_tokens if hasattr(result, 'usage') else 0
    tokens_out = getattr(result, 'usage', {}).output_tokens if hasattr(result, 'usage') else 0
    model_used = getattr(result, 'model', 'unknown') if hasattr(result, 'model') else 'unknown'

    log_data = {
        "agency_id": agency_id,
        "agent_type": agent_type,
        "client_id": client_id if client_id and len(client_id) == 36 else None, # Only if it's a UUID
        "input_data": kwargs,
        "output_data": str(result) if result else None,
        "model_used": model_used,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "prompt_hash": prompt_hash,
        "duration_ms": duration,
        "status": status,
        "error_msg": error
    }
    
    try:
        supabase.table("agent_logs").insert(log_data).execute()
        print(f"[LOG] {agent_type} logged to Supabase.")
    except Exception as e:
        print(f"[ERROR] Failed to log agent to Supabase: {e}")

def run_with_retry(agent_fn, agent_type: str, client_id: str, **kwargs):
    # Read first 8 characters of md5 hash of system prompt
    try:
        with open(f'config/prompts/{agent_type}_system.txt', 'rb') as f:
            prompt_hash = hashlib.md5(f.read()).hexdigest()[:8]
    except FileNotFoundError:
        prompt_hash = "unknown"

    start = time.time()

    for attempt in range(MAX_RETRIES):
        try:
            result = agent_fn(client_id=client_id, **kwargs)
            log_agent(agent_type, client_id, kwargs, result, prompt_hash, int((time.time() - start) * 1000), 'success')
            return result

        except anthropic.RateLimitError:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAYS[attempt])
                continue
            log_agent(agent_type, client_id, kwargs, None, prompt_hash, int((time.time() - start) * 1000), 'error', 'rate_limit_exceeded')
            raise

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAYS[attempt])
                continue
            log_agent(agent_type, client_id, kwargs, None, prompt_hash, int((time.time() - start) * 1000), 'error', str(e))
            raise
