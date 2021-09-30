import pymongo
from bson.objectid import ObjectId
import logging
from .runcode import RunCppCode
from sctokenizer import CppTokenizer

# Config mongodb
# myclient = pymongo.MongoClient("mongodb://scoss_tagger_mongo:27017/",
#                                username='root',
#                                password='example')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["scoss"]
mycol = mydb["code"]


def save_code_mongodb(codes: list):
    for code in codes:
        mycol.insert(code)
    return {
            "errCode": 200,
            "errMess": 'Save Successful'
        }


def get_code() -> dict:
    code = None
    count = 0
    list_code = list(mycol.aggregate([{"$match": {"count": count}}, {"$sample": { "size": 1 }}]))
    if len(list_code) > 0:
        code = list_code[0]
    while (code == None and count < 20):
        count = count + 1
        list_code = list(mycol.aggregate([{"$match": {"count": count}}, {"$sample": { "size": 1 }}]))
        if len(list_code) > 0:
            code = list_code[0]

    if code == None:
        return {
            "errCode": 500,
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

def run_code(id: str, label: str, submit= False) -> dict:
    check_id = True
    code_doc = None
    try:
        code_doc = mycol.find_one({"_id": ObjectId(id)})
    except:
        logging.exception('Not found doc by id ' + id)
        check_id = False
    if (code_doc == None and check_id == False):
        return {
            'errCode': 500,
            'errMess': 'Not found doc by id ' + id
        }
    else:
        count = int(code_doc['count']) + 1
        run = RunCppCode(str(label), code_doc)
        rescompil, resrun, save_label, result_run = run.run_cpp_code()

        if save_label and submit:

            # check same code
            tokenizer = CppTokenizer()
            token_label = tokenizer.tokenize(label)
            token_code = tokenizer.tokenize(code_doc["src"])

            if len(token_code) == len(token_label):
                same_code = True
                for i in range(len(token_label)):
                    if (token_label[i].token_type != token_code[i].token_type) \
                        or (token_label[i].token_value != token_code[i].token_value):
                        
                        same_code = False
                        break
                if same_code:
                    return {
                        'errCode': 400,
                        'errMess': 'Khong duoc submit source code trung nhau'
                    }

            mycol.update_one({'_id': ObjectId(id)}, {"$set": {'label' + str(count): label, 'count': count}}, upsert=True)

    return {'errCode': 200,
            'save_label': save_label,
            'rescompil' :rescompil,
            'output': result_run
        }     

def compile_code(id: str, label: str) -> dict:
    check_id = True
    code_doc = None
    try:
        code_doc = mycol.find_one({"_id": ObjectId(id)})
    except:
        logging.exception('Not found doc by id ' + id)
        check_id = False
    if (code_doc == None and check_id == False):
        return {
            'errCode': 500,
            'errMess': 'Not found doc by id ' + id
        }
    else:
        count = int(code_doc['count']) + 1
        run = RunCppCode(str(label), code_doc)
        res, rescompil = run.compile_cpp_code()

    if res == 0:
        return {'errCode': 200,
                'rescompil' : "Bien dich thanh cong!"
            }

    return {'errCode': 500,
            'rescompil' :rescompil
        }      
