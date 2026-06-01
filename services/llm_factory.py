import yaml
from pathlib import Path
from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"

def _load_cfg() -> dict:
    try:
        if CONFIG_PATH.exists():
            return yaml.safe_load(CONFIG_PATH.read_text()) or {}
    except Exception:
        pass
    return {}

def resolve_key(provider: str, model_id: str) -> str:
    """Resolve API key based on provider and model rules."""
    cfg = _load_cfg()
    providers_cfg = cfg.get("providers", {})
    
    if provider not in providers_cfg:
        raise ValueError(f"Provider {provider} not configured.")
        
    p_cfg = providers_cfg[provider]
    
    if provider == "openrouter":
        # Look for model-level key
        for m in p_cfg.get("models", []):
            if m.get("id") == model_id:
                api_key = m.get("api_key")
                if api_key and str(api_key).strip():
                    return str(api_key).strip()
        raise ValueError(f"API key for OpenRouter model {model_id} not found or is empty.")
    else:
        # Look for provider-level key
        api_key = p_cfg.get("api_key")
        if api_key and str(api_key).strip():
            return str(api_key).strip()
        raise ValueError(f"API key for provider {provider} not found or is empty.")

def get_base_url(provider: str) -> Optional[str]:
    cfg = _load_cfg()
    return cfg.get("providers", {}).get(provider, {}).get("base_url")

def get_chat_model(provider: str, model_id: str) -> BaseChatModel:
    """Instantiate LangChain chat model dynamically from services/providers/."""
    import importlib
    try:
        module = importlib.import_module(f"services.providers.{provider}")
        get_model = getattr(module, "get_model")
    except (ImportError, AttributeError):
        raise ValueError(f"Unsupported provider: {provider}")

    if provider == "mock":
        return get_model(model_id, "mock")
    elif provider == "ollama":
        base_url = get_base_url(provider)
        if not base_url:
            raise ValueError("base_url for ollama not found in config.yaml")
        return get_model(model_id, base_url)
    else:
        api_key = resolve_key(provider, model_id)
        return get_model(model_id, api_key)
