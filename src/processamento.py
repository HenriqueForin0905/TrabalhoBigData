"""
Processamento para camada Silver.

Este módulo contém funções básicas usando pandas para:
- carregar arquivos Bronze
- padronizar tipos (datas, numéricos)
- tratar nulos simples
- salvar em Silver

Uso:
    python src/processamento.py
"""
from pathlib import Path
import logging
import pandas as pd


def _parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    # Tenta converter colunas que contenham 'date' ou 'dt'
    for col in df.columns:
        if 'date' in col or col.endswith('_dt') or col.endswith('_date'):
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except Exception:
                logging.debug('Could not parse dates for column %s', col)
    return df


def clean_bronze_to_silver(datasets_dir: Path) -> None:
    bronze_dir = datasets_dir / 'Bronze'
    silver_dir = datasets_dir / 'Silver'
    silver_dir.mkdir(parents=True, exist_ok=True)

    for path in sorted(bronze_dir.glob('*.csv')):
        logging.info('Processing Bronze file: %s', path)
        try:
            df = pd.read_csv(path)
        except Exception:
            logging.exception('Failed reading %s', path)
            continue

        # basic cleaning
        df.columns = [c.strip().lower() for c in df.columns]
        df = _parse_dates(df)

        # fill simple nulls for numeric columns
        num_cols = df.select_dtypes(include=['number']).columns
        df[num_cols] = df[num_cols].fillna(0)

        # save to silver
        out_path = silver_dir / path.name
        try:
            df.to_parquet(out_path.with_suffix('.parquet'), index=False)
            logging.info('Saved Silver parquet: %s', out_path.with_suffix('.parquet'))
        except Exception:
            logging.exception('Failed writing Silver file: %s', out_path)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    repo_root = Path(__file__).resolve().parent.parent
    datasets_dir = repo_root / 'Datasets'
    clean_bronze_to_silver(datasets_dir)


if __name__ == '__main__':
    main()
