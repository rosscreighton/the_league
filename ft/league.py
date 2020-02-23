class League(object):
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

    def get_team_by_abbrev(self, abbrev):
        """
        Args:
            abbrev (str): Team name abbreviation

        Returns:
            (ft.team.Team)
        """
        return next(t for t in self.teams.values() if t.abbrev == abbrev)

    def get_next_matchup_for_team(self, team):
        """
        Args:
            team (ft.team.Team)

        Returns:
            (ft.team.Team)
        """
        matchup_map = {}
        for matchup in self.next_matchup_data["schedule"]:
            matchup_map[matchup["home"]["teamId"]] = matchup["away"]["teamId"]
            matchup_map[matchup["away"]["teamId"]] = matchup["home"]["teamId"]
        return self.teams[matchup_map[team.id]]
