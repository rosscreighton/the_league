from config import config


class Matchup(object):
    def __init__(self, data, league=None):
        """
        Args:
            data (dict): From the https://fantasy.espn.com/apis/v3/games/fba/seasons/2020/segments/0/leagues/
                endpoint - body.schedule[<some index>]
        """
        self.data = data
        self.league = league
        self.box_score = {
            self.home_id: self.calc_stats("home"),
            self.away_id: self.calc_stats("away"),
        }

    @property
    def period(self):
        """
        Returns:
            (int)
        """
        return self.data["matchupPeriodId"]

    @property
    def home_id(self):
        """
        Returns:
            (int)
        """
        return self.data["home"]["teamId"]

    @property
    def away_id(self):
        """
        Returns:
            (int)
        """
        return self.data["away"]["teamId"]

    @property
    def home_team(self):
        """
        Returns:
            (int)
        """
        return self.league.teams[self.home_id]

    @property
    def away_team(self):
        """
        Returns:
            (int)
        """
        return self.league.teams[self.away_id]

    def calc_stats(self, team_type):
        """
        Args:
            team_type (str): home|away

        Returns:
            scoring_stats (dict): Maps stat ID to score
        """
        team_data = self.data[team_type]

        stats_up_to_current_scoring_period = {
            int(stat_id): stat_data["score"]
            for stat_id, stat_data in team_data["cumulativeScore"][
                "scoreByStat"
            ].items()
            if int(stat_id) in config.COUNTING_STAT_IDS
        }
        stats_for_current_scoring_period = {}
        if "rosterForCurrentScoringPeriod" in team_data:
            for player in team_data["rosterForCurrentScoringPeriod"]["entries"]:
                player_stats = player["playerPoolEntry"]["player"]["stats"]
                if not player_stats:
                    continue
                for stat_id, score in player_stats[0]["stats"].items():
                    stat_id = int(stat_id)
                    if stat_id not in config.COUNTING_STAT_IDS:
                        continue
                    cumulative_score = stats_for_current_scoring_period.get(stat_id, 0)
                    stats_for_current_scoring_period[stat_id] = cumulative_score + score
        counted_stats = {}
        for stat_id, score in stats_up_to_current_scoring_period.items():
            current_score = stats_for_current_scoring_period.get(stat_id, 0)
            counted_stats[stat_id] = score + current_score

        scoring_stats = {}

        fgm = counted_stats[config.STAT_IDS["FGM"]]
        fga = counted_stats[config.STAT_IDS["FGA"]]
        ftm = counted_stats[config.STAT_IDS["FTM"]]
        fta = counted_stats[config.STAT_IDS["FTA"]]
        scoring_stats[config.STAT_IDS["FG%"]] = fgm / fga if fga else 0
        scoring_stats[config.STAT_IDS["FT%"]] = ftm / fta if fta else 0

        for stat_id, score in counted_stats.items():
            if stat_id not in [
                config.STAT_IDS[name] for name in ["FGA", "FGM", "FTA", "FTM"]
            ]:
                scoring_stats[stat_id] = score
        return scoring_stats
