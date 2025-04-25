from pathlib import Path
import json
import pandas as pd

from src.settings import filter_texts


class DataLoader:
    """
    A class to load data from JSON files in a specified directory.
    """

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.filter_texts = filter_texts

    def load(self) -> pd.DataFrame:
        records: list[dict] = []
        for file in self.data_dir.glob("**/*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("content") in self.filter_texts:
                    continue
                records.append(data)
        return pd.DataFrame(records)
