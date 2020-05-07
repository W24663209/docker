import pymysql
import csv
import codecs


def get_conn():
    db = pymysql.connect("localhost", "root", "666666WW", "pangu", charset='utf8')

    return db


def execute_all(cursor, sql, args):
    cursor.execute(sql, args)
    return cursor.fetchall()


def red_mysql_to_csv(filename):
    with codecs.open(filename=filename, mode='w', encoding='utf-8')as f:
        db = get_conn()
        cursor = db.cursor()
        cursor_dict = db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = 'select * from tb_user'
        results = execute_all(cursor=cursor, sql=sql, args=None)
        write = csv.writer(f, dialect='excel')
        fields = []
        for field in cursor.description:
            fields.append(field[0])
        write.writerow(fields)
        for res in results:
            print(res)
            write.writerow(res)


if __name__ == '__main__':
    red_mysql_to_csv("tb_user.csv")
