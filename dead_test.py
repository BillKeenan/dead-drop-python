from unittest.mock import patch, ANY
from deadWeb.dead import  drop_handler
import pprint

@patch('pymongo.MongoClient')
def test_dead(mock_pymongo):
  dead = drop_handler(mock_pymongo)
  data = {"test":"here"}
  dead.drop(data)
  mock_pymongo.dead.drop.insert_one.assert_called_with({"key": ANY, "data":data})


@patch('pymongo.MongoClient')
def test_drop_deleted_when_accessed(mock_pymongo):

  key = "anything"
  mock_pymongo.dead.drop.find.return_value=[{'data':"test data return"}]
  dead = drop_handler(mock_pymongo)
  val = dead.pickup(key)
  
  assert val == "test data return"
  mock_pymongo.dead.drop.find.assert_called_with({"key": key})
  mock_pymongo.dead.drop.remove.assert_called_with({"key": key})





@patch('pymongo.MongoClient')
def test_return_none_when_not_existing(mock_pymongo):

  key = "anything"
  mock_pymongo.dead.drop.find.return_value=[]
  dead = drop_handler(mock_pymongo)
  val = dead.pickup(key)
  
  assert val == "{}"
  mock_pymongo.dead.drop.find.assert_called_with({"key": key})
  mock_pymongo.dead.drop.remove.assert_not_called()


@patch('pymongo.MongoClient')
def test_timed_key_is_saved(mock_pymongo):
  dead = drop_handler(mock_pymongo)
  timed_key = dead.get_timed_key()
  mock_pymongo.dead.formKeys.insert_one.assert_called_with({"key": timed_key,"created": ANY})
