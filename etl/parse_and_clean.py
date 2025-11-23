# etl/parse_and_clean.py
"""
Reads Sample Data Excel, parses Goods Description to extract model/capacity/material/price-in-USD,
cleans numeric fields, computes Grand Total and Landed Cost per Unit, and writes processed CSV.
"""
import pandas as pd
import numpy as np
from dateutil import parser
from tqdm import tqdm
from etl.utils import USD_PRICE_RE, QTY_IN_DESC_RE, CAPACITY_RE, MATERIAL_RE, MODEL_RE, normalize_unit
import re

tqdm.pandas()

def parse_goods_description(desc: str):
    """Return dict with parsed fields and a simple confidence score."""
    out = {
        'model_name': None,
        'model_number': None,
        'capacity_spec': None,
        'material': None,
        'embedded_quantity': None,
        'original_unit_price_usd': None,
        'parsing_confidence': 0.0
    }
    if not isinstance(desc, str) or desc.strip() == '':
        return out
    raw = desc

    # USD price
    m_usd = USD_PRICE_RE.search(raw)
    if m_usd:
        usd_s = m_usd.group('usd').replace(',', '')
        try:
            out['original_unit_price_usd'] = float(usd_s)
            out['parsing_confidence'] += 1.0
        except:
            pass

    # embedded qty
    m_qty = QTY_IN_DESC_RE.search(raw)
    if m_qty:
        try:
            out['embedded_quantity'] = int(m_qty.group('qty'))
            out['parsing_confidence'] += 0.8
        except:
            pass

    # capacity
    m_cap = CAPACITY_RE.search(raw)
    if m_cap:
        out['capacity_spec'] = m_cap.group('cap').strip()
        out['parsing_confidence'] += 0.8

    # material
    m_mat = MATERIAL_RE.search(raw)
    if m_mat:
        out['material'] = m_mat.group(1).lower()
        out['parsing_confidence'] += 0.7

    # model heuristic
    models = MODEL_RE.findall(raw)
    if models:
        # prefer tokens containing digits or slashes/hyphens
        candidate = None
        for t in models:
            if re.search(r"\d", t) or '/' in t or '-' in t:
                candidate = t
                break
        if candidate is None:
            candidate = models[0]
        out['model_number'] = candidate
        out['parsing_confidence'] += 1.0

    # model name heuristic: take first meaningful title-case word(s)
    words = re.split(r"[\s,;|()\/-]+", raw)
    for w in words[:6]:
        if len(w) > 2 and not re.fullmatch(r"\d+", w) and not CAPACITY_RE.search(w) and not MATERIAL_RE.search(w):
            out['model_name'] = w
            out['parsing_confidence'] += 0.3
            break

    return out

def _clean_numeric(x):
    if pd.isna(x): return np.nan
    s = str(x)
    # remove common non-numeric tokens
    s = s.replace(',', '').replace('INR', '').replace('Rs.', '').replace('Rs', '').strip()
    s = re.sub(r'[^\d\.\-]', '', s)
    try:
        return float(s) if s != '' else np.nan
    except:
        return np.nan

def clean_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    # keep raw description
    df['raw_description'] = df.get('Goods Description', '').astype(str)

    parsed = df['raw_description'].progress_apply(parse_goods_description).apply(pd.Series)
    df = pd.concat([df, parsed], axis=1)

    # normalize units
    df['Unit_standard'] = df.get('Unit','').astype(str).apply(normalize_unit)

    # numeric cleaning
    for col in ['Unit Price (INR)', 'Total Value (INR)', 'Duty Paid (INR)', 'Quantity']:
        if col in df.columns:
            df[col + '_num'] = df[col].apply(_clean_numeric)

    # Dates
    if 'Date of Shipment' in df.columns:
        df['Date'] = pd.to_datetime(df['Date of Shipment'], dayfirst=True, errors='coerce')
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month

    # Grand Total
    df['Grand Total (INR)'] = df.get('Total Value (INR)_num', 0).fillna(0) + df.get('Duty Paid (INR)_num', 0).fillna(0)

    # Landed cost per unit (safe divide)
    qty = df.get('Quantity_num', pd.Series([np.nan]*len(df))).replace(0, np.nan)
    df['Landed Cost per Unit (INR)'] = df['Grand Total (INR)'] / qty

    df['parsing_confidence'] = df['parsing_confidence'].fillna(0)
    df['parsing_pass'] = df['parsing_confidence'] >= 2.0

    return df

def main(input_excel_path: str, output_csv_path: str):
    print("Reading Excel:", input_excel_path)
    df_raw = pd.read_excel(input_excel_path, sheet_name=0, dtype=str, engine='openpyxl')
    print("Rows read:", len(df_raw))
    df_clean = clean_dataframe(df_raw)
    print("Writing processed CSV:", output_csv_path)
    df_clean.to_csv(output_csv_path, index=False)
    print("Done.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='../data/Sample Data 2.xlsx')
    parser.add_argument('--output', default='../outputs/processed_trade_sample.csv')
    args = parser.parse_args()
    main(args.input, args.output)
