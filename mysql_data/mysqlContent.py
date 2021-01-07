#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from six import itervalues
import pymysql
import time
import logging


class SQL():
    logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                        filename='running.log',
                        filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        # 日志格式
                        )
    #数据库初始化
    def __init__(self):
        logger = logging.getLogger()
        handler = logging.FileHandler('running.log')
        logger.handlers.append(handler)
        #数据库连接相关信息
        hosts    = '127.0.0.1' #数据库服务器
        username = 'root'
        password = '123456'
        database = 'dbname'
        charsets = 'utf8'
        ports = 61509
        self.connection = False
        try:
            self.conn = pymysql.connect(host = hosts,user = username,passwd = password,db = database,port= ports,charset = charsets)
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names "+charsets)
            self.connection = True
        except Exception as e:
            logging.exception("Cannot Connect To Mysql!/n")
            logging.exception(e)
            print("Cannot Connect To Mysql!/n",e)

    def escape(self,string):
        return '%s' % string

    def selectall(self,tablename=None):
        # 查询需要更新dzi的图片
        sql_countAll = "SELECT id,file_url,deepzoom,dzi_time FROM %s WHERE deepzoom IS NULL OR deepzoom = '' OR dzi_time < update_time;" % tablename
        self.cursor.execute(sql_countAll)
        json_data = self.sql_fetch_json()
        return json_data

    def setdzi(self,tablename=None,dzi_url='',sid=1):
        if self.connection:
            tablename = self.escape(tablename)
            try:
                #dzi_time = time.strftime("%Y-%m-%d %X")
                dzi_time = int(round(time.time() * 1000))
                self.cursor.execute('update %s set deepzoom = "%s",dzi_time = "%s" where id = %s;' %(tablename,dzi_url,dzi_time,sid))
                self.conn.commit()
                return True
            except Exception as e:
                logging.exception("An Error Occured: ")
                logging.exception(e)
                print ("An Error Occured: ",e)
                return False

    #插入数据到数据库
    def insert(self,tablename=None,**values):

        if self.connection:
            tablename = self.escape(tablename)
            if values:
                _keys = ",".join(self.escape(k) for k in values)
                _values = ",".join(['%s',]*len(values))
                sql_query = "insert into %s (%s) values (%s)" % (tablename,_keys,_values)
            else:
                sql_query = "replace into %s default values" % tablename
            try:
                if values:
                    self.cursor.execute(sql_query,list(itervalues(values)))
                else:
                    self.cursor.execute(sql_query)
                self.conn.commit()
                return True
            except Exception as e:
                print ("An Error Occured: ",e)
                return False

    def find(self,tablename=None,linename=None,whois=1):
        if self.connection:
            tablename = self.escape(tablename)
            if linename:
                self.cursor.execute("select * from %s where %s = %s;" %(tablename,linename,whois))
                json_data = self.sql_fetch_json()
                return json_data

    def setname(self,tablename=None,linename=None,whois=1):
        if self.connection:
            tablename = self.escape(tablename)
            try:
                self.cursor.execute('update %s set name = "%s" where id = %s;' %(tablename,linename,whois))
                self.conn.commit()
                return True
            except Exception as e:
                print ("An Error Occured: ",e)
                return False

    def setclname(self,tablename=None,linename=None,whois=1):
        if self.connection:
            tablename = self.escape(tablename)
            try:
                self.cursor.execute('update %s set C_NICK = "%s" where C_ID = %s;' %(tablename,linename,whois))
                self.conn.commit()
                return True
            except Exception as e:
                print ("An Error Occured: ",e)
                return False

    def sql_fetch_json(self):
        keys = []
        for column in self.cursor.description:
            keys.append(column[0])
        key_number = len(keys)

        json_data = []
        for row in self.cursor.fetchall():
            item = dict()
            for q in range(key_number):
                item[keys[q]] = row[q]
            json_data.append(item)
        return json_data
