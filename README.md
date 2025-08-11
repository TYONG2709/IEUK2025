# IEUK2025
This is an engineering skills project from IEUK2025.

The main goal for this project is to resolve the concerns from a *small music media startup* where some growing traffic on their websites may be **non-human**, and the servers are becoming **overwhelmed**. 
- Parts of the website **go down** every few days due to the steer volume of traffic.
- With an engineering team of just **three** people, this downtime is severely impacting their productivity.

## Task
Using the provided set of logs - [sample log](./sample-log.log), **identify the problem** and determine the **best way to handle the increased traffic**.

---

## Identifying the root cause of the problem
Environment to analyse the [sample log](./sample-log.log):
- Language: `Python` (pip version 22.0.4)
- Libraries: `pandas`, `matplotlib` (for visualisations)
- Analysis Notebook: `ipykernel` (for Jupiter notebook)

---

### Analysis & Investigation
Questions:
- which pages are receiving the most visits
- which IP addresses are the most active
- what is the traffic pattern over time (e.g. requests per hour)
- what is the distribution of User-Agents

https://www.sitelock.com/blog/ddos-how-to-prevent-hackers-from-overloading-your-web-server/#:~:text=Look%20for%20signs%20of%20server%20overload
