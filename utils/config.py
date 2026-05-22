import os, subprocess, yaml
from pathlib import Path
from typing import Optional, List, Tuple
from dotenv import load_dotenv

# Load .env explicitly from the project root
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"
SUPPORTED_PROVIDERS = ["gemini", "openai", "anthropic", "openrouter", "ollama", "mock"]

def _load_cfg() -> dict:
    try:
        if CONFIG_PATH.exists():
            return yaml.safe_load(CONFIG_PATH.read_text()) or {}
    except Exception:
        pass
    return {}

def get_api_key(provider: str) -> Optional[str]:
    """Get key from ENV or config.yaml providers section."""
    env_map = {"gemini": "GOOGLE_API_KEY", "openrouter": "OPENROUTER_API_KEY", "openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
    key = os.getenv(env_map.get(provider, ""))
    if key: return key
    if provider == "openrouter":
        key = os.getenv("OPEN_ROUTER_GEMMA_26B_FREE")
        if key: return key
    return _load_cfg().get("providers", {}).get(provider, {}).get("default")

def get_base_url(provider: str) -> Optional[str]:
    """Get base_url (e.g. for Ollama)."""
    return _load_cfg().get("providers", {}).get(provider, {}).get("base_url")

def get_default_key_name(provider: str) -> str:
    """Return default key name."""
    return "default"

def get_configured_models() -> List[Tuple[str, str, str]]:
    """Returns (provider, label, model_name) for active models."""
    cfg = _load_cfg()
    models = []
    for provider, model_list in cfg.get("models", {}).items():
        if get_api_key(provider):
            for m in model_list:
                models.append((provider, m.get("label", m["name"]), m["name"]))
    try:
        res = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0:
            for line in res.stdout.strip().split("\n")[1:]:
                if line.strip():
                    name = line.split()[0]
                    models.append(("ollama", f"Ollama: {name}", name))
    except Exception: pass
    if not models: models.append(("mock", "Mock Test", "test"))
    return models

def get_default_provider() -> str: return _load_cfg().get("defaults", {}).get("provider", "gemini")
def get_default_model() -> str: return _load_cfg().get("defaults", {}).get("model", "gemini-2.0-flash")

def is_provider_configured(provider: str) -> bool:
    if provider in ["ollama", "mock"]: return True
    return get_api_key(provider) is not None
