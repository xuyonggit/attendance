# -*- coding:utf-8 -*-
import xlrd
import xlsxwriter
import pymysql
from datetime import date
import datetime


class Annual():
    def __init__(self):
        self.year = date.today().year

    # 数据库连接
    def Con(self):
        return pymysql.connect(
            host='123.59.67.196',
            port=3306,
            user='attendance',
            passwd='attendance',
            db='attendance',
            charset='utf8mb4',
            autocommit=True
        )

    # 获取所有用户信息
    def get_alluser(self):
        """
        :return: type: dict {'李旭广': datetime.date(2018, 5, 3)}
        """
        tmp_dic1 = {}
        with self.Con().cursor() as cur:
            cur.execute("select * from annual;")
            for d in cur:
                tmp_dic1[d[0]] = d[1]
        return tmp_dic1

    #  计算年假余额
    def annual_suoplus(self):
        """
        :return: type: dict {'徐勇': 2.9, '李旭广': 1.3}
        """
        user_data = self.get_alluser()
        # 年天数
        self.year = int(self.year)
        if (self.year % 400 == 0 or (self.year % 4 == 0 and self.year % 100 != 0)):
            days = 366
        else:
            days = 365
        # 年初日期
        first_date = datetime.datetime.strptime("{}-01-01".format(self.year), '%Y-%m-%d').date()
        tmp_dic2 = {}
        for name, indate in user_data.items():
            # 计算工龄
            if date.today().year - indate.year < 10:
                annual = 5
            else:
                annual = 10
            if indate.year < date.today().year:
                workdays = (date.today() - first_date).days
                annual_num_souplus = round(workdays / days * annual, 1)
            else:
                workdays = (date.today() - indate).days
                annual_num_souplus = round(workdays / days * annual, 1)
            tmp_dic2[name] = annual_num_souplus
        print(tmp_dic2)

    # 获取请假记录
    def get_detail(self):
        try:
            workbook = xlrd.open_workbook("请假记录表.xlsx")
            data_sheet = workbook.sheet_by_index(0)
            for cols in range(2, data_sheet.nrows):
                name = data_sheet.cell_value(cols, 0)
                if data_sheet.cell(cols, 1).ctype == 3:
                    d = xlrd.xldate_as_tuple(data_sheet.cell_value(cols, 1), workbook.datemode)
                    out_date = datetime.datetime.strptime('{}-{}-{}'.format(d[0], d[1], d[2]), '%Y-%m-%d').date()
                day = data_sheet.cell_value(cols, 2)
                d_type = data_sheet.cell_value(cols, 3)
                d_list = []
                if day > 1:
                    d_dict = {}
                    n = 0
                    for i in range(round(day, 0)):
                        if i - n > 1:
                            d_day = 1
                        else:
                            d_day = i - n
                        tmp_d = out_date + datetime.timedelta(days=i)
                        d_dict['name'], d_dict['date'],d_dict['day'], d_dict['type'] = name, tmp_d, d_day, d_type
                        d_list.append(d_dict)
                    print(d_list)
        except FileNotFoundError as f:
            print("打开记录表失败，文件不存在！")


if __name__ == '__main__':
    M = Annual()
    M.get_detail()
