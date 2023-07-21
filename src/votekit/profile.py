from ballot import Ballot
from typing import Optional
from pydantic import BaseModel, validator

# from functools import cache


class PreferenceProfile(BaseModel):
    """
    ballots (list of ballots): ballots from an election
    candidates (list): list of candidates, can be user defined
    """

    ballots: list[Ballot]
    candidates: Optional[list] = None

    @validator("candidates")
    def cands_must_be_unique(cls, candidates: list) -> list:
        if not len(set(candidates)) == len(candidates):
            raise ValueError("all candidates must be unique")
        return candidates

    def get_ballots(self) -> list[Ballot]:
        """
        Returns list of ballots
        """
        return self.ballots

    # @cache
    def get_candidates(self) -> list:
        """
        Returns list of unique candidates
        """
        if self.candidates is not None:
            return self.candidates

        unique_cands: set = set()
        for ballot in self.ballots:
            unique_cands.update(*ballot.ranking)

        return list(unique_cands)

    # can also cache
    def num_ballots(self):
        """
        Assumes weights correspond to number of ballots given to a ranking
        """
        num_ballots = 0
        for ballot in self.ballots:
            num_ballots += ballot.weight

        return num_ballots

    # class Config:
    #     arbitrary_types_allowed = True

    # def __init__(self, ballots, candidates):
    #     """
    #     Args:
    #         ballots (list of Ballot): a list of ballots in the election
    #         candidates (list of Candidates): a list of candidates in the election
    #     """
    #     self.id = uuid.uuid4()
    #     self.ballots = ballots
    #     self.candidates = candidates
    #     self.ballot_weights = [b.score for b in ballots]
