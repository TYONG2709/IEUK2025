"""Module that provides several functions 
that performs analysis on specific ips"""
import pandas as pd
import matplotlib.pyplot as plt

def extract_specific_ips_df(log_df: pd.DataFrame, ip_pattern: str) -> pd.DataFrame:
    """
    Extract the log dataframe with specific ip pattern.

    Returns:
      pd.DataFrame: IPs specific dataframe.
    """
    return log_df[log_df['ip'].str.contains(r"" + ip_pattern)]

def find_bot_user_agent(ips_df: pd.DataFrame, ip: str) -> tuple:
    """
    Search for existence of bot-like user agent in dataframe.

    Returns:
      tuple: size 2 tuple (<code>pd.DataFrame</code>, <code>pd.Series</code>)
      <br> 0. IPs affected by bot-like user agent
      <br> 1. List of bot-like user agents
    """
    # find potential bot pattern on user agent
    bot = ['bot', 'spider', 'crawler', 'python-request']
    bot_pattern = '|'.join(bot) # '|' means bitstring OR
    bot_traffic_ips = ips_df[ips_df['user_agent'].str.contains(bot_pattern, case=False, na=False)]
    # return empty df if no bot-like user agent found
    if bot_traffic_ips.empty:
        return (bot_traffic_ips, f'None of the traffic found on using bot-like agent with IPs {ip}')
    # show type of agent/s used
    type_bot_traffic_ips = bot_traffic_ips['user_agent'].value_counts()
    type_bot_traffic_ips.name = f'bot-like user agent used in IPs {ip}'
    return bot_traffic_ips, type_bot_traffic_ips

def find_urls_bot_user_agent(bot_traffic_ips_df: pd.DataFrame) -> pd.Series:
    """
    Search for unique urls that got affected by bot-like user agent.

    Returns:
      pd.Series: URLs affected by bot-like user agent, empty if none.
    """
    # return empty series if none traffic got affected
    if bot_traffic_ips_df.empty is True:
        return pd.Series()
    
    url_bot_ips = bot_traffic_ips_df['url'].value_counts()
    url_bot_ips.name = ""
    return url_bot_ips

def find_other_agents(ips_df: pd.DataFrame, ip: str) -> tuple:
    """
    Search none bot user agents in dataframe.

    Returns:
      tuple: size 2 tuple (<code>pd.DataFrame</code>, <code>pd.Series</code>)
      <br> 0. IPs
      <br> 1. List of other user agents
    """
    # extract by ignore bot patterns
    bot = ['bot', 'spider', 'crawler', 'python-request']
    bot_pattern = '|'.join(bot) # '|' means bitstring OR
    traffic_ips = ips_df[~ips_df['user_agent'].str.contains(bot_pattern, case=False, na=False)]
    # show type of agents used
    type_traffic_ips = traffic_ips['user_agent'].value_counts()
    type_traffic_ips.name = f'none bot agents used in IPs {ip}'
    return traffic_ips, type_traffic_ips

def find_urls_user_agent(traffic_ips_df: pd.DataFrame) -> pd.Series:
    """
    Search for unique urls from none bot user agents.

    Returns:
      pd.Series: URLs
    """    
    url_ips = traffic_ips_df['url'].value_counts()
    url_ips.name = ""
    return url_ips

def get_status_codes(ips_df: pd.DataFrame, ip: str) -> tuple:
    """
    Produce a bar graph of the status codes from the requests by specific ips.

    Returns:
      tuple: size 2 tuple (<code>str</code> or <code>pd.DataFrame</code>, <code>str</code>)
      <br> 0. the info of status code.
      <br> 1. the file name of the visualisation.
    """    
    # extract status code for both both-like and other user agents
    status_ips = ips_df['status'].value_counts()
    status_ips.index = status_ips.index.astype(str)
    bot_status_ips = (find_bot_user_agent(ips_df, ip)[0])['status'].value_counts()
    bot_status_ips.index = bot_status_ips.index.astype(str)
    if status_ips.nunique() == 1:
        status_info = f'No error status. All {status_ips.values} requests ended with OK (200) status.'
    else:
        status_info = pd.DataFrame({
            'Status Code': status_ips.index,
            'All requests': status_ips.values
        })
        if bot_status_ips.empty is False:
            status_info['By bot-like user agent'] = bot_status_ips.values
    # plot bar graph
    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(status_ips.index, status_ips.values, width=0.5)
    ax.bar_label(bars, label_type='edge', padding=2)
    ax.set_xlabel('Status Code')
    ax.set_ylabel('Number of Requests')
    ax.set_title(f"{status_ips.values.sum()} Requests in different status code from IPs {ip}")
    if bot_status_ips.empty is False:
        bars_bot = ax.bar(bot_status_ips.index, bot_status_ips.values, width=0.5)
        ax.bar_label(bars_bot)
        ax.legend(["all requests", "requests by bot-like user agent"])
    fig.tight_layout()
    image_file = f'visualisations/status_code_{ip}.png'
    fig.savefig(image_file)
    plt.close()
    return status_info, image_file

def attacked_timestamp(ips_df: pd.DataFrame, ip: str) -> str:
    """
    Check the attacked timeframe from the specific ips.

    Returns: 
      str: the message telling the attacked timeframe.
    """
    # check its attack timestamp
    start_time = ips_df['timestamp'].min()
    end_time = ips_df['timestamp'].max()
    duration = int((end_time - start_time).total_seconds())
    days = ((duration//3600) % 24) if (duration//3600 >= 24) else 0
    hours = ((duration//3600) - (days*24)) if (days >= 1) else (duration//3600)
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    return f'Attack timeframe from IPs {ip} :\n -> from {start_time} to {end_time} \n -> duration: {days} days, {hours} hours, {minutes} minutes and {seconds} seconds'

def attacked_region(ips_df: pd.DataFrame) -> str:
    """
    Check the attacked region/s by the specific ips.

    Returns:
      str: the message telling the attacked region/s.
    """
    # find attack region/s
    region_ips = ips_df['region'].unique()
    return f'{region_ips.size} region/s got affected: \n{region_ips}'