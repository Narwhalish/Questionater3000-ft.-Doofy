# -*- coding: utf-8 -*-
"""
Create python server.
"""
import os
import socket
import re

filesToSend = {
    b"css/clean-blog.css":b"css",
    b"css/clean-blog.min.css":b"css",
    b"css/header.css":b"css",
    b"scss/_bootstrap-overrides.scss":b"scss",
    b"scss/_contact.scss":b"scss",
    b"scss/_footer.scss":b"scss",
    b"scss/_global.scss":b"scss",
    b"scss/_masthead.scss":b"scss",
    b"scss/_mixins.scss":b"scss",
    b"scss/_navbar.scss":b"scss",
    b"scss/_post.scss":b"scss",
    b"scss/_variables.scss":b"scss",
    b"vendor/font-awesome/css/font-awesome.css":b"css",
    b"vendor/font-awesome/css/font-awesome.css.map":b"map",
    b"vendor/font-awesome/css/font-awesome.min.css":b"css",
    b"vendor/font-awesome/fonts/fontawesome-webfont.eot":b"eot",
    b"vendor/font-awesome/fonts/fontawesome-webfont.svg":b"svg",
    b"vendor/font-awesome/fonts/fontawesome-webfont.ttf":b"ttf",
    b"vendor/font-awesome/fonts/fontawesome-webfont.woff":b"woff",
    b"vendor/font-awesome/fonts/fontawesome-webfont.woff2":b"woff2",
    b"vendor/font-awesome/fonts/FontAwesome.otf":b"otf",
    b"vendor/font-awesome/less/animated.less":b"less",
    b"vendor/font-awesome/less/bordered-pulled.less":b"less",
    b"vendor/font-awesome/less/core.less":b"less",
    b"vendor/font-awesome/less/fixed-width.less":b"less",
    b"vendor/font-awesome/less/font-awesome.less":b"less",
    b"vendor/font-awesome/less/icons.less":b"less",
    b"vendor/font-awesome/less/larger.less":b"less",
    b"vendor/font-awesome/less/list.less":b"less",
    b"vendor/font-awesome/less/mixins.less":b"less",
    b"vendor/font-awesome/less/path.less":b"less",
    b"vendor/font-awesome/less/rotated-flipped.less":b"less",
    b"vendor/font-awesome/less/screen-reader.less":b"less",
    b"vendor/font-awesome/less/stacked.less":b"less",
    b"vendor/font-awesome/less/variables.less":b"less",
    b"vendor/font-awesome/scss/_animated.scss":b"scss",
    b"vendor/font-awesome/scss/_bordered-pulled.scss":b"scss",
    b"vendor/font-awesome/scss/_core.scss":b"scss",
    b"vendor/font-awesome/scss/_fixed-width.scss":b"scss",
    b"vendor/font-awesome/scss/_icons.scss":b"scss",
    b"vendor/font-awesome/scss/_larger.scss":b"scss",
    b"vendor/font-awesome/scss/_list.scss":b"scss",
    b"vendor/font-awesome/scss/_mixins.scss":b"scss",
    b"vendor/font-awesome/scss/_path.scss":b"scss",
    b"vendor/font-awesome/scss/_rotated-flipped.scss":b"scss",
    b"vendor/font-awesome/scss/_screen-reader.scss":b"scss",
    b"vendor/font-awesome/scss/_stacked.scss":b"scss",
    b"vendor/font-awesome/scss/_variables.scss":b"scss",
    b"vendor/font-awesome/scss/font-awesome.scss":b"scss",
    b"scss/clean-blog.scss":b"scss",
    b"vendor/bootstrap/css/bootstrap.css":b"css",
    b"vendor/bootstrap/css/bootstrap.css.map":b"map",
    b"vendor/bootstrap/css/bootstrap.min.css":b"css",
    b"vendor/bootstrap/css/bootstrap.min.css.map":b"map",
    b"img/about-bg.jpg":b"jpeg",
    b"html/textupload.html":b"html",
    b"js/clean-blog.js":b"js",
    b"js/clean-blog.min.js":b"js",
    b"js/getanswers.js":b"js",
    b"js/gulpfile.js":b"js",
    b"js/jqBootstrapValidation.js":b"js",
    b"js/jqBootstrapValidation.min.js":b"js",
    b"js/questions.js":b"js",
    b"vendor/jquery/jquery.js":b"js",
    b"vendor/jquery/jquery.min.js":b"js",
    b"vendor/jquery/jquery.slim.js":b"js",
    b"vendor/jquery/jquery.slim.min.js":b"js",
    b"vendor/bootstrap/js/bootstrap.bundle.min.js":b"js",
    b"img/favicon-32x32.png":b"png",
    b"img/logo.PNG":b"png",
    b"questionGenerators/fill_out.txt":b"txt",
    b"questionGenerators/tf_out.txt":b"txt",
}

defaultFile = [b"html/textupload.html",b"html"]
def sendFile(conn,filename,type):
    conn.send(type)
    conn.send(b"\n\n")
    f = open(filename,"rb")
    conn.send(f.read())
    f.close()

def handler(conn):
    data = conn.recv(9000)
    conn.send(b"HTTP/1.1 200 OK\nContent-type: text/")
    sentSomething = False

    for filename,type in filesToSend.items():
        if data.find(filename) != -1:
            sentSomething = True
            sendFile(conn,filename,type)
            break

    if not sentSomething:
        if data.find(b"textquiz.html") != -1:
            pattern = re.compile(b'text=(.*)\s')
            text = pattern.findall(data)[0]
            t = open('questionGenerators/input.txt', 'w')
            t.write(text.decode('utf8'))
            t.close()
            os.system('python txttofile.py')
            conn.send(b"html\n\n")
            fillstring = b""
            tfstring = b""
            fill = open("questionGenerators/fill_out.txt", "rb")
            tf = open("questionGenerators/tf_out.txt", "rb")
            fillcontents = fill.readlines()
            tfcontents = tf.readlines()
            for line in fillcontents:
                fillstring += line
            for line in tfcontents:
                tfstring += line
            f = open("html/textquiz.html","rb")
            conn.send(f.read().replace(b"[QUESTIONS]", fillstring + tfstring))
            f.close()
        else:
            sendFile(conn,defaultFile[0],defaultFile[1])
        conn.close()

def main():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(("",80))
    serv.listen(65)
    while True:
        conn,_ = serv.accept()
        handler(conn)
        #except: pass
    serv.close()
while True:
    main()
    #except: pass
