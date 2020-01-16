from collections import defaultdict

from ft.simulation import Simulation

CURRENT_MATCHUP_PERIOD = 13
MY_TEAM = "ROSS"

sim = Simulation(CURRENT_MATCHUP_PERIOD, MY_TEAM)

reports =  [
    "historical_results",
    "historical_records",
    "historical_total_wins",
    "historical_stat_rankings",
]

for rep in reports:
    getattr(sim, rep)
    print("")
