#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-06-04 16:33:38
# Author     : 陈小雪
# E-mail     : shell_chen@yeah.net
# Version    : 1.0.1

import os
import time
import json

from flask import render_template, request

from sunshine import ClassViews
from setting import STOREPATH
from publish import BlogData

name = "blog"
bp = "this is bp"

def setid():
    return int(time.time() - 1419598800)


def getkv(line):
    tmp = line[1:].split(':', 1)
    if len(tmp) < 2:
        return []
    return (tmp[0].strip().lower(), tmp[1].strip())

def get_info(file_path):
    info = { }
    tex_index = 0
    flags = False
    with open(file_path, "r") as fp:
        lines = fp.readlines()

    for index,line in enumerate(lines):
        if line[0] == "%":
            try:
                k, v = getkv(line)
                info[k] = v
                flags = True
            except:
                pass

        else:
            if flags:
                tex_index = index
                break
    tex = "".join(lines[tex_index:])
    return (info, tex)

class Blog(ClassViews):
    def GET(self):
        return render_template("blog/index.html")


class Chapters(ClassViews):
    def GET(self):
        return render_template("blog/add.html")

    def POST(self):
        form = json.loads(request.data)
        tex = form.get("tex", " ")
        Id = setid()
        dir_path = os.path.join(STOREPATH,str(Id))

        if os.path.isdir(dir_path):
            return "-1"      #路径重复

        os.mkdir(dir_path)

        file_path = os.path.join(dir_path, "index.md")

        with open(file_path, "w")  as fp:
            fp.write(tex)

        (infos, tex) = get_info(file_path)
        BD = BlogData(STOREPATH)
        BD.add(Id, infos, tex)
        return str(Id)

    def PUT(self):
        print dir(request)
        Id = request.args.get("id")
        data = json.loads(request.data).get("tex","")
        dir_path = os.path.join(STOREPATH, str(Id))

        if not os.path.isdir(dir_path):
            return "-1"   #路径不存在
        file_path = os.path.join(dir_path, "index.md")
        (infos, tex) = get_info(file_path)
        BD = BlogData(STOREPATH)
        BD.update(Id, infos, tex)
        return str(Id)




urls = (
        "/",            Blog,
        "/chapters/",   Chapters,
    )


