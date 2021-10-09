import pymongo
from bson.objectid import ObjectId
import logging

from sctokenizer.token import TokenType
from .runcode import RunCppCode
from sctokenizer import CppTokenizer
import datetime
import uuid
import os
from subprocess import call


# Config mongodb
# myclient = pymongo.MongoClient("mongodb://scoss_tagger_mongo:27017/",
#                                 username='root',
#                                 password='example')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["scoss"]
mycol = mydb["code"]
col_student = mydb["student"]

def save_code_mongodb(codes: list):
    for code in codes:
        mycol.insert(code)
    return {
            "errCode": 200,
            "errMess": 'Save Successful'
        }


def save_student_info(student_id, student_name, class_id):
    st = col_student.find_one({"student_id": student_id, "class_id": class_id})
    if st == None:
        id = str(uuid.uuid4())
        col_student.insert({'_id': id, 'student_id': student_id, 'student_name':student_name, 'class_id': class_id})
        return {'id': id}
    
    return {'id': st["_id"]}


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
            "src": (code['src']),
            "input": code["input"],
            "output": code["output"]
        }

def run_code(id: str, label: str, student_id: str, hints, submit= False) -> dict:
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
        rescompil, save_label, result_run = run.run_cpp_code()

        if save_label and submit:
            # check same code
            tokenizer = CppTokenizer()

            tokenLabel = tokenizer.tokenize(label)
            tokenCode = tokenizer.tokenize(code_doc['src'])

            token_label = []
            for i in tokenLabel:
                if i.token_type != TokenType.COMMENT_SYMBOL:
                    token_label.append(i)
            token_code = []
            for i in tokenCode:
                if i.token_type != TokenType.COMMENT_SYMBOL:
                    token_code.append(i)

            if len(token_code) == len(token_label):
                same_code = True
                for i in range(len(token_label)):
                    if (token_label[i].token_type != token_code[i].token_type) or (str(token_label[i].token_value) != str(token_code[i].token_value)):
                        same_code = False
                        break
                if same_code:
                    return {
                        'errCode': 400,
                        'errMess': 'Không được submit source code mẫu!'
                    }
            # save label
            doc_save = {
                'label': label,
                'hints': hints
            }
            mycol.update_one({'_id': ObjectId(id)}, {"$set": {'label' + str(count): doc_save, 'count': count}}, upsert=True)

            # update data student
            student_doc = col_student.find_one({"_id": student_id})
            if  student_doc == None:
                return {
                    'errCode': 500,
                    'errMess': 'Vui lòng nhập thông tin sinh viên'
                }
            number = 1
            if "number" in student_doc:
                number = student_doc["number"] + 1
            col_student.update_one({'_id': student_id}, {"$set": {'date' + str(number): datetime.datetime.now(), 'number': number}}, upsert=True)
                    


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
                'rescompil' : "Biên dịch thành công!"
            }

    return {'errCode': 500,
            'rescompil' :rescompil
        }      
