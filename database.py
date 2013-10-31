#! /usr/bin/env python

import MySQLdb

class DB:
  """
  Database object that allows querying of the specified database.

  Params:
    db_name - name of the database.
  """

  def __init__(self, db_name):
    self.db = MySQLdb.connect(host="acadmysql.duc.auburn.edu", user="dmb0025",
                         passwd="y0l0sw4gg", db=db_name)
    self.cursor = self.db.cursor()

  def query(self, query):
    """
    Queries the database and then returns the results as a list of dicts where
    the keys of the dicts will be the column names.

    Params:
      query - mySQL query.

    Returns:
      list of dicts where the keys of the dicts will be the column names.
    """
    self.cursor.execute(query)
    results = list()
    fields = [column[0] for column in self.cursor.description]
    for row in self.cursor.fetchall():
      comp = dict()
      for i in range(0, len(fields)):
        comp[fields[i]] = row[i]
      results.append(comp)

    return results
