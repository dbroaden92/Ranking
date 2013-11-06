#! /usr/bin/env python

import random

import database
import rank

"""
System that allows a user
"""

# Database Table Names
db_name = "LeagueRank"
comp_table = "Champions"
tag_table = "Tags"
rank_table = "TagRanking"

db = database.DB(db_name)

def getCompetitors():
  """

  """
  tags = db.query("SELECT * FROM {0}".format(tag_table))
  comps = db.query("SELECT * FROM {0}".format(comp_table))
  ranks = db.query("SELECT * FROM {0}".format(rank_table))

  print tags
  print comps
  print ranks


def updateRanks(tag, comp1, comp2, winner_id):
  """

  """

def main(args):
  getCompetitors()

if __name__ == "__main__":
  main(None)
