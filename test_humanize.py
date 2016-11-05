"""
Nose tests for humanizing time
"""

import flask_main

def test_humanize():
    assert flask_main.humanize_arrow_date('2015-11-04') == 'a year ago'
    assert flask_main.humanize_arrow_date('2016-10-04') == 'a month ago'
    assert flask_main.humanize_arrow_date('2016-11-02') == '2 days ago'
    assert flask_main.humanize_arrow_date('2016-11-03') == 'yesterday'
    assert flask_main.humanize_arrow_date('2016-11-04') == 'today'
    assert flask_main.humanize_arrow_date('2016-11-05') == 'tomorrow'
    assert flask_main.humanize_arrow_date('2016-11-06') == 'in 2 days'
    assert flask_main.humanize_arrow_date('2016-12-04') == 'in a month'
