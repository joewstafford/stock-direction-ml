import yfinance as yf
import pandas as pd
from pathlib import Path

subfolder_path = Path.cwd().parent / "data" / "raw"
subfolder_path = Path(__file__).resolve().parent.parent / "data" / "raw"
file_path = subfolder_path / "SPY_2016-09-01_2026-09-01.parquet"

if file_path.exists():
    data = pd.read_parquet(file_path)
    print("Cache loaded")
else:
    data = yf.download("SPY", start="2016-09-01", end="2026-09-01", auto_adjust=True)
    data.to_parquet(file_path)
    print("Data downloaded")

