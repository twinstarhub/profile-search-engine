"""
Helper methods for analysis
"""
import threading
import pandas as pd


def analyse(sent_reqs):
    """Analyse the scraped data."""
    analyser_thread = threading.Thread(target=_analyse, args=(sent_reqs,))
    analyser_thread.start()


def _analyse(sent_reqs):
    """Analyse the scraped data."""
    # Extract the request logs from the sent requests.
    print("\nSTATUS CODE ANALYSIS\n")
    data = [req.request_log[0] for req in sent_reqs]
    # Convert the list of dictionaries to a DataFrame.
    df = pd.DataFrame(data)
    # Get counts for each unique status code.
    status_counts = df["status"].value_counts().rename_axis("Status").reset_index(name="Count")
    status_counts.index = [''] * len(status_counts)
    print(f"\nStatus Code Distribution:\n{_pretty_dataframe(status_counts)}\n")
    # Group by platform and display count of each status code, order by total non 200 status codes.
    platform_distribution = df.groupby("platform")["status"].value_counts().unstack()\
        .fillna(0).astype(int)
    platform_distribution.columns.name = 'Platform'
    platform_distribution.index.name = None
    print(f"\nStatus Code Distribution by Platform:\n{_pretty_dataframe(platform_distribution)}\n")


def _pretty_dataframe(df: pd.DataFrame):
    """Pretty print a DataFrame."""
    lines = df.to_string().splitlines()
    lines.insert(1, '-' * len(lines[0]))
    return '\n'.join(lines)
