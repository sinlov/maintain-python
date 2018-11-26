# coding=utf-8

__author__ = 'sinlov'

import json


class Py2Json:
    """
    for python2 json utils

    use as

    from tools.py2_json import Py2Json

    Py2Json.dict_json_beauty(dict)
    """

    def __init__(self):
        pass

    @staticmethod
    def dict_json_printer(json_dict=dict, encode='utf-8'):
        # type: (dict, str)->None
        """
        print json with utf-8

        :param json_dict: for print dict
        :param encode: default is utf-8
        :return: None
        """
        print(json.dumps(json_dict, encoding=encode, ensure_ascii=False))

    @staticmethod
    def dict_json_print_beauty(json_dict=dict, encode='utf-8'):
        # type: (dict, str)->None
        """
        print json with utf-8 beauty

        :param json_dict: for print dict
        :param encode: default is utf-8
        :return: None
        """
        print(json.dumps(json_dict, encoding=encode, ensure_ascii=False, indent=4))

    @staticmethod
    def dict_json_encoding_utf_8(json_dict=dict):
        # type: (dict)->str
        """
        let python2 Json format utf-8

        :param json_dict: for format dict
        :return: json str
        """
        return json.dumps(json_dict, encoding='utf-8', ensure_ascii=False)

    @staticmethod
    def dict_json_beauty(json_dict=dict, encode='utf-8'):
        # type: (dict, str)->str
        """
        let python2 Json format more right

        :param json_dict: for format dict
        :param encode: default is utf-8
        :return: json str
        """
        return json.dumps(json_dict, encoding=encode, ensure_ascii=False, indent=4)

    @staticmethod
    def json_beauty(obj_json, encode='utf-8'):
        # type: (object, str)->str
        """
        let python2 Json format more right

        :param obj_json: for format obj
        :param encode: default is utf-8
        :return: json str
        """
        return json.dumps(obj_json, encoding=encode, ensure_ascii=False, indent=4)
