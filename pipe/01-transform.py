from pathlib import Path
import logging
import pandas as pd

# =========================
# Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# =========================
# Configurações
# =========================
DATE_COLS = [
    "order date (DateOrders)",
    "shipping date (DateOrders)"
]

FINANCIAL_COLS = [
    'Sales',
    'Benefit per order',
    'Order Profit Per Order',
    'Sales per customer',
    'Product Price',
    'Order Item Total',
    'Order Item Discount'
]

# =========================
# Funções
# =========================
def load_dataset(path: Path, encoding: str = "utf-8") -> pd.DataFrame:
    try:
        df = pd.read_csv(path, encoding=encoding)
        logger.info(f"Carregado: {path.name} | Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar {path}: {e}")
        raise


def convert_dates(df: pd.DataFrame, date_cols: list) -> pd.DataFrame:
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            invalid = df[col].isna().sum()
            if invalid:
                logger.warning(f"{invalid} datas inválidas em '{col}'")
        else:
            logger.warning(f"Coluna de data não encontrada: {col}")
    return df


def enforce_numeric_types(df: pd.DataFrame) -> pd.DataFrame:
    for col in FINANCIAL_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            nulls = df[col].isna().sum()
            if nulls:
                logger.warning(f"{nulls} valores inválidos em '{col}'")
    return df


# =========================
# Pipeline principal
# =========================
def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    data_dir = repo_root / "datasets" / "DataCo_Smart_Supply"

    # 1️⃣ tokenized_access_logs.csv
    log_path = data_dir / "tokenized_access_logs.csv"
    logger.info(f"Processando {log_path.name}")
    log_df = load_dataset(log_path)

    if 'Date' in log_df.columns:
        log_df['Date'] = pd.to_datetime(log_df['Date'], errors='coerce')

    # sobrescreve o arquivo original
    log_df.to_csv(log_path, index=False)

    # 2️⃣ DataCoSupplyChainDataset.csv
    main_path = data_dir / "DataCoSupplyChainDataset.csv"
    logger.info(f"Processando {main_path.name}")
    main_df = load_dataset(main_path, encoding="latin-1")

    main_df = convert_dates(main_df, DATE_COLS)
    main_df = enforce_numeric_types(main_df)

    # sobrescreve o arquivo original
    main_df.to_csv(main_path, index=False)

    logger.info("Arquivos tratados e salvos com os mesmos nomes originais")


if __name__ == "__main__":
    main()
