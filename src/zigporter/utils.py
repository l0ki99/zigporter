def normalize_ieee(ieee: str) -> str:
    """Normalize an IEEE address to a 16-char lowercase hex string (no separators or prefix)."""
    s = ieee.lower().replace(":", "").replace("-", "")
    if s.startswith("0x"):
        s = s[2:]
    return s.zfill(16)
