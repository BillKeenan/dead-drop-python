from unittest.mock import patch, ANY
from deadWeb.dead import test, drop_handler
import pprint

@patch('pymongo.MongoClient')
def insert(mock_pymongo):
  
  dead = drop_handler(mock_pymongo)
  data = {"test":"here"}
  dead.drop(data)
  mock_pymongo.dead.drop.insert_one.assert_called_with({"key": ANY, "data":data})
