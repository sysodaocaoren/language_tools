from DBUtils.PersistentDB import PersistentDB
import pymysql

POOL = PersistentDB(
    creator=pymysql,  # 使用链接数据库的模块  
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制  
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]  
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always  
    closeable=False,
    # 如果为False时， conn.close() 实际上被忽略，供下次使用，再线程关闭时，才会自动关闭链接。如果为True时， conn.close()则关闭链接，那么再次调用pool.connection时就会报错，因为已经真的关闭了连接（pool.steady_connection()可以获取一个新的链接）  
    threadlocal=None,  # 本线程独享值得对象，用于保存链接对象，如果链接对象被重置  
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456Aa?',
    database='news',
    charset='utf8',
)

def getall(table_name):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    cursor.execute('select * from ' + table_name)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Data = [str(i), hit["content"], hit["starttime"], hit["endtime"], hit["path"]]

def insert_news(data):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    sql = "INSERT INTO t_news_info (`title`, `summry`, `user_id`, `create_time`, `news_id`, `source_type`,user_name, comment_count, vote_count)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    # 提交事务
    conn.commit()
    id = cursor.lastrowid
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return id

def insert_comment(data):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    sql = "INSERT INTO t_comment_info ( `content`, `news_id`, `user_id`, `user_name`, `location_prov`, `create_time`, `location_city`, `view_point_tags`, `emo_tags`, `content_tags`, `zan_num`, `child_comment_num`) "
    sql = sql + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    # 提交事务
    conn.commit()
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

def insert_search(data):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    sql = "INSERT INTO t_serch_info (`keyword`, `news_id`, `create_time`) VALUES (%s,%s,%s)"
    cursor.execute(sql, data)
    # 提交事务
    conn.commit()
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

def get_by_keyword(table_name, id):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    cursor.execute('select * from ' + table_name + "where id = " + id)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def del_by_id(table_name, id):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    sql = "delete from " + table_name + " where id = " + id
    cursor.execute(sql)
    # 提交事务
    conn.commit()
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

def get_by_id(table_name, id):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    cursor.execute('select * from ' + table_name + "where id = " + id)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_comment_by_newsid(newsid):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    cursor.execute("select * from t_comment_info where news_id = " + newsid)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def getTopVoteNews(type, limit, keyword):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    cursor.execute("select summry, user_name, vote_count, comment_count, create_time from t_news_info where source_type = '"+ type +"' and id in (select news_id from t_serch_info where keyword like '"+keyword+"%') and summry not like '%图片%' and summry not like '%…%' order by (vote_count + comment_count) desc limit 40, " + str(limit))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def getTopVoteComment(type, limit, keyword):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    cursor.execute("select DISTINCT cm.content from t_comment_info cm , t_news_info ns , t_serch_info ts where ts.news_id=ns.id and cm.news_id=ns.news_id and ns.source_type='"+type+"' and ts.keyword='"+keyword+"' and cm.content not like '%[图片]%' and  cm.content not like '%…%' order by zan_num desc limit " + str(limit))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
