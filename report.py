import datetime
from collections import defaultdict

from jinja2 import Template

from ft.simulation import Simulation
from ft.template import HOME_TEMPLATE, TEAM_TEMPLATE

CURRENT_MATCHUP_PERIOD = 18
MY_TEAM = "ROSS"

ALL_TEAMS = [
    "420",
    "AJZ",
    "CHOP",
    "DECK",
    "HELM",
    "MEYE",
    "PANI",
    "PAT",
    "REIN",
    "ROSS",
]

sim = Simulation(CURRENT_MATCHUP_PERIOD, MY_TEAM, last_num_periods=1)


def run():
    print(sim.run())


def generate_all_teams():
    today_str = datetime.datetime.today().strftime("%Y-%m-%d")
    home_template = Template(HOME_TEMPLATE)
    with open(f"public/index.html", "w") as f:
        f.write(home_template.render(teams=ALL_TEAMS))
    team_template = Template(TEAM_TEMPLATE)
    for team in ALL_TEAMS:
        print(f"Generating {team}")
        sim = Simulation(CURRENT_MATCHUP_PERIOD, team, last_num_periods=3)
        simulation_result = sim.run()
        with open(f"public/{team}.html", "w") as f:
            f.write(team_template.render(simulation_result=simulation_result))


if __name__ == "__main__":
    # run()
    generate_all_teams()
