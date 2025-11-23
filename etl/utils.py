# etl/utils.py
import re

# regex patterns (tune if needed)
USD_PRICE_RE = re.compile(r"\b(?:USD|US\$|\$)?\s*(?P<usd>[0-9]{1,3}(?:[,\.][0-9]{3})*(?:\.[0-9]+)?)\s*(?:USD)?\b", re.I)
QTY_IN_DESC_RE = re.compile(r"(?P<qty>\b[0-9]{1,6}\b)\s*(?:pcs|nos|pieces|units|set|sets)\b", re.I)
CAPACITY_RE = re.compile(r"(?P<cap>[0-9]{1,4}(?:\.[0-9]+)?\s*(?:ml|l|ltr|kg|g|mm|cm|in|inch|kw|hp))", re.I)
MATERIAL_RE = re.compile(r"\b(stainless\s*steel|steel|glass|borosilicate|opalware|plastic|wood|aluminium|brass|copper)\b", re.I)
MODEL_RE = re.compile(r"\b([A-Z0-9]{2,20}(?:[-/][A-Z0-9]{1,20})?)\b")

# unit normalization map
UNIT_MAP = {
    'pcs': 'pcs','pcs.':'pcs','pieces':'pcs','nos':'pcs','no.':'pcs','no':'pcs','units':'pcs',
    'kg':'kg','kgs':'kg','kilogram':'kg','kilograms':'kg','mt':'mt','ton':'mt','tons':'mt',
    'set':'set','sets':'set'
}

def normalize_unit(u: str) -> str:
    if not isinstance(u, str): return None
    key = u.strip().lower()
    return UNIT_MAP.get(key, key)
