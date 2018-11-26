# coding=utf-8

import sys
import os
import optparse

from mysqldumpxls import PLog
from mysqldumpxls import Py2Json
from mysqldumpxls import ExcelUtils
from mysqldumpxls import mysql_conf_default

reload(sys)
sys.setdefaultencoding('utf-8')

mysql_conf = mysql_conf_default
mysql_conf['database'] = 'user'

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

__author__ = 'sinlov'

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
    parser.add_option('--conn_dict', dest='conn_dict', type="string",
                      help="conn_dict"
                      , metavar="user_id")
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
             '{6} -> {7}\n'
             .format('mysql_conf', Py2Json.json_beauty(mysql_conf),
                     'sheet_name', options.sheet_name,
                     'table_name', options.table_name,
                     'out_path', options.out_path,
                     ), 'i', True)

    mysql_excel = ExcelUtils()
    mysql_excel.mysql_to_excel(mysql_conn=mysql_conf,
                               sheet_name=options.sheet_name,
                               table_name=options.table_name,
                               out_path=options.out_path)
