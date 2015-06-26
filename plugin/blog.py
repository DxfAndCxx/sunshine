#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-06-04 16:33:38
# Author     : 陈小雪
# E-mail     : shell_chen@yeah.net
# Version    : 1.0.1

import os

from flask import render_template, request

from sunshine import ClassViews
from setting import STOREPATH
from publish import BlogData

name = "blog"
bp = "this is bp"

class Blog(ClassViews):
    def GET(self):
        return render_template("blog/index.html")


class Article(ClassViews):
    def get(self):
        return render_template("blog/add.html")

    def post(self):
        form = request.form
        title = form.get("title")
        tags = form.get("tags")
        if tags:
            tags = tags.split(",")
        else:
            tags = [ ]

        cls = form.get("cls","undefine")
        context = form.get("context")
        publish = form.get("publish", False)

        bd = BlogData(STOREPATH)
        bd.add(title, context, tags, cls, publish)

        return "sucess!"

# class Articles(ClassViews)





urls = (
        "/",           Blog,
        "/add/",   Article,
    )


