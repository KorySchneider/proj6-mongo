"""
Nose tests for humanizing time
"""

import flask_main, arrow

def test_humanize():
    """
    Make sure times are humanized correctly
    """
    today = arrow.now()
    assert flask_main.humanize_arrow_date(today.replace(years=-1).date()) == 'a year ago'
    assert flask_main.humanize_arrow_date(today.replace(months=-1).date()) == 'a month ago'
    assert flask_main.humanize_arrow_date(today.replace(days=-2).date()) == '2 days ago'
    assert flask_main.humanize_arrow_date(today.replace(days=-1).date()) == 'yesterday'
    assert flask_main.humanize_arrow_date(today.date()) == 'today'
    assert flask_main.humanize_arrow_date(today.replace(days=+1).date()) == 'tomorrow'
    assert flask_main.humanize_arrow_date(today.replace(days=+2).date()) == 'in 2 days'
    assert flask_main.humanize_arrow_date(today.replace(months=+1).date()) == 'in a month'
    assert flask_main.humanize_arrow_date(today.replace(years=+1).date()) == 'in a year'
