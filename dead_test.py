from unittest.mock import patch, ANY
from deadWeb.dead import  DropHandler
import pprint
import datetime
from freezegun import freeze_time



@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_track_is_saved(mock_pymongo):
  dead = DropHandler(mock_pymongo)
  dead.setRequestHash("127.0.0.1")
  data = {"test":"here"}
  dead.drop(data)
  mock_pymongo.dead.track.insert_one.assert_called_with({"key": ANY,"userHash":ANY, "createdDate":datetime.datetime(2012, 1, 14),"pickedUp":ANY})


@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_drop_is_saved(mock_pymongo):
  dead = DropHandler(mock_pymongo)
  data = {"test":"here"}
  dead.drop(data)
  mock_pymongo.dead.drop.insert_one.assert_called_with({"key": ANY, "data":data,"createdDate":datetime.datetime(2012, 1, 14)})

@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_drop_deleted_when_accessed(mock_pymongo):

    sampleDrop = get_sample_drop()
    mock_pymongo.dead.drop.find_one_and_delete.return_value=sampleDrop
    dead = DropHandler(mock_pymongo)
    import pprint
    pprint.pprint("XXXXX")
    pprint.pprint(sampleDrop)
    val = dead.pickup(sampleDrop['key'])
    
    pprint.pprint(val)
    mock_pymongo.dead.drop.find_one_and_delete.assert_called_with({"key": sampleDrop['key']})
    assert sampleDrop["data"] == val

@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_track_updated_when_accessed(mock_pymongo):

    sampleDrop = get_sample_drop()
    mock_pymongo.dead.drop.find_one_and_delete.return_value = sampleDrop
    dead = DropHandler(mock_pymongo)
    val = dead.pickup(sampleDrop['key'])
    mock_pymongo.dead.track.update.assert_called_with({"key": sampleDrop['key']}, {"$set":{"pickedUp":datetime.datetime(2012, 1, 14)},"$unset":{"key":""}})
    assert sampleDrop["data"] == val

def get_sample_stats():
  samplestats =[
      { "_id" : { "year" : 2018, "month" : 3, "day" : 2 }, "count" : 67, "distinctCount" : 49 },
      { "_id" : { "year" : 2018, "month" : 3, "day" : 3 }, "count" : 24, "distinctCount" : 15 }
    ]

  return samplestats


@patch('pymongo.MongoClient')
def test_stats_returned(mock_pymongo):
    #db.track.aggregate({ $group: { _id: { "year":{$year:"$createdDate"},"month":{$month:"$createdDate"},"day":{$dayOfMonth: "$createdDate"}},createdDate: { $sum: 1 } } })
    

    

    mock_pymongo.dead.track.find.return_value= get_sample_stats()
    dead = DropHandler(mock_pymongo)
    val = dead.stats()
    expected =[
            {"$group": 
            { "_id": { "year":{"$year":"$createdDate"},"month":{"$month":"$createdDate"},"day":{"$dayOfMonth": "$createdDate"},"userHash":"$userHash"},
                "count": { "$sum": 1 } ,
            } 
            },
            {"$group": 
                { "_id": { "year":"$_id.year","month":"$_id.month","day":"$_id.day"},
                "count": { "$sum": "$count" },
                "distinctCount": { "$sum": 1 }
                } 
            },
            {"$sort":  {"_id.year":1,"_id.month":1,"_id.day":1}},
            
        ];
    mock_pymongo.dead.track.aggregate.assert_called_with(expected)



@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_drop_not_retruned_when_no_create_date(mock_pymongo):
  # to handle old drops
  sampleDrop = get_sample_drop()
  sampleDrop.pop('createdDate')
  mock_pymongo.dead.drop.find_one_and_delete.return_value=sampleDrop
  dead = DropHandler(mock_pymongo)
  val = dead.pickup(sampleDrop['key'])
  pprint.pprint(sampleDrop)
  pprint.pprint(val)
  
  mock_pymongo.dead.drop.find_one_and_delete.assert_called_with({"key": sampleDrop['key']})
  assert val == []



def get_sample_drop():
  return {'key':'12345','data':"test data return","createdDate":datetime.datetime.now()}


@patch('pymongo.MongoClient')
@freeze_time("2012-01-14")
def test_drop_deleted_and_not_returned_when_24hours_old(mock_pymongo):

  key = "anything"
  sampleDrop = get_sample_drop()
  sampleDrop["createdDate"] = datetime.datetime(2012, 1, 12)
  mock_pymongo.dead.drop.find.return_value=[sampleDrop]
  dead = DropHandler(mock_pymongo)
  val = dead.pickup(key)
  
  assert val == []
  mock_pymongo.dead.drop.find_one_and_delete.assert_called_with({"key": key})



@patch('pymongo.MongoClient')
def test_return_none_when_not_existing(mock_pymongo):

  sampleDrop = get_sample_drop()
  mock_pymongo.dead.drop.find_one_and_delete.return_value=[]
  dead = DropHandler(mock_pymongo)
  val = dead.pickup(sampleDrop['key'])
  
  assert val == []
  mock_pymongo.dead.drop.find_one_and_delete.assert_called_with({"key": sampleDrop['key']})


@patch('pymongo.MongoClient')
def test_timed_key_is_saved(mock_pymongo):
  dead = DropHandler(mock_pymongo)
  timed_key = dead.get_timed_key()
  mock_pymongo.dead.formKeys.insert_one.assert_called_with({"key": timed_key,"created": ANY})
