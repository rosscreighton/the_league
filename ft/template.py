HOME_TEMPLATE = """
<!Doctype html>
<html>
<head>
    <title>The League</title>
    <style>
        body {
            font-family: "Lucida Console", Monaco, monospace;
            margin: 50px;
        }
    </style>
</head>
<body>
    {% for team_name in teams %}
        <p><a href="{{team_name}}.html">{{team_name}}</a></p>
    {% endfor %}
</body>
</html>
"""

TEAM_TEMPLATE = """
<!Doctype html>
<html>
<head>
    <title>The League</title>
    <style>
        body {
            font-family: "Lucida Console", Monaco, monospace;
            margin: 50px;
        }
    </style>
</head>
<body>
    {% for report_name in [
        "current_matchup_prediction",
        "historical_stat_rankings",
        "historical_results",
        "historical_records",
        "historical_total_wins",
    ] %}
        <h2>{{simulation_result|attr(report_name)|attr('heading')}}</h2>
        <p>{{simulation_result|attr(report_name)|attr('content')}}</p>
    {% endfor %}
</body>
</html>
"""
