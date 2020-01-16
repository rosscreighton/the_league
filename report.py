from collections import defaultdict

from ft.simulation import Simulation

sim = Simulation(13)
for rep in ["historical_results", "historical_records", "historical_total_wins"]:
    getattr(sim, rep)
    print("")
raise
