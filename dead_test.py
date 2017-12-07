from unittest.mock import patch, ANY
from deadWeb.dead import test, drop_handler
import pprint

@patch('pymongo.MongoClient')
def test_dead(mock_pymongo):
  dead = drop_handler(mock_pymongo)
  data = {"test":"here"}
  dead.drop(data)
  pprint.pprint (mock_pymongo.dead.drop.insert_one.assert_called_with({"key": ANY, "data":data}))


@patch('pymongo.MongoClient')
def test_drop_deleted_when_accessed(mock_pymongo):

  key = "anything"
  mock_pymongo.dead.drop.find.return_value=[{'data':"test data return"}]
  dead = drop_handler(mock_pymongo)
  val = dead.pickup(key)
  
  assert val == "test data return"
  pprint.pprint (mock_pymongo.dead.drop.find.assert_called_with({"key": key}))
  pprint.pprint (mock_pymongo.dead.drop.remove.assert_called_with({"key": key}))
