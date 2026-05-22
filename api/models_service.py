import yaml
import httpx
from pathlib import Path
from typing import List, Dict, Any
from api.schemas import ProviderOptions, ModelOption

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"

def _load_cfg() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    try:
        content = CONFIG_PATH.read_text(encoding="utf-8")
        return yaml.safe_load(content) or {}
    except Exception:
        return {}

async def get_available_models() -> List[ProviderOptions]:
    cfg = _load_cfg()
    providers_cfg = cfg.get("providers", {})
    available_providers = []

    # Process standard providers
    for provider in ["openai", "anthropic", "gemini"]:
        p_cfg = providers_cfg.get(provider, {})
        api_key = p_cfg.get("api_key")
        if api_key and str(api_key).strip():
            models = [
                ModelOption(id=m["id"], label=m.get("label", m["id"])) 
                for m in p_cfg.get("models", [])
            ]
            if models:
                available_providers.append(ProviderOptions(provider=provider, models=models))

    # Process OpenRouter
    or_cfg = providers_cfg.get("openrouter", {})
    or_models = []
    for m in or_cfg.get("models", []):
        api_key = m.get("api_key")
        if api_key and str(api_key).strip():
            or_models.append(ModelOption(id=m["id"], label=m.get("label", m["id"])))
    if or_models:
        available_providers.append(ProviderOptions(provider="openrouter", models=or_models))

    # Process Ollama (async fetch)
    ollama_cfg = providers_cfg.get("ollama", {})
    base_url = ollama_cfg.get("base_url")
    if base_url:
        ollama_models = []
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.get(f"{base_url.rstrip('/')}/api/tags")
                response.raise_for_status()
                data = response.json()
                for model in data.get("models", []):
                    name = model.get("name")
                    if name:
                        ollama_models.append(ModelOption(id=name, label=f"Ollama: {name}"))
        except (httpx.RequestError, ValueError, KeyError):
            pass # Gracefully handle offline Ollama or parse errors
        
        # We can append Ollama even if empty, or only if models exist. The plan implies we return [] for Ollama on error.
        # So we include Ollama with whatever we found (even empty).
        available_providers.append(ProviderOptions(provider="ollama", models=ollama_models))

    return available_providers
