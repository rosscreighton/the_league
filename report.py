from collections import defaultdict

from ft.simulation import Simulation

CURRENT_MATCHUP_PERIOD = 13

sim = Simulation(CURRENT_MATCHUP_PERIOD)

reports =  [
    "historical_results",
    "historical_records",
    "historical_total_wins",
    "historical_stat_rankings",
]

for rep in reports:
    getattr(sim, rep)
    print("")
