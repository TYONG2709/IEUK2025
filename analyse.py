import matplotlib.pyplot as plt
from parse import parse_log_file, pd

# sample log file path
FILE_PATH = "sample-log.log"

def traffic_analysis(log_df: pd.DataFrame):
    """
    Analyse the parsed log DataFrame to find suspicious traffic patterns.
    """
    print("\n--- Traffic Analysis Report ---")
    print("-------------------------------")
    # get the most active IP addresses that exceed average requests
    requests = log_df.size
    unique_ip = log_df['ip'].nunique()
    average_requests = round(requests / unique_ip)
    print(f"Total requests: {requests}")
    print(f"Total number of unique IP address: {unique_ip}")
    print(f"Average requests per IP: {average_requests} (rounded)")
    print("---------------------------------")
    print("Number of IP that have requests more than average: ")
    top_ips = log_df['ip'].value_counts().nlargest(20)
    suspicious_ips = top_ips[top_ips > average_requests]
    print(suspicious_ips)
    print(f"(Total of {suspicious_ips.size} suspicious IP addresses)")
    # generate visualisation on suspicious IP addresses
    suspicious_ips.sort_values(ascending=False).plot(kind='barh', figsize=(10, 6))
    plt.title(f'{suspicious_ips.size} Suspicious Active IP addresses')
    plt.xlabel('Number of Requests')
    plt.ylabel('IP Addresses')
    plt.text(2750, 13, f'NOTE: Average requests per IP in this log: {average_requests}', fontsize=11, color='red')
    plt.tight_layout()
    plt.savefig('visualisations/suspicious_ips.png')
    plt.close()

if __name__ == "__main__":
    df = parse_log_file(FILE_PATH)
    print(df.head())
    traffic_analysis(df)