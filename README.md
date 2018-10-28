# Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Run Instructions](README.md#run-instructions)

# Problem

A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years. 

As a data engineer, I was asked to create a mechanism to analyze past years data, specificially calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications. In the following, I am describing the approach to solve the problem.

# Approach

The broad idea for solving the problem is to parse through the input file, count the certified applications while listing the SOC name and WORK STATE name. To perform this, I start with two empty Python dictionaries: `SOC` and `STATES`. `SOC` will have SOC names as keys and `STATES` will have state names as keys. I read the first line (header text) from the input file and get the index positions for the application status, visa category, SOC name and work state name. From the next line until end of file, I perform the following:

1. if application status is **certified** and visa category is **H1B** then look at the SOC name and the STATE name
2. if the SOC name already exists in `SOC` keys, I increment the count of current SOC key by 1. Otherwise, I create a new key with the SOC name and initialize the count with 0
3. if the state name already exists in `STATES` keys, I increment the count of current state key by 1. Otherwise, I create a new key with the state name and initialize the count with 0

Now, the two dictionaries `SOC` and `STATES` essentially have a summary of the input file. To get the desired result, I need to sort the SOC names and the state names according to the number of applications certified. To that end, I make two lists: `lst_soc` and `lst_states`.  The `lst_soc` is a list of tuples. each tuple contains the soc name, certified application count and percentage. Additionally, the `lst_states` is a list of tuples. each tuple contains the state name, certified application count and percentage. I sort these two lists: first alphabetically and then according to the 2nd element of each tuple (the number of certified applications). Finally, I write the top-10 entries from each list into `txt` files in the required location.

# Run Instructions

Please put the input `.csv` file in the `input` folder. You can modify the `run.sh` file to change the input/output filenames. Then in Terminal, run the following command: 

```
insight~$ ./run.sh
```
