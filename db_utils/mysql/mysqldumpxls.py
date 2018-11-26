# coding=utf-8

import sys
import os
import platform
import inspect
import time
import getpass
import logging
import logging.handlers

import json
import optparse

import pymysql
import xlwt

__author__ = 'sinlov'

reload(sys)
sys.setdefaultencoding('utf-8')

mysql_conf = {
    'host': '主机host',
    'port': 3306,
    'user': '用户名',
    'password': '密码',
    'database': '库名',
    'charset': 'utf8'
}

is_verbose = False
root_run_path = os.getcwd()

logger_tag = 'mysql_dump_xls_{0}_'.format(mysql_conf['database'])
logger_time_format = '%Y_%m_%d_%H_%M_%S'

"""
auto clean time default is one mouth
"""
out_of_time_log_auto_clean = 60 * 60 * 24 * 7 * 31

cli_help_info = """
This tools used to mysql to xls
At first time must run
pip install pymysql==0.9.2
pip install xlwt==1.3.0
"""


class PLog:
    logger = None

    def __init__(self):
        pass

    _runtime_version_error = """
    This script must run python 2.7.+
    """

    ERROR = '\033[91m'
    OK_GREEN = '\033[96m'
    WARNING = '\033[93m'
    OK_BLUE = '\033[94m'
    HEADER = '\033[95m'
    WRITE = '\033[98m'
    BLACK = '\033[97m'
    END_LI = '\033[0m'

    @staticmethod
    def current_file_directory():
        path = os.path.realpath(sys.path[0])  # interpreter starter's path
        if os.path.isfile(path):  # starter is excutable file
            path = os.path.dirname(path)
            return os.path.abspath(path)  # return excutable file's directory
        else:  # starter is python script
            caller_file = inspect.stack()[1][1]  # function caller's filename
            return os.path.abspath(os.path.dirname(caller_file))  # return function caller's file's directory

    @staticmethod
    def check_current_log_path_and_auto_clean():
        """
        auto clean log by :out_of_time_log_auto_clean
        :return:
        """
        log_path = os.path.join(PLog.current_file_directory(), 'log')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        else:
            check_time = time.time()
            for walk_dir, walk_folder, walk_file in os.walk(log_path):
                for f in walk_file:
                    if f.endswith('.log'):
                        check_path_join = os.path.join(walk_dir, f)
                        m_time = os.path.getmtime(check_path_join)
                        if check_time - m_time > out_of_time_log_auto_clean:
                            os.remove(check_path_join)
                            print 'auto_clean log file : %s' % check_path_join
        return log_path

    @staticmethod
    def init_logger(first_tag, sec_tag=str):
        log_file = first_tag + sec_tag + '.log'
        log_path = PLog.check_current_log_path_and_auto_clean()
        log_path_join = os.path.join(log_path, log_file)
        handler = logging.handlers.RotatingFileHandler(log_path_join, maxBytes=1024 * 1024, backupCount=5)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        PLog.logger = logging.getLogger(str(getpass.getuser()))
        PLog.logger.addHandler(handler)
        PLog.logger.setLevel(logging.DEBUG)
        return PLog.logger

    @staticmethod
    def find_now_time_format(format_time):
        # type: (str) -> format_time
        """
        :return: time string
        """
        return time.strftime(format_time, time.localtime(time.time()))

    @staticmethod
    def init_logger_by_time(tag=str):
        # type: (str) -> tag
        return PLog.init_logger(tag, PLog.find_now_time_format(logger_time_format))

    @staticmethod
    def log_printer(msg, lev=str, must=False):
        # type: (str, str, bool) -> None
        if PLog.logger is None:
            print('not use PLog.init_logger(), please check!')
            return
        if is_verbose or must:
            print msg,
        if lev == 'i':
            PLog.logger.info(msg)
        elif lev == 'd':
            PLog.logger.debug(msg)
        elif lev == 'w':
            PLog.logger.warning(msg)
        elif lev == 'e':
            PLog.logger.error(msg)
        else:
            PLog.logger.info(msg)

    @staticmethod
    def log_normal(info, must=False):
        print(PLog.WRITE + info + PLog.END_LI)
        PLog.log_printer(info, '', must)

    @staticmethod
    def log_assert(info, must=False):
        print(PLog.BLACK + info + PLog.END_LI)
        PLog.log_printer(info, 'w', must)

    @staticmethod
    def log_info(info, must=False):
        print(PLog.OK_GREEN + info + PLog.END_LI)
        PLog.log_printer(info, 'i', must)

    @staticmethod
    def log_debug(info, must=False):
        print(PLog.OK_BLUE + info + PLog.END_LI)
        PLog.log_printer(info, 'd', must)

    @staticmethod
    def log_warning(info, must=False):
        print(PLog.WARNING + info + PLog.END_LI)
        PLog.log_printer(info, 'w', must)

    @staticmethod
    def log_error(info, must=False):
        print(PLog.ERROR + info + PLog.END_LI)
        PLog.log_printer(info, 'e', must)

    @staticmethod
    def log(msg, lev=str, must=False):
        # type: (str, str, bool) -> None
        if is_verbose or must:
            if not platform.system() == "Windows":
                if lev == 'i':
                    PLog.log_info('%s' % msg)
                elif lev == 'd':
                    PLog.log_debug('%s' % msg)
                elif lev == 'w':
                    PLog.log_warning('%s' % msg)
                elif lev == 'e':
                    PLog.log_error('%s' % msg)
                elif lev == 'a':
                    PLog.log_assert('%s' % msg)
                else:
                    PLog.log_normal('%s' % msg)
            else:
                print('%s\n' % msg)
                if lev == 'i':
                    PLog.log_printer(msg, 'i', must)
                elif lev == 'd':
                    PLog.log_printer(msg, 'd', must)
                elif lev == 'w':
                    PLog.log_printer(msg, 'w', must)
                elif lev == 'e':
                    PLog.log_printer(msg, 'e', must)
                elif lev == 'a':
                    PLog.log_printer(msg, 'w', must)
                else:
                    PLog.log_printer(msg, '', must)

    @staticmethod
    def check_runtime():
        PLog.log('Python version %s' % platform.python_version(), 'd')
        version_split = platform.python_version().split('.')
        if version_split[0] != '2':
            PLog.log(PLog._runtime_version_error, 'e', True)
            exit(1)
        if version_split[1] < '7':
            PLog.log(PLog._runtime_version_error, 'e', True)
            exit(1)


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


class MySQLUtil:
    _is_conn = False

    def __init__(self, conf):
        try:
            self.conn = pymysql.connect(**conf)
            self.cursor = self.conn.cursor()
            self._is_conn = True
        except Exception as e:
            PLog.log('mysql conn error as {0}, error info {1}'.format(Py2Json.json_beauty(conf), e), 'e', True)
            pass

    def is_connect(self):
        """
        是否连接上
        :return:
        """
        return self._is_conn

    def get_cur(self):
        """
        获取游标
        :return:
        """
        return self.cursor

    def commit(self):
        """
        事务提交
        :return:
        """
        self.conn.commit()

    def close(self):
        """
        关闭连接
        :return:
        """
        self.conn.close()
        self._is_conn = False

    def cur_close(self):
        """
        关闭游标
        :return:
        """
        self.cursor.close()

    def rollback(self):
        """
        回滚事务
        :return:
        """
        self.conn.rollback()

    def query_operation_excel(self, sql, flag):
        """
        数据导入excel的查询操作

        flag等于1：查询结果集
        flag等于2：查询表结构描述
        :param sql: 查询语句
        :param flag: 查询结果集
        :return:
        """
        if not self._is_conn:
            PLog.log('not connect mysql at query_operation_excel()', 'e', True)
            return
        # 获取数据库游标
        cur = self.get_cur()
        # 执行查询
        try:
            cur.execute(sql)
            # 移动游标位置
            cur.scroll(0, mode="absolute")
            # 查询结果条数
            # row = cur.rowcount
            # 查询结果集
            # flag等于1：查询结果集
            # flag等于2：查询表结构描述
            if flag == 1:
                data_list = cur.fetchall()
            elif flag == 0:
                data_list = cur.description
        except Exception as e:
            PLog.log('查询结果集异常{0}'.format(e), 'e', True)
        # 关闭游标
        # cur.close()
        # 关闭数据连接
        # self.close()
        # 返回查询结果集
        PLog.log('{}'.format(data_list), 'd')
        return data_list

    def get_mysql_data(self, table_name, flag):
        """
        根据 sql 获取数据
        :param table_name:
        :param flag:
        :return:
        """
        if not self._is_conn:
            PLog.log('not connect mysql at get_mysql_data()', 'e', True)
            return
        sql = "SELECT * FROM {0}".format(table_name)
        try:
            PLog.log('{}'.format(sql), 'd')
            data = self.query_operation_excel(sql, flag)
        except Exception as e:
            PLog.log('get_mysql_data error at {}'.format(e), 'e', True)
        else:
            PLog.log('获取excel数据成功：{}'.format(data))
            return data


class ExcelUtils:
    def __init__(self):
        pass

    def mysql_to_excel(self, sheet_name, table_name, out_path, flag1=1, flag2=0):
        # type: (str, str, str, object, object) -> None
        """
            mysql数据导入excel
            sheet_name:excel excel名称
            dbname:数据库名
            table_name:表名
            out_path:文件存放路径
            flag1:数据表结果集查询标志
            flag2:数据表描述查询标志
        """
        mysql_db = MySQLUtil(mysql_conf)
        if not mysql_db.is_connect():
            PLog.log('not connect mysql!', 'e', True)
            return
        # 结果集
        data_list = mysql_db.get_mysql_data(table_name, flag1)
        PLog.log('结果集：{}'.format(data_list), 'd')
        # 表描述
        table_desc = mysql_db.get_mysql_data(table_name, flag2)
        PLog.log('表描述：{}'.format(table_desc), 'd')
        # 创建excel
        workbook = xlwt.Workbook()
        # 创建excel中的sheet
        sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)

        # 插入表描述到excel
        for desc in range(0, len(table_desc)):
            sheet.write(0, desc, table_desc[desc][0])
        row = 1
        col = 0
        # 插入数据到excel
        for row in range(1, len(data_list) + 1):
            for col in range(0, len(table_desc)):
                sheet.write(row, col, u'%s' % data_list[row - 1][col])
        try:
            # 保存excel
            workbook.save(out_path)
        except Exception as e:
            PLog.log('导出数据到excel失败 db -> {0}'
                     'sheet_name -> {1}'
                     'table_name -> {2}'
                     'out_path -> {3}'
                     'Error -> {4}'.
                     format(mysql_conf['database'],
                            sheet_name,
                            table_name,
                            out_path,
                            e,
                            ), 'e', True)
        else:
            PLog.log('导出成功 db -> {0}'
                     'sheet_name -> {1}'
                     'table_name -> {2}'
                     'out_path -> {3}'.
                     format(mysql_conf['database'],
                            sheet_name,
                            table_name,
                            out_path,
                            ), 'i', True)
            # 数据库连接关闭二连
            mysql_db.cur_close()
            mysql_db.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You must input params or see -h"
        exit(1)
    check_p = str(sys.argv[1])
    if not check_p.startswith('-'):
        print 'You params is error please see -h'
        exit(1)
    parser = optparse.OptionParser('%prog {}'.format(cli_help_info))
    parser.add_option('-v', '--verbose', dest='v_verbose', action="store_true",
                      help="see verbose", default=False)
    parser.add_option('-o', '--out_path', dest='out_path', type="string",
                      help="out path of xlsx"
                      , metavar="user")
    parser.add_option('--sheet_name', dest='sheet_name', type="string",
                      help="sheet name of xlsx"
                      , metavar="user")
    parser.add_option('--table_name', dest='table_name', type="string",
                      help="table name"
                      , metavar="user_id")
    (options, args) = parser.parse_args()
    PLog.init_logger_by_time(logger_tag)
    if options.v_verbose:
        is_verbose = True
    PLog.check_runtime()

    if options.out_path is None:
        PLog.log('error out_path is not set', 'e', True)
        exit(1)
    if options.sheet_name is None:
        PLog.log('error sheet_name is not set', 'e', True)
        exit(1)
    if options.table_name is None:
        PLog.log('error table_name is not set', 'e', True)
        exit(1)
    PLog.log('{0} -> {1}\n'
             '{2} -> {3}\n'
             '{4} -> {5}\n'
             .format('sheet_name', options.sheet_name,
                     'table_name', options.table_name,
                     'out_path', options.out_path,
                     ), 'i', True)
    mysql_excel = ExcelUtils()
    mysql_excel.mysql_to_excel(options.sheet_name, options.table_name, options.out_path)
