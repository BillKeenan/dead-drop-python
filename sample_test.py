from unittest.mock import patch
from deadWeb.dead import test
import mock
import pprint

# @patch('pymongo.MongoClient')
# def test_dead(mock):
#   pprint(pymongo.MongoClient)
# content of test_sample.py
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4
