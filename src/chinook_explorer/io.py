"""
io.py - Data loading module for Chinook Explorer.

This module defines the ChinookLoader class, which is responsible for:
- Dynamically loading all CSV files from the `data/` folder.
- Parsing datetime columns automatically.
- Providing a summary of the loaded tables.
- (Optional) validating basic schema properties like key uniqueness.

It is designed to be schema-agnostic and robust against slight filename or column changes.
"""

import os
import pandas as pd
from typing import Dict


class ChinookLoader:
    """
    Loads Chinook database CSV files into pandas DataFrames.

    Attributes:
        data_dir (str): Path to the directory containing CSV files.
        tables (Dict[str, pd.DataFrame]): A dictionary mapping table names to DataFrames.
    """

    def __init__(self, data_dir: str = None) -> None:
        """
        Initialize the ChinookLoader.

        Args:
            data_dir (str, optional): Path to the CSV folder. Defaults to '../data' relative to this file.
        """
        # Automatically set the default data directory if not provided
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")

        self.data_dir: str = os.path.abspath(data_dir)
        self.tables: Dict[str, pd.DataFrame] = {}

    def load_tables(self) -> Dict[str, pd.DataFrame]:
        """
        Load all CSV files from the data directory into pandas DataFrames.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary of table name -> DataFrame.

        Raises:
            FileNotFoundError: If the data directory does not exist.
            ValueError: If no CSV files are found in the directory.
        """
        # Check if data directory exists
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

        # Loop through all files in the data directory
        for filename in os.listdir(self.data_dir):
            if filename.lower().endswith(".csv"):
                table_name = os.path.splitext(filename)[0].lower()
                file_path = os.path.join(self.data_dir, filename)

                try:
                    df = pd.read_csv(file_path)
                except Exception as e:
                    raise ValueError(f"Failed to read {filename}: {e}")

                # Try to parse any column containing 'date' as datetime
                for col in df.columns:
                    if "date" in col.lower():
                        try:
                            df[col] = pd.to_datetime(df[col], errors="coerce")
                        except Exception:
                            # Non-fatal: just skip parsing if conversion fails
                            pass

                self.tables[table_name] = df

        if not self.tables:
            raise ValueError("No CSV files were found in the data directory.")

        return self.tables

    def summary(self) -> pd.DataFrame:
        """
        Generate a summary of all loaded tables (rows, columns, and missing values).

        Returns:
            pd.DataFrame: A summary DataFrame with table statistics.

        Raises:
            ValueError: If no tables are loaded yet.
        """
        if not self.tables:
            raise ValueError("No tables loaded. Call `load_tables()` first.")

        summary_data = []
        for name, df in self.tables.items():
            summary_data.append(
                {
                    "table": name,
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "missing_values": int(df.isnull().sum().sum()),
                }
            )

        return pd.DataFrame(summary_data)

    def validate_schema(self) -> pd.DataFrame:
        """
        (Optional) Perform basic schema validation:
        - Check for duplicate rows
        - Check for fully empty columns

        Returns:
            pd.DataFrame: A DataFrame of potential schema warnings.
        """
        if not self.tables:
            raise ValueError("No tables loaded. Call `load_tables()` first.")

        issues = []

        for name, df in self.tables.items():
            # Check for duplicate rows
            if df.duplicated().any():
                issues.append({"table": name, "issue": "Contains duplicate rows"})

            # Check for completely empty columns
            empty_cols = [col for col in df.columns if df[col].isnull().all()]
            if empty_cols:
                issues.append(
                    {
                        "table": name,
                        "issue": f"Empty columns detected: {', '.join(empty_cols)}",
                    }
                )

        if issues:
            return pd.DataFrame(issues)
        else:
            return pd.DataFrame([{"status": "No major schema issues detected."}])

