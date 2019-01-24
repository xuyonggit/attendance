gintong 考勤处理软件
===================
# attendance
## version - 0.0.4
        新增23层考勤处理功能
## version - 0.0.5
        增加一系列异常抓取抛出，新增使用说明书（考勤配置文件.xlsx中）
## version - 0.0.6
        新增GUI页面，一切操作均在页面执行
## version - 1.1.0
        新增：加班分析选择（可单独分析出勤数据也可额外选择分析加班数据-同一Excel）
        新增日志输出
        优化代码性能
## version - 1.1.1
        新增：人员总工时统计
        修改：默认考勤区域选择（由默认11层改为默认23层）
        备注：单次未打卡情况按照正常工时8小时计算相加；

# 软件截图：
![](https://github.com/xuyonggit/attendance/blob/latest/png/software.png)

# 环境安装
```
pip install -r requirefile
```

# 打包方式
```
python setup.py
```
