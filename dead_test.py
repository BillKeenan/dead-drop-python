from unittest.mock import patch, ANY
from deadWeb.dead import  drop_handler
import pprint
import datetime
from freezegun import freeze_time



@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_drop_is_saved(mock_pymongo):
  dead = drop_handler(mock_pymongo)
  data = {"test":"here"}
  dead.drop(data)
  mock_pymongo.dead.drop.insert_one.assert_called_with({"key": ANY, "data":data,"createdDate":datetime.datetime(2012, 1, 14)})


@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_drop_deleted_when_accessed(mock_pymongo):

  sampleDrop = get_sample_drop()
  mock_pymongo.dead.drop.find.return_value=[sampleDrop]
  dead = drop_handler(mock_pymongo)
  val = dead.pickup(sampleDrop['key'])
  mock_pymongo.dead.drop.find.assert_called_with({"key": sampleDrop['key']})
  mock_pymongo.dead.drop.remove.assert_called_with({"key":  sampleDrop['key']})
  assert sampleDrop["data"] == val


@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_drop_retruned_when_no_create_date(mock_pymongo):
  # to handle old drops
  print('test old')
  sampleDrop = get_sample_drop()
  sampleDrop.pop('createdDate')
  print('old')
  pprint.pprint(sampleDrop)
  mock_pymongo.dead.drop.find.return_value=[sampleDrop]
  dead = drop_handler(mock_pymongo)
  val = dead.pickup(sampleDrop['key'])
  pprint.pprint(sampleDrop)
  
  mock_pymongo.dead.drop.find.assert_called_with({"key": sampleDrop['key']})
  mock_pymongo.dead.drop.remove.assert_called_with({"key":  sampleDrop['key']})
  assert sampleDrop["data"] == val



def get_sample_drop():
  return {'key':'12345','data':"test data return","createdDate":datetime.datetime(2012, 1, 14)}


@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_drop_deleted_and_not_returned_when_24hours_old(mock_pymongo):

  key = "anything"
  sampleDrop = get_sample_drop()
  sampleDrop["createdDate"] = datetime.datetime(2012, 1, 12)
  mock_pymongo.dead.drop.find.return_value=[sampleDrop]
  dead = drop_handler(mock_pymongo)
  val = dead.pickup(key)
  
  assert val == []
  mock_pymongo.dead.drop.find.assert_called_with({"key": key})
  mock_pymongo.dead.drop.remove.assert_called_with({"key": key})


@patch('pymongo.MongoClient')
def test_return_none_when_not_existing(mock_pymongo):

  sampleDrop = get_sample_drop()
  mock_pymongo.dead.drop.find.return_value=[]
  dead = drop_handler(mock_pymongo)
  val = dead.pickup(sampleDrop['key'])
  
  assert val == []
  mock_pymongo.dead.drop.find.assert_called_with({"key": sampleDrop['key']})
  mock_pymongo.dead.drop.remove.assert_not_called()


@patch('pymongo.MongoClient')
def test_timed_key_is_saved(mock_pymongo):
  dead = drop_handler(mock_pymongo)
  timed_key = dead.get_timed_key()
  mock_pymongo.dead.formKeys.insert_one.assert_called_with({"key": timed_key,"created": ANY})
