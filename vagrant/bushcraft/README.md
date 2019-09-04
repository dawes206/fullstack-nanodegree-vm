## Item Catalog



##Steps for database_setup

## pre-requisite Knowledge

## Getting started

##API's






## LogsAnalysis
LogsAnalysis is a simple python script used to answer 3 questions about the traffic data stored in a news agency's database; what are the agency's most popular articles, who are the most popular authors, and when did users have the hardest time navigating to the agency's website?

## Pre-requisite Knowledge
<li>SQL and Python</li>

## Needed files
<li>LogsAnalysis.py - Python script to perform analysis</li>
<li>newsdata.sql - File used to populate database</li>

## Steps
1. Place LogsAnalysis.py and newsdata.sql into the folder shared between your host machine and your VM.
2. Install psycopg2 package onto your host machine. Full documentation <a href="http://initd.org/psycopg/docs/">here</a>
3. Install PostgreSQL (psql) onto your VM. Full documentation <a href="https://www.postgresql.org/docs/9.4/app-psql.html">here</a>
4. From your vm, import psql data by cd-ing to where you saved newsdata.sql and using the command `psql -d news -f newsdata.sql`.
5. Access your database with the command `psql news` and create the necessary views (see below) by copy and pasting them into the terminal and pressing enter
6. Exit the database with ctrl+D
7. Navigate to the folder with LogsAnalysis.py and run `python3.5 LogsAnalysis.py` to perform analysis
8. Results will be saved in Analysis.txt in the same folder as LogsAnalysis.py


## Program Design
The program is composed of several functions that relate to each question. These functions are called at the end of the program to produce the solutions.

Each query was assigned to a string before being executed, in order to simplify the code. This way queries could be combined without typing out one, overly complicated query.

After completing the queries, each function writes the results to Analysis.txt. This approach gives more control over formatting than psycopg2's copy_expert module and psql's COPY statement.

## Necessary Views
`CREATE VIEW Articlevisits as SELECT SUBSTRING(Log.path from 10) as path, ip, method, status, time, id from Log WHERE POSITION('/article' in log.path) = 1;`
