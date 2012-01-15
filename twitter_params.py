#!/usr/bin/env python
#coding: utf8

import urllib
import datetime

three_days_jp = urllib.quote_plus('(本日+OR+今日+OR+明日+OR+明後日)')
event_jp = urllib.quote_plus('(発表+OR+開催+OR+実施+OR+参加+OR+受付+OR+会場+OR+開場+OR+申し込み+OR+展示+OR+開演+OR+主催)')

def days_from_today(n):
    '''generate paramaters n days from today.'''
    s = ''
    today = datetime.datetime.today()
    return days_from_day(today, n)

def days_from_today_jp(n):
    '''generate paramaters n days from today Japanese.'''
    s = ''
    today = datetime.datetime.today()
    return days_from_day_jp(today, n)

def days_from_day_jp(d, n):
    '''generate paramaters n days from a day Japanese.'''
    s = ''
    for i in range(n):
        d_ = d + datetime.timedelta(i)
        s += '%s月%s日+OR+' % (d_.month, d_.day)
    return urllib.quote_plus(s[:-4])

def days_from_day(d, n):
    '''generate paramaters n days from a day.'''
    s = ''
    for i in range(n):
        d_ = d + datetime.timedelta(i)
        s += '%s/%s+OR+' % (d_.month, d_.day)
    return urllib.quote_plus(s[:-4])
    
dft = days_from_today
dftj = days_from_today_jp
dfd = days_from_day
dfdj = days_from_day_jp