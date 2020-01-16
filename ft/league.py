class League(object):
    def __init__(self):
        self.teams = {}

    def add_team(self, team):
        """
        Args:
            team (ft.team.Team)
        """
        self.teams[team.id] = team
        team.league = self

    def get_team_by_abbrev(self, abbrev):
        """
        Args:
            abbrev (str): Team name abbreviation

        Returns:
            (ft.team.Team)
        """
        return next(t for t in self.teams.values() if t.abbrev == self.my_team_abbrev)
