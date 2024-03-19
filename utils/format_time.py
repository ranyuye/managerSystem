import datetime
import functools
import os
import pytz


def set_timezone(timezoneName: str):
    """
    设置并返回指定的时区对象。

    :param timezoneName: 时区名称，字符串类型，例如 'Asia/Shanghai'。
    :return: pytz时区对象。
    :raises ValueError: 当指定的时区名称无效时抛出。
    """
    try:
        timezone = pytz.timezone(timezone_name)
    except pytz.UnknownTimeZoneError:
        raise ValueError(f"无效的时区名称: {timezone_name}")
    return timezone


# 通过环境变量获取时区名称，回退到默认值（Asia/Shanghai）如果环境变量未设置。
timezone_name = os.getenv("APP_TIMEZONE", 'Asia/Shanghai')
pytz_time = set_timezone(timezone_name)
time_zone = pytz_time

# 创建一个部分函数，用于获取带时区的当前时间。
now = functools.partial(datetime.datetime.now, tz=pytz_time)

# 示例：打印当前时间
try:
    print(now())
except Exception as e:
    print(f"获取当前时间时发生错误: {e}")
