import requests


SESSION_TOKEN = "AEBTme8atYoFS7%2F%2F3Hua%2B6yMowd3TwWtmI9AJQ1aY7XH%2BpFt%2BDmLMaxjZatwi%2F1Z0fm%2BuEoVNH0WK%2FS%2FJZ1TVkNli9LsuSs95dhrv9GjVPDhI0JlJbJ5Jqw%2BfMv0aqfb21Mw0h2V0SartwqYX8N5QUkgOnjlIFvZaEI9Q8971zz0e%2FuHhZEZ7tVXTusbhPeCSUhu4eRA5py1swPHhM40r3blg6tz377iwXXOzrX7o6Wr9CboSES6MYsti2Oekn%2F65fXy37tlSWBT2oDI3japvDfQ"

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
        self.season = kwargs.pop("season", 2020)
        self.segment = kwargs.pop("segment", 0)
        self.league_id = kwargs.pop("league_id", 239167)
        self.session_token = kwargs.pop("session_token", SESSION_TOKEN)

    def fetch_league_data(self, matchup_period):
        """
        Args:
            matchup_period (str)
        """
        cookies = {"espn_s2": SESSION_TOKEN}
        headers = {"x-fantasy-filter": '{"schedule":{"filterMatchupPeriodIds":{"value":[' + str(matchup_period) + ']}}}'}
        query_params = "?" + "&".join([f"{k}={v}" for k, v in QUERY_PARAMS])
        url = f"https://fantasy.espn.com/apis/v3/games/fba/seasons/{self.season}/segments/0/leagues/{self.league_id}{query_params}"
        res = requests.get(url, cookies=cookies, headers=headers)
        res.raise_for_status()
        return res.json()
