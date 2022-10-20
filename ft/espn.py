import requests


SESSION_TOKEN = "AEB1OP0LRm6OyUEb3syy%2FZgSmALxhJDo0kUaG7YRg1QqpOVPqSDqA2U3U6AVs1s4JHdIXcKoshN%2FPeVbuXnlS4cjA67eTdNbIrpMakcp3gwtnKH%2BRv%2FSOtZS6tTcWwKTEvIO4gnO2Z63xIWikorhJtGEK0HC4t3nLJsXVxTMd%2Br8opTO2FT5ojJaVUNjOnk7Qeu0fGkJQVRgFS9WfRtUZ9P5%2FozqK6i0r1aodsU6MwcJ%2Bm6dJ3lhfOGaUJaWivU3QLhcuBde7mfXyi1fLT8eI8HP"

QUERY_PARAMS = [
    ("view", "mMatchupScore"),
    ("view", "mNav"),
    ("view", "mPendingTransactions"),
    ("view", "mRoster"),
    ("view", "mScoreboard"),
    ("view", "mSettings"),
    ("view", "mStatus"),
    ("view", "mTeam"),
    ("view", "mTopPerformers"),
    ("view", "modular"),
]


class Espn(object):
    """
    This class encapsulates communication with the ESPN https://fantasy.espn.com API
    """

    def __init__(self, **kwargs):
        """
        Args:
            session_token (str): The value of the espn_s2 cookie taken from a
                logged in fantasy.espn.com account.
            season (int): Four digit year of season
            segment (int): Not sure what this is yet. Always 0 for now.
            league_id (int)
        """
        self.season = kwargs.pop("season", 2023)
        self.segment = kwargs.pop("segment", 0)
        self.league_id = kwargs.pop("league_id", 239167)
        self.session_token = kwargs.pop("session_token", SESSION_TOKEN)

    def fetch_league_data(self, matchup_period):
        """
        Args:
            matchup_period (str)
        """
        cookies = {"espn_s2": SESSION_TOKEN}
        headers = {
            "x-fantasy-filter": '{"schedule":{"filterMatchupPeriodIds":{"value":['
            + str(matchup_period)
            + "]}}}"
        }
        query_params = "?" + "&".join([f"{k}={v}" for k, v in QUERY_PARAMS])
        url = f"https://fantasy.espn.com/apis/v3/games/fba/seasons/{self.season}/segments/0/leagues/{self.league_id}{query_params}"
        res = requests.get(url, cookies=cookies, headers=headers)
        res.raise_for_status()
        return res.json()
