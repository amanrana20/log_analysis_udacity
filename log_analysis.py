#!/usr/bin/env python

"""
Code for Udacity Full Stack Nanodegree project 1: Log Analysis.

Author: Aman Rana
Dated: Nov. 11, 2018
"""

from datetime import datetime
import psycopg2


DB_NAME = "news"


def process_query(q):
    """Return all results from the 'database', most recent first."""
    try:
        db = psycopg2.connect(database=DB_NAME)
        c = db.cursor()
        c.execute(q)
        results = c.fetchall()
        db.close()
        return list(results)
    except Exception as e:
        print("Error processing query !\n{}".format(e))
        return None


def main():
    """Main."""
    # TOP 3 MOST POPULAR ARTICLES
    d = {
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

    # Processing each query as a separate request
    for query_id in d.keys():
        response = process_query(d[query_id]["query"])
        if not response:
            print("Could not process query> Try again later.")
            exit(-1)

        print(
            "{}\n{}".format(
                d[query_id]["desciption"],
                '='*len(d[query_id]["desciption"])
            )
        )

        if d[query_id]["limit"]:
            response = response[:d[query_id]["limit"]]

        for i, res in enumerate(response):
            if not query_id == 3:
                print(
                    "{}: \t {}{}".format(
                        res[0],
                        res[1],
                        d[query_id]["postfix"]
                    )
                )
            else:
                print(
                    "{}: \t {:.2f}{}".format(
                        res[0],
                        float(res[1])*100.0,
                        d[query_id]["postfix"]
                    )
                )

        print("\n\n")


if __name__ == "__main__":
    main()
