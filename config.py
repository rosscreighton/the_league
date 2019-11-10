STAT_NAMES = {
    0: "PTS",
    1: "BLK",
    2: "STL",
    3: "AST",
    4: "OREB",
    5: "DREB",
    6: "REB",
    7: "",
    8: "",
    9: "PF",
    10: "",
    11: "TO",
    12: "",
    13: "FGM",
    14: "FGA",
    15: "FTM",
    16: "FTA",
    17: "3PTM",
    18: "3PTA",
    19: "FG%",
    20: "FT%",
    21: "3PT%",
    22: "",
    23: "",
    24: "",
    25: "",
    26: "",
    27: "",
    28: "MPG",
    29: "",
    30: "",
    31: "",
    32: "",
    33: "",
    34: "",
    35: "",
    36: "",
    37: "DD",
    38: "",
    39: "",
    40: "MIN",
    41: "GP",
    42: "",
    43: "",
    44: "",
}

STAT_IDS = {v: k for k, v in STAT_NAMES.items()}


class Config(object):
    def __init__(self):
        pass

    SCORING_STATS = [
        "PTS",
        "BLK",
        "STL",
        "AST",
        "REB",
        "3PTM",
        "FG%",
        "FT%",
        "DD",
    ]

    COUNTING_STATS = [
        "PTS",
        "BLK",
        "STL",
        "AST",
        "REB",
        "3PTM",
        "DD",
        "FGM",
        "FGA",
        "FTM",
        "FTA",
    ]

    SCORING_STAT_IDS = [STAT_IDS[stat] for stat in SCORING_STATS]
    COUNTING_STAT_IDS = [STAT_IDS[stat] for stat in COUNTING_STATS]
    STAT_IDS = STAT_IDS
    STAT_NAMES = STAT_NAMES

config = Config()
