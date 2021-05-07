import pymongo
from bson.objectid import ObjectId
import logging
from .runcode import RunCppCode


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
            "src": code['src'],
            "input": code["input"],
            "output": code["output"]
        }

def save_code(id: str, label: str) -> dict:
    check_id = True
    code_doc = None
    try:
        code_doc = mycol.find_one({"_id": ObjectId(id)})
    except:
        logging.exception('Not found doc by id ' + id)
        check_id = False
    if (code_doc == None and check_id == False):
        return {
            'errCode': 400,
            'errMess': 'Not found doc by id ' + id
        }
    else:
        count = int(code_doc['count']) + 1
        run = RunCppCode(str(label), code_doc)
        rescompil, resrun, save_label = run.run_cpp_code()

        if rescompil == "":
            print("ok")
            #mycol.update_one({'_id': ObjectId(id)}, {"$set": {'label' + str(count): label, 'count': count}}, upsert=True)

        return {'errCode': 200,
                'errMess': 'upload success',
                'save_label': save_label
            }       