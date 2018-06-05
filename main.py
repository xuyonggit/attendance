# -*- coding:utf-8 -*-
import xlrd
import xlsxwriter
import datetime, time
import calendar
import os


class attendance():
    def __init__(self, conffilename='conffilename', filename='filename'):
        self.timeconf = ['上班时间', '下班时间', '迟到时间']
        self.up_downtime = {}  # 上下班时间，格式：{'下班时间': '18-00-00', '上班时间': '09-00-00'}
        self.holidays = {}  # 节假日设定，格式：{'清明': ['2018-04-05', '2018-04-06', '2018-04-07']}
        self.year = ""  # 考勤年
        self.month = ""  # 考勤数据月份
        self.notneed_person = []
        self.conffile = conffilename
        self.filename = filename

    def get_conf(self):
        # 获取配置：上下班时间
        workbook = xlrd.open_workbook(self.conffile)
        # 获取上下班时间配置
        worktimeconf = workbook.sheet_by_name('上下班时间')
        for cols in range(worktimeconf.nrows):
            if worktimeconf.cell_value(cols, 0) in self.timeconf:
                if worktimeconf.cell(cols, 1).ctype == 3:
                    date_value = xlrd.xldate_as_tuple(worktimeconf.cell_value(cols, 1), workbook.datemode)
                    datestr = datetime.time(*date_value[3:5]).strftime('%H:%M')
                    self.up_downtime[worktimeconf.cell_value(cols, 0)] = datestr
        # print(self.up_downtime)
        # 获取配置：节假日设定
        workholidaysconf = workbook.sheet_by_name('节假日设定')
        for rows in range(workholidaysconf.nrows):
            if workholidaysconf.cell(rows, 1).ctype == 3 and workholidaysconf.cell(rows, 2).ctype == 3:
                temp_list_holidays = []
                # 获取假期起始日期
                date_start_value = xlrd.xldate_as_tuple(workholidaysconf.cell_value(rows, 1), workbook.datemode)
                startdate = datetime.datetime.strptime(datetime.date(*date_start_value[:3]).strftime('%Y-%m-%d'),
                                                       "%Y-%m-%d")
                # 获取假期结束日期
                date_end_value = xlrd.xldate_as_tuple(workholidaysconf.cell_value(rows, 2), workbook.datemode)
                enddate = datetime.datetime.strptime(datetime.date(*date_end_value[:3]).strftime('%Y-%m-%d'),
                                                     "%Y-%m-%d")
                while startdate < enddate:
                    date_str = startdate.strftime('%Y-%m-%d')
                    temp_list_holidays.append(date_str)
                    startdate += datetime.timedelta(days=1)
                self.holidays[workholidaysconf.cell_value(rows, 0)] = temp_list_holidays
        # print(self.holidays)
        # 获取考勤数据月份
        workotherconf = workbook.sheet_by_name('其他配置')
        for rows in range(workotherconf.nrows):
            if workotherconf.cell_value(rows, 0) == '考勤月份':
                self.month = int(workotherconf.cell_value(rows, 1))
            if workotherconf.cell_value(rows, 0) == '考勤年':
                self.year = int(workotherconf.cell_value(rows, 1))
            # 获取免打卡人员
            if workotherconf.cell_value(rows, 0) == u'免打卡人员':
                self.notneed_person = workotherconf.cell_value(rows, 1).split('|')

    # 获取当月所有工作日
    def get_days(self, type=0):
        """
        :param type:0  所有工作日 1 所有周末以及节假日
        :return: list
        """
        type = type
        days = []  # 当月所有日期，格式：['2018-03-01', ... '2018-03-31']
        self.get_conf()
        temp_list_holiday_1 = []
        monthrange = calendar.monthrange(self.year, self.month)
        if self.month < 10:
            self.month = "0{}".format(self.month)
        # 集中假期日期
        for holiday in self.holidays.values():
            for day in holiday:
                temp_list_holiday_1.append(day)
        if type == 0:
            for m in range(1, monthrange[1] + 1):
                if m < 10:
                    m = "0{}".format(m)
                    mon = "{}-{}-{}".format(self.year, self.month, m)
                else:
                    mon = "{}-{}-{}".format(self.year, self.month, m)
                if mon not in temp_list_holiday_1 \
                        and 0 < int(time.strftime('%w', time.strptime(mon, '%Y-%m-%d'))) < 6:
                    days.append(mon)
        elif type == 1:
            for m in range(1, monthrange[1] + 1):
                if m < 10:
                    m = "0{}".format(m)
                    mon = "{}-{}-{}".format(self.year, self.month, m)
                else:
                    mon = "{}-{}-{}".format(self.year, self.month, m)
                if mon in temp_list_holiday_1 \
                        or int(time.strftime('%w', time.strptime(mon, '%Y-%m-%d'))) == 6 \
                        or int(time.strftime('%w', time.strptime(mon, '%Y-%m-%d'))) == 0:
                    days.append(mon)
        else:
            raise Exception
        return days

    def get_data(self):
        temp_list_data_1 = []
        temp_dic_data_1 = {}
        # open data file
        workbook = xlrd.open_workbook(self.filename, encoding_override='gbk')
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
                                                                                             '%H:%M') < datetime.datetime.strptime(
                        '12:00', '%H:%M'):
                    if not one:
                        one = datalist[n]
                        continue
                if datetime.datetime.strptime('17:00', '%H:%M') <= datetime.datetime.strptime(datalist[n],
                                                                                              '%H:%M') < datetime.datetime.strptime(
                        '23:59', '%H:%M'):
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
    def make_data(self):
        temp_dict_data_2 = {}
        data = self.get_data()
        days_work = self.get_days()
        days_out = self.get_days(type=1)
        self.get_conf()
        up_time = self.up_downtime.get('上班时间')
        down_time = self.up_downtime.get('下班时间')
        out_time = self.up_downtime.get('迟到时间')
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
                            if datetime.datetime.strptime(starttime, '%H:%M') > datetime.datetime.strptime(out_time,
                                                                                                           '%H:%M'):
                                lasttime = str((datetime.datetime.strptime(starttime,
                                                                           '%H:%M') - datetime.datetime.strptime(
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
                        elif 'one' not in alltime.keys() and 'end' in alltime.keys():
                            values['result'][notedate]['uptime'] = '未打卡'
                            values['result'][notedate]['downtime'] = alltime['end']
                        # 缺勤
                        else:
                            values['result'][notedate]['uptime'] = '未打卡'
                            values['result'][notedate]['downtime'] = '未打卡'
                            values['result'][notedate]['losttime'] = 8
                        # 加班
                        if 'out' in alltime.keys():
                            values['result'][notedate]['outtime'] = datetime.datetime.strptime(alltime['out'],
                                                                                               '%H:%M') - datetime.datetime.strptime(
                                '21:00', '%H:%M')
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
                        # print(values['date'][notedate2], alltime)
                        outwork_time = datetime.datetime.strptime(alltime['end'], '%H:%M') - \
                                       datetime.datetime.strptime(alltime['one'], '%H:%M')
                        values['result'][notedate2]['holidayworktime'] = outwork_time
        return data

    # create excel table
    def make_excel(self):
        self.get_conf()
        if not os.path.exists('result'):
            os.mkdir('result')
        else:
            if os.path.exists(os.path.join('result', '金桐{}月份考勤.xlsx'.format(self.month))):
                os.remove(os.path.join('result', '金桐{}月份考勤.xlsx'.format(self.month)))
        result_data = self.make_data()
        # create excel table
        workbook = xlsxwriter.Workbook(os.path.join('result', '金桐{}月份考勤.xlsx'.format(self.month)))
        # create sheet
        worksheet = workbook.add_worksheet('金桐{}月份考勤'.format(self.month))
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
        worksheet.set_column('A:N', 12)
        # 边框实线
        workbook.add_format({'border': 1})
        # ============================================================
        worksheet_cols = 1
        # 表头信息
        table_head = ['姓名', '上班未打卡日期', '上班未打卡次数',
                      '下班未打卡日期', '下班未打卡次数', '迟到日期', '迟到时间',
                      '早退日期', '早退时间', '加班日期', '加班时长',
                      '缺勤日期', '周末及节假日加班日期', '周末及节假日加班时长', '备注', '签字']
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
            # 周末节假日加班日期及时长
            holiday_list = []
            holiday_time = []
            days2 = self.get_days(type=1)
            days = self.get_days()
            for date in days:
                date_result = result_data[name]['result'][date]
                print(date_result)
                if date_result['uptime'] == '未打卡' and date_result['downtime'] != '未打卡':
                    no_uptime_list.append(date)
                    no_uptime_num += 1
                if date_result['downtime'] == '未打卡' and date_result['uptime'] != '未打卡':
                    no_downtime_list.append(date)
                    no_downtime_num += 1
                if date_result['losttime'] == 8:
                    passwork_list.append(date)
                if date_result['latertime']:
                    lastdate_list.append(date)
                    lastdate_time.append(str(date_result['latertime']))
                if date_result['befortime']:
                    before_list.append(date)
                    before_time.append(str(date_result['befortime']))
                if 'outtime' in date_result.keys():
                    outtime_list.append(date)
                    outtime_time.append(str(date_result['outtime']))
                lostwork_hour += date_result['losttime']
            for date2 in days2:
                if date2 in result_data[name]['result'].keys():
                    date_result = result_data[name]['result'][date2]
                    if 'holidayworktime' in date_result.keys():
                        holiday_list.append(date2)
                        holiday_time.append(str(date_result['holidayworktime']))

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
            if outtime_list and outtime_time:
                worksheet.write(worksheet_cols, 9, ' '.join(outtime_list), cell_format_date)
                worksheet.write(worksheet_cols, 10, '\n'.join(outtime_time), cell_format_date)
            if passwork_list:
                worksheet.write(worksheet_cols, 11, ' '.join(passwork_list), cell_format_date)
            if holiday_list and holiday_time:
                worksheet.write(worksheet_cols, 12, ' '.join(holiday_list), cell_format_date)
                worksheet.write(worksheet_cols, 13, '\n'.join(holiday_time), cell_format_date)
            worksheet_cols += 1
        workbook.close()


if __name__ == '__main__':
    C = attendance(conffilename='考勤配置文件.xlsx', filename=r'考勤.xls')
    C.make_excel()
