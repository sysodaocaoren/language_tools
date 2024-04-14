import mysql.connector
import random
# 创建数据库连接
import numpy as np

# 创建一个一维数组
all_tables = np.array(['t_video_sanguo', 't_video_xiyou', 't_video_honglou', 't_video_shuihu'])


def init():
    cnx = mysql.connector.connect(user='root', password='123456Aa?',
                              host='localhost', database='video')
    return cnx

def queryall(content):
    result = []
    np.random.shuffle(all_tables)
    for table_name in all_tables:
        result = query(content, table_name)
        if (len(result) > 0):
            return result
    return result

def query(content, table_name):
    cnx = init()

    # 创建游标对象
    cursor = cnx.cursor()

    # 执行SQL查询
    query = "SELECT * FROM  " + str(table_name)
    if (len(content) > 0):
        query = query + " where content like '%" + content + "%'"
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()

    # 打印结果
    # for row in result:
    #     print(row)

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()

    return result;


def queryAroud(id, table_name):
    cnx = init()

    # 创建游标对象
    cursor = cnx.cursor()

    # 执行SQL查询
    start_id = 0
    end_id = int(id) + 50
    if(int(id) < 6 ):
        start_id = 0
    else:
        start_id = int(id) - 6

    query = "SELECT * FROM " + str(table_name) + " where id > " + str(start_id) + " and id < " + str(end_id)
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()

    # 打印结果
    # for row in result:
    #     print(row)

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()

    return result;

def insert (data, table_name):
    cnx = init()
   # 创建游标对象
    cursor = cnx.cursor()

    # 批量插入数据
    query = "INSERT INTO " + table_name + " (content, start_time, end_time, path) VALUES (%s, %s, %s, %s)"
    cursor.executemany(query, data)

    # 提交事务
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


def update_pinyin (id, pinyin, table_name):
    cnx = init()
   # 创建游标对象
    cursor = cnx.cursor()

    # 批量插入数据
    query = "update " + table_name + " set pinyin = '" + pinyin + "' where id = '" + id + "'"
    print(query)
    cursor.execute(query)

    # 提交事务
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


def queryBypinyin(pinyin,pinyin_end, table_name, type):
    cnx = init()

    # 创建游标对象
    cursor = cnx.cursor()

    # 执行SQL查询
    query = "SELECT * FROM  " + str(table_name)
    if (len(pinyin) > 0):
        if (type == 0):
            query = query + " where (pinyin like '%-" + pinyin_end + "1' or pinyin like '%-" + pinyin_end + "2'  or pinyin like '%-" + pinyin_end + "3' or pinyin like '%-" \
                    + pinyin_end + "4' or pinyin like '%-" + pinyin_end + "5') and pinyin not like '%-" \
                    + pinyin_end + "1-%' and pinyin not like '%-" + pinyin_end + "2-%' and pinyin not like '%-" \
                    + pinyin_end + "3-%' and pinyin not like '%-" + pinyin_end + "4-%' and pinyin not like '%-" + pinyin_end + "5-%'"
        if (type == 1):
            query = query + " where pinyin like '%-" + pinyin + "%'"
    print(query)
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()

    # 打印结果
    # for row in result:
    #     print(row)

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()

    return result;