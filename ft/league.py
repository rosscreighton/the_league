class League(object):
    BYE_TEAM_ID = 1000000000000

    def __init__(self):
        self.teams = {}
        self.next_matchup_data = {}

    def add_team(self, team):
        """
        Args:
            team (ft.team.Team)
        """
        self.teams[team.id] = team
        team.league = self

    def add_bye_team(self, team):
        """
        Args:
            team (ft.team.Team)
        """
        team.id = self.BYE_TEAM_ID
        team.abbrev = "BYE"
        self.teams[team.id] = team
        team.league = self

    def get_team_by_abbrev(self, abbrev):
        """
        Args:
            abbrev (str): Team name abbreviation

        Returns:
            (ft.team.Team)
        """
        return next(t for t in self.teams.values() if t.abbrev == abbrev)
