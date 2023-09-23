# Web Log data processor

## Setup
1. download *config.json*, *process_data.py* files
2. in Terminal, go to the folder where you saved these files
3. edit *config.json* file and specify proper values
4. run *python3 process_data.py*
5. execution log will be saved in the *./execution.log* file

### **This version downloads and processes data in several threads**

### Objective
Write a python script/program to transform web traffic data stored in time-record format where
each row is a page view into a per-user format where each row is a different user and the
columns represent the time spent on each of the pages.

### Source Data
The data set consists of 26 CSV files in an AWS S3 bucket. The files are named with lowercase
ascii letters (a.csv, b.csv. c.csv, … z.csv).

Each CSV file has a header row labeling the included columns, which are:  
* drop: Whether or not this was the last page the user visited before leaving the site.  
* length: How long the user spent on the page in seconds.  
* path: The page within the website that the user visited.  
* user_agent: The browser identifier of the user visiting the page.  
* user_id: The unique identifier for the user visiting the page.  

### Output data

Write a program that converts the web traffic from these 26 CSV files into a single CSV file that
contains one row for each user_id and has columns populated with the length of time each user
spent on each path. 

### Success criteria

* The program should be designed so that the root URL could be changed later and the program re-run on new data. That means downloading the data must be done within the program.
* The program should write out to a standard CSV file that can be opened in Excel for review

-------

## Assumptions/Conditions

1. This program is intended to download 26 CSV files with pre-defined names (a.csv ... z.csv) and with identical data schema (set of fields)
2. This program is a ***lightweight*** version that implements the required functionality.
   * If performance is a concern, then something like a multithreading can be introduced - it is possible to distribute downloading/calculation of smaller chunks (1..x of files) and apply final calculation on top at the end 
3. If target folder does not exist, the resulted file will be saved in the current directory
4. Resulted data might be not accurate in case some of the source files are missed/broken. In case there are missed/broken files, there will be a message sent to the _execution.log_ file for the further investigations
5. All non-numeric values (if any) will be ignored and omitted from the final result
6. The overall data size in all files is small enough (i.e. up to 1Gb) to be effectively processed using Pandas DataFrames.
   * In case the overall size is greater than 1Gb, I would suggest some modifications to the algorithm (such as applying group/sum to each file in the cycle, and then applying the final group/sum to the interim results)
   * If volume of each file does not fit into Pandas DataFrame, then I would recommend to switch to another technology (Apache Spark, Database Engines) for this data processing.
7. There are no tests created. Let me know if it is a part of the requirements
