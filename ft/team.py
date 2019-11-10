from config import config


class Team(object):
    def __init__(self, id_, abbrev, league):
        """
        Args:
            id_ (int): The ESPN team ID
            abbrev (str): The ESPN abbreviation
            league (ft.league.League)
        """
        self.id = id_
        self.abbrev = abbrev
        self.league = league
        self.matchups = {}
        league.add_team(self)

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
        """
        return self.matchups[period].box_score[self.id]

    def get_score_against(self, team_id, period):
        """
        Args:
            team_id (int)
            period (int)
        """
        opponent = self.league.teams[team_id]
        their_scores = opponent.box_score_for_period(period)
        our_scores = self.box_score_for_period(period)
        wins = 0
        losses = 0
        ties = 0
        for stat_id in config.SCORING_STAT_IDS:
            if our_scores[stat_id] > their_scores[stat_id]:
                wins += 1
            elif our_scores[stat_id] < their_scores[stat_id]:
                losses += 1
            else:
                ties += 1
        return (wins, losses, ties)
