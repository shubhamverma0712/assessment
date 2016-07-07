import pymongo
from pprint import pprint
import csv
from pymongo.errors import BulkWriteError
import re
from operator import itemgetter

client = pymongo.MongoClient("localhost", 27017)
db_access = client.shubham_assess
table_db = db_access.database_city_1

csv_file= "./US/US.txt"
csv_header = ["Country",
                "Pincode",
                "Place_Name",
                "State_Name",
                "State_Code",
                "County_Name",
                "County_Code",
                "Community_Name",
                "Community_Code",
                "Latitude",
                "Longitude",
                "Accuracy"
            ]






def find_elements_or(table_db, search_dict):
    
    global csv_header
    return_list = list()
    new_search_dict = dict()
    or_list = list()
    for each_key in search_dict:
        or_list.append({each_key:re.compile(re.escape(search_dict[each_key]), re.IGNORECASE)})

    new_search_dict["$or"]=or_list
    
    for each_find in table_db.find(new_search_dict):
        temp_list = [each_find[th_el] for th_el in csv_header]
        return_list.append(temp_list)

    return_list = sorted(return_list,key=itemgetter(csv_header.index("Place_Name")))
    return_list = sorted(return_list,key=itemgetter(csv_header.index("State_Name")))


    return return_list


def find_search_string(table_db,str_find):
    return find_elements_or(table_db,{"Pincode":str_find,"Place_Name":str_find})

if __name__=="__main__":
    k=  find_search_string(table_db, "wiscon")

    for each_k in k:
        print each_k