import os.path
from typing import Generic, TypeVar,Optional
from result import Result
from enums import *

class LogReader:
    def __init__(self,):
        self.list_log_dict = []

    @staticmethod
    def convert_to_type(i, param):
        if param is None:
            return param
        if i == 0:
            try:
                return attribute_info[i][1](int(float(param)))
            except Exception as e:
                return None
        try:
            return attribute_info[i][1](param)
        except Exception as e:
            return None

    @staticmethod
    def valid_path(path):
        if not os.path.isfile(path):
            return Result(error=Error.FILE_DOES_NOT_EXISTS)
        return Result()

    def load_file(self,path:str):
        self.list_log_dict.clear()
        res = self.valid_path(path)
        if not res.success():
            return Result(error=res.get_error())
        with open(path) as f:
            for line in f:
                d = dict()
                parts = line.split("	")
                for i, part in enumerate(parts):
                    d[attribute_info[i][0]] = self.convert_to_type(i, part)
                self.list_log_dict.append(d)
        return Result(value=Info.FILE_LOADED)

    def valid_dict(self,dct,value,condition):
        match condition[0]:
            case Conditions.INTERVAL: #value in ()
                ts = dct["ts"]
                if (value[0].date() <= value[1].date()) and value[0].date() <= ts.date() <= value[1].date():
                    return Result(value=True)
            case Conditions.SEARCH:
                if condition[1] in dct:
                    if dct[condition[1]] == value:
                        return Result(value=True)
                return Result(error=Error.BAD_PARAM_TO_FIND)
        return Result(error=Error.BAD_CONDITION)


    # condition = (Conditions.Interval,) value = (,)
    # condition = (Conditions.Search,param) value =
    def sort_by(self,condition,value,lst):
        r = []
        for dct in lst:
            if self.valid_dict(dct,value,condition).success():
                r.append(dct)
        return Result(value=r) if len(r) >0 else Result(error=Error.NO_DATA_AFTER_SORT)

    def display_logs(self):
        return Result(value=self.list_log_dict) if len(self.list_log_dict) >0 else Result(error=Error.NO_DATA)

reader = LogReader()
