from pathlib import Path

import pandas as pd


def main() -> None:
    """Load the tokenized access log dataset, normalize its dates, and print a sample."""
    # === Resolve dataset path ===
    repo_root = Path(__file__).resolve().parent.parent
    data_path = repo_root / "datasets" / "DataCo_Smart_Supply" / "tokenized_access_logs.csv"
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        raise SystemExit(f"Dataset not found at {data_path}")

    # === Shape & stats for tokenized log ===
    print(f"tokenized_access_logs.csv shape: {df.shape}")
    print("tokenized_access_logs.csv stats (numerical columns):")
    print(df.describe().transpose())

    # === Format dates ===
    # Convert the Date column to datetime to normalize inconsistent formats first.
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=False, errors="coerce")
    # Then format it back as DD/MM/YYYY for consistent display.
    df["Date"] = df["Date"].dt.strftime("%d/%m/%Y")

    print("Sample from tokenized_access_logs.csv:")
    print(df.head(5))

    # === Additional dataset preview ===
    secondary_path = repo_root / "datasets" / "DataCo_Smart_Supply" / "DataCoSupplyChainDataset.csv"
    try:
        secondary_df = pd.read_csv(secondary_path, encoding="latin-1")
    except FileNotFoundError:
        raise SystemExit(f"Secondary dataset not found at {secondary_path}")

    # === Normalize secondary date columns ===
    date_columns = ["order date (DateOrders)", "shipping date (DateOrders)"]
    for column in date_columns:
        if column in secondary_df.columns:
            secondary_df[column] = pd.to_datetime(
                secondary_df[column], dayfirst=False, errors="coerce"
            )
            secondary_df[column] = secondary_df[column].dt.strftime("%d/%m/%Y")
        else:
            print(f"Warning: expected column {column} missing from {secondary_path}")
            
    print("\nSample from DataCoSupplyChainDataset.csv:")
    print(secondary_df.head(5))

    # === Shape & stats for secondary dataset ===
    print(f"\nDataCoSupplyChainDataset.csv shape: {secondary_df.shape}")
    print("DataCoSupplyChainDataset.csv stats (numerical columns):")
    print(secondary_df.describe().transpose())

    # === Recalculate 'Benefit per order' and 'Sales per customer' ===
    print("\nRecalculating 'Benefit per order' and 'Sales per customer'...")
    
    # Recalculate 'Benefit per order'
    # We assume that 'Order Profit Per Order' is the profit for each item in an order.
    # We group by 'Order Id' and sum the profit for each order.
    secondary_df['Benefit per order'] = secondary_df.groupby('Order Id')['Order Profit Per Order'].transform('sum')

    # Recalculate 'Sales per customer'
    # We group by 'Customer Id' and sum the 'Sales' for each customer.
    secondary_df['Sales per customer'] = secondary_df.groupby('Customer Id')['Sales'].transform('sum')
    
    print("After recalculation:")
    print(secondary_df[['Sales', 'Benefit per order', 'Sales per customer']].describe())

    # === Deep Dive into Extreme Negative Benefit ===
    print("\nInvestigating extreme negative 'Benefit per order' values...")
    min_benefit_order = secondary_df[secondary_df['Benefit per order'] == secondary_df['Benefit per order'].min()]

    if not min_benefit_order.empty:
        problem_order_id = min_benefit_order['Order Id'].iloc[0]
        print(f"The most problematic Order ID is: {problem_order_id}")

        problem_order_items = secondary_df[secondary_df['Order Id'] == problem_order_id]
        print(f"This order has {len(problem_order_items)} items.")
        
        print("Details of items in the problematic order:")
        print(problem_order_items[['Order Id', 'Order Item Quantity', 'Order Profit Per Order', 'Benefit per order']])
    else:
        print("Could not find the minimum benefit order. This is unexpected.")

    # === Save transformed CSVs ===
    output_dir = repo_root / "data"
    output_dir.mkdir(exist_ok=True)
    log_output_path = output_dir / "tokenized_access_logs_transformed.csv"
    df.to_csv(log_output_path, index=False)
    print(f"Transformed tokenized_access_logs saved to {log_output_path}")

    secondary_output_path = output_dir / "DataCoSupplyChainDataset_transformed.csv"
    secondary_df.to_csv(secondary_output_path, index=False)
    print(f"Transformed DataCoSupplyChainDataset saved to {secondary_output_path}")


if __name__ == "__main__":
    main()
