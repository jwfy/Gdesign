#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-17
# e-mail: jwfy0902@foxmail.com

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Header import Header

from jinja2 import Template
"""
    docs:https://zh.wikipedia.org/wiki/%E5%A4%9A%E7%94%A8%E9%80%94%E4%BA%92%E8%81%AF%E7%B6%B2%E9%83%B5%E4%BB%B6%E6%93%B4%E5%B1%95
"""
Host = 'smtp.qq.com'
Port = '25'
Sender = 'jwfy0902@foxmail.com'
From = 'DMovie 找回密码<jwfy0902@foxmail.com>'
Password = 'syb0902+-*/.CHQQ'


def send_email(html, text, To, title='找回密码', kwargs={}):
    """
    邮件发送
    参数说明：
    html:发送的html文件
    text:发送的html文件对应的txt文件
    title:发送邮件的标题
    to:发送者的基本信息
    """
    Content = {}
    for k,v in kwargs.iteritems():
        Content[k] = unicode(v.decode('utf-8'))
    msg = MIMEMultipart('alternative')
    msg["Subject"] = title
    msg["From"] = From
    msg["To"] = To
    html = open(html).read().decode('utf-8')
    text = open(text).read().decode('utf-8')
    tp1 = Template(html)
    html = tp1.render(Content)
    tp2 = Template(text)
    text = tp2.render(Content)
    _html = MIMEText(html, 'html', 'utf-8')
    _text = MIMEText(text, 'plain', 'utf-8')
    msg.attach(_html)
    msg.attach(_text)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(Host, Port)
        smtp.login(Sender, Password)
        smtp.sendmail(From, To, msg.as_string())
        smtp.quit()
        print '发送成'
        return 1, "邮件发送成功"
    except Exception as e:
        print 0, e


if __name__ == "__main__":
    html = 'email_template/example.html'   
    text = 'email_template/example.txt'    
    title = "Test"                         
    to = 'rd@lanrenzhoumo.com'    
    k = {'name':'你好'}
    send_message(html, text, to, title, k)
