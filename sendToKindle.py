#-*-coding=utf-8*-*
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.Header import Header

def sendEMAIL(filename):
    from_address = "1808025091@qq.com"
    password = "cbwojmmcoscvcjhg"
    # smtp 服务器地址
    smtp_address = "smtp.qq.com"

    # 目标地址
    to_address = "1443061377@kindle.cn"
    #to_address = "houleile@mail.ustc.edu.cn"
    try:
        msg = MIMEMultipart()
        msg['From']= formataddr(["sender",from_address])   #括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']= formataddr(["receiver",to_address])   #括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = '黑白漫画推送'.decode('utf-8').encode('gbk') #邮件的主题，也可以说是标题

        #邮件正文内容
        msg_text = MIMEText('This is a email test send by python.', 'plain', 'utf-8')
        msg.attach(msg_text)

        # 邮件附件
        print('正在发送：' + filename)
        msg_attachment = MIMEApplication(open('pdf/' + filename , 'rb').read())
        msg_attachment.add_header('Content-Disposition', 'attachment', filename=str(Header(filename.decode('utf-8'), 'gb2312')))
        msg.attach(msg_attachment)
        print('连接服务器')
        server = smtplib.SMTP(smtp_address, 587)
        print '登录'
        server.starttls()
        server.login(from_address, password)
        print '开始发送'
        server.sendmail(from_address, [to_address], msg.as_string())
        server.quit()
        print('邮件发送成功！')
    except Exception as e:
        if("535" in str(e)):
            sendEMAIL(filename)
        else:
            print("There is a exception:", e)

if __name__ == '__main__':
    sendEMAIL('天黑请睁眼  所谓艺术的灵魂.pdf')