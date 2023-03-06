from config import config


class MatchupResult(object):
    def __init__(self, team, opponent, period):
        """
        Args:
            team (ft.team.Team)
            opponent (ft.team.Team)
            period (int): The period in which this matchup took place
        """
        self.team = team
        self.opponent = opponent
        self.period = period

    @property
    def our_scores(self):
        """
        Returns:
            (dict): Maps stat ID to score
        """
        if self.team.id == self.team.league.BYE_TEAM_ID:
            return {stat_id: 0 for stat_id in self.their_scores.keys()}
        return self.team.box_score_for_period(self.period)

    @property
    def their_scores(self):
        """
        Returns:
            (dict): Maps stat ID to score
        """
        if self.opponent.id == self.team.league.BYE_TEAM_ID:
            return {stat_id: 0 for stat_id in self.our_scores.keys()}
        return self.opponent.box_score_for_period(self.period)

    @property
    def results(self):
        """
        Returns:
            (dict) Maps stat ID to winning team or None for a tie
        """
        res = {}

        for stat_id in config.SCORING_STAT_IDS:
            winner = None
            if self.our_scores[stat_id] > self.their_scores[stat_id]:
                winner = self.team
            elif self.our_scores[stat_id] < self.their_scores[stat_id]:
                winner = self.opponent
            res[stat_id] = winner

        return res

    @property
    def wins(self):
        """
        Returns:
            (int): Number of wins for self.team in this matchup
        """
        return len([team for team in self.results.values() if team is self.team])

    @property
    def losses(self):
        """
        Returns:
            (int): Number of losses for self.team in this matchup
        """
        return len([team for team in self.results.values() if team is self.opponent])

    @property
    def ties(self):
        """
        Returns:
            (int): Number of wins for self.team in this matchup
        """
        return len([team for team in self.results.values() if team is None])

    @property
    def is_win(self):
        return self.wins > self.losses

    @property
    def is_tie(self):
        return self.wins == self.losses
