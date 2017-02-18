# -*- coding:utf-8 -*- 
import os   #Python的标准库中的os模块包含普遍的操作系统功能  
import re   #引入正则表达式对象  
import urllib   #用于对URL进行编解码  
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  #导入HTTP处理相关的模块  
from SocketServer import TCPServer, StreamRequestHandler  
  
#自定义处理程序，用于处理HTTP请求  
class MainHTTPHandler(BaseHTTPRequestHandler):  
    #处理GET请求  
    def do_POST(self):  
        #页面输出模板字符串  
        templateStr ="OK"
      
      
        # 将正则表达式编译成Pattern对象  
        pattern1 = re.compile(r'/handler\?cmd=([^\&]+)$') 
        pattern2 = re.compile(r'/handler\?cmd=([^\&]+)\&url=([^\&]+)$')   
        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None  
        match1 = pattern1.match(self.path)  
        match2 = pattern2.match(self.path);
        cmd = ''  
        url = ''
        inputFilename="input.png";
        outputFilename="output.png";
        if match1 or match2:  
            # 使用Match获得分组信息  
            if match1:
                cmd = urllib.unquote(match1.group(1))
            if match2:
                cmd = urllib.unquote(match2.group(1))
                url = urllib.unquote(match2.group(2))
            print("cmd:"+cmd+",url:"+url);
            
            # 把url或是body中的图片数据保存到本地。
            if url!='':
                urllib.urlretrieve(url, inputFilename);  
            else :
                fd = open(inputFilename, 'wb') 
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len) 
                try:
                    fd.write(post_body)  
                finally:
                    fd.close()  
            if os.path.exists(inputFilename):
                if(os.path.exists(outputFilename)):
                    os.remove(outputFilename);
                os.system("pngquant "+inputFilename+" -o "+outputFilename)
                
                self.protocal_version = 'HTTP/1.1'  #设置协议版本  
                self.send_response(200) #设置响应状态码  
                self.end_headers()
                if(os.path.getsize(inputFilename)>os.path.getsize(outputFilename)):
                    fout=open(outputFilename,'rb');
                else:
                    fout=open(inputFilename,'rb');
                try:
                    self.wfile = self.connection.makefile('wb', self.wbufsize)
                    self.wfile.write(fout.read())   #输出响应内容
                finally:
                    fout.close(); 
            else :
                self.protocal_version = 'HTTP/1.1'  #设置协议版本  
                self.send_response(400) #设置响应状态码  
        else:
            self.protocal_version = 'HTTP/1.1'  #设置协议版本  
            self.send_response(404) #设置响应状态码  
        





#启动服务函数  
def start_server(port):  
    http_server = HTTPServer(('', int(port)), MainHTTPHandler)  
    http_server.serve_forever() #设置一直监听并接收请求  
  
# os.chdir('static')  #改变工作目录到 static 目录  
start_server(9100)  #启动服务，监听8000端口  