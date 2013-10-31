#! /usr/bin/env python

import random

import database
import rank

db_name = "LeagueRank"
comp_table = "Champions"
tag_table = "Tags"
rank_table = "Ranks"

db = database.DB(db_name)

def getCompetitors():
  tags = db.query("SELECT * FROM {0}".format(tag_table))
  comps = db.query("SELECT * FROM {0}".format(comp_table))


def updateRanks(tag, comp1, comp2, winner_id):
