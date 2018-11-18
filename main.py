#-*-coding=utf-8-*-
from spider import spider
from pdfSolve import dirtopdf, dir_merge_pdf
from sendToKindle import sendEMAIL
import os
import shutil
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datafmt='%a, %d %b %Y %H:%M:%S',
                    filename='/var/log/diary.txt',
                    filemode='a')

def main():
    print('现在是：' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #爬取
    print '开始爬取'
    web = spider()
    web.start()
    print '爬取完成'
    #转pdf
    print '开始转换'
    for title in web.titleSet:
        dirtopdf(title)
        dir_merge_pdf(title)
    print '转换完成'
    #发送到Kindle
    print '开始发送'
    files = os.listdir("pdf")
    for file in files:
        sendEMAIL(file)
    print '发送完成'

    print '开始清理'
    for title in web.titleSet:
        shutil.rmtree(title)
    for file in os.listdir("pdf"):
        os.remove("pdf/" + file)
    print '清理完成'

    print 'ALL DONE!'

if __name__ == '__main__':
    try:
        scheduler = BlockingScheduler()
        scheduler.add_job(main, 'cron', day_of_week='0-6', hour=10, minute=0)
        scheduler.start()
    except Exception as e:
        scheduler.start()
    #main()
