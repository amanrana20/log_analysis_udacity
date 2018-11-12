# Submission for Udacity Full Stack Developer Nanogergee
## PROJET: Log Analysis
### Submission by Aman Rana (amanrana20@icloud.com)

* * *

## Files in submission folder
1. The code for the submission is present in './log_analysis.py' file.
2. The output for the submission can be seen in './output.txt'
3. README.md: Containes explaination of code and VIEW statements.
4. newsdata.sql: File provided by Udacity.

* * *

## Instructions for running the python file

1. Install python [here](https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/)
2. Download and install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
3. Download [Vagrant](https://www.vagrantup.com/downloads.html)
4. Clone the github repo (containing code and VM configuration file [Github](https://github.com/amanrana20/log_analysis_udacity)
5. Download the news database [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), unzip it and save it into the cloned github repo **log_analysis_udacity**

Clone the github repo into Downloads folder and *cd* into it.
```sh
$ cd Downloads/log_analysis_udacity/
$ vagrant up  # Configure the virtual machine using VM configuration file (need to be done once only)
$ vagrant ssh  # start the virtual machine
```

The python file is standalone for the project. Inside **vagrant ssh** do the following:

```sh
# Write all this after running vagrant ssh
$ cd /vagrant/
# Make sure the database file: newsdata.sql is present
$ psql  # Start psql
$ CREATE DATABASE news  # create a new daatbase 'news'
# Ctrl + D to exit psql interface
$ psql -d news -f newsdata.sql  # Load the tables from .sql file into news database
$ python log_analysis.py
```

* * *

## Code design
The aim was to write a small python script successfully implenting the solution problem statements. The code contains the *main* function and *process_query* function.

The *process_query()* function takes in the command to execute, connects to *news* database, executes the command, fetches the results, closes the connection and returns the result as a lists. 

```python
def process_query(q):
    """Return all results from the 'database', most recent first."""
    try:
        db = psycopg2.connect(database=DB_NAME)
        c = db.cursor()
        c.execute(q)
        results = c.fetchall()
        db.close()
        return list(results)
    except:
        return None
```

The *main()* fuction contains a dictionary storing the *params* for the three problem statements and also stores the commands to run. A for loop is implemented to run the solution to the three problem statements and print the output to screen. The output has been saved to a text file using:
```sh
python log_analysis.py >> output.txt
```

```python
{
    1: {
        "desciption": "TOP 3 ARTICLES",
        "query": """SELECT title, COUNT(path) AS c
            FROM log, articles
            WHERE articles.slug = substring(
            log.path, position('e/' in log.path)+2)
            GROUP BY title ORDER BY c DESC;""",
        "limit": 3,
        "postfix": " views"
    },
    2: {
        "desciption": "MOST POPULAR ARTICLE AUTHORS OF ALL TIMES",
        "query": """SELECT name, COUNT(name) AS c
            FROM log, articles, authors
            WHERE articles.slug = substring(
            log.path,
            position('e/' in log.path)+2) and articles.author = authors.id
            GROUP BY name ORDER BY c DESC;""",
        "limit": None,
        "postfix": " views"
    },
    3: {
        "desciption": "ERROR REQUEST (>1%) DAYS",
        "query": """CREATE VIEW errors as
            SELECT time::date as date, COUNT(*) as c
            FROM log
            WHERE status != '200 OK'
            GROUP BY date
            ORDER BY c DESC;
            CREATE VIEW totals as
            SELECT time::date as date, COUNT(*) as c
            FROM log GROUP BY date
            ORDER BY c DESC;
            CREATE VIEW ratios AS
            SELECT errors.date, errors.c/totals.c::float as percent
            FROM errors, totals WHERE errors.date = totals.date;
            SELECT TO_CHAR(date::DATE, 'Mon dd, yyyy'), percent
            FROM ratios
            WHERE percent > 0.01;""",
        "limit": None,
        "postfix": r"% error"
    }
}
```

## Output from code
```sh
TOP 3 ARTICLES
==============
Candidate is jerk, alleges rival: 	 338647 views
Bears love berries, alleges bear: 	 253801 views
Bad things gone, say good people: 	 170098 views



MOST POPULAR ARTICLE AUTHORS OF ALL TIMES
=========================================
Ursula La Multa: 	 507594 views
Rudolf von Treppenwitz: 	 423457 views
Anonymous Contributor: 	 170098 views
Markoff Chaney: 	 84557 views



ERROR REQUEST (>1%) DAYS
========================
Jul 17, 2016: 	 2.26% error




```

## Views created
```sql
1. 	CREATE VIEW errors as 
    SELECT time::date as date, COUNT(*) as c 
    FROM log 
    WHERE status != '200 OK' 
    GROUP BY date 
    ORDER BY c DESC;

2. 	CREATE VIEW totals as 
    SELECT time::date as date, COUNT(*) as c 
    FROM log GROUP BY date 
    ORDER BY c DESC;

3.	CREATE VIEW ratios AS 
    SELECT errors.date, errors.c/totals.c::float as percent 
    FROM errors, totals WHERE errors.date = totals.date;
```