#!/usr/bin/python
#-*- encoding:utf-8 -*-

import tornado.ioloop
import tornado.web
import time
import os
import mail
import json
import re


class ChartHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("charts.html")


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('''
        文件上传接口url: /sendreport
        ''')
        items = ["Jia", "yi", "Bing"]
        self.render("charts.html", title="Mrk", items=items)

mail_to_lsit = [
    #"cdhmuer333@126.com",
    #"chendh@youme.im",
    #"qa@youme.im",
    #"fish@youme.im",
    "ci@youme.im",
    #"zhuhui@youme.im",
    #"lingguodong@youme.im",
    #"xiangyun@youme.im",
    #"jessie@youme.im",
    #"eason@youme.im",
    #"liuyang@youme.im",
    #"im@youme.im",
    #"rtc@youme.im"
]


class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./upload.html")

    def put(self):
        #print(self.request.body)
        file_metas = None
        upload_path = os.path.join(os.path.dirname(__file__), "datas")  # 文件的暂存路径
        try:
            file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
            #print(file_metas)
            #print self.request.files
        except KeyError:
            self.write({"errno": 1000, "msg": "Parameter error"})
            self.finish()

        try:
            for meta in file_metas:
                filename = meta['filename']
                #if re.search("report(.*)\.html$",filename):
                if re.search("\.html$", filename):
                    print("send")
                    sub = filename
                    #mail_content = meta['body'].replace("\\n", "\\r\\n", -1)
                    #print meta["body"]
                    mail.send_mail(mail_to_lsit, sub, meta['body'])
                    #sub = "%s_report" % filename

                path = os.path.join(upload_path, "perf_report")
                time_stamp = time.strftime("%Y%m%d_%H%M%S")
                save_file = "_".join([path, time_stamp])
                print(save_file)
                with open(save_file, 'wb+') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
                self.write({"errno": 0, "msg": "ok"})
        except IOError as e:
            #print(e)
            self.write({"errno": 2001, "msg": "Write Error"})


    def post(self):
        self.put()

settings = {
    "debug": True
}

class YoumeHandler(tornado.web.RequestHandler):
    def post(self):
        param = self.request.body
        #param = json.loads(param)
        #print(param)
       # print (type(self.request.headers))
        with open("set_talk_cc_callback.log", "wb+") as f:
            f.write(param)
            f.write(str(self.request.headers).decode('utf-8'))
        #print self.request.headers
        #self.write(self.request.headers)
        self.write('Ok')

app=tornado.web.Application([
    (r"/", MainHandler),
    (r"/sendreport",UploadFileHandler),
    (r"/charts", ChartHandler),
    (r"/testfortest", YoumeHandler)
], **settings)

if __name__ == '__main__':
    app.listen(8890)
    tornado.ioloop.IOLoop.instance().start()
