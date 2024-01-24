import functools
import collections

from config import config
from ft.espn import Espn
from ft.team import Team
from ft.league import League
from ft.matchup import Matchup


class SimulationResult(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


ReportResult = collections.namedtuple("ReportResult", ["heading", "content"])


class Simulation(object):
    def __init__(self, period, my_team, last_num_periods=3):
        """
        period (int): The matchup period for which to run the analysis
        my_team (str): The abbrev of team we want to analyze
        last_num_periods (int): Nuber of historical periods to include in
            analysis
        """
        self.period = period
        self.my_team_abbrev = my_team
        self.last_num_periods = last_num_periods
        self.periods = range(max(period + 1 - last_num_periods, 1), period + 1)
        self.league = League()
        self.espn = Espn(season=2024)
        self.matchup_results_by_period = {}
        self.stat_wins_by_team = {}
        self.stat_wins_by_stat = collections.defaultdict(dict)
        self.overall_wins_by_team = collections.defaultdict(lambda: 0)
        self.build_league()
        self.derive_data()

    def build_league(self):
        data = self.espn.fetch_league_data(self.period)
        for team_data in data["teams"]:
            team = Team(team_data["id"], team_data["abbrev"])
            self.league.add_team(team)
        self.league.add_bye_team(Team(None, None))

        for period in self.periods:
            data = self.espn.fetch_league_data(period)
            for matchup_data in data["schedule"]:
                matchup = Matchup(matchup_data, self.league)
                self.league.teams[matchup.home_id].add_matchup(matchup)
                self.league.teams[matchup.away_id].add_matchup(matchup)

    @property
    def my_team(self):
        return self.league.get_team_by_abbrev(self.my_team_abbrev)

    @property
    def sorted_teams(self):
        return sorted(self.league.teams.values(), key=lambda t: t.abbrev)

    def run(self):
        return SimulationResult(
            **{
                report_name: getattr(self, report_name)
                for report_name in [
                    "current_matchup_prediction",
                    "next_matchup_prediction",
                    "historical_stat_rankings",
                    "historical_results",
                    "historical_records",
                    "historical_total_wins",
                ]
            }
        )

    def derive_data(self):
        for period in self.periods:
            results = []
            for team in self.sorted_teams:
                if team.id == self.my_team.id:
                    continue
                results.append(self.my_team.get_score_against(team, period))
            self.matchup_results_by_period[period] = results

        for team in self.sorted_teams:
            stat_wins = collections.defaultdict(lambda: 0)
            for period in self.periods:
                for opponent in self.sorted_teams:
                    if opponent is team:
                        continue
                    result = team.get_score_against(opponent, period)
                    if result.is_win:
                        self.overall_wins_by_team[team] += 1
                    else:
                        self.overall_wins_by_team[team] = self.overall_wins_by_team[
                            team
                        ]
                    for stat_id, winner in result.results.items():
                        if winner is team:
                            stat_wins[stat_id] += 1
                        else:
                            stat_wins[stat_id] = stat_wins[stat_id]
            self.stat_wins_by_team[team] = stat_wins
            for stat_id, wins in stat_wins.items():
                self.stat_wins_by_stat[stat_id][team] = wins

    def get_stat_ranks_for_team(self, team):
        """
        Args:
            team (ft.team.Team)

        Returns:
            (dict): Maps stat ID to rank
        """
        stat_ranks = {}
        for stat_id, wins_by_team in self.stat_wins_by_stat.items():
            ranked_teams = sorted(
                wins_by_team.items(), key=lambda i: i[1], reverse=True
            )
            rank = [i[0] for i in ranked_teams].index(team) + 1
            stat_ranks[stat_id] = rank
        return stat_ranks

    @property
    def current_opponent(self):
        """
        Returns:
            (ft.team.Team)
        """
        curr_matchup = self.my_team.matchups[self.period]
        opp_id = (
            curr_matchup.away_id
            if self.my_team.id == curr_matchup.home_id
            else curr_matchup.home_id
        )
        return self.league.teams[opp_id]

    @property
    def historical_results(self):
        res = ""
        for period, results in self.matchup_results_by_period.items():
            wins = [r for r in results if r.is_win]
            losses = [r for r in results if not r.is_win]
            res += "<br />"
            res += f"MATCHUP {period}: {len(wins)} wins, {len(losses)} losses<br />"
            res += "<br />"
            for r in results:
                res += f"{'W' if r.is_win else 'L'} {r.wins}-{r.losses}-{r.ties} vs. {r.opponent.abbrev}<br />"
        return ReportResult(
            f"Scores if {self.my_team.abbrev} had played ALL TEAMS in THE LAST {self.last_num_periods} MATCHUP PERIODS.",
            res,
        )

    @property
    def historical_records(self):
        res = ""
        historical_records = collections.defaultdict(
            lambda: {"wins": 0, "losses": 0, "ties": 0}
        )
        for period, results in self.matchup_results_by_period.items():
            for r in results:
                res_type = None
                if r.is_win:
                    res_type = "wins"
                elif r.is_tie:
                    res_type = "ties"
                else:
                    res_type = "losses"
                historical_records[r.opponent][res_type] += 1
        for opponent, record in historical_records.items():
            wins = record["wins"]
            losses = record["losses"]
            ties = record["ties"]
            is_win = wins > losses
            res += f"{'W' if is_win else 'L'} {wins}-{losses}-{ties} vs. {opponent.abbrev}<br />"
        return ReportResult(
            f"Historical record vs. each team, if {self.my_team.abbrev} had played all teams in THE LAST {self.last_num_periods} MATCHUP PERIODS:",
            res,
        )

    @property
    def historical_total_wins(self):
        res = ""
        sorted_rankings = sorted(
            self.overall_wins_by_team.items(), key=lambda r: r[1], reverse=True
        )
        for team, overall_wins in sorted_rankings:
            res += f"{team.abbrev} - {overall_wins}<br />"

        res += "<br />"
        res += "Number of wins by stat:<br />"
        res += "<br />"
        for stat_id in config.SCORING_STAT_IDS:
            stat_rankings = [
                (team, stat_wins[stat_id])
                for team, stat_wins in self.stat_wins_by_team.items()
            ]
            sorted_rankings = sorted(stat_rankings, key=lambda r: r[1], reverse=True)
            res += f"{config.STAT_NAMES[stat_id]}:<br />"
            res += "<br />"
            for team, overall_wins in sorted_rankings:
                res += f"{team.abbrev} - {overall_wins}<br />"
            res += "<br />"
        return ReportResult(
            f"Number of wins if each team had played all other teams in THE LAST {self.last_num_periods} MATCHUP PERIODS:",
            res,
        )

    @property
    def historical_stat_rankings(self):
        res = ""
        stat_ranks = self.get_stat_ranks_for_team(self.my_team)
        for stat_id, rank in sorted(stat_ranks.items(), key=lambda i: i[1]):
            res += f"{config.STAT_NAMES[stat_id]}: {rank}<br />"
        return ReportResult(
            f"{self.my_team.abbrev}'s ranking by stat if each team had played all other teams in THE LAST {self.last_num_periods} MATCHUP PERIODS:",
            res,
        )

    def matchup_prediction(self, team):
        res = ""
        my_ranks = self.get_stat_ranks_for_team(self.my_team)
        their_ranks = self.get_stat_ranks_for_team(team)
        wins = []
        for stat_id, rank in my_ranks.items():
            if rank < their_ranks[stat_id]:
                wins.append(stat_id)
        total = len(my_ranks.keys())
        win_count = len(wins)
        loss_count = total - win_count
        res += f"{self.my_team.abbrev} is projected to {'win' if win_count > loss_count else 'lose'} {win_count}-{loss_count} based on data from THE LAST {self.last_num_periods} MATCHUP PERIODS:<br />"
        res += "<br />"
        for stat_id in my_ranks.keys():
            stat_name = config.STAT_NAMES[stat_id]
            my_rank = my_ranks[stat_id]
            their_rank = their_ranks[stat_id]
            res += f"{'W' if stat_id in wins else 'L'} {stat_name} ({my_rank} vs. {their_rank})<br />"
        return res

    @property
    def current_matchup_prediction(self):
        current_team = self.my_team.get_opponent_by_period(self.period)
        res = self.matchup_prediction(current_team)
        return ReportResult(
            f"{self.my_team.abbrev}'s current matchup is {current_team.abbrev}", res
        )

    @property
    def next_matchup_prediction(self):
        next_data = self.espn.fetch_league_data(self.period + 1)
        next_team = None
        for matchup_data in next_data["schedule"]:
            if "away" not in matchup_data:
                away_id = self.league.BYE_TEAM_ID
            else:
                away_id = matchup_data["away"]["teamId"]
            home_id = matchup_data["home"]["teamId"]
            if self.my_team.id == away_id:
                next_team = self.league.teams[home_id]
            if self.my_team.id == home_id:
                next_team = self.league.teams[away_id]

        if next_team is None:
            return None
        res = self.matchup_prediction(next_team)
        return ReportResult(
            f"{self.my_team.abbrev}'s next matchup is {next_team.abbrev}", res
        )
