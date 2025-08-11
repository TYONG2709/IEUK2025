"""This is the MAIN module for analysing the sample log file"""
from parse import parse_log_file
from analyse_traffic import find_suspicious_ips, observe_ips_timestamp
from analyse_ips import (extract_specific_ips_df, 
                         find_bot_user_agent, find_urls_bot_user_agent,
                         find_other_agents, find_urls_user_agent,
                         get_status_codes,
                         attacked_region, attacked_timestamp)
import pandas as pd
import time

# sample log file path
FILE_PATH = "sample-log.log"

def traffic_analysis(log_df: pd.DataFrame):
    """
    Analyse the parsed log DataFrame to find suspicious traffic patterns.
    """
    print("\n--------- Traffic Analysis Report ---------")
    print("--------------------------------------------")
    # get the most active IP addresses that exceed average requests
    requests = log_df.size
    unique_ip = log_df['ip'].nunique()
    average_requests = round(requests / unique_ip)
    print(f"Total requests: {requests}")
    print(f"Total number of unique IP address: {unique_ip}")
    print(f"Average requests per IP: {average_requests} (rounded)")
    print("--------------------------------------------")
    suspicious_ips, image_name = find_suspicious_ips(log_df, average_requests)
    print(suspicious_ips)
    print("--------------------------------------------")
    print(f'View its bar graph under {image_name}')
    print("--------------------------------------------")
    image_name = observe_ips_timestamp(log_df, suspicious_ips)
    print(f'View heatmap of the timestamp of suspicious ips under {image_name}')

def suspicious_ips_analysis(log_df: pd.DataFrame, ips: str):
    """
    Analyse specific suspicious ip addresses to figure out issues.
    """
    print(f'\n------ Suspicious IPs Analysis Report: IPs {ips} ------')
    print("---------------------------------------------------------------")
    ip_pattern = ips[:ips.find('x')]
    df_ips = extract_specific_ips_df(log_df, ip_pattern)
    # get list of urls affected by bot-like user agents
    bot_traffic_ips, type_bot_traffic_ips = find_bot_user_agent(df_ips, ips)
    print(type_bot_traffic_ips)
    # only show list of affected urls if bot agent is not empty
    if bot_traffic_ips.empty is False:
        print()
        url_bot_ips = find_urls_bot_user_agent(bot_traffic_ips)
        print(f'Number of unique url affected by bot-like user agent: {url_bot_ips.size}')
        print("-------------------------------------------------------------")
        print(url_bot_ips)
    print("---------------------------------------------------------------")
    # get lists of none affected urls
    traffic_ips, type_traffic_ips = find_other_agents(df_ips, ips)
    print(type_traffic_ips)
    print("----------------------------")
    url_ips = find_urls_user_agent(traffic_ips)
    print(f'Number of unique url that requested by none bot user agents: {url_ips.size}')
    print("---------------------------------------------------------------")
    print(url_ips)
    print("---------------------------------------------------------------")
    # extract and analyse status code
    status_code, image_name = get_status_codes(df_ips, ips)
    print(status_code)
    print("---------------------------------------------------------------")
    print(f'View the status code bar graph under {image_name}')
    print("---------------------------------------------------------------")
    # check attack timestamp
    attack_timeframe = attacked_timestamp(df_ips, ips)
    print(attack_timeframe)
    print("---------------------------------------------------------------")
    # check attack region/s
    attack_regions = attacked_region(df_ips)
    print(attack_regions)
    print("---------------------------------------------------------------")
    print()

if __name__ == "__main__":
    df = parse_log_file(FILE_PATH)
    print(df.head())
    traffic_analysis(df)
    print("\n")
    time.sleep(2)
    # IPs 45.133.1.x
    suspicious_ips_analysis(df, "45.133.1.x")
    print("\n")
    time.sleep(2)
    # IP 35.185.0.156
    suspicious_ips_analysis(df, "35.185.0.156")
    print("\n")
    time.sleep(2)
    # IPs 194.168.1.x
    suspicious_ips_analysis(df, "194.168.1.x")
    print("\n")
    time.sleep(2)
    # IPs 185.220.x.x
    suspicious_ips_analysis(df, "185.220.x.x")
    print("\n")