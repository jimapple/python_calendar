import calendar
import datetime
from dateutil.parser import parse
from sqlalchemy.sql import sqltypes
from sqlalchemy.sql.functions import AnsiFunction

'''
返回指定年和月的第一天是星期几，这个月总共有多少天。
例如
(6,31)
'''


def get_month_range(year, month):
    return calendar.monthrange(year, month)

'''
返回这个月所有周包含的日期
例如
[
[0, 0, 0, 0, 0, 0, 1],
[2, 3, 4, 5, 6, 7, 8],
[9, 10, 11, 12, 13, 14, 15],
[16, 17, 18, 19, 20, 21, 22],
[23, 24, 25, 26, 27, 28, 29],
[30, 31, 0, 0, 0, 0, 0]
]
'''


def get_month_calendar(year, month):
    return calendar.monthcalendar(year, month)

'''
获取某个月包含的所有周
例如
['48', '49', '50', '51', '52']
'''


def get_weeks_from_month(year, month):
    day_min = 1
    day_max = [31, 29 if calendar.isleap(int(year)) else 28,
               31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    date_min_str = "{0}-{1}-{2}".format(year, month, day_min)
    date_max_str = "{0}-{1}-{2}".format(year, month, day_max[int(month) - 1])

    date_time_week_min = datetime.datetime.strptime(date_min_str, "%Y-%m-%d").strftime('%U')
    date_time_week_max = datetime.datetime.strptime(date_max_str, "%Y-%m-%d").strftime('%U')

    return [i for i in range(int(date_time_week_min), int(date_time_week_max) + 1)]


'''
传参数为某一天
获取该天所在月包含的所有周
例如
['48', '49', '50', '51', '52']
'''


def get_week_from_month(now_day):
    year = datetime.datetime.strptime(now_day, "%Y-%m-%d").strftime("%Y")
    month = datetime.datetime.strptime(now_day, "%Y-%m-%d").strftime("%m")
    day_min = 1
    day_max = [31, 29 if calendar.isleap(int(year)) else 28,
               31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    date_min_str = "{0}-{1}-{2}".format(year, month, day_min)
    date_max_str = "{0}-{1}-{2}".format(year, month, day_max[int(month) - 1])

    date_time_week_min = datetime.datetime.strptime(date_min_str, "%Y-%m-%d").strftime('%U')
    date_time_week_max = datetime.datetime.strptime(date_max_str, "%Y-%m-%d").strftime('%U')

    return [i for i in range(int(date_time_week_min), int(date_time_week_max) + 1)]

'''
传参数为某一天
获取该天所在季度或者上季度包含的所有周
例如
[40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]
'''


def get_week_from_quarter(now_day, is_this_quarter=None):
    year = datetime.datetime.strptime(now_day, "%Y-%m-%d").strftime('%Y')
    month = datetime.datetime.strptime(now_day, "%Y-%m-%d").strftime('%m')

    if is_this_quarter == 1:
        month_tuple = get_month_from_quarter(now_day)
    else:
        if int(month)-3 <= 0:
            month = 12
            year = int(year) - 1
        now_day = '{0}-{1}-{2}'.format(year, int(month)-3, 1)
        month_tuple = get_month_from_quarter(now_day)
    quarter_set = set()
    for month in month_tuple:
        for week in get_weeks_from_month(year, month):
            quarter_set.add(week)

    return {year: list(quarter_set)}

'''
获取从开始月到结束月包含的所有周
例如
{1: ['01', '02', '03', '04', '05'], 2: ['05', '06', '07', '08']}
'''


def get_weeks_from_range_month(year, start, end):
    if start is not None:
        start = int(start)
    else:
        return 0
    if end is not None:
        end = int(end)
    else:
        return 0
    weeks_in_months = {}
    for month in range(start, end + 1):
        weeks_in_months[month] = get_weeks_from_month(year, month)
    return weeks_in_months

'''
传入向前几年，向后几年两个参数，返回这些年的列表
例如
[2016, 2017, 2018, 2019]
'''


def generate_year_list(x_offset, y_offset, year):
    init_year = year - x_offset
    last_year = year + y_offset
    year_list = []
    for i in range(init_year, last_year + 1):
        year_list.append(i)
    return year_list

'''
传入向前几年，向后几年两个参数，返回这些年的列表
以及这些年的序号，形成一个元祖
例如
[(1, 2016), (2, 2017), (3, 2018), (4, 2019)]
'''


def generate_year_select(x_offset, y_offset, year=int(datetime.datetime.now().strftime("%Y"))):
    years = generate_year_list(x_offset, y_offset, year)
    ret = []
    for i in range(1, len(years) + 1):
        tt = []
        tt.append(i)
        tt.append(years[i - 1])
        ret.append(tuple(tt))
    return ret

'''
传入例如2017-04-23，2019-02-22
输出
{
2017: [4, 5, 6, 7, 8, 9, 10, 11, 12],
2018: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
2019: [1, 2]
}
'''


def get_ym_dict(start, end):
    if start == "" or start is None:
        return {}
    if end == "" or end is None:
        return {}

    start_year = datetime.datetime.strptime(start, "%Y-%m-%d").year
    end_year = datetime.datetime.strptime(end, "%Y-%m-%d").year
    start_month = datetime.datetime.strptime(start, "%Y-%m-%d").month
    end_month = datetime.datetime.strptime(end, "%Y-%m-%d").month

    rslt_dict = {}

    if start_year < end_year:
        years = [i for i in range(start_year, end_year + 1)]
    elif start_year == end_year:
        years = [start]
    else:
        years = []

    if len(years) == 1:
        rslt_dict[start_year] = [i for i in range(start_month, end_month + 1)]
    elif len(years) == 2:
        rslt_dict[start_year] = [i for i in range(start_month, 13)]
        rslt_dict[end_year] = [i for i in range(1, end_month + 1)]
    else:
        rslt_dict[start_year] = [i for i in range(start_month, 13)]
        for left_year in range(start_year + 1, end_year):
            rslt_dict[left_year] = [i for i in range(1, 13)]
        rslt_dict[end_year] = [i for i in range(1, end_month + 1)]

    return rslt_dict

'''
计算当前月所包含的周以及该周下的日期
'''


def get_days_from_this_week():
    now = datetime.datetime.now()
    week_day = now.weekday()
    end = int(now.strftime("%W"))

    a = {}
    weeklist = get_weeks_from_month(now.year, now.month)

    print(weeklist)
    weekpare = get_month_calendar(now.year, now.month)
    for i in range(0, len(weeklist)):
        a.setdefault(weeklist[i], weekpare[i])
    b = {}
    for (k, v) in sorted(a.items(), key=lambda a: a[0], reverse=False):
        b[k] = v

    print(end)
    print(b.get(str(end))[week_day])
    week_list = []

    for i in b.get(str(end)):
        if i == 0:
            pass
        else:
            week_list.append(i)

    return b

'''
通过某天计算该天所在的年，月，日
'''


def get_week_month(day):
    week = day.strftime("%W")
    month = day.strftime("%m")
    year = day.strftime("%Y")

    return week, month, year

'''
传入某一天，通过该天所在季度
返回该季度包含哪几个月
'''


def get_month_from_quarter(day):
    month = int(datetime.datetime.strptime(day, "%Y-%m-%d").strftime('%m'))
    if month in (1, 2, 3):
        return 1, 2, 3

    if month in (4, 5, 6):
        return 4, 5, 6

    if month in (7, 8, 9):
        return 7, 8, 9

    if month in (10, 11, 12):
        return 10, 11, 12

'''
获取两段时间内所包含的周
'''


def get_weeks_from_range_day(start_date, end_date):
    start_date_datetime = parse(start_date)
    end_date_datetime = parse(end_date)

    start_week = start_date_datetime.strftime("%W")
    start_year = start_date_datetime.strftime("%Y")
    end_week = end_date_datetime.strftime("%W")
    end_year = end_date_datetime.strftime("%Y")
    week_dict = {}

    if int(start_year) != int(end_year):
        start_year_week_list = []
        end_year_week_list = []
        week = int(datetime.datetime.strptime(start_year+'-12-31', '%Y-%m-%d').strftime("%W"))

        for i in range(int(start_week), int(week)+1):
            start_year_week_list.append(i)
        week_dict[start_year] = start_year_week_list
        for i in range(1, int(end_week)+1):
            end_year_week_list.append(i)
        week_dict[end_year] = end_year_week_list
    else:
        week_dict[start_year] = [j for j in range(int(start_week), int(end_week)+1)]

    return week_dict


'''
传入日期和(week或者month)
# 如果是以周为时间维度，把这个日期转为该日期所在周的第一天的日期(例如：2017-11-30 转后：2017-11-27)
# 如果是以月为时间维度，把这个日期转为该日期所在周的第一天的日期(例如：2017-11-30 转后：2017-11-01)
'''


class Date2Week(AnsiFunction):
    type = sqltypes.Date

    def __init__(self, formate_date, type_name):
        self.formate_date = formate_date
        self.type_name = type_name
        super(Date2Week, self).__init__()

    def date_to_date(self):
        self.formate_date = datetime.datetime.strptime(self.formate_date, '%Y-%m-%d')
        print(type(self.formate_date))
        # 如果是以周为时间维度
        if self.type_name == 'week':
            # 把日期转为年和周(例如:2017-11-27 转为年和周:201748)
            year_day = '%d%d' % (self.formate_date.isocalendar()[0], self.formate_date.isocalendar()[1])
            d = year_day[0:4] + '-W' + year_day[4:]
            r = datetime.datetime.strptime(d + '-' + str(1), "%Y-W%W-%w")
            return r.strftime('%Y-%m-%d')
        # 如果是以月为时间维度
        elif self.type_name == 'month':
            return self.formate_date.strftime('%Y-%m-%d')[0:8]+'01'

'''
通过年和周来获取此周所包含的日期
'''


def get_week_first_day(year, week):
    year_str = year  # 取到年份
    week_str = week  # 取到周
    tuesday = None
    wednesday = None
    thursday = None
    friday = None
    saturday = None
    sunday = None
    if int(week_str) >= 53:
        monday = "Error,Week Num greater than 53!"
    else:
        year_start_str = year_str + '0101'  # 当年第一天
        year_start = datetime.datetime.strptime(year_start_str, '%Y%m%d')  # 格式化为日期格式
        year_start_calendar_msg = year_start.isocalendar()  # 当年第一天的周信息
        year_start_weekday = year_start_calendar_msg[2]
        year_start_year = year_start_calendar_msg[0]
        if year_start_year < int(year_str):
            day_de_1 = (8 - int(year_start_weekday)) + (int(week_str) - 1) * 7
            day_de_2 = (8 - int(year_start_weekday)+1) + (int(week_str) - 1) * 7
            day_de_3 = (8 - int(year_start_weekday)+2) + (int(week_str) - 1) * 7
            day_de_4 = (8 - int(year_start_weekday)+3) + (int(week_str) - 1) * 7
            day_de_5 = (8 - int(year_start_weekday)+4) + (int(week_str) - 1) * 7
            day_de_6 = (8 - int(year_start_weekday)+5) + (int(week_str) - 1) * 7
            day_de_7 = (8 - int(year_start_weekday)+6) + (int(week_str) - 1) * 7
        else:
            day_de_1 = (8 - int(year_start_weekday)) + (int(week_str) - 2) * 7
            day_de_2 = (8 - int(year_start_weekday)+1) + (int(week_str) - 2) * 7
            day_de_3 = (8 - int(year_start_weekday)+2) + (int(week_str) - 2) * 7
            day_de_4 = (8 - int(year_start_weekday)+3) + (int(week_str) - 2) * 7
            day_de_5 = (8 - int(year_start_weekday)+4) + (int(week_str) - 2) * 7
            day_de_6 = (8 - int(year_start_weekday)+5) + (int(week_str) - 2) * 7
            day_de_7 = (8 - int(year_start_weekday)+6) + (int(week_str) - 2) * 7

        monday = (year_start + datetime.timedelta(days=day_de_1)).date()
        tuesday = (year_start + datetime.timedelta(days=day_de_2)).date()
        wednesday = (year_start + datetime.timedelta(days=day_de_3)).date()
        thursday = (year_start + datetime.timedelta(days=day_de_4)).date()
        friday = (year_start + datetime.timedelta(days=day_de_5)).date()
        saturday = (year_start + datetime.timedelta(days=day_de_6)).date()
        sunday = (year_start + datetime.timedelta(days=day_de_7)).date()

    return monday, tuesday, wednesday, thursday, friday, saturday, sunday


def main():
    year = 2017
    month = 1

    print('#' * 50)
    # print(get_month_range(year, month))
    # print(get_month_calendar(year, month))
    # print(get_week_from_quarter('2017-12-20'))
    print(get_weeks_from_range_day('2016-08-04','2017-06-02'))
    # print(get_weeks_from_range_month(2017, 1, 2))
    # print(generate_year_select(1,2))
    # print(get_month_range(2017,11))
    # print(get_ym_dict('2017-04-23', '2019-02-22'))
    # start = 1
    # end = 2
    # year = 2015
    # for i in range(start, end+1):
    #    [print(a) for a in get_weeks_from_month(year,i)]
    # print(get_week_month(parse("2017-12-21 14:15:00")))
    # date = Date2Week('2017-12-20', 'week')
    # print(get_week_first_day('2017', '1'))
    # print(get_month_from_quarter('4'))
    # print(get_weeks_from_range_day('2017-01-04', '2017-04-08'))

if __name__ == '__main__':
    main()


