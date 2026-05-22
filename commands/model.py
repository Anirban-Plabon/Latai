from utils.config import SUPPORTED_PROVIDERS
from services.session import session


def execute(args: str) -> str:
    if not args or "/" not in args:
        return "Error: Usage /model <provider>/<model-name>"

    parts = args.split("/", 1)
    if len(parts) != 2:
        return "Error: Usage /model <provider>/<model-name>"

    provider, model_name = parts

    if provider not in SUPPORTED_PROVIDERS:
        valid = ", ".join(SUPPORTED_PROVIDERS)
        return f"Error: Invalid provider. Must be one of: {valid}"

    session.set_model(provider, model_name)
    return f"Model swapped to {provider}/{model_name}"
