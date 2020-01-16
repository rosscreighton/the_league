from config import config

from ft.matchup_result import MatchupResult


class Team(object):
    def __init__(self, id_, abbrev):
        """
        Args:
            id_ (int): The ESPN team ID
            abbrev (str): The ESPN abbreviation
        """
        self.id = id_
        self.abbrev = abbrev
        self.league = None
        self.matchups = {}

    def add_matchup(self, matchup):
        """
        Args:
            matchup_period (int)
            match (ft.matchup.Matchup)
        """
        self.matchups[matchup.period] = matchup

    def box_score_for_period(self, period):
        """
        Args:
            period (int)

        Returns:
            (dict): Maps stat ID to score for this team and period
        """
        return self.matchups[period].box_score[self.id]

    def get_score_against(self, opponent, period):
        """
        Args:
            opponent (ft.team.Team)
            period (int)

        Returns:
            (ft.matchup_result.MatchupResult)
        """
        return MatchupResult(self, opponent, period)
