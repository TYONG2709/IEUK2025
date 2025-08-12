# Solutions Report
Traffic analysis are performed under this [Jupyter notebook](./analysis.ipynb).

## Problem Identification
Under [sample log](./sample-log.log), there are:
- a total of **4320960 requests**
- a total number of **40887 unique IP address** acrossed these requests

These sum up that an **average requests per IP is 106** (rounded). 

However, there are 16 suspicious IP addresses that generate enormous amount of requests from each of them (**exceeding average requests**). 

### Suspicious IPs

<image src="./visualisations/suspicious-ips.png" />

The attacked timeframes from these suspicious IPs can be viewed in the heatmap below: 

<image src="./visualisations/timestamp.png" />

I conducted an analysis on these IP addresses in [**Jupyter notebook**](./analysis.ipynb). I will list down some key points I observed from their patterns. 

### Issues with these IPs
#### IPs `45.133.1.x` - <ins>API attack</ins>
- There are **10800 requests targeted on 1200+ various unique API endpoints** using various user agents.
  - Among these 10800 requests, there are **1165 requests** targeting on **753 various unique API endpoints** using **systematic enumeration with `python-requests/2.28.1`**.
- Besides that, there are:

    <image src="./visualisations/status_code_45.133.1.x.png" height="300px" />

  - 7826 requests with `404` HTTP error status
  - 184 requests with `403` authentication error status
  
  A total of **8010 error status** out of 10800 requests.
  - User agent `python-requests/2.28.1` causes 853 `404` errors and 16 `403` errors.
- The total attack duration is **1 hour**, in between **15:00 and 16:00** on **02/07/2025**.
- A total of 1 region got affected by this API attack - `RU` (Russia).

#### IP `35.185.0.156` - <ins>Web Scrapper</ins>
- This IP called **3,600 requests** with **user agent `Wget/1.20.3 (linux-gnu)`**, accessing 2280 various unique search endpoints.

    <image src="./visualisations/status_code_35.185.0.156.png" height="300px" />
    
    - All requests are accessed **without error status** (OK `200` status for all requests).
- The attack duration is **30 minutes**, in between **05:00 and 06:00** on **02/07/2025**.
- A total of 1 region got affected by this web scrapping - `US` (United States).

#### IPs `194.168.1.x` - <ins>Overloaded Requests within specific timeframe</ins>
- Among these 14400 requests, there are:

    <image src="./visualisations/status_code_194.168.1.x.png" height="300px" />

  - 1469 `500` internal server error
  - 1459 `504` gateway timeout error
  - 1430 `503` service unavailable error
  - 1429 `429` too many requests error 
  
  A total of **5787 requests with errors**.
- These IPs might had **exceeded requests limit within a specific timeframe**, leading to **server overwhelm**, causes internal server errors, then causes gateway timeout.
- The attack duration is **1 hour**, in between **12:00 and 13:00** on **03/07/2025**.
- A total of 1 region that got affected by these IPs - `UK` (United Kingdom).

#### IPs `185.220.x.x` - <ins>Credential Stuffing Botnet</ins>
- Among 7200 requests from these IPs, there are **904 requests** targeting on **726 login endpoints** using **bot tool like `python-requests/2.28.1`**.
  - Even the other requests **does not** called from bot-like user agent, the **rest of the 6296 requests** still targeting on **1520+ login and sign in API endpoints using other various tools**.
- Besides that, there are:

    <image src="./visualisations/status_code_185.220.x.x.png" height="300px" />

  - 5338 `401` unauthorised error status
  - 992 `403` insufficient permission error
  - 427 `423` resource accessbility error status
  - 419 `429` "Too Many Requests" status
  
  A total of **7176 error status** out of 7200 requests.
    - User agent `python-requests/2.28.1` causes 693 `401` errors, 108 `403` errors, 49 `423` and 53 `429` errors.
- The attack duration is **1 hour**, in between **19:00 and 20:00** on **04/07/2025**.
- A total of 4 regions got affected by these IPs - `IR` (Iran), `KP` (North Korea), `CN` (China) and `RU` (Russia).

## Solutions to problems
| Solutions | Which IPs / Issues | Expected Impact |
|-|:-:|-|
| ***IP Blocking*** <br> Directly block the problematic IPs immediately | All suspicious IP addresses | Directly **reduce 36000 requests**, fall in traffic by **88%** (out of 40887 unique api)  |
| ***User-Agent Filtering*** <br> Block requests that contains bot-like keywords, for eg. `bot`, `crawler`, `scraper`, and `python-requests` patterns | IP addresses with bot-like user agent - `45.133.1.x` & `185.220.x.x` | Block requests containing these bot-like user agents in the future incoming requests. |
| ***Nginx Rate Limting*** <br> Limit the incoming requests to specific amount within certain timeframe per IP | IP addresses that causes "too many requests" error status (`429`) - `194.168.1.x` | With **limit to 20-30 requests per minute per IP (around 30 requests lower than average requests above)**, expect it to avoid overwhelming traffic. |

These should expect to reduce the traffic, eliminate downtime. With these solutions, the small engineering team should be able to use these solutions without any additional costs. 

[back to README](./README.md)