from parse import parse_log_file, pd

# sample log file path
FILE_PATH = "sample-log.log"

def traffic_analysis(log_df: pd.DataFrame):
    """
    Analyse the parsed log DataFrame to find suspicious traffic patterns.
    """
    print("\n--- Traffic Analysis Report ---\n")

    print("Top 10 Most Active IP Addresses: ")
    top_ips = log_df['ip'].value_counts().nlargest(10)
    print(top_ips)
    print("---------------------------------\n")

if __name__ == "__main__":
    df = parse_log_file(FILE_PATH)
    traffic_analysis(df)