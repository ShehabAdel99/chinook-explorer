"""
analytics.py - Analysis and KPIs module for Chinook Explorer.

This module defines the ChinookAnalyzer class, which calculates insights, KPIs,
and statistics from the modeled Chinook data such as revenue trends, top performers,
customer lifetime value, RFM segmentation, and text-based insights.
"""

import pandas as pd
import numpy as np
from typing import Optional


class ChinookAnalyzer:
    """
    Provides analytical methods for Chinook sales and catalog data.

    Attributes:
        sales_df (pd.DataFrame): The sales line items DataFrame created by ChinookModel.
        catalog_df (Optional[pd.DataFrame]): Optional catalog data for text and track analysis.
    """

    def __init__(self, sales_df: pd.DataFrame, catalog_df: Optional[pd.DataFrame] = None) -> None:
        """
        Initialize the analyzer with prepared data.

        Args:
            sales_df (pd.DataFrame): Sales line items DataFrame.
            catalog_df (pd.DataFrame, optional): Catalog DataFrame for text/duration analysis.
        """
        if sales_df is None or not isinstance(sales_df, pd.DataFrame):
            raise ValueError("sales_df must be a valid pandas DataFrame.")

        self.sales_df = sales_df.copy()
        self.catalog_df = catalog_df.copy() if catalog_df is not None else None

        # Validate required columns
        required_cols = {"InvoiceDate", "LineTotal"}
        missing = required_cols - set(self.sales_df.columns)
        if missing:
            raise KeyError(f"Missing required columns in sales_df: {', '.join(missing)}")

        # Ensure InvoiceDate is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.sales_df["InvoiceDate"]):
            self.sales_df["InvoiceDate"] = pd.to_datetime(self.sales_df["InvoiceDate"], errors="coerce")

    # ---------------------------------------------------------------------
    #  Revenue Over Time
    # ---------------------------------------------------------------------
    def revenue_by_month(self) -> pd.DataFrame:
        """
        Compute total revenue aggregated by month.

        Returns:
            pd.DataFrame: Monthly revenue time series with columns ['Month', 'Revenue'].
        """
        df = self.sales_df.copy()
        df["Month"] = df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
        result = df.groupby("Month")["LineTotal"].sum().reset_index()
        result.rename(columns={"LineTotal": "Revenue"}, inplace=True)
        return result.sort_values("Month")

    # ---------------------------------------------------------------------
    #  Top Entities by Revenue
    # ---------------------------------------------------------------------
    def top_countries_by_revenue(self, n: int = 10) -> pd.DataFrame:
        """Find the top N countries by total revenue."""
        self._check_column("Country")
        result = (
            self.sales_df.groupby("Country")["LineTotal"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )
        result.rename(columns={"LineTotal": "Revenue"}, inplace=True)
        return result

    def top_genres_by_revenue(self, n: int = 10) -> pd.DataFrame:
        """Find the top N genres by total revenue."""
        self._check_column("Name_genre")
        result = (
            self.sales_df.groupby("Name_genre")["LineTotal"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )
        result.rename(columns={"LineTotal": "Revenue"}, inplace=True)
        return result

    def top_artists_by_revenue(self, n: int = 10) -> pd.DataFrame:
        """Find the top N artists by total revenue."""
        self._check_column("Name_artist")
        result = (
            self.sales_df.groupby("Name_artist")["LineTotal"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )
        result.rename(columns={"LineTotal": "Revenue"}, inplace=True)
        return result

    # ---------------------------------------------------------------------
    #  Customer Lifetime Value (CLV)
    # ---------------------------------------------------------------------
    def customer_lifetime_value(self, n: int = 20) -> pd.DataFrame:
        """Compute total revenue per customer."""
        self._check_column("CustomerId")
        result = (
            self.sales_df.groupby(["CustomerId", "FirstName", "LastName"])["LineTotal"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )
        result.rename(columns={"LineTotal": "TotalRevenue"}, inplace=True)
        return result

    # ---------------------------------------------------------------------
    #  RFM Analysis (Recency, Frequency, Monetary)
    # ---------------------------------------------------------------------
    def rfm_analysis(self) -> pd.DataFrame:
        """
        Perform RFM (Recency, Frequency, Monetary) analysis for customers.

        Returns:
            pd.DataFrame: DataFrame with RFM scores and segments.
        """
        self._check_column("CustomerId")

        today = self.sales_df["InvoiceDate"].max() + pd.Timedelta(days=1)
        rfm = (
            self.sales_df.groupby("CustomerId")
            .agg(
                Recency=("InvoiceDate", lambda x: (today - x.max()).days),
                Frequency=("InvoiceId", "nunique"),
                Monetary=("LineTotal", "sum"),
            )
            .reset_index()
        )

        # Define a safe_qcut helper to avoid bin errors
        def safe_qcut(series, q=5, reverse=False):
            try:
                bins = pd.qcut(series, q=q, labels=False, duplicates="drop")
            except ValueError:
                # Fallback: use rank-based binning if qcut fails
                bins = pd.qcut(series.rank(method="first"), q=q, labels=False, duplicates="drop")

            bins = pd.Series(bins) + 1  # convert 0-based labels to 1-based scores
            if reverse:
                bins = (bins.max() + 1) - bins
            return bins.astype(int)

        #  Apply safe_qcut to each dimension
        rfm["R_Score"] = safe_qcut(rfm["Recency"], q=5, reverse=True)
        rfm["F_Score"] = safe_qcut(rfm["Frequency"], q=5, reverse=False)
        rfm["M_Score"] = safe_qcut(rfm["Monetary"], q=5, reverse=False)

        # Calculate total RFM score
        rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

        return rfm.sort_values("RFM_Score", ascending=False)

    # ---------------------------------------------------------------------
    #  Text Analysis: Top Words in Track Titles
    # ---------------------------------------------------------------------
    def top_words_in_track_titles(self, n: int = 20, stopwords: Optional[set] = None) -> pd.DataFrame:
        """Analyze track titles and return the most common words."""
        if self.catalog_df is None:
            raise ValueError("catalog_df is required for text analysis.")

        self._check_column("Name", df=self.catalog_df)

        if stopwords is None:
            stopwords = {"the", "a", "and", "of", "to", "in", "on", "for", "with"}

        words = (
            self.catalog_df["Name"]
            .dropna()
            .astype(str)
            .str.lower()
            .str.replace(r"[^a-z\s]", "", regex=True)
            .str.split()
        )

        flat_words = [w for sublist in words for w in sublist if w not in stopwords]
        word_counts = pd.Series(flat_words).value_counts().head(n).reset_index()
        word_counts.columns = ["Word", "Frequency"]
        return word_counts

    # ---------------------------------------------------------------------
    #  Duration Statistics
    # ---------------------------------------------------------------------
    def duration_stats(self) -> pd.Series:
        """Calculate descriptive statistics for track durations."""
        if self.catalog_df is None:
            raise ValueError("catalog_df is required for duration analysis.")

        self._check_column("DurationMin", df=self.catalog_df)
        return self.catalog_df["DurationMin"].describe()

    # ---------------------------------------------------------------------
    #  Utility: Column Check
    # ---------------------------------------------------------------------
    def _check_column(self, col: str, df: Optional[pd.DataFrame] = None) -> None:
        """
        Internal helper to check if a column exists in the given DataFrame.

        Args:
            col (str): Column name.
            df (pd.DataFrame, optional): DataFrame to check. Defaults to sales_df.

        Raises:
            KeyError: If the column does not exist.
        """
        if df is None:
            df = self.sales_df
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' is missing.")


