#! python3
# -*- coding: utf-8 -*-

"""
@Time    : 2017/9/1 16:59
@Author  : typhoon
@Site    : 
@File    : timing.py
@Software: PyCharm
@desc    :
"""
import time, os, sched

# 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
# 第二个参数以某种人为的方式衡量时间
schedule = sched.scheduler(time.time, time.sleep)


def perform_command(cmd, inc):
    os.system(cmd)
    schedule.enter(inc, 0, perform_command, (cmd, inc))


def timming_exe(cmd, inc=60):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()


# print("show time after 10 seconds:")
# timming_exe("echo %time%", 1)

now = time.time()
local_time = time.localtime()
print(now)
print(local_time)
print(local_time[2])
print(local_time[2] == 1)

is_time_do_something = True
if time.localtime()[2] == 1:
    if is_time_do_something:
        # dosomething
        time.sleep()
    is_time_do_something = False
else:
    is_time_do_something = True
