#! /usr/bin/env python

import random

import database
import rank

"""
Interface for a controller that selects competitors to compare and a tag to
compare them with from a database, and then updates the database after a winner
is chosen.
"""

class Tag:
  """
  Represents a tag from a database and includes the name of the tag and its
  unique ID.

  Variables:
    tid - unique Tag ID [Note: when a Tag object is created, tid is not checked
        against other Tag objects to assure uniqueness, it is assumed unique].
    name - name of tag.
  """

  def __init__(self, tid, name):
    self.tid = tid
    self.name = name

  def getDict(self):
    return {"tid": self.tid, "name": self.name}


class Competitor:
  """
  Represents a competitor from a database and includes the name, unique ID, and
  rank of the competitor. The competitor may also have an uncertainty value.

  Variables:
    cid - unique Competitor ID [Note: when a Competitor object is created, cid
        is not checked against other Competitor objects to assure uniqueness,
        it is assumed unique].
    name - name of competitor.
    rank - rank of competitor.
    uncertainty - uncertainty of competitor that influences how much the
        competitor's rank is affected by competitons.
  """

  def __init__(self, cid, name, rank):
    self.cid = cid
    self.name = name
    self.rank = rank

  def __init__(self, cid, name, rank, uncertainty):
    self.cid = cid
    self.name = name
    self.rank = rank
    self.uncertainty = uncertainty

  def getDict(self):
    comp = {"cid": self.cid, "name": self.name, "rank": self.rank}
    if self.uncertainty:
      comp["uncertainty"] = self.uncertainty
    return comp

def getCompetitors(db_name, tag_table, comp_table, rank_table):
  """
  Randomly selects a tag from the Tag table and two competitors from the
  Competitor table to be compared. For each competitor, if they have been
  compared using the selected tag before, their rank and uncertainty will be
  taken from the Rank table. Otherwise, their rank and uncertainty will be set
  to default values.

  Params:
    db_name - name of MySQL database.
    tag_table - name of MySQL table with all of the tags.
    comp_table - name of MySQL table with all of the competitors.
    rank_table - name of MySQL table with the ranks and uncertainties for
        competitors that have already been compared.

  Returns:
    tuple with Tag object, and two Competitors respectively.
  """
  #Get all data from the MySQL tables.
  db = database.DB(db_name)
  tags = db.query("SELECT * FROM {0}".format(tag_table))
  comps = db.query("SELECT * FROM {0}".format(comp_table))
  ranks = db.query("SELECT * FROM {0}".format(rank_table))

  print tags
  print comps
  print ranks

  # Randomly select the tag and competitors.
  random_tag = random.choice(tags)
  random_comp1 = random.choice(comps)
  while True:
    random_comp2 = random.choice(comps)
    if random_comp1["cid"] != random_comp2["cid"]:
      break

  # Create a Tag object for the tag.
  tag = Tag(random_tag["tid"], random_tag["name"])

  # Create a Competitor object for comp1.
  comp1_rank_data = db.query("SELECT rank, uncertainty FROM {0} WHERE tid={1} "
      "AND cid={2}".format(rank_table, tag.tid, random_comp1["cid"]))
  if len(comp1_rank_data) > 1:
    raise LookupError("Too many rows; should only return at most 1 row")
  elif len(comp1_rank_data) == 0:
    comp1 = Competitor(random_comp1["cid"], random_comp1["name"], 1500, 0.15)
  else:
    if (comp1_rank_data[0]["uncertainty"].lower() == "null" or
        comp1_rank_data[0]["uncertainty"] <= 0):
      comp1 = Competitor(random_comp1["cid"], random_comp1["name"],
          comp1_rank_data[0]["rank"])
    else:
      comp1 = Competitor(random_comp1["cid"], random_comp1["name"],
          comp1_rank_data[0]["rank"], comp1_rank_data[0]["uncertainty"])

  # Create a Competitor object for comp2.
  comp2_rank_data = db.query("SELECT rank, uncertainty FROM {0} WHERE tid={1} "
      "AND cid={2}".format(rank_table, tag.tid, random_comp2["cid"]))
  if len(comp2_rank_data) > 1:
    raise LookupError("Too many rows; should only return at most 1 row")
  elif len(comp2_rank_data) == 0:
    comp2 = Competitor(random_comp2["cid"], random_comp2["name"], 1500, 0.15)
  else:
    if (comp2_rank_data[0]["uncertainty"].lower() == "null" or
        comp2_rank_data[0]["uncertainty"] <= 0):
      comp2 = Competitor(random_comp2["cid"], random_comp2["name"],
          comp2_rank_data[0]["rank"])
    else:
      comp2 = Competitor(random_comp2["cid"], random_comp2["name"],
          comp2_rank_data[0]["rank"], comp2_rank_data[0]["uncertainty"])

  return (tag, comp1, comp2)


def updateRanks(db_name, tag_table, comp_table, rank_table, tag, comp1, comp2,
    winner_id):
  """
  Updates the ranks of competitors for a tag based on which was the winner. The
  updated competitors' ranks are then updated on the given MySQL database.

  Params:
    db_name - name of MySQL database.
    tag_table - name of MySQL table with all of the tags.
    comp_table - name of MySQL table with all of the competitors.
    rank_table - name of MySQL table with the ranks and uncertainties for
        competitors that have already been compared.
    tag - Tag object with which the competitors were compared.
    comp1 - first Competitor object to be compared.
    comp2 - second Competitor object to be compared.
    winner_id - unique ID of the winning competitor [Note: winner_id does not
        have to be specified. If winner_id is not specified, a winner will be
        chosen randomly, with chances weighted towards the competitor with the
        higher rank].
  """

def main(args):
  db_name = "LeagueRank"
  tag_table = "Tags"
  comp_table = "Champions"
  rank_table = "TagRanking"
  tag, comp1, comp2 = getCompetitors(db_name, tag_table, comp_table,
      rank_table)
  print tag.getDict()
  print comp1.getDict()
  print comp2.getDict()

if __name__ == "__main__":
  main(None)
