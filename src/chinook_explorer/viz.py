"""
viz.py - Visualization module for Chinook Explorer.

This module provides plotting utilities for visualizing the results of analysis
and KPIs from the Chinook dataset. It includes time series plots, bar charts,
distributions, and RFM segmentation visuals.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

sns.set(style="whitegrid", context="talk")


class ChinookVisualizer:
    """
    Visualization class for Chinook analytics.

    Attributes:
        analyzer: ChinookAnalyzer instance used to generate the data to visualize.
    """

    def __init__(self, analyzer) -> None:
        """
        Initialize with an analyzer object (ChinookAnalyzer).

        Args:
            analyzer: A ChinookAnalyzer object containing prepared data and methods.
        """
        self.analyzer = analyzer

    # ---------------------------------------------------------------------
    #  Revenue Time Series
    # ---------------------------------------------------------------------
    def plot_revenue_over_time(self, save_path: Optional[str] = None) -> None:
        """Plot total revenue over time (monthly)."""
        df = self.analyzer.revenue_by_month()

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x="Month", y="Revenue", marker="o", linewidth=2.5)
        plt.title("Monthly Revenue Over Time", fontsize=20)
        plt.xlabel("Month")
        plt.ylabel("Revenue ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    # ---------------------------------------------------------------------
    #  Revenue by Country
    # ---------------------------------------------------------------------
    def plot_revenue_by_country(self, n: int = 10, save_path: Optional[str] = None) -> None:
        """Plot top N countries by revenue."""
        df = self.analyzer.top_countries_by_revenue(n=n)

        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x="Revenue", y="Country", palette="viridis")
        plt.title(f"Top {n} Countries by Revenue", fontsize=20)
        plt.xlabel("Revenue ($)")
        plt.ylabel("Country")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    # ---------------------------------------------------------------------
    #  Top Genres and Artists
    # ---------------------------------------------------------------------
    def plot_top_genres(self, n: int = 10, save_path: Optional[str] = None) -> None:
        """Plot top N genres by revenue."""
        df = self.analyzer.top_genres_by_revenue(n=n)

        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x="Revenue", y="Name_genre", palette="magma")
        plt.title(f"Top {n} Genres by Revenue", fontsize=20)
        plt.xlabel("Revenue ($)")
        plt.ylabel("Genre")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    def plot_top_artists(self, n: int = 10, save_path: Optional[str] = None) -> None:
        """Plot top N artists by revenue."""
        df = self.analyzer.top_artists_by_revenue(n=n)

        plt.figure(figsize=(12, 6))
        sns.barplot(data=df, x="Revenue", y="Name_artist", palette="cubehelix")
        plt.title(f"Top {n} Artists by Revenue", fontsize=20)
        plt.xlabel("Revenue ($)")
        plt.ylabel("Artist")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    # ---------------------------------------------------------------------
    #  Customer Lifetime Value
    # ---------------------------------------------------------------------
    def plot_top_customers(self, n: int = 20, save_path: Optional[str] = None) -> None:
        """Plot top N customers by total revenue."""
        df = self.analyzer.customer_lifetime_value(n=n)

        plt.figure(figsize=(12, 8))
        sns.barplot(data=df, x="TotalRevenue", y="FirstName", palette="coolwarm")
        plt.title(f"Top {n} Customers by Total Revenue", fontsize=20)
        plt.xlabel("Total Revenue ($)")
        plt.ylabel("Customer (First Name)")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    # ---------------------------------------------------------------------
    #  RFM Segmentation Visualization
    # ---------------------------------------------------------------------
    def plot_rfm_distribution(self, save_path: Optional[str] = None) -> None:
        """Visualize the distribution of R, F, and M scores."""
        rfm = self.analyzer.rfm_analysis()

        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        sns.histplot(rfm["R_Score"], bins=5, kde=False, ax=axes[0], color="royalblue")
        axes[0].set_title("Recency Score Distribution")
        sns.histplot(rfm["F_Score"], bins=5, kde=False, ax=axes[1], color="darkorange")
        axes[1].set_title("Frequency Score Distribution")
        sns.histplot(rfm["M_Score"], bins=5, kde=False, ax=axes[2], color="seagreen")
        axes[2].set_title("Monetary Score Distribution")

        for ax in axes:
            ax.set_xlabel("Score (1-5)")
            ax.set_ylabel("Count")

        plt.suptitle("RFM Score Distributions", fontsize=22)
        plt.tight_layout(rect=[0, 0, 1, 0.95])

        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    # ---------------------------------------------------------------------
    #  Word Frequency Visualization
    # ---------------------------------------------------------------------
    def plot_top_words(self, n: int = 20, save_path: Optional[str] = None) -> None:
        """Visualize most common words in track titles."""
        df = self.analyzer.top_words_in_track_titles(n=n)

        plt.figure(figsize=(12, 8))
        sns.barplot(data=df, x="Frequency", y="Word", palette="viridis")
        plt.title(f"Top {n} Words in Track Titles", fontsize=20)
        plt.xlabel("Frequency")
        plt.ylabel("Word")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    # ---------------------------------------------------------------------
    #  Duration Distribution
    # ---------------------------------------------------------------------
    def plot_duration_distribution(self, save_path: Optional[str] = None) -> None:
        """Plot distribution of track durations."""
        if self.analyzer.catalog_df is None:
            raise ValueError("Catalog DataFrame is required for duration analysis.")

        df = self.analyzer.catalog_df

        plt.figure(figsize=(12, 6))
        sns.histplot(df["DurationMin"], bins=50, kde=True, color="steelblue")
        plt.title("Distribution of Track Durations", fontsize=20)
        plt.xlabel("Duration (Minutes)")
        plt.ylabel("Count")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

