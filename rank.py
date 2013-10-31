#! /usr/bin/env python

import random

from __future__ import division

"""
Competition between two given competitors. The competitors' ranks are
updated based on the results of the competition and returned.
"""


def compete(comp1, comp2, winner_id=None, decr_uncertainty=0.002,
    min_uncertainty=0.05):
  """
  Competetion between the given two competitors. Their ranks are updated as a
  result of the competition. If a winner_id is not specified or an id that does
  not belong to one of the competitors is specified, the winner will be
  determined semi-randomly, with a winner chosen at random, but weighted
  towards the competitor with the higher rank. Competitors are represented as
  dicts that include an id and a rank and no other fields. If a competitor does
  not have an id or rank, then an error will be thrown. The minimum uncertainty
  and the amount that uncertainty is decreased by can also be specified for
  updating the uncertainties of each competitor.

  Params:
    comp1 - first competitor.
    comp2 - second competitor.
    winner_id - id of the competitor that is the winner, set to None by
        default.
    decr_uncertainty - amount that uncertainty is decreased by, set to 0.2%
        (0.002) by default.
    min_uncertainty - minumum value allowed for an uncertainty, set to 5%
        (0.05) by default.

  Returns:
    tuple with updated comp1, updated comp2, and winner_id respectively.

  Raises:
    TypeError - if either competitor is not a valid.
  """
  # Check that both competitors are valid.
  try:
    isValidCompetitor(comp1)
    isValidCompetitor(comp2)
  except:
    raise TypeError("Invalid competitor")

  # If a winner_id isn't specified, one is semi-randomly determined.
  if not winner_id or not winner_id in [comp1["id"], comp2["id"]]:
    favored = dict()
    unfavored = dict()
    if comp1["rank"] > comp2["rank"]:
      favored = comp1
      unfavored = comp2
    else:
      favored = comp2
      unfavored = comp1
    if random.random() >= (favored["rank"] / (favored["rank"] +
        unfavored["rank"])):
      winner_id = unfavored["id"]
    else:
      winner_id = favored["id"]

  # Assign the winner and loser
  winner = dict()
  loser = dict()
  if winner_id == comp1["id"]:
    winner = comp1
    loser = comp2
  else:
    winner = comp2
    loser = comp1

  # Update ranks and uncertainties
  winner, loser = updateRanks(winner, loser, decr_uncertainty=decr_uncertainty,
      min_uncertainty=min_uncertainty)

  if winner["id"] = comp1["id"]:
    return winner, loser, winner_id
  return loser, winner, winner_id


def isValidCompetitor(comp):
  """
  Checks whether the given object is a valid competitor that includes an id and
  a rank. If the object is not a valid an error will be thrown.

  Params:
    comp - competitor.

  Returns:
    True if the object is a valid competitor.

  Raises:
    TypeError - if object is not a dict.
    KeyError - if dict does not have an id or rank key.
    LookupError - if dict does not have an id or valid rank.
  """
  if not isinstance(comp, dict):
    raise TypeError("Invalid object; competitor must be a dict")
  if not "id" in comp:
    raise KeyError("Invalid competitor; competitor must include an id")
  if not "rank" in comp:
    raise KeyError("Invalid competitor; competitor must include a rank")
  if not comp["id"]:
    raise LookupError("Invalid competitor; competitor must include an id")
  if not comp["rank"]:
    raise LookupError("Invalid competitor; competitor must include a rank")
  else if not comp["rank"] > 0:
    raise LookupError("Invalid rank; rank must be greater than 0")

  return True


def updateRanks(winner, loser, decr_uncertainty=0.002, min_uncertainty=0.05):
  """
  Updates the ranks of the winner and loser. The amount that each's rank is
  changed is based on which competitor was favored. An optional uncertainty
  value is also checked to determine the amount that each's rank is altered.
  If an uncertainty value is not specified, a value of 10% (0.10) will be used.
  Uncertainty values will be decreased by the specified amount, if an amount
  is not specified, they will be decreased by 0.2% (0.002) down to a minimum
  uncertainty value that will be 5% (0.05) by default.

  Params:
    winner - winning competitor.
    loser - losing competitor.
    decr_uncertainty - amount that uncertainty is decreased by.
    min_uncertainty - minumum uncertainty value.

  Returns:
    tuple containing updated winner and loser respectively.

  Raises:
    TypeError - if either competitor is not valid.
  """
  # Check that both competitors are valid.
  try:
    isValidCompetitor(winner)
    isValidCompetitor(loser)
  except:
    raise TypeError("Invalid competitor")

  # Determine the favored competitor.
  favored = NULL
  favored_rank = 0
  unfavored_rank = 0
  if winner["rank"] > loser["rank"]:
    favored = winner["id"]
    favored_rank = winner["rank"]
    unfavored_rank = loser["rank"]
  else:
    favored = loser["id"]
    favored_rank = loser["rank"]
    unfavored_rank = winner["rank"]

  # Update winner's rank
  uncertainty = 0.10 # Default uncertainty value.
  if "uncertainty" in winner:
    uncertainty = winner["uncertainty"]
    if uncertainty > (min_uncertainty + decr_uncertainty):
      winner["uncertainty"] = uncertainty - decr_uncertainty
    else:
      winner["uncertainty"] = min_uncertainty
  if favored = winner["id"]:
    winner["rank"] = favored_rank + (uncertainty * unfavored_rank)
  else:
    winner["rank"] = unfavored_rank + (uncertainty * favored_rank)

  # Update loser's rank
  uncertainty = 0.10 # Default uncertainty value.
  if "uncertainty" in loser:
    uncertainty = loser["uncertainty"]
    if uncertainty > (min_uncertainty + decr_uncertainty):
      loser["uncertainty"] = uncertainty - decr_uncertainty
    else:
      loser["uncertainty"] = min_uncertainty
  if favored = loser["id"]:
    loser["rank"] = favored_rank - (uncertainty * favored_rank)
  else:
    loser["rank"] = unfavored_rank - (uncertainty * unfavored_rank)

  return winner, loser
