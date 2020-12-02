# encoding: utf-8
import os
import smtplib
import zipfile
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# 数据库用户名
from email.utils import formataddr

email_from = 'keppelfei@sina.com'
email_passwd = '23b2df1aaad36b3d'
# email_to = ['keppelfei@sina.com', '894478374@qq.com']
email_to = ['1136681198@qq.com']


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
    z.close()
    
    sendToEmail(file_path)


# 定时发送备份到指定邮箱中去
def sendToEmail(file_path):
    msg = MIMEMultipart()
    msg["Subject"] = Header("数据备份", 'utf-8')
    msg["From"] = formataddr(['大飞哥', email_from])
    msg["To"] = formataddr(['泰邦组员', ','.join(email_to)])
    # 附件部分
    with open(file_path, 'rb') as fin:
        data = fin.read()
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(data)
        # 把附件编码
        encoders.encode_base64(part)
        
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(file_path))
        msg.attach(part)
    try:
        # 连接邮件服务器， 端口默认为25
        s = smtplib.SMTP_SSL('smtp.sina.com', timeout=30)
        # 发起登录
        s.login(email_from, email_passwd)
        # 发送邮件
        s.sendmail(email_from, email_to, msg.as_string())
        print('发送成功！')
        s.quit()
    except:
        print('发送失败！')


if __name__ == "__main__":
    zip_dir("/root/zhangming/work_bash")
