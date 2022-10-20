import datetime
import logging
from collections import defaultdict

from jinja2 import Template

from ft.simulation import Simulation
from ft.template import HOME_TEMPLATE, TEAM_TEMPLATE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CURRENT_MATCHUP_PERIOD = 1
LAST_NUM_PERIODS = 1
MY_TEAM = "ROSS"

ALL_TEAMS = [
    "420",
    "AJZ",
    "CHOP",
    "DECK",
    "IAN ",
    "JZ",
    "NUT",
    "PANI",
    "PAT",
    "PRYN",
    "PSQd",
    "ROSS",
]


def generate_all_teams():
    today_str = datetime.datetime.today().strftime("%Y-%m-%d")
    home_template = Template(HOME_TEMPLATE)
    with open(f"public/index.html", "w") as f:
        f.write(home_template.render(teams=ALL_TEAMS))
    team_template = Template(TEAM_TEMPLATE)
    for team in ALL_TEAMS:
        print(f"Generating {team}")
        try:
            sim = Simulation(
                CURRENT_MATCHUP_PERIOD, team, last_num_periods=LAST_NUM_PERIODS
            )
            simulation_result = sim.run()
        except:
            logger.exception("Could not run simulation for %s", team)
            continue
        with open(f"public/{team}.html", "w") as f:
            f.write(team_template.render(simulation_result=simulation_result))


if __name__ == "__main__":
    generate_all_teams()
