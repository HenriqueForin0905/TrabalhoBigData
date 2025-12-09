import re
import argparse
import logging
from pathlib import Path
import pandas as pd


def _norm_column(col: str) -> str:
    col = str(col).strip().lower()
    col = re.sub(r"\s+", "_", col)
    col = re.sub(r"[^0-9a-zA-Z_]+", "_", col)
    col = re.sub(r"_+", "_", col)
    return col.strip("_")


def ingest_csv(filename: str, source_dir: Path, raw_dir: Path, bronze_dir: Path) -> None:
    src_path = source_dir / filename
    logging.info("Ingesting file: %s", src_path)

    if not src_path.exists():
        logging.warning("Source file not found: %s", src_path)
        return

    try:
        df = pd.read_csv(src_path)
    except Exception as e:
        logging.exception("Failed to read %s: %s", src_path, e)
        return

    raw_path = raw_dir / filename
    try:
        df.to_csv(raw_path, index=False)
        logging.info("Saved RAW: %s", raw_path)
    except Exception:
        logging.exception("Failed to write RAW file: %s", raw_path)
        return

    df = df.copy()
    df.columns = [_norm_column(col) for col in df.columns]

    bronze_path = bronze_dir / filename
    try:
        df.to_csv(bronze_path, index=False)
        logging.info("Saved BRONZE: %s", bronze_path)
    except Exception:
        logging.exception("Failed to write BRONZE file: %s", bronze_path)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Ingest CSV files into RAW and BRONZE layers")
    parser.add_argument("--source", "-s", default=None, help="Source directory with original CSVs")
    parser.add_argument("--datasets-dir", "-d", default=None, help="Path to the Datasets folder (defaults to parent of this script)")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    this_file = Path(__file__).resolve()
    default_datasets_dir = this_file.parent.parent

    datasets_dir = Path(args.datasets_dir).expanduser().resolve() if args.datasets_dir else default_datasets_dir

    source_dir = Path(args.source).expanduser().resolve() if args.source else datasets_dir / "Source"
    raw_dir = datasets_dir / "Raw"
    bronze_dir = datasets_dir / "Bronze"

    for p in (source_dir, raw_dir, bronze_dir):
        try:
            p.mkdir(parents=True, exist_ok=True)
        except Exception:
            logging.exception("Failed creating directory: %s", p)

    logging.info("Using source dir: %s", source_dir)

    for entry in sorted(source_dir.iterdir()) if source_dir.exists() else []:
        if entry.is_file() and entry.suffix.lower() == ".csv":
            ingest_csv(entry.name, source_dir, raw_dir, bronze_dir)


if __name__ == "__main__":
    main()
