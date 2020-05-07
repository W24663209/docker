import csv
import json
import os
import sys
from typing import Any, Iterator

import pymysql
from pymysql.cursors import SSDictCursor
import codecs
import datetime


def get_conn():
    db = pymysql.connect("localhost", "root", "666666WW", "pangu", charset='utf8')

    return db


def dump():
    '''
    mysql导出csv
    '''
    db_name = 'pangu'
    # 打开数据库连接
    db = get_conn()

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 使用execute方法执行SQL语句
    cursor.execute("select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA='%s'" % db_name)

    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchall()

    for table in data:
        red_mysql_to_csv('../db/%s.csv' % table[0], table[0])

        # 导出csv
        with open('import.sql', 'r') as f:
            mongo_sql = f.readline() \
                .replace('TABLE_SCHEMA', db_name) \
                .replace('TABLE_NAME', table[0]) \
                .replace('CSV_PATH', '/db/%s.csv' % table[0])
            with open('../db/import.sh', 'a') as f:
                print(mongo_sql)
                f.write(mongo_sql+'\n')


def execute_all(cursor, sql, args):
    cursor.execute(sql, args)
    return cursor.fetchall()


def red_mysql_to_csv(filename, db_table):
    with codecs.open(filename=filename, mode='w', encoding='utf-8')as f:
        db = get_conn()
        cursor = db.cursor()
        sql = 'select * from %s' % db_table
        results = execute_all(cursor=cursor, sql=sql, args=None)
        write = csv.writer(f, dialect='excel')
        fields = []
        for field in cursor.description:
            fields.append(field[0])
        write.writerow(fields)
        for res in results:
            # print(res)
            write.writerow(res)


if __name__ == '__main__':
    dump()

# popen = os.popen('ls ./db').readlines()
# for js in popen:
#     with open('./db/%s'%js.replace('\n',''),'r') as f:
#         print(list(f.readlines()))
