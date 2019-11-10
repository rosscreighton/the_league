class League(object):
    def __init__(self):
        self.teams = {}

    def add_team(self, team):
        """
        Args:
            team (ft.team.Team)
        """
        self.teams[team.id] = team
