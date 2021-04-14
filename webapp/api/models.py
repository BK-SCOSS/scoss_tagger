import pymongo
from bson.objectid import ObjectId
import logging

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["scoss"]
mycol = mydb["code"]

def get_code() -> dict:
    count = 0
    code = mycol.find_one({"count": count})
    while (code == None and count < 20):
        count = count + 1
        code = mycol.find_one({"count": count})

    if code == None:
        return {
            "errCode": 400,
            "errMess": 'Not found code'
        }
    else:
        return {
            "errCode": 200,
            "id": str(code['_id']),
            "src": code['src']
        }

def save_code(id: str, label: str) -> dict:
    check_id = True
    code = None
    try:
        code = mycol.find_one({"_id": ObjectId(id)})
    except:
        logging.exception('Not found doc by id ' + id)
        check_id = False
    if (code == None and check_id == False):
        return {
            'errCode': 400,
            'errMess': 'Not found doc by id ' + id
        }
    else:
        count = int(code['count']) + 1
        mycol.update_one({'_id': ObjectId(id)}, {"$set": {'label' + str(count): label, 'count': count}}, upsert=True)
        return {'errCode': 200,
                'errMess': 'upload success'
            }       