# coidng=utf-8

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    # json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
    # parsed_json = json.loads(json_string)
    # print(parsed_json['first_name'])

    jsonFile = '../../../data/test.json'
    with open(jsonFile, 'r') as jf:
        data = json.load(jf)
        for line in data:
            for e in line:
                print(e, line[e])
            print('-----------------------')
