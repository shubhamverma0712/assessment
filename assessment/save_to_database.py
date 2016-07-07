from assessment.basic import table_db, csv_header,csv_file

import pymongo
from pprint import pprint
import csv
from pymongo.errors import BulkWriteError
import re
from operator import itemgetter

def convert_to_dict(the_list, this_csv_header=None):
    if this_csv_header ==None:
        global csv_header
        this_csv_header = csv_header
    assert(len(the_list)== len(csv_header))
    data_dict = dict()
    for index in  xrange(len(the_list)):
        data_dict[this_csv_header[index]] = the_list[index]
    return data_dict


def write_to_db (table_db, csv_file,csv_header=None ):
    bulk = table_db.initialize_unordered_bulk_op()
    
    with open(csv_file) as fil:
        fil_csv_reader = csv.reader(fil,delimiter='\t')
        for each_line in fil_csv_reader:
            try:
                this_dict = convert_to_dict(each_line,csv_header)
            except AssertionError:
                print "CSV inconsistent"
                return False
            bulk.insert(this_dict)
    try:
        bulk.execute()
    except BulkWriteError as bwe:
        pprint(bwe.details)
        return False
    return True
if __name__ == "__main__":
    if (not write_to_db(db,csv_file)):
        print "Some Error Occured"