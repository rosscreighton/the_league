from collections import defaultdict

from config import config
from ft.espn import Espn
from ft.team import Team
from ft.league import League
from ft.matchup import Matchup

CURRENT_PERIOD = 3
MY_TEAM = 3
PERIODS = range(1, CURRENT_PERIOD + 1)

espn = Espn()
data = espn.fetch_league_data(CURRENT_PERIOD)

league = League()
for team_data in data["teams"]:
    team = Team(team_data["id"], team_data["abbrev"], league)

for period in PERIODS:
    data = espn.fetch_league_data(period)
    for matchup_data in data["schedule"]:
        matchup = Matchup(matchup_data)
        home_id = matchup.home_id
        away_id = matchup.away_id
        league.teams[home_id].add_matchup(matchup)
        league.teams[away_id].add_matchup(matchup)

my_team = league.teams[MY_TEAM]
print("")
print(f"Report for team {my_team.abbrev}")

sorted_teams = sorted(league.teams.values(), key=lambda t: t.abbrev)
historical_records = defaultdict(lambda: {"wins": 0, "losses": 0})

for period in PERIODS:
    results = []
    for team in sorted_teams:
        if team.id == my_team.id:
            continue
        wins, losses, ties = my_team.get_score_against(team.id, period)
        is_win = wins > losses
        results.append((team, is_win, wins, losses, ties))
        if is_win:
            historical_records[team]["wins"] += 1
        else:
            historical_records[team]["losses"] += 1
    wins = [r for r in results if r[1]]
    losses = [r for r in results if not r[1]]
    print("")
    print(f"WEEK {period} - {len(wins)} wins, {len(losses)} losses:")
    print("")
    for team, is_win, wins, losses, ties in results:
        print(f"{'W' if is_win else 'L'} {wins}-{losses}-{ties} vs. {team.abbrev}")


print("")
print(f"Historical record vs. each team")
print("")
for team, record in historical_records.items():
    wins = record["wins"]
    losses = record["losses"]
    is_win = wins > losses
    print(f"{'W' if is_win else 'L'} {wins}-{losses} vs. {team.abbrev}")


print("")
print("Power rankings:")
print("")
rankings = []
for team in sorted_teams:
    overall_wins = 0
    for period in PERIODS:
        for opponent in sorted_teams:
            wins, losses, ties = team.get_score_against(opponent.id, period)
            if wins > losses:
                overall_wins += 1
    rankings.append((team, overall_wins))
sorted_rankings = sorted(rankings, key=lambda r: r[1], reverse=True)
for team, overall_wins in sorted_rankings:
    print(f"{team.abbrev} - {overall_wins}")
