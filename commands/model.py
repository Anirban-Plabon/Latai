from services.session import session

def execute(args: str) -> str:
    if not args or "/" not in args:
        return "Error: Usage /model <provider>/<model-name>"
    
    parts = args.split("/", 1)
    if len(parts) != 2:
        return "Error: Usage /model <provider>/<model-name>"
        
    provider, model_name = parts
    
    valid_providers = ["gemini", "openai", "anthropic", "openrouter"]
    if provider not in valid_providers:
        return f"Error: Invalid provider. Must be one of {', '.join(valid_providers)}"
        
    session.set_model(provider, model_name)
    return f"Model swapped to {provider}/{model_name}"
