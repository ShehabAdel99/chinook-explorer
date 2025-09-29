"""
modeling.py - Data modeling and transformation module for Chinook Explorer.

This module defines the ChinookModel class, which is responsible for:
- Joining normalized Chinook CSV tables into analysis-ready DataFrames.
- Creating a "sales line items" fact table.
- Building a "catalog" table with track, album, artist, and genre info.
- Creating a customer dimension table with geographic and representative details.
- Adding engineered features (monetary totals, datetime components, durations, etc.).
"""

import pandas as pd
from typing import Dict


class ChinookModel:
    """
    A class responsible for building analysis-ready data models from the raw Chinook tables.

    Attributes:
        tables (Dict[str, pd.DataFrame]): A dictionary of raw Chinook tables loaded from CSV.
    """

    def __init__(self, tables: Dict[str, pd.DataFrame]) -> None:
        """
        Initialize the model with pre-loaded tables.

        Args:
            tables (Dict[str, pd.DataFrame]): Dictionary of raw DataFrames from ChinookLoader.
        """
        if not tables or not isinstance(tables, dict):
            raise ValueError("`tables` must be a dictionary of pandas DataFrames.")
        self.tables = tables

    # ---------------------------------------------------------------------
    #  Sales Line Items Fact Table
    # ---------------------------------------------------------------------
    def sales_line_items(self) -> pd.DataFrame:
        """
        Create a fact table that combines invoice items with all relevant dimensions.

        Returns:
            pd.DataFrame: Sales line items table with monetary totals, datetime components, and metadata.
        """

        # Validate required tables exist
        required = [
            "invoiceline",
            "invoice",
            "customer",
            "track",
            "album",
            "artist",
            "genre",
            "mediatype",
        ]
        self._check_required_tables(required)

        # Perform incremental joins
        df = self.tables["invoiceline"].copy()

        # Merge with invoices
        df = df.merge(
            self.tables["invoice"],
            on="InvoiceId",
            how="left",
            suffixes=("", "_invoice"),
        )

        # Merge with customers
        df = df.merge(
            self.tables["customer"],
            on="CustomerId",
            how="left",
            suffixes=("", "_customer"),
        )

        # Merge with tracks
        df = df.merge(
            self.tables["track"],
            on="TrackId",
            how="left",
            suffixes=("", "_track"),
        )

        # Merge with albums
        df = df.merge(
            self.tables["album"],
            on="AlbumId",
            how="left",
            suffixes=("", "_album"),
        )

        # Merge with artists
        df = df.merge(
            self.tables["artist"],
            on="ArtistId",
            how="left",
            suffixes=("", "_artist"),
        )

        # Merge with genres
        df = df.merge(
            self.tables["genre"],
            on="GenreId",
            how="left",
            suffixes=("", "_genre"),
        )

        # Merge with media types
        df = df.merge(
            self.tables["mediatype"],
            on="MediaTypeId",
            how="left",
            suffixes=("", "_media"),
        )

        # Feature Engineering ------------------------------------------------
        # Monetary feature
        df["LineTotal"] = df["UnitPrice"] * df["Quantity"]

        # Ensure InvoiceDate is datetime
        if "InvoiceDate" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["InvoiceDate"]):
            df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

        # Datetime components
        if "InvoiceDate" in df.columns:
            df["Year"] = df["InvoiceDate"].dt.year
            df["Month"] = df["InvoiceDate"].dt.month
            df["Quarter"] = df["InvoiceDate"].dt.quarter
            df["Week"] = df["InvoiceDate"].dt.isocalendar().week
            df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()

        # Reorder columns for readability
        important_cols = [
            "InvoiceLineId",
            "InvoiceId",
            "InvoiceDate",
            "CustomerId",
            "FirstName",
            "LastName",
            "Country",
            "City",
            "TrackId",
            "Name",  # track name
            "Title",  # album title
            "ArtistId",
            "Name_artist",
            "GenreId",
            "Name_genre",
            "MediaTypeId",
            "Name_media",
            "UnitPrice",
            "Quantity",
            "LineTotal",
            "Year",
            "Month",
            "Quarter",
            "Week",
            "DayOfWeek",
        ]

        # Keep only columns that exist (in case of naming differences)
        df = df[[col for col in important_cols if col in df.columns]]

        return df

    # ---------------------------------------------------------------------
    #  Catalog Table (Tracks + Albums + Artists + Genres + MediaTypes)
    # ---------------------------------------------------------------------
    def catalog(self) -> pd.DataFrame:
        """
        Create a catalog table of all tracks enriched with metadata.

        Returns:
            pd.DataFrame: Catalog table with track details and metadata.
        """

        required = ["track", "album", "artist", "genre", "mediatype"]
        self._check_required_tables(required)

        catalog = self.tables["track"].copy()

        # Merge with albums → artists → genres → media types
        catalog = catalog.merge(self.tables["album"], on="AlbumId", how="left")
        catalog = catalog.merge(self.tables["artist"], on="ArtistId", how="left", suffixes=("", "_artist"))
        catalog = catalog.merge(self.tables["genre"], on="GenreId", how="left", suffixes=("", "_genre"))
        catalog = catalog.merge(self.tables["mediatype"], on="MediaTypeId", how="left", suffixes=("", "_media"))

        # Feature: duration in minutes
        if "Milliseconds" in catalog.columns:
            catalog["DurationMin"] = catalog["Milliseconds"] / 60000

        return catalog

    # ---------------------------------------------------------------------
    #  Customer Dimension Table
    # ---------------------------------------------------------------------
    def customers_dim(self) -> pd.DataFrame:
        """
        Create a customer dimension table with demographics and support info.

        Returns:
            pd.DataFrame: Customer dimension table.
        """

        required = ["customer", "employee"]
        self._check_required_tables(required)

        customers = self.tables["customer"].copy()

        # Merge support rep info (optional)
        if "employee" in self.tables and "SupportRepId" in customers.columns:
            customers = customers.merge(
                self.tables["employee"],
                left_on="SupportRepId",
                right_on="EmployeeId",
                how="left",
                suffixes=("", "_rep"),
            )

        return customers

    # ---------------------------------------------------------------------
    #  Utility: Check required tables
    # ---------------------------------------------------------------------
    def _check_required_tables(self, required: list) -> None:
        """
        Internal helper to validate that required tables are present.

        Args:
            required (list): List of table names expected in self.tables.

        Raises:
            KeyError: If any required table is missing.
        """
        missing = [t for t in required if t not in self.tables]
        if missing:
            raise KeyError(f"Missing required tables: {', '.join(missing)}")

