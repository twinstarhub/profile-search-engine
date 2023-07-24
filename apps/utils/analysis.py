"""
Helper methods for analysis
"""
from ast import literal_eval
from collections import Counter
from itertools import chain
import os
import threading
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from apps.utils.custom_logger import BaseLogger
from apps.utils.markdown_handler import MarkdownHandler
sns.set_theme(style="darkgrid")

from apps.utils.mongo import MongoDBConnector


class RequestAnalyser:
    """A class to analyse status code trends of sent records."""
    logger = BaseLogger("RequestAnalyser")

    @classmethod
    def analyse(cls, sent_reqs):
        """Analyse the scraped data."""
        analyser_thread = threading.Thread(target=cls._analyse, args=(sent_reqs,))
        analyser_thread.start()

    @classmethod
    def _analyse(cls, sent_reqs):
        """Analyse the scraped data."""
        # Extract the request logs from the sent requests.
        cls.logger.info("\nSTATUS CODE ANALYSIS\n")
        data = [req.request_log[0] for req in sent_reqs]
        # Convert the list of dictionaries to a DataFrame.
        df = pd.DataFrame(data)
        df['sent_at_sec'] = df['sent_at'].dt.round('1s')
        cls._analyse_status_counts(df)
        cls._analyse_platform_status(df)
        platform_status_time_series = cls._analyse_platform_trend(df)
        cls._analyse_status_trend(platform_status_time_series)

    @classmethod
    def _analyse_status_counts(cls, df):
        """Analyse the status code counts."""
        status_counts = df["status"].value_counts().rename_axis("Status").reset_index(name="Count")
        status_counts.index = [''] * len(status_counts)
        cls.logger.info(
            "\nStatus Code Distribution:\n"
            f"{cls._pretty_dataframe(status_counts)}\n"
        )

    @classmethod
    def _analyse_platform_status(cls, df):
        """Analyse the status code distribution by platform."""
        platform_distribution = df.groupby("platform")["status"].value_counts().unstack()\
            .fillna(0).astype(int)
        platform_distribution.columns.name = 'Platform'
        platform_distribution.index.name = None
        cls.logger.info(
            "\nStatus Code Distribution by Platform:\n"
            f"{cls._pretty_dataframe(platform_distribution)}\n"
        )

    @classmethod
    def _analyse_platform_trend(cls, df):
        """Analyse the platform status trend."""
        platform_status_time_series = df.groupby(['platform', 'sent_at_sec'])['status']\
            .apply(lambda x: x.mode().iloc[0])
        cls.logger.info(
            "\nPlatform Status Trend:\n"
            f"{cls._pretty_dataframe(platform_status_time_series)}\n"
        )
        
        return platform_status_time_series

    @classmethod
    def _analyse_status_trend(cls, platform_status_time_series):
        """Analyse the status code trend."""
        status_distribution_over_time = platform_status_time_series.groupby(['sent_at_sec', 'status'])\
            .size().unstack().fillna(0).astype(int)
        status_distribution_over_time.index.name = None
        status_distribution_over_time.columns.name = 'Time'
        cls.logger.info(
            "\nStatus Code Distribution over Time:\n"
            f"{cls._pretty_dataframe(status_distribution_over_time)}\n"
        )

    @classmethod
    def _pretty_dataframe(cls, df: pd.DataFrame):
        """Pretty print a DataFrame."""
        lines = df.to_string().splitlines()
        lines.insert(1, '-' * len(lines[0]))
        return '\n'.join(lines)


class ResponseAnalyser:
    """A class to analyse the scraped results."""
    def __init__(self, report_name: str = "report.md"):
        self.report_name = report_name
        self.markdown_handler = MarkdownHandler(report_name)
        self.df = None
        self.logger = BaseLogger("ResponseAnalyser")

    def analyse_results(self):
        """Analyse the scraped results."""
        with MongoDBConnector() as connector:
            profiles = connector.get_all_documents('Profiles')
        with self.markdown_handler as report_file:
            self.df = pd.DataFrame(profiles)
            self.df.drop(columns=['_id'], inplace=True)
            self._write_intro(report_file)
            self._write_high_level_overview(report_file)
            self._write_platform_vs_metadata(report_file)
            self._write_metadata_analysis(report_file)
            self._write_value_analysis(report_file)
            self.logger.success(
                "Finished writing report. "
                "Please check this file for the results:\n%s",
                os.path.abspath(self.report_name)
            )

    def _write_intro(self, report_file: MarkdownHandler):
        unique_platforms = self.df['platform'].unique()
        report_file.add_header("Scraped Data Analysis")
        report_file.write(
            "This report contains the analysis of the scraped data.\n\n"
            "The following platforms were scraped:\n"
            f"{self.markdown_handler.list_to_markdown(unique_platforms, flat=False)}\n\n"
        )

    def _write_high_level_overview(self, report_file: MarkdownHandler):
        report_file.add_header("High Level Overview", level=2)
        metadata_dist_dict = {
            "Total Profiles": len(self.df),
            "Empty Snippets": self.df['snippet'].isna().sum(),
            "Non Empty Snippets": self.df['snippet'].notna().sum(),
            "Metadata Presence Ratio": f"{self.df['snippet'].notna().sum() / len(self.df) * 100:.2f}%"
        }
        metadata_dist_df = pd.DataFrame(metadata_dist_dict, index=[''])
        report_file.write(metadata_dist_df.to_markdown(index=False))
        snippet_counts = self.df['snippet'].isna().apply(lambda x: 'Empty' if x else 'Metadata').value_counts()
            # Plot the pie chart, add legend and title.
        snippet_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.legend()
        plt.title("Snippet Distribution")
        report_file.save_image(plt)

    def _write_platform_vs_metadata(self, report_file: MarkdownHandler):
        report_file.add_header("Platform vs Metadata Distribution", level=2)
        platform_distribution = self.df.groupby("platform")["snippet"].apply(
            lambda x: x.isna().value_counts()
        ).unstack().fillna(0).astype(int).sort_values(by=True, ascending=False)
        platform_distribution.index.name = "Platform"
        platform_distribution.columns = ['No Metadata', 'Has Metadata']
        report_file.write(platform_distribution.to_markdown(index=True))
        platform_distribution.plot.bar(
            stacked=True,
            rot=0, 
            figsize=(self.df['platform'].nunique() * 1.1, 5)
        )
        self.markdown_handler.save_image(plt)

    def _write_metadata_analysis(self, report_file: MarkdownHandler):
        report_file.add_header("Metadata Analysis", level=2)

        non_empty_snippets = self.df[self.df['snippet'].notna()]
        fields_available = non_empty_snippets.groupby("platform")["snippet"].apply(
            lambda x: set().union(*x.apply(lambda y: y.keys()))
        ).sort_values(key=lambda x: x.apply(len), ascending=False)
        fields_available = fields_available.to_frame()
        fields_available["Count"] = fields_available.apply(
            lambda x: len(x['snippet']), axis=1
        )
        fields_available.index.name = "Platform"
        fields_available.columns = ['Schema', 'Count']
        
        metadata_fieds_distribution = non_empty_snippets['snippet'].apply(
            lambda x: list(x.keys())
        ).explode().value_counts()[:10].to_frame().reset_index()
        metadata_fieds_distribution.columns = ['Field', 'Count']

        cntr = Counter(chain.from_iterable(fields_available["Schema"]))
        most_common_fields_df: pd.DataFrame = pd.DataFrame.from_dict(
            cntr, orient='index'
        ).sort_values(by=[0], ascending=False)[:10].reset_index()
        most_common_fields_df.columns = ['Field', 'Count']

        table_dict = {
            "Top 10 Overlapped fields across Platforms": most_common_fields_df.to_html(index=False),
            "Top 10 metadata fields occuring in results": metadata_fieds_distribution.to_html(index=False)
        }
        report_file.write(self.markdown_handler.dict_to_table(table_dict))

        plot = sns.barplot(x='Field', y='Count', data=metadata_fieds_distribution, width=0.5)
        plot.set_xticklabels(plot.get_xticklabels(), rotation=15)
        self.markdown_handler.save_image(plt)

        report_file.write("\n\nFields available in each platform\n\n")
        report_file.write(fields_available.to_markdown(index=True))

    def _write_value_analysis(self, report_file: MarkdownHandler):
        report_file.add_header("Value Analysis", level=2)
        non_empty_snippets = self.df[self.df['snippet'].notna()].copy()
        non_empty_snippets["snippet"] = non_empty_snippets["snippet"].astype(str)
        total_non_empty_snippets = len(non_empty_snippets)
        unique_values = non_empty_snippets["snippet"].astype(str).unique()
        total_unique_values = len(unique_values)
        report_file.write(
            f"\n\nTotal non empty snippets: {total_non_empty_snippets}\n"
            f"\nTotal unique snippets: {total_unique_values}\n"
            f"\nValue uniqueness ratio: {total_unique_values / total_non_empty_snippets * 100:.2f}%\n\n"
        )
        duplicate_values = non_empty_snippets.loc[
            non_empty_snippets.duplicated(subset='snippet', keep=False)
        ].sort_values(by='snippet')[:10]
        if len(duplicate_values) > 0:
            report_file.add_header("Duplicate Values", level=3)
            report_file.write(duplicate_values[["title", "platform", "link", "snippet"]].to_markdown(index=False))
            report_file.write(
                "\n\n> Note: Duplicate Records might indicate similar profiles."
                "\nOr the platform has some redirection logic.\n\n"
            )
        non_empty_snippets["snippet_value_set"] = non_empty_snippets["snippet"].apply(
            lambda x: [
                val for val in literal_eval(x).values()
                if (
                    val
                    and isinstance(val, str)
                    and val != "None"
                    and not val.isdigit()
                )
            ]
        )
        cntr = Counter(
            chain.from_iterable(non_empty_snippets['snippet_value_set'])
        )
        cntr = {k: v for k, v in cntr.items() if v > 1}
        most_common_values_df: pd.DataFrame = pd.DataFrame.from_dict(
            cntr, orient='index'
        )[:10].sort_values(by=[0], ascending=False).reset_index()
        most_common_values_df.columns = ['Value', 'Count']
        report_file.add_header("Top 10 most common values", level=3)
        report_file.write(most_common_values_df.to_markdown(index=False))
        most_common_values_df.plot(kind='barh', figsize=(15, 8))
        for bar, key in zip(plt.gca().patches, most_common_values_df['Value']):
            if len(key) > 100:
                key = key[:100] + '...'
            plt.gca().text(
                0.5,
                bar.get_y() + bar.get_height() / 2,
                key, ha='left', va='center'
            )
        plt.title("Top 10 most common values")
        plt.xlabel("")
        plt.ylabel("")
        plt.tight_layout()
        self.markdown_handler.save_image(plt)


if __name__ == "__main__":
    ResponseAnalyser("../../report.md").analyse_results()
