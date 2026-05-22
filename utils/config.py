import os, subprocess, yaml
from pathlib import Path
from typing import Optional, List, Tuple
from dotenv import load_dotenv

# Load .env explicitly from the project root
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"
SUPPORTED_PROVIDERS = ["gemini", "openai", "anthropic", "openrouter", "ollama", "mock"]

def _load_cfg() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    try:
        content = CONFIG_PATH.read_text(encoding="utf-8")
        return yaml.safe_load(content) or {}
    except Exception:
        return {}

def get_api_key(provider: str, model_id: str | None = None) -> Optional[str]:
    """Get key from config.yaml. Supports model-level resolution for openrouter."""
    cfg = _load_cfg()
    providers_cfg = cfg.get("providers", {})
    p_cfg = providers_cfg.get(provider, {})
    
    if provider == "openrouter" and model_id:
        for m in p_cfg.get("models", []):
            if m.get("id") == model_id:
                return m.get("api_key")
    
    return p_cfg.get("api_key")

def get_base_url(provider: str) -> Optional[str]:
    """Get base_url (e.g. for Ollama)."""
    return _load_cfg().get("providers", {}).get(provider, {}).get("base_url")

def get_configured_models() -> List[Tuple[str, str, str]]:
    """Returns (provider, label, model_name) for active models based on visibility rules."""
    cfg = _load_cfg()
    providers_cfg = cfg.get("providers", {})
    models = []

    # Standard Providers
    for provider in ["openai", "anthropic", "gemini"]:
        p_cfg = providers_cfg.get(provider, {})
        api_key = p_cfg.get("api_key")
        if api_key and str(api_key).strip():
            for m in p_cfg.get("models", []):
                models.append((provider, m.get("label", m["id"]), m["id"]))

    # OpenRouter (Model-level keys)
    or_cfg = providers_cfg.get("openrouter", {})
    for m in or_cfg.get("models", []):
        api_key = m.get("api_key")
        if api_key and str(api_key).strip():
            models.append(("openrouter", m.get("label", m["id"]), m["id"]))

    # Ollama (Subprocess fallback for synchronous TUI lookup)
    try:
        res = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=1)
        if res.returncode == 0:
            for line in res.stdout.strip().split("\n")[1:]:
                if line.strip():
                    parts = line.split()
                    if parts:
                        name = parts[0]
                        models.append(("ollama", f"Ollama: {name}", name))
    except Exception:
        pass

    if not models:
        models.append(("mock", "Mock Test", "test"))
    
    return models

def get_default_provider() -> str: return _load_cfg().get("defaults", {}).get("provider", "gemini")
def get_default_model() -> str: return _load_cfg().get("defaults", {}).get("model", "gemini-2.0-flash")

def is_provider_configured(provider: str) -> bool:
    if provider in ["ollama", "mock"]: return True
    return get_api_key(provider) is not None
