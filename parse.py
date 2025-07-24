"""Module providing sereral functions to parse the sameple log file into pandas DataFrame"""
import pandas as pd

def parse_log_line(log_line: str) -> pd.DataFrame:
    """Parse log line into suitable object.

    Args: 
        log_line (str): The line of log.

    Returns: 
        pd.DataFrame: A single line pandas DataFrame consist of the log information.
    """
    # indices of notations
    square_bracket_1 = log_line.find('[')
    square_bracket_2 = log_line.find(']')
    quote_1 = log_line.find('"')
    quote_2 = log_line.find('"', quote_1 + 1)
    quote_3 = log_line.find('"', quote_2 + 1)
    quote_5 = log_line.find('"', quote_3 + 1 + 1 + 1)
    quote_6 = log_line.find('"', quote_5 + 1)
    end = log_line.find('\n')

    ip = log_line[:square_bracket_1].split(sep=' ')[0]

    region = log_line[:square_bracket_1].split(sep=' ')[2]

    timestamp = log_line[square_bracket_1 + 1 : square_bracket_2]

    # request = method + url + protocol
    request = log_line[quote_1 + 1 : quote_2].split(sep=' ')
    method, url, protocol = request[0], request[1], request[2]

    status = log_line[quote_2 + 1 : quote_3].split(sep=' ')[1]

    size = log_line[quote_2 + 1 : quote_3].split(sep=' ')[2]

    user_agent = log_line[quote_5 + 1 : quote_6]

    duration = log_line[quote_6 + 1 : end]

    return {
        'ip': ip,
        'region': region,
        'timestamp': timestamp,
        'method': method,
        'url': url,
        'protocol': protocol,
        'status': status,
        'size': size,
        'user_agent': user_agent,
        'duration (ms)': duration
    }


def parse_log_file(file_path: str) -> pd.DataFrame:
    """Parse log in log files into pandas DataFrame. 

    Args: 
        file_path (str): The path to the log file.

    Returns:
        pd.DataFrame: A pandas DataFrame consists of logs information.
    """
    # parse log
    records = []
    try: 
        with open(file_path, 'r', encoding="utf-8") as f:
            for line in f:
                records.append(parse_log_line(line))
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Adjustment to correct format
    ## dd/mm/yyyy format timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y:%H:%M:%S')
    ## numerical format for suitable columns
    df['status'] = pd.to_numeric(df['status'])
    df['size'] = pd.to_numeric(df['size'])
    df.dropna(inplace=True)

    return df