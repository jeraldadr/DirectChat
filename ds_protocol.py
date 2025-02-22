"""ds_protocol.py"""
# Jerald Adriano
# jaadrian@uci.edu
# 91201228

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['token', 'message', 'type_'])


def extract_json(json_msg: str) -> DataTuple:
    '''takes the json msg and extract it into the Datatuple'''
    try:
        json_obj = json.loads(json_msg)
        try:
            token = json_obj['response']['token']
            message = json_obj['response']['message']
            type_ = json_obj['response']['type']
        except KeyError:
            try:
                message = json_obj['response']['message']
                type_ = json_obj['response']['type']
                return DataTuple('', message, type_)
            except KeyError:
                try:
                    type_ = json_obj['response']['type']
                    message_lst = json_obj['response']['messages']
                    return DataTuple('', message_lst, type_)
                except KeyError:
                    return False
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return False
    return DataTuple(token, message, type_)
