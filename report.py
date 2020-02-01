import datetime
from collections import defaultdict

from ft.simulation import Simulation

CURRENT_MATCHUP_PERIOD = 15
MY_TEAM = "CHOP"

ALL_TEAMS = ["AJZ", "ROSS", "PAT", "PANI", "HELM", "MEYE", "REIN", "DECK", "420", "CHOP"]

sim = Simulation(CURRENT_MATCHUP_PERIOD, MY_TEAM, last_num_periods=1)

def run():
    print(sim.run())


def generate_all_teams():
    today_str = datetime.datetime.today().strftime("%Y-%m-%d")
    for team in ALL_TEAMS:
        sim = Simulation(CURRENT_MATCHUP_PERIOD, team, last_num_periods=3)
        with open(f"ESPN_FBA_Simulation-{team}-{today_str}.txt", "w") as f:
            f.write(sim.run())


if __name__ == "__main__":
    run()
    # generate_all_teams()
