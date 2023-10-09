import copy
import os
import re
import time
import requests, json
from ast import literal_eval
import configparser
import json
import datetime as dt
from dateutil.parser import parse
# 아래 2개의 패키지 설치!!!!필수 !!!! (pymysql, sshtunnel)
import pymysql
import numpy as np
import pandas as pd
from tqdm import tqdm
import xlrd
from sqlalchemy import create_engine

### 접속 정보 파일 가져오기
with open('/home/dataqi/automatching/config.json', 'r', encoding='utf-8') as f:
# with open('config.json', 'r', encoding='utf-8') as f:
    json_text = f.read()
    pt = re.compile('\/\*.*\*\/')
    find_no_text_list = re.findall(pattern=pt, string=json_text)
    for f_text in find_no_text_list:
        json_text = re.sub(re.escape(f_text), '', json_text)

### 전역변수 설정
# str 타입 => dictionary 타입으로 변경
config = literal_eval(json_text) # 딕셔너리로 변경
TODAY_DT = dt.datetime.today().strftime('%Y-%m-%d')
NOW_DT = dt.datetime.today().strftime('%Y%m%d_%H%M%S')
collect_date = parse(TODAY_DT) - dt.timedelta(1)
C_DT = collect_date.strftime('%Y-%m-%d')

class Db():
    '''
    초기화 작업
    회사용
    init
    '''

    # def __init__(self, oper_position, site):
    #     # site_cat = 'direct.child'
    #     # site = site_cat.split('.')[0] # 사이트(프로젝트) : 'direct'
    #     # category = site_cat.split('.')[1] # 카테고리 : 'child'(기저귀), 'computer'(노트북) 등
    #     # self.site = category
    #
    #     self.site = site
    #     self.config = config['DIRECT'] # DIRECT 접속 정보 가져오기
    #     self.backup_config = config['BACK_UP']  # 백업 서버 접속 정보 가져오기
    #     # SK MAGIC ELASTIC 서버 해시데이터 접속 정보
    #     es_config = config['DIRECT']['ES_SERVER_CONFIG']
    #     hd_str = copy.deepcopy(es_config['HEADER'])
    #     es_config['HEADER'] = literal_eval(str(hd_str))  # str => dict타입으로 변환
    #     self.es_config = es_config
    #     print('DIRECT ELASTIC 접속 세팅 완료!!')
    #     # DIRECT ITEM MASTER 서버 및 데이터 베이스 접속 정보
    #     direct_config = config['DIRECT']['ITEM_MASTER_CONFIG']
    #
    #     # 자동정제 서버내 DB 접속정보 딕셔너리 선언
    #     db_config = config['AUTOMATCHING']['DATABASE_CONFIG']['DIRECT']
    #     if oper_position == 'local':
    #         # SSH로 접속
    #         ssh_auto_config = config['AUTOMATCHING']['SERVER_CONFIG']
    #         ssh_auto = SSHTunnelForwarder((ssh_auto_config['HOST_NAME'], int(ssh_auto_config['PORT'])),
    #                                       # 'ssh터널 host 주소'
    #                                       ssh_username=ssh_auto_config['SSH_USERNAME'],
    #                                       ssh_password=ssh_auto_config['SSH_PASSWORD'],
    #                                       ssh_pkey=ssh_auto_config['SSH_PKEY'],
    #                                       remote_bind_address=('127.0.0.1', 3306))
    #         ssh_auto.start() # 원격 서버 접속 실행
    #         ENGINE = create_engine(
    #             "mysql+pymysql://" + db_config['DATABASE_USERNAME'] + ":" + db_config['DATABASE_PASSWORD'] + "@" \
    #             + '127.0.0.1' + ":" + str(ssh_auto.local_bind_port) + "/" + db_config['DATABASE_NAME'], encoding='utf-8')  # ENGINE
    #
    #         self.ENGINE = ENGINE
    #     else: # server에서 실행시 접속
    #         ENGINE = create_engine("mysql+pymysql://" + db_config['DATABASE_USERNAME'] + ":" + db_config['DATABASE_PASSWORD'] + "@" \
    #             + '127.0.0.1' + ":" + '3306' + "/" + db_config['DATABASE_NAME'], encoding='utf-8')  # ENGINE
    #         self.ENGINE = ENGINE
    #
    #     # 아이템 마스터 정보 엔진생성
    #     ssh_im_config = direct_config['SERVER_CONFIG']  # SSH 연결
    #     ssh_im_auto = SSHTunnelForwarder((ssh_im_config['HOST_NAME'], int(ssh_im_config['PORT'])),
    #                                      # 'ssh터널 host 주소'
    #                                      ssh_username=ssh_im_config['SSH_USERNAME'],
    #                                      ssh_password=ssh_im_config['SSH_PASSWORD'],
    #                                      # ssh_pkey=ssh_im_config['SSH_PKEY'],
    #                                      remote_bind_address=('127.0.0.1', 3306))
    #     ssh_im_auto.start()  # 원격 서버 접속 실행
    #
    #     # MYSQL 접속
    #     db_im_config = direct_config['DATABASE_CONFIG']
    #     IM_ENGINE = create_engine(
    #         "mysql+pymysql://" + db_im_config['DATABASE_USERNAME'] + ":" + db_im_config['DATABASE_PASSWORD'] + "@" \
    #         + '127.0.0.1' + ":" + str(ssh_im_auto.local_bind_port) + "/" + db_im_config['DATABASE_NAME'], encoding='utf-8')  # ENGINE
    #     # str(ssh_im_auto.local_bind_port)
    #     self.IM_ENGINE = IM_ENGINE
    #
    #     print('Mysql 데이터 베이스 접속 및 ENGINE 세팅 완료!!')

    '''
    초기화 작업
    로컬PC용
    init
    '''
    def __init__(self, oper_position, site):
        self.oper_position = oper_position # 작업 위치(서버/로컬PC)
        self.site = site # 프로젝트(사이트명)

        # DB 접속 ENGINE 세팅
        ENGINE = create_engine("mysql+pymysql://" + 'root' + ":" + '0000' + "@" \
                        + '127.0.0.1' + ":" + '3306' + "/" + site, encoding='utf-8')  # ENGINE
        self.ENGINE = ENGINE



    '''
    1. 기존 아이템 마스터 백업 테이블 생성
    2. 현재 아이템 마스터 UPLOAD(등록)
    3. 작업 Logging(이력) 테이블에 INSERT
    '''
    def upload_item_master(self, upload_df):
        ### 1. 기존 아이템 마스터 백업 테이블 생성
        # 1-1. 기존 아이템 마스터 불러오기
        base_im_df = self.import_data('item_master')
        # 1-2. 백업 아이템 마스터 IMPORT
        self.upload_data(base_im_df, 'item_master_'+NOW_DT)

        ### 2. 현재 아이템 마스터 UPLOAD(등록)
        self.upload_data(upload_df, 'item_master')

        ### 3. 작업 Logging(이력) 테이블에 INSERT
        # self.insert_logging()
        return











    '''
    데이터 IMPORT
    파라미터
    1. 임포트할 테이블명
    '''
    def import_data(self, import_tb_nm):
        # TABLE_NAME = f'item_master'
        sql = f"select * from {self.site}.{import_tb_nm};"
        print('실행 명령문 :', sql)
        db_df = pd.read_sql(sql=sql, con=self.ENGINE, index_col=None)
        print('DB에서 불러온 데이터 출력 :', db_df.head())
        return db_df
    '''
    데이터 UPLOAD
    파리미터
    1. 업로드 대상 데이터 프레임
    2. 업로드 할 테이블명
    '''
    def upload_data(self, df, upload_tb_nm):
        # TABLE_NAME = f'item_master'
        print('UPLOAD 테이블명 :', upload_tb_nm)
        df.to_sql(name=upload_tb_nm, index=False, chunksize=10000, con=self.ENGINE, if_exists='replace')
        print(f'{"#"*100}  UPLOAD 완료  {"#"*100}')
        return

    '''
    로깅 테이블 정보 INSERT
    '''
    def insert_logging(self, logging_info):
        # TABLE_NAME = f'oper_logging'
        # print('UPLOAD 테이블명 :', TABLE_NAME)
        # df.to_sql(name=TABLE_NAME, index=False, chunksize=10000, con=self.ENGINE, if_exists='replace')
        # print(f'{"#" * 100}  UPLOAD 완료  {"#" * 100}')
        return


    # 기존 테이블 불러와서 백업테이블로 만들기
sql = f'create table as {SITE}.item_master_backup_{NOW_DT} select * from {SITE}.item_master'





# 새로운 아이템 마스터 INSERT 하기




ENGINE