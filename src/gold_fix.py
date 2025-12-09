"""
Gerar tabelas Gold (KPIs) a partir da camada Silver (fix).

Uso:
    python src/gold_fix.py
"""
from pathlib import Path
import logging
import pandas as pd


def load_all_silver(silver_dir: Path) -> dict:
    tables = {}
    for p in sorted(silver_dir.glob('*.parquet')):
        name = p.stem
        try:
            tables[name] = pd.read_parquet(p)
        except Exception:
            logging.exception('Failed reading %s', p)
    return tables


def avg_price_by_category(products_df: pd.DataFrame, items_df: pd.DataFrame) -> pd.DataFrame:
    merged = items_df.merge(products_df, on='product_id', how='left')
    res = merged.groupby('product_category_name').price.mean().reset_index()
    res = res.rename(columns={'price': 'avg_price'})
    return res


def price_variation_over_time(items_df: pd.DataFrame) -> pd.DataFrame:
    df = items_df.copy()
    if 'order_approved_at' in df.columns:
        df['month'] = pd.to_datetime(df['order_approved_at']).dt.to_period('M')
    else:
        df['month'] = pd.NaT
    grouped = df.groupby('month').price.agg(['mean', 'min', 'max']).reset_index()
    grouped = grouped.rename(columns={'mean': 'avg_price'})
    return grouped


def save_gold(datasets_dir: Path) -> None:
    silver_dir = datasets_dir / 'Silver'
    gold_dir = datasets_dir / 'Gold'
    gold_dir.mkdir(parents=True, exist_ok=True)

    tables = load_all_silver(silver_dir)

    products = tables.get('products', pd.DataFrame())
    items = tables.get('order_items', pd.DataFrame())

    if not products.empty and not items.empty:
        kpi1 = avg_price_by_category(products, items)
        kpi1.to_csv(gold_dir / 'avg_price_by_category.csv', index=False)
        logging.info('Saved avg_price_by_category')

    if not items.empty:
        kpi2 = price_variation_over_time(items)
        kpi2.to_csv(gold_dir / 'price_variation_by_month.csv', index=False)
        logging.info('Saved price_variation_by_month')


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    repo_root = Path(__file__).resolve().parent.parent
    datasets_dir = repo_root / 'Datasets'
    save_gold(datasets_dir)


if __name__ == '__main__':
    main()
