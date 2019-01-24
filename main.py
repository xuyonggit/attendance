# -*- coding:utf-8 -*-
import xlrd
import xlsxwriter
import datetime, time
import calendar
import os, re
import sys
import attendan
from PyQt5.QtWidgets import QApplication, QMainWindow
import logging

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('attendance.log', encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:(%(lineno)d) - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class attendance():
    def __init__(self, filename='filename', filename23='filename'):
        self.timeconf = ['上班时间', '下班时间', '迟到时间']
        self.up_downtime = {}  # 上下班时间，格式：{'下班时间': '18-00-00', '上班时间': '09-00-00'}
        self.year = ""  # 考勤年
        self.month = ""  # 考勤数据月份
        self.notneed_person = []
        self.filename = filename
        self.filename_23 = filename23
        self.get_conf()

    def get_conf(self):
        sdata = getconf()
        # 获取上下班时间配置
        self.up_downtime['上班时间'], self.up_downtime['下班时间'], self.up_downtime['迟到时间'] = \
            sdata['utime'], sdata['dtime'], sdata['outtime']
        # 获取考勤数据月份
        self.year = int(sdata['year'])
        self.month = int(sdata['month'])
        # 判断是否需要分析加班
        self.workovertime = sdata['workovertime']
        # 获取考勤区域
        self.type = int(sdata['type'])
        self.holidays = {}  # 节假日设定，格式：{'清明': ['2018-04-05', '2018-04-06', '2018-04-07']}
        hdays = sdata['hdays']
        if hdays:
            for name in hdays.keys():
                self.holidays[name] = []
                if len(hdays[name]) > 1:
                    startdate = datetime.datetime.strptime(hdays[name][0], "%Y-%m-%d")
                    enddate = datetime.datetime.strptime(hdays[name][1], "%Y-%m-%d")
                    while startdate <= enddate:
                        date_str = startdate.strftime('%Y-%m-%d')
                        self.holidays[name].append(date_str)
                        startdate += datetime.timedelta(days=1)
                else:
                    startdate = datetime.datetime.strptime(hdays[name][0], "%Y-%m-%d")
                    date_str = startdate.strftime('%Y-%m-%d')
                    self.holidays[name].append(date_str)
        nonotes = sdata['nonotes']
        self.notneed_person = nonotes

    # 获取当月所有工作日
    def get_days(self, type=0):
        """
        :param type:0  所有工作日 1 所有周末以及节假日
        :return: list
        """
        type = type
        days = []  # 当月所有日期，格式：['2018-03-01', ... '2018-03-31']
        #self.get_conf()
        temp_list_holiday_1 = []
        monthrange = calendar.monthrange(self.year, self.month)
        if self.month < 10:
            month = "0{}".format(self.month)
        else:
            month = self.month
        # 集中假期日期
        for holiday in self.holidays.values():
            for day in holiday:
                temp_list_holiday_1.append(day)
        if type == 0:
            for m in range(1, monthrange[1] + 1):
                if m < 10:
                    m = "0{}".format(m)
                    mon = "{}-{}-{}".format(self.year, month, m)
                else:
                    mon = "{}-{}-{}".format(self.year, month, m)
                if mon not in temp_list_holiday_1 \
                        and 0 < int(time.strftime('%w', time.strptime(mon, '%Y-%m-%d'))) < 6:
                    days.append(mon)
        elif type == 1:
            for m in range(1, monthrange[1] + 1):
                if m < 10:
                    m = "0{}".format(m)
                    mon = "{}-{}-{}".format(self.year, month, m)
                else:
                    mon = "{}-{}-{}".format(self.year, month, m)
                if mon in temp_list_holiday_1 \
                        or int(time.strftime('%w', time.strptime(mon, '%Y-%m-%d'))) == 6 \
                        or int(time.strftime('%w', time.strptime(mon, '%Y-%m-%d'))) == 0:
                    days.append(mon)
        else:
            raise Exception
        return days

    # 获取考勤数据
    def get_date(self):
        temp_list_data_1 = []
        temp_dic_data_1 = {}
        # open data file
        try:
            workbook = xlrd.open_workbook(self.filename, encoding_override='gbk')
        except FileNotFoundError as f:
            logger.error("系统发生异常：")
            logger.error("Error:找不到考勤文件【{}】，请检查文件名是否有误\n或者有多余空格 ：".format(self.filename))
        data_sheet = workbook.sheet_by_index(0)
        for c in range(data_sheet.ncols):
            temp_list_data_1.append(data_sheet.cell_value(0, c))
        # "姓名"在第几列
        username_index = temp_list_data_1.index('姓名')
        # "星期"在第几列
        week_index = temp_list_data_1.index('星期')
        # "刷卡日期"在第几列
        notesdate_index = temp_list_data_1.index('刷卡日期')
        # "刷卡时间"在第几列
        notestime_index = temp_list_data_1.index('刷卡时间')
        # "签到方式"在第几列
        notestype_index = temp_list_data_1.index('签到方式')
        for n in range(1, data_sheet.nrows):
            username = data_sheet.cell_value(n, username_index)  # 姓名
            notesdate = data_sheet.cell_value(n, notesdate_index)  # 刷卡日期
            # 刷卡时间
            if data_sheet.cell(n, notestime_index).ctype == 3:
                date_value = xlrd.xldate_as_tuple(data_sheet.cell_value(n, notestime_index), workbook.datemode)
                notestime = datetime.time(*date_value[3:5]).strftime('%H:%M:%S')
            else:
                notestime = data_sheet.cell_value(n, notestime_index)
            notestype = data_sheet.cell_value(n, notestype_index)  # 签到方式
            if username not in temp_dic_data_1.keys():
                temp_dic_data_1[username] = {}
                temp_dic_data_1[username]['date'] = {}
            if notestype == '指纹':
                if notesdate not in temp_dic_data_1[username]['date'].keys():
                    temp_dic_data_1[username]['date'][notesdate] = []
                temp_dic_data_1[username]['date'][notesdate].append(notestime)
        del temp_dic_data_1['']
        return temp_dic_data_1

    # 处理考勤记录
    def check_note(self, datalist=[], outtime='12:00'):
        """
        :param datalist:打卡记录数据列表['09:00', '12:00', ...]
        :param outtime: 上班打卡截止时间，超过改时间将不计入上班打卡
        :return: datalist
        """
        datalist = datalist
        outtime = outtime
        if outtime != 'None':
            L = {}
            one = ''
            end = ''
            out = ''
            for n in range(len(datalist)):
                if datetime.datetime.strptime('7:30', '%H:%M') <= datetime.datetime.strptime(datalist[n],
                                                                                             '%H:%M') < datetime.datetime.strptime('12:00',
                                                                                                                                   '%H:%M'):
                    if not one:
                        one = datalist[n]
                        continue
                if datetime.datetime.strptime('17:00', '%H:%M') <= datetime.datetime.strptime(datalist[n],
                                                                                              '%H:%M') < datetime.datetime.strptime('23:59',
                                                                                                                                    '%H:%M'):
                    end = datalist[n]
                if datetime.datetime.strptime('21:00', '%H:%M') <= datetime.datetime.strptime(datalist[n], '%H:%M'):
                    out = datalist[n]
            if one:
                L['one'] = one
            if end:
                L['end'] = end
            if out:
                L['out'] = out
            return L
        else:
            L = {}
            one = datalist[0]
            end = datalist[-1]
            if one:
                L['one'] = one
            if end:
                L['end'] = end
            return L

    # 处理数据
    def make_data(self, type=1):
        """
        :param type: int {1: 11层数据, 2: 23层数据}
        :return:
        """
        temp_dict_data_2 = {}
        if type == 1:
            data = self.get_date()
        elif type == 2:
            data = self.get_23data()
        days_work = self.get_days()
        days_out = self.get_days(type=1)
        #self.get_conf()
        up_time = self.up_downtime.get('上班时间', '9:00')
        down_time = self.up_downtime.get('下班时间', '18:00')
        out_time = self.up_downtime.get('迟到时间', '9:30')
        # 标准工时
        default_worktime = datetime.datetime.strptime(down_time, '%H:%M') - datetime.datetime.strptime(up_time, '%H:%M')
        for name, values in data.items():
            # 初始化综合结果
            if 'result' not in values.keys():
                values['result'] = {}
            # for notedate, alltime in values['date'].items():
            for notedate in days_work:
                if notedate not in values['result']:
                    data[name]['result'][notedate] = {}
                    # -----------------------------------------------------------
                    # 初始化未打卡统计
                    if 'onelostnotes' not in values['result'][notedate].keys():
                        data[name]['result'][notedate]['onelostnotes'] = 0
                    if 'endlostnotes' not in values['result'][notedate].keys():
                        data[name]['result'][notedate]['endlostnotes'] = 0
                    # 初始化缺勤(小时)
                    data[name]['result'][notedate]['losttime'] = 0
                    # 初始化当天总工时
                    data[name]['result'][notedate]['worktime'] = 0
                    # 初始化早退时间
                    data[name]['result'][notedate]['befortime'] = 0
                    # 初始化迟到时间
                    data[name]['result'][notedate]['latertime'] = 0
                    # 初始化工时，单位 s
                    data[name]['result'][notedate]['allworktimes'] = 0
                    # -----------------------------------------------------------
                    if notedate in values['date'].keys():
                        alltime = self.check_note(values['date'][notedate], outtime='12:00')
                        if 'one' in alltime.keys() and 'end' in alltime.keys():
                            starttime = alltime['one']
                            endtime = alltime['end']
                            values['result'][notedate]['uptime'] = starttime
                            values['result'][notedate]['downtime'] = endtime
                            worktime = datetime.datetime.strptime(endtime, '%H:%M') - datetime.datetime.strptime(
                                starttime, '%H:%M')
                            # 递增总工时
                            data[name]['result'][notedate]['allworktimes'] = ((datetime.datetime.strptime(
                                    alltime['end'], '%H:%M') - datetime.datetime.strptime(
                                    alltime['one'], '%H:%M')).seconds) - 3600
                            if datetime.datetime.strptime(starttime, '%H:%M') > datetime.datetime.strptime(out_time, '%H:%M'):
                                lasttime = str((datetime.datetime.strptime(starttime, '%H:%M') - datetime.datetime.strptime(
                                    out_time, '%H:%M')))
                                data[name]['result'][notedate]['latertime'] = lasttime
                            else:
                                # 早退
                                if worktime < default_worktime:
                                    losttime = default_worktime - worktime
                                    values['result'][notedate]['befortime'] = losttime
                        # 未打卡
                        elif 'one' in alltime.keys() and 'end' not in alltime.keys():
                            values['result'][notedate]['uptime'] = alltime['one']
                            values['result'][notedate]['downtime'] = '未打卡'
                            # 递增总工时
                            data[name]['result'][notedate]['allworktimes'] = 8 * 3600
                        elif 'one' not in alltime.keys() and 'end' in alltime.keys():
                            values['result'][notedate]['uptime'] = '未打卡'
                            values['result'][notedate]['downtime'] = alltime['end']
                            # 递增总工时
                            data[name]['result'][notedate]['allworktimes'] = 8 * 3600
                        # 缺勤
                        else:
                            values['result'][notedate]['uptime'] = '未打卡'
                            values['result'][notedate]['downtime'] = '未打卡'
                            values['result'][notedate]['losttime'] = 8
                        # 加班
                        if 'out' in alltime.keys():
                            #values['result'][notedate]['outtimes_21'] = 0
                            #values['result'][notedate]['outtimes_23'] = 0
                            values['result'][notedate]['outtime'] = datetime.datetime.strptime(alltime['out'],
                                '%H:%M') - datetime.datetime.strptime('21:00', '%H:%M')
                            if values['result'][notedate]['outtime'] >= datetime.timedelta(hours=2):
                                values['result'][notedate]['outtimes_23'] = 1
                            else:
                                values['result'][notedate]['outtimes_21'] = 1
                    else:
                        values['result'][notedate]['uptime'] = '未打卡'
                        values['result'][notedate]['downtime'] = '未打卡'
                        values['result'][notedate]['losttime'] = 8

            # 节假日以及周末加班处理
            for notedate2 in days_out:
                if notedate2 in values['date'].keys():
                    if notedate2 not in values['result']:
                        values['result'][notedate2] = {}
                        # -----------------------------------------------------------
                        # 初始化未打卡统计
                    if len(values['date'][notedate2]) >= 2:
                        alltime = self.check_note(data[name]['date'][notedate2], outtime='None')
                        # print(alltime)
                        # print(values['date'][notedate2], alltime)
                        outwork_time = datetime.datetime.strptime(alltime['end'], '%H:%M') - \
                                       datetime.datetime.strptime(alltime['one'], '%H:%M')
                        values['result'][notedate2]['holidayworktime'] = outwork_time
                        values['result'][notedate2]['allworktimes'] = outwork_time.seconds

        return data

    # create excel table
    def make_excel(self):
        self.get_conf()
        logg("开始处理【11】层{}年{}月考勤数据".format(self.year, self.month))
        logg('--------------------------------------------')
        logg("上班时间：{}".format(self.up_downtime['上班时间']))
        logg("下班时间：{}".format(self.up_downtime['下班时间']))
        logg("迟到时间：{}".format(self.up_downtime['迟到时间']))
        for d in self.holidays.keys():
            items = ''
            for i in self.holidays[d]:
                items += ' {}'.format(str(i))
            logg('节假日：{}, {}'.format(d, items))
        logg('免打卡人员：{}'.format(','.join(s for s in self.notneed_person)))
        logg('--------------------------------------------')
        if not os.path.exists('result'):
            os.mkdir('result')
        else:
            if os.path.exists(os.path.join('result', '金桐11层{}月份考勤.xlsx'.format(self.month))):
                try:
                    os.remove(os.path.join('result', '金桐11层{}月份考勤.xlsx'.format(self.month)))
                except PermissionError as f:
                    logg(f)
                    logger.error(f)
        result_data = self.make_data()
        # create excel table
        workbook = xlsxwriter.Workbook(os.path.join('result', '金桐11层{}月份考勤.xlsx'.format(self.month)))
        # create sheet
        worksheet = workbook.add_worksheet('金桐11层{}月份考勤'.format(self.month))
        # Excel 格式
        # ============================================================
        # 表头格式：加粗,居中
        cell_format_head = workbook.add_format(
            {'text_wrap': True, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'fg_color': '#9900FF'})
        # 首列姓名格式
        cell_format_name = workbook.add_format(
            {'text_wrap': True, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
        # 统计数字格式
        cell_format_number = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        # 日期格式：自动换行，列宽12，居中
        cell_format_date = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        if self.workovertime:
            worksheet.set_column('A:Q', 12)
        else:
            worksheet.set_column('A:J', 12)
        # 设置默认行高 22
        worksheet.set_default_row(22)
        # 边框实线
        workbook.add_format({'border': 1})
        # ============================================================
        worksheet_cols = 1
        table_head = self.tableHead()
        for vn in range(len(table_head)):
            worksheet.write(0, vn, table_head[vn], cell_format_head)

        for name in result_data.keys():
            # 排除免打卡人员
            if name in self.notneed_person:
                continue
            worksheet.write(worksheet_cols, 0, name, cell_format_name)
            # 旷工日期
            passwork_list = []
            # 缺勤(小时)
            lostwork_hour = 0
            # 上班未打卡日期
            no_uptime_list = []
            # 上班未打卡次数
            no_uptime_num = 0
            # 下班未打卡日期
            no_downtime_list = []
            # 下班未打卡次数
            no_downtime_num = 0
            # 迟到日期 / 时间
            lastdate_list = []
            lastdate_time = []
            # 早退日期 / 时间
            before_list = []
            before_time = []
            # 加班日期及时间
            outtime_list = []
            outtime_time = []
            # 21点打卡次数
            times_of_21 = 0
            # 23点打卡次数
            times_of_23 = 0
            # 周末节假日加班日期及时长
            holiday_list = []
            holiday_time = []
            # 总工时
            allworktimes = 0
            days2 = self.get_days(type=1)
            days = self.get_days()
            for date in days:
                date_result = result_data[name]['result'][date]
                # 计算加班次数
                times_of_21 += date_result.get('outtimes_21', 0)
                times_of_23 += date_result.get('outtimes_23', 0)
                # 计算上班未打卡日期和次数
                if date_result['uptime'] == '未打卡' and date_result['downtime'] != '未打卡':
                    no_uptime_list.append(date)
                    no_uptime_num += 1
                # 计算下班未打卡日期和次数
                if date_result['downtime'] == '未打卡' and date_result['uptime'] != '未打卡':
                    no_downtime_list.append(date)
                    no_downtime_num += 1
                # 计算缺勤日期
                if date_result['losttime'] == 8:
                    passwork_list.append(date)
                # 计算迟到日期和时间
                if date_result['latertime']:
                    lastdate_list.append(date)
                    lastdate_time.append(str(date_result['latertime']))
                # 计算早退日期和时间
                if date_result['befortime']:
                    before_list.append(date)
                    before_time.append(str(date_result['befortime']))
                # 计算加班日期和时间
                if 'outtime' in date_result.keys():
                    outtime_list.append(date)
                    outtime_time.append(str(date_result['outtime']))
                lostwork_hour += date_result['losttime']
                # 计算总工时
                allworktimes += date_result['allworktimes']
            for date2 in days2:
                if date2 in result_data[name]['result'].keys():
                    date_result = result_data[name]['result'][date2]
                    # 计算节假日加班日期和时间
                    if 'holidayworktime' in date_result.keys():
                        holiday_list.append(date2)
                        holiday_time.append(str(date_result['holidayworktime']))
                        allworktimes += date_result['allworktimes']
            # 写入excel
            # '上班未打卡日期', '上班未打卡次数'
            if no_uptime_list and no_uptime_num:
                worksheet.write(worksheet_cols, 1, ' '.join(no_uptime_list), cell_format_date)
                worksheet.write(worksheet_cols, 2, no_uptime_num, cell_format_number)
            # '下班未打卡日期', '下班未打卡次数'
            if no_downtime_list and no_downtime_num:
                worksheet.write(worksheet_cols, 3, ' '.join(no_downtime_list), cell_format_date)
                worksheet.write(worksheet_cols, 4, no_downtime_num, cell_format_number)
            # '迟到日期', '迟到时间'
            if lastdate_list and lastdate_time:
                worksheet.write(worksheet_cols, 5, ' '.join(lastdate_list), cell_format_date)
                worksheet.write(worksheet_cols, 6, '\n'.join(lastdate_time), cell_format_date)
            # '早退日期', '早退时间'
            if before_list and before_time:
                worksheet.write(worksheet_cols, 7, ' '.join(before_list), cell_format_date)
                worksheet.write(worksheet_cols, 8, '\n'.join(before_time), cell_format_date)
            #
            if self.workovertime:
                # '加班日期', '加班时长'
                if outtime_list and outtime_time:
                    worksheet.write(worksheet_cols, 9, ' '.join(outtime_list), cell_format_date)
                    worksheet.write(worksheet_cols, 10, '\n'.join(outtime_time), cell_format_date)
                # '21点打卡次数', '23点打卡次数'
                if times_of_21 != 0:
                    worksheet.write(worksheet_cols, 11, times_of_21, cell_format_date)
                if times_of_23 != 0:
                    worksheet.write(worksheet_cols, 12, times_of_23, cell_format_date)
                # '周末及节假日加班日期', '周末及节假日加班时长'
                if holiday_list and holiday_time:
                    worksheet.write(worksheet_cols, 13, ' '.join(holiday_list), cell_format_date)
                    worksheet.write(worksheet_cols, 14, '\n'.join(holiday_time), cell_format_date)
                # '缺勤日期'
                if passwork_list:
                    worksheet.write(worksheet_cols, 15, ' '.join(passwork_list), cell_format_date)
                # '总工时(h)'
                if allworktimes:
                    worksheet.write(worksheet_cols, 16, round(allworktimes / 3600, 1), cell_format_date)
            else:
                # '缺勤日期'
                if passwork_list:
                    worksheet.write(worksheet_cols, 9, ' '.join(passwork_list), cell_format_date)
                # '总工时(h)'
                if allworktimes:
                    worksheet.write(worksheet_cols, 10, round(allworktimes / 3600, 1), cell_format_date)
            worksheet_cols += 1
        workbook.close()
        logg("操作完成。")
        self.write_cache_file(11, ','.join(self.notneed_person))

    # 获取23层考勤数据
    def get_23data(self):
        temp_list_data_1 = []
        temp_dic_data_1 = {}
        # open data file
        try:
            workbook = xlrd.open_workbook(self.filename_23, encoding_override='gbk')
        except FileNotFoundError as f:
            logger.error("系统发生异常：")
            logger.error("Error:找不到考勤文件【{}】，请检查文件名是否有误\n或者有多余空格 ：".format(self.filename_23))
        data_sheet = workbook.sheet_by_index(0)
        for c in range(data_sheet.ncols):
            temp_list_data_1.append(data_sheet.cell_value(0, c))
        # "姓名"在第几列
        username_index = temp_list_data_1.index('姓名')
        # "刷卡时间"在第几列
        notestime_index = temp_list_data_1.index('日期时间')
        # "签到方式"在第几列
        notestype_index = temp_list_data_1.index('比对方式')
        for n in range(1, data_sheet.nrows):
            username = data_sheet.cell_value(n, username_index)  # 姓名
            date = xlrd.xldate_as_tuple(data_sheet.cell_value(n, notestime_index), 0)  # 刷卡日期
            # 日期以0补全
            if date[1] < 10:
                mon = '0{}'.format(date[1])
            else:
                mon = date[1]
            if date[2] < 10:
                day = '0{}'.format(date[2])
            else:
                day = date[2]
            notesdate = '{}-{}-{}'.format(date[0], mon, day)
            # 刷卡时间
            if data_sheet.cell(n, notestime_index).ctype == 3:
                date_value = xlrd.xldate_as_tuple(data_sheet.cell_value(n, notestime_index), workbook.datemode)
                notestime = datetime.time(*date_value[3:4]).strftime('%H:%M')
            else:
                notestime = data_sheet.cell_value(n, notestime_index)
            notestype = data_sheet.cell_value(n, notestype_index)  # 签到方式
            if username not in temp_dic_data_1.keys():
                temp_dic_data_1[username] = {}
                temp_dic_data_1[username]['date'] = {}
            if notestype == '指纹':
                if notesdate not in temp_dic_data_1[username]['date'].keys():
                    temp_dic_data_1[username]['date'][notesdate] = []
                temp_dic_data_1[username]['date'][notesdate].append(notestime)
        return temp_dic_data_1

    # create excel table
    def make_excel_23(self):
        self.get_conf()
        logg("开始处理【23】层考勤数据")
        logg('--------------------------------------------')
        logg("上班时间：{}".format(self.up_downtime['上班时间']))
        logg("下班时间：{}".format(self.up_downtime['下班时间']))
        logg("迟到时间：{}".format(self.up_downtime['迟到时间']))
        for d in self.holidays.keys():
            items = ''
            for i in self.holidays[d]:
                items += ' {}'.format(str(i))
            logg('节假日：{}, {}'.format(d, items))
        logg('免打卡人员：{}'.format(','.join(s for s in self.notneed_person)))
        logg('--------------------------------------------')
        if not os.path.exists('result'):
            os.mkdir('result')
        else:
            if os.path.exists(os.path.join('result', '金桐23层{}月份考勤.xlsx'.format(self.month))):
                try:
                    os.remove(os.path.join('result', '金桐23层{}月份考勤.xlsx'.format(self.month)))
                except PermissionError as f:
                    logger.error(f)
        result_data = self.make_data(type=2)
        # create excel table
        workbook = xlsxwriter.Workbook(os.path.join('result', '金桐23层{}月份考勤.xlsx'.format(self.month)))
        # create sheet
        worksheet = workbook.add_worksheet('金桐23层{}月份考勤'.format(self.month))
        # Excel 格式
        # ============================================================
        # 表头格式：加粗,居中
        cell_format_head = workbook.add_format(
            {'text_wrap': True, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'fg_color': '#9900FF'})
        # 首列姓名格式
        cell_format_name = workbook.add_format(
            {'text_wrap': True, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
        # 统计数字格式
        cell_format_number = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        # 日期格式：自动换行，列宽15，居中
        cell_format_date = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        if self.workovertime:
            worksheet.set_column('A:Q', 12)
        else:
            worksheet.set_column('A:J', 12)
        # 设置默认行高 22
        worksheet.set_default_row(22)
        # 边框实线
        workbook.add_format({'border': 1})
        # ============================================================
        worksheet_cols = 1
        table_head = self.tableHead()
        for vn in range(len(table_head)):
            worksheet.write(0, vn, table_head[vn], cell_format_head)
        for name in result_data.keys():
            if name in self.notneed_person:
                continue
            worksheet.write(worksheet_cols, 0, name, cell_format_name)
            # 旷工日期
            passwork_list = []
            # 缺勤(小时)
            lostwork_hour = 0
            # 上班未打卡日期
            no_uptime_list = []
            # 上班未打卡次数
            no_uptime_num = 0
            # 下班未打卡日期
            no_downtime_list = []
            # 下班未打卡次数
            no_downtime_num = 0
            # 迟到日期 / 时间
            lastdate_list = []
            lastdate_time = []
            # 早退日期 / 时间
            before_list = []
            before_time = []
            # 加班日期及时间
            outtime_list = []
            outtime_time = []
            # 21点打卡次数
            times_of_21 = 0
            # 23点打卡次数
            times_of_23 = 0
            # 周末节假日加班日期及时长
            holiday_list = []
            holiday_time = []
            # 总工时
            allworktimes = 0
            days2 = self.get_days(type=1)
            days = self.get_days()
            for date in days:
                date_result = result_data[name]['result'][date]
                # 计算加班次数
                times_of_21 += date_result.get('outtimes_21', 0)
                times_of_23 += date_result.get('outtimes_23', 0)

                # 计算上班未打卡次数
                if date_result['uptime'] == '未打卡' and date_result['downtime'] != '未打卡':
                    no_uptime_list.append(date)
                    no_uptime_num += 1

                # 计算下班未打卡日期和次数
                if date_result['downtime'] == '未打卡' and date_result['uptime'] != '未打卡':
                    no_downtime_list.append(date)
                    no_downtime_num += 1

                # 计算缺勤次数
                if date_result['losttime'] == 8:
                    passwork_list.append(date)

                # 计算迟到日期和时间
                if date_result['latertime']:
                    lastdate_list.append(date)
                    lastdate_time.append(str(date_result['latertime']))

                # 计算早退日期和时间
                if date_result['befortime']:
                    before_list.append(date)
                    before_time.append(str(date_result['befortime']))

                # 计算加班日期和时间
                if 'outtime' in date_result.keys():
                    outtime_list.append(date)
                    outtime_time.append(str(date_result['outtime']))
                lostwork_hour += date_result['losttime']
                # 计算总工时
                allworktimes += date_result['allworktimes']
            for date2 in days2:
                if date2 in result_data[name]['result'].keys():
                    date_result = result_data[name]['result'][date2]
                    if 'holidayworktime' in date_result.keys():
                        holiday_list.append(date2)
                        holiday_time.append(str(date_result['holidayworktime']))
                        allworktimes += date_result['allworktimes']

            # 写入excel
            if no_uptime_list and no_uptime_num:
                worksheet.write(worksheet_cols, 1, ' '.join(no_uptime_list), cell_format_date)
                worksheet.write(worksheet_cols, 2, no_uptime_num, cell_format_number)
            if no_downtime_list and no_downtime_num:
                worksheet.write(worksheet_cols, 3, ' '.join(no_downtime_list), cell_format_date)
                worksheet.write(worksheet_cols, 4, no_downtime_num, cell_format_number)
            if lastdate_list and lastdate_time:
                worksheet.write(worksheet_cols, 5, ' '.join(lastdate_list), cell_format_date)
                worksheet.write(worksheet_cols, 6, '\n'.join(lastdate_time), cell_format_date)
            if before_list and before_time:
                worksheet.write(worksheet_cols, 7, ' '.join(before_list), cell_format_date)
                worksheet.write(worksheet_cols, 8, '\n'.join(before_time), cell_format_date)
                # 写入加班数据
                if self.workovertime:
                    # '加班日期', '加班时长'
                    if outtime_list and outtime_time:
                        worksheet.write(worksheet_cols, 9, ' '.join(outtime_list), cell_format_date)
                        worksheet.write(worksheet_cols, 10, '\n'.join(outtime_time), cell_format_date)
                    # '21点打卡次数', '23点打卡次数'
                    if times_of_21 != 0:
                        worksheet.write(worksheet_cols, 11, times_of_21, cell_format_date)
                    if times_of_23 != 0:
                        worksheet.write(worksheet_cols, 12, times_of_23, cell_format_date)
                    # '周末及节假日加班日期', '周末及节假日加班时长'
                    if holiday_list and holiday_time:
                        worksheet.write(worksheet_cols, 13, ' '.join(holiday_list), cell_format_date)
                        worksheet.write(worksheet_cols, 14, '\n'.join(holiday_time), cell_format_date)
                    # '缺勤日期'
                    if passwork_list:
                        worksheet.write(worksheet_cols, 15, ' '.join(passwork_list), cell_format_date)
                    # '总工时(h)'
                    if allworktimes:
                        worksheet.write(worksheet_cols, 16, round(allworktimes / 3600, 1), cell_format_date)
                else:
                    # '缺勤日期'
                    if passwork_list:
                        worksheet.write(worksheet_cols, 9, ' '.join(passwork_list), cell_format_date)
                    # '总工时(h)'
                    if allworktimes:
                        worksheet.write(worksheet_cols, 10, round(allworktimes / 3600, 1), cell_format_date)
            worksheet_cols += 1
        workbook.close()
        logg("操作完成。")
        self.write_cache_file(23, ','.join(self.notneed_person))

    # create excel for 加班统计
    def make_excel_count(self):
        if not os.path.exists('result'):
            os.mkdir('result')
        else:
            if os.path.exists(os.path.join('result', '金桐{}月份加班统计.xlsx'.format(self.month))):
                try:
                    os.remove(os.path.join('result', '金桐{}月份加班统计.xlsx'.format(self.month)))
                except PermissionError as f:
                    logger.error(f)
        if self.type == 11:
            result_data = self.make_data()
        else:
            result_data = self.make_data(type=2)
        # print(result_data)
        # create excel table
        workbook = xlsxwriter.Workbook(os.path.join('result', '金桐{}月份加班统计.xlsx'.format(self.month)))
        # create sheet
        worksheet = workbook.add_worksheet('金桐{}月份加班统计'.format(self.month))
        # Excel 格式
        # ============================================================
        # 表头格式：加粗,居中
        cell_format_head = workbook.add_format(
            {'text_wrap': True, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'fg_color': '#9900FF'})
        # 首列姓名格式
        cell_format_name = workbook.add_format(
            {'text_wrap': True, 'bold': True, 'align': 'center', 'valign': 'vcenter'})
        # 统计数字格式
        cell_format_number = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        # 日期格式：自动换行，列宽15，居中
        cell_format_date = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        worksheet.set_column('A:N', 15)
        # 边框实线
        workbook.add_format({'border': 1})
        # ============================================================
        worksheet_cols = 1
        # 表头信息
        table_head = [
            '姓名', '21点打卡次数', '23点打卡次数', '周末加班日期', '周末加班时长（小时）'
        ]
        for vn in range(len(table_head)):
            worksheet.write(0, vn, table_head[vn], cell_format_head)
        for name in result_data.keys():
            if name in self.notneed_person:
                continue
            worksheet.write(worksheet_cols, 0, name, cell_format_name)
            # 21点打卡次数
            times_of_21 = 0
            # 23点打卡次数
            times_of_23 = 0
            # 周末节假日加班日期及时长
            holiday_list = []
            holiday_time = []
            days = self.get_days()
            days2 = self.get_days(type=1)
            for date in days:
                date_result = result_data[name]['result'][date]
                times_of_21 += date_result.get('outtimes_21', 0)
                times_of_23 += date_result.get('outtimes_23', 0)
            for date2 in days2:
                if date2 in result_data[name]['result'].keys():
                    date_result = result_data[name]['result'][date2]
                    if 'holidayworktime' in date_result.keys():
                        holiday_list.append(date2)
                        holiday_time.append(str(date_result['holidayworktime']))
            if times_of_21 == 0 \
                    and times_of_23 == 0 \
                    and len(holiday_list) == 0:
                continue

            if times_of_21 != 0:
                worksheet.write(worksheet_cols, 1, times_of_21, cell_format_number)
            if times_of_23 != 0:
                worksheet.write(worksheet_cols, 2, times_of_23, cell_format_number)
            if holiday_list and holiday_time:
                worksheet.write(worksheet_cols, 3, ' '.join(holiday_list), cell_format_date)
                worksheet.write(worksheet_cols, 4, '\n'.join(holiday_time), cell_format_date)
            worksheet_cols += 1
        workbook.close()

    # write cache file
    def write_cache_file(self, type=11, cache_str=''):
        """
        :param type: 11 or 23 11层或者23层
        :param cache_str: 缓存数据
        :return:
        """
        math = "type_{}-".format(type)
        cache_str = cache_str
        try:
            if os.path.exists('cache.txt'):
                with open('cache.txt', 'r', encoding='utf-8') as r:
                    wlist = []
                    n = 0
                    for line in r.readlines():
                        if re.match("{}*".format(math), line.strip()):
                            n = 1
                        wlist.append(line.strip())
                    if n == 0:
                        wlist.append('{}{}'.format(math, cache_str))
                    else:
                        for i in wlist:
                            if re.match("{}*".format(math), i):
                                wlist[wlist.index(i)] = '{}{}'.format(math, cache_str)
                    # 删除空元素
                    for i in wlist:
                        if i == "":
                            wlist.remove(i)
            else:
                wlist = []
                wlist.append('{}{}'.format(math, cache_str))
        except Exception as e:
            logger.error(e)
        finally:
                with open('cache.txt', 'w+', encoding='utf-8') as w:
                    for line in wlist:
                        w.write(line + '\n')

    # excel head
    def tableHead(self):
        # 表头信息
        table_head = ['姓名', '上班未打卡日期', '上班未打卡次数',
                      '下班未打卡日期', '下班未打卡次数', '迟到日期', '迟到时间',
                      '早退日期', '早退时间']
        # 加班分析表头
        if self.workovertime:
            table_head += ['加班日期', '加班时长',
                           '21点打卡次数', '23点打卡次数',
                           '周末及节假日加班日期', '周末及节假日加班时长', '缺勤日期', '总工时(h)']
        else:
            table_head += ['缺勤日期', '总工时(h)']
        return table_head


if __name__ == '__main__':
    App = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = attendan.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # 设置默认值
    # 默认年、月份
    # 默认当前年
    ui.cyear.setValue(datetime.datetime.today().year)
    # 默认当前月
    ui.cmonth.setValue(datetime.datetime.today().month)
    ui.textEdit_2.setPlainText("元旦:2018-01-01 2018-01-03")
    ui.textEdit.setPlainText("佩奇,猪大")
    # -
    def logg(text):
        ui.textBrowser.append(text)

    def getconf():
        clist = {}
        clist['year'] = ui.cyear.text()
        clist['month'] = ui.cmonth.text()
        clist['utime'] = ui.utime.text()
        clist['dtime'] = ui.dtime.text()
        clist['outtime'] = ui.otime.text()
        # 判断是否需要分析加班
        if ui.checkBox.isChecked():
            clist['workovertime'] = True
        else:
            clist['workovertime'] = False
            # 获取区域
        if ui.radioButton.isChecked():
            clist['type'] = 11
        else:
            clist['type'] = 23
        hdays = ui.textEdit_2.toPlainText()
        clist['hdays'] = {}
        if hdays:
            try:
                for i1 in hdays.split(','):
                    if len(i1.split(':')[1].split()) == 2:
                        clist['hdays'][i1.split(':')[0]] = [i1.split(':')[1].split()[0], i1.split(':')[1].split()[1]]
                    else:
                        clist['hdays'][i1.split(':')[0]] = [i1.split(':')[1].split()[0]]
            except Exception as e:
                logg("Error: 节假日格式错误，未生效。{}".format(e))
                logger.error("Error: 节假日格式错误，未生效。{}".format(e))
                clist['hdays'] = {}
        nonotes = ui.textEdit.toPlainText()
        tmp_d2 = []
        if nonotes:
            for i2 in nonotes.split(','):
                tmp_d2.append(i2)
        clist['nonotes'] = tmp_d2
        return clist

    def Main():
        if ui.radioButton.isChecked():
            C.make_excel()
        else:
            C.make_excel_23()

    def auto_set():
        """
        自动获取免打卡人员,缓存数据,本地文件缓存
        :return:
        """
        if ui.radioButton.isChecked():
            m = 11
        else:
            m = 23
        math = 'type_{}-'.format(m)
        if not os.path.exists('cache.txt'):
            pass
        else:
            try:
                with open('cache.txt', 'r', encoding='utf-8') as f:
                    for line in f.readlines():
                        if re.match(math, line.strip()):
                            ui.textEdit.setPlainText(str(line.strip().split(math)[1]))
            except Exception as e:
                logger.error(e)
    C = attendance(filename=r'11层考勤.xls', filename23=r'23层考勤.xls')
    ui.textBrowser.setText('')
    auto_set()
    ui.radioButton.toggled.connect(auto_set)
    ui.pushButton.clicked.connect(Main)
    sys.exit(App.exec_())
