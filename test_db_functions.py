"""
Nose tests for db_functions.py
"""

import db_functions, flask_main, uuid, arrow

col = db_functions.connect() # db collection

def test_create_remove():
    """
    Make sure memos are properly added and removed from the database
    """
    uid = uuid.uuid4()
    assert col.find({ '_id': uid }).count() == 0

    db_functions.create('memo text', '2017-01-01', uid)
    assert col.find({ '_id': uid }).count() == 1

    db_functions.remove(uid)
    assert col.find({ '_id': uid }).count() == 0

def test_get():
    """
    Make sure memos are returned in chronological order
    """
    memo_list = db_functions.get_memos()
    for i in range(0, len(memo_list)):
        if i != (len(memo_list) - 1):
            assert memo_list[i]['date'] < memo_list[i+1]['date']
