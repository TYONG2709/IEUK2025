"""Module providing sereral functions to analyse the traffic in sample log file"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def find_suspicious_ips(log_df: pd.DataFrame, average_requests: int) -> tuple:
    """
    Get suspicious ips that exceed average requests in pandas Series format.
    
    Returns:
      tuple: size 2 tuple (<code>pd.DataFrame</code>, <code>str</code>)
      <br> 0. suspicious ips 
      <br> 1. the file name of the visualisation
    """
    top_ips = log_df['ip'].value_counts().nlargest(20)
    suspicious_ips = top_ips[top_ips > average_requests]
    suspicious_ips.name = "top ips with largest requests that's more than average"
    # generate visualisation on suspicious IP addresses
    fig, ax = plt.subplots()
    bars = ax.barh(suspicious_ips.index, suspicious_ips.values)
    ax.bar_label(bars, padding=3)
    ax.set_xlabel('Number of Requests')
    ax.set_ylabel('IP Addresses')
    ax.set_xlim(right=6000) # set the max limit of x-axis
    ax.set_title(f'{suspicious_ips.size} Suspicious Active IP addresses')    
    ax.text(4000, 13, f'NOTE: \nAverage requests per IP \nin this log: {average_requests}',
            ha="center", fontsize=8 ,color='red')
    fig.tight_layout()
    image_file = "visualisations/suspicious-ips.png"
    fig.savefig(image_file)
    plt.close()
    return suspicious_ips, image_file

def observe_ips_timestamp(log_df: pd.DataFrame, sus_ips: pd.Series) -> str:
    """
    Generate heatmap to observe the traffic of suspicious ips over time.

    Returns:
      str: the file name of the visualisation
    """
    # create pivot table - IPs on x-axis, timestamp on y-axis
    heatmap_data = ((log_df[log_df['ip'].isin(sus_ips.index)]).set_index('timestamp')
                                                            .groupby('ip')
                                                            .resample('5Min')['url'].size()
                                                            .unstack(level='ip')
                                                            .fillna(0))
    # plot heatmap
    plt.figure(figsize=(18, 10))
    sns.heatmap(heatmap_data, cmap='coolwarm', linewidths=0.5)
    plt.title("Heatmap of Requests per 5 minute for Suspicious IPs")
    plt.xlabel("IP Address")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Time')
    plt.tight_layout()
    image_file = "visualisations/timestamp.png"
    plt.savefig(image_file)
    plt.close()
    return image_file