#!/usr/bin/env python
# encoding: utf-8
import datetime
import os
import shutil
import smtplib
import subprocess
import time
import zipfile
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
# 数据库用户名
from email.mime.text import MIMEText
from email.utils import formataddr
db_user = "root"
# 数据库密码
db_password = "keppel2016"
# 备份目录
backup_dir = "/home/keppel/data/bakup"
# backup_dir = "/var/test_backup"
# backup_prefix和backup_suffix分别为备份文件的前缀和后缀，如test_backup_2019-09-19-11则代表该文件是在2019年9月19日的11点时备份的
backup_prefix = "test_backup"
backup_suffix = "%Y-%m-%d-%H"
# 备份数据库列表
backup_databases = [
    "dikar_imp",
    "dikar_imp_ac",
    "dikar_imp_codegen",
    "dikar_imp_config",
    "dikar_imp_job",
    "dikar_imp_mp"
]
# 容器名
container_name = "mysql"
# 过期小时，定期删除50个小时前的备份文件
expire_hour = 350
email_from = 'keppelfei@sina.com'
email_passwd = '23b2df1aaad36b3d'
email_to = ['1136681198@qq.com']
# 获取备份文件名
def get_backup_filename():
    t = time.strftime(backup_suffix, time.localtime())
    return "%s_%s" % (backup_prefix, t)
def get_backup_path():
    return "%s%s%s" % (backup_dir, os.sep, get_backup_filename())
# 获取过期时间戳
def get_expire_time():
    t = datetime.datetime.now() - datetime.timedelta(hours=expire_hour)
    return int(time.mktime(t.timetuple()))
def create_dir(dir_path):
    # 如果目录存在则退出
    if os.path.exists(dir_path):
        return
    os.mkdir(dir_path)
cmd_template = "mysqldump -u{db_user} -p{db_password} {database} > {file_path}"
# 备份指定数据库
def backup_database(backup_path, database):
    file_path = os.sep.join([backup_path, "%s.sql" % database])
    d = {
        "db_user": db_user,
        "db_password": db_password,
        "database": database,
        "file_path": file_path,
    }
    cmd = cmd_template.format(**d)
    subprocess.call(cmd, shell=True)
def zip_dir(dir_path):
    file_path = '.'.join([dir_path, "zip"])
    if os.path.exists(file_path):
        os.remove(file_path)
    z = zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED)
    for root, directories, files in os.walk(dir_path):
        fpath = root.replace(dir_path, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in files:
            z.write(os.path.join(root, filename), fpath + filename)
    sendToEmail(file_path)
    z.close()
# 定时发送备份到指定邮箱中去
def sendToEmail(file_path):
    msg = MIMEMultipart()
    msg["Subject"] = "数据库备份"
    msg["From"] = formataddr(['大飞哥', email_from])
    msg["To"] = formataddr(['泰邦组员', ','.join(email_to)])
    # 附件部分
    with open(file_path, 'rb') as fin:
        data = fin.read()
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=' + file_path[12:])
        msg.attach(part)
    try:
        # 连接邮件服务器， 端口默认为25
        s = smtplib.SMTP('smtp.sina.com', timeout=30)
        # 发起登录
        s.login(email_from, email_passwd)
        # 发送邮件
        s.sendmail(email_from, email_to, msg.as_string())
        print('发送成功！')
        s.close()
    except:
        print('发送失败！')
# 备份数据库
def backup():
    backup_path = get_backup_path()
    try:
        create_dir(backup_path)
        for database in backup_databases:
            backup_database(backup_path, database)
        zip_dir(backup_path)
    finally:
        shutil.rmtree(backup_path)
# 清理过期备份文件
def clean():
    expire_time = get_expire_time()
    for root, directories, files in os.walk(backup_dir):
        for file in files:
            if not file.startswith(backup_prefix):
                continue
            if not file.endswith(".zip"):
                continue
            file_path = os.sep.join([root, file])
            t = os.path.getctime(file_path)
            if t < expire_time:
                os.remove(file_path)
if __name__ == "__main__":
    try:
        backup()
    finally:
        clean()