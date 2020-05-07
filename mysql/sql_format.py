import re
import copy


def listener(log_path):
    pos = 0
    while True:
        con = open(log_path)
        if pos != 0:
            con.seek(pos, 0)
        while True:
            line = con.readline()
            if line.strip():
                sql_formay(line)
            pos = pos + len(line)
            if not line.strip():
                break
        con.close()


exclude = ['autocommit', 'commit', 'Quit', '@@session', 'character_set_results', 'WARNINGS', 'SET NAMES utf8']

sql = ''


def sql_formay(content):
    global sql
    flag = False
    # 包含系统sql过滤
    for e in exclude:
        if content.upper().__contains__(e.upper()):
            flag = True
            break
    if flag:
        return

    # 获取手写sql
    if content.__contains__('Query') and len(sql) > 0:
        # 过滤前缀数据
        prefix = re.findall('.*?Query', sql)
        this_sql = sql.replace(prefix[0], '').replace('\n', '')
        print(this_sql)
        sql = ''
        sql += content
    else:
        sql += content


if __name__ == '__main__':
    listener('./log/mysql.log')
