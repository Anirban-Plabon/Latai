"""Runtime guard for tree-sitter language availability."""

from functools import lru_cache


@lru_cache(maxsize=None)
def is_language_supported(language: str | None) -> bool:
    """Return True only if the language grammar is actually loadable at runtime.

    TextArea.available_languages returns BUILTIN_LANGUAGES unconditionally,
    even when the grammar binary is not installed. This function probes the
    actual runtime availability via textual._tree_sitter.get_language().
    """
    if not language or language == "plain":
        return False
    try:
        from textual._tree_sitter import get_language
        return get_language(language) is not None
    except Exception:
        return False


def safe_language(language: str | None) -> str | None:
    """Return language if its tree-sitter grammar is available, else None."""
    return language if is_language_supported(language) else None
