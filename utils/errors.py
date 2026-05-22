from typing import Any

def format_error_message(error: Exception | str) -> str:
    """
    Standardizes error messages across different providers (OpenAI, Anthropic, Gemini, Ollama)
    and wraps them in bold red Rich markup for consistent display in the TUI.
    
    Translates technical HTTP codes and transport errors into human-readable instructions.
    """
    error_str = str(error)
    
    # Common error cleanup/translation logic
    if "401" in error_str or "unauthorized" in error_str.lower():
        msg = "Authentication Failed: Please check your API key in config.yaml."
    elif "404" in error_str or "not found" in error_str.lower():
        msg = "Resource Not Found: The selected model or endpoint is unavailable."
    elif "connection" in error_str.lower() or "503" in error_str:
        msg = "Connection Error: Backend service (Ollama/Provider) is unreachable."
    elif "rate limit" in error_str.lower() or "429" in error_str:
        msg = "Rate Limit Exceeded: Too many requests. Please wait a moment."
    else:
        # Generic fallback, cleaning up potential tracebacks or tech-heavy strings
        msg = f"System Error: {error_str}"

    return f"[bold red]❌ {msg}[/]"
