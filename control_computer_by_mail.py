# -*- coding: utf-8 -*-
import imaplib
import email
import os
import time
from email.header import decode_header


class EmailControl(object):
    """通过邮件控制你的电脑"""

    def __init__(self):
        self.host = "imap.qq.com"  # imap服务器地址
        self.username = "xxxxxxxxx@qq.com"  # 用户名
        self.password = "xxxxxxxxxxxx"  # 授权码
        self.email_count = 0  # 信箱中可以查看的邮件数目
        self._is_first = True  # 是否第一次执行程序
        self.old_email_count = 0  # 前一次信箱中可以查看的邮件数目
        self._first_login = True  # 是否第一次登陆

    def login(self):
        serv = imaplib.IMAP4_SSL(self.host, 993)  # 链接服务器
        serv.login(self.username, self.password)  # 登陆
        serv.select()  # 选择邮件文件夹, 默认为邮件收信箱
        return serv

    def hasNew(self, serv):
        '''检查是否有新邮件'''
        typ, data = serv.search(None, 'ALL')  # 搜索电子邮件
        newlist = data[0].split()  # 返回邮件标号列表
        self.email_count = len(newlist)  # 获取信箱中邮件数量
        if self.email_count > self.old_email_count:
            self.old_email_count = self.email_count
            return data, True
        else:
            return '', False

    def get_mail(self, serv, data):
        '''获取邮件主题信息'''
        newlist = data[0].split()
        typ, data = serv.fetch(newlist[-1], '(RFC822)')
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        subject_str = msg.get('Subject')
        subject, charset = decode_header(subject_str)[0]
        if charset:
            subject = subject.decode(charset)

        return subject  # 返回邮件主题内容, 及命令内容

    def comm(self, command):
        '''执行命令'''
        if command.startswith("cmd:"):
            print('正在执行命令:　%s' % command[5:])
            os.system(command[5:])

    def run(self):
        while True:
            try:
                if self._first_login:
                    serv = self.login()
                    self._first_login = False
                data, new = self.hasNew(serv)
                if new:
                    if self._is_first:
                        self._is_first = False
                    else:
                        command = self.get_mail(serv, data)
                        self.comm(command)
            except Exception as e:
                print(e)
            time.sleep(5)
            
if __name__ == '__main__':
    control = EmailControl()
    control.run()
