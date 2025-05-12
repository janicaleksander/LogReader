import  datetime
from enum import Enum

attribute_info = {
    0: ("ts", datetime.datetime.fromtimestamp),
    1: ("uid", str),
    2: ("id.orig_h", str),
    3: ("id.orig_p", int),
    4: ("id.resp_h", str),
    5: ("id.resp_p", int),
    6: ("trans_depth", int),
    7: ("method", str),
    8: ("host", str),
    9: ("uri", str),
    10: ("referrer", str),
    11: ("user_agent", str),
    12: ("request_body_len", int),
    13: ("response_body_len", int),
    14: ("status_code", int),
    15: ("status_msg", str),
    16: ("info_code", str),
    17: ("info_msg", str),
    18: ("filename", str),
    19: ("tags", str),
    20: ("username", str),
    21: ("password", str),
    22: ("proxied", str),
    23: ("orig_fuids", str),
    24: ("orig_mime_types", str),
    25: ("resp_fuids", str),
    26: ("resp_mime_types", str)
}
class Info(Enum):
    FILE_LOADED = 1

class Error(Enum):
    PATH_DOES_NOT_EXISTS = 1
    INVALID_PATH = 2
    FILE_DOES_NOT_EXISTS = 3
    BAD_CONDITION = 4
    BAD_PARAM_TO_FIND =5
    NO_DATA = 6
    NO_DATA_AFTER_SORT=7

class Conditions(Enum):
    INTERVAL = 1
    SEARCH = 2

