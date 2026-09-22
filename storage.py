import json
from pathlib import Path
from decimal import Decimal

INVOICE_DIR = Path('invoices')


def _json_default(value):
    if isinstance(value, Decimal):
        return str(value)
    raise TypeError(f'Cannot serialize {type(value).__name__}')


def _safe_name(invoice_number):
    cleaned = ''.join(c for c in str(invoice_number) if c.isalnum() or c in ('-', '_'))
    return cleaned or 'invoice'


def save_invoice(invoice, directory=INVOICE_DIR):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{_safe_name(invoice['invoice_number'])}.json"
    path.write_text(json.dumps(invoice, indent=2, default=_json_default), encoding='utf-8')
    return path


def list_invoices(directory=INVOICE_DIR):
    directory = Path(directory)
    if not directory.exists():
        return []
    return sorted(p.stem for p in directory.glob('*.json'))


def load_invoice(invoice_number, directory=INVOICE_DIR):
    path = Path(directory) / f'{_safe_name(invoice_number)}.json'
    return json.loads(path.read_text(encoding='utf-8'))
