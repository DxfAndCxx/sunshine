#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-05-29 11:07:47
# Author     : 陈小雪
# E-mail     : shell_chen@yeah.net
# Version    : 1.0.1

import os
import json
import time
import threading

class KvCache(object):
    def __init__(self, cache=None, save_timeout = 2*60, timeout=2*60*60):
        self.timeout = timeout
        self.cache_file = cache
        self.save_timeout = save_timeout

        self.save_time = time.time()
        self.caches = { }

        self.last_save_time_key = "last_save_time_key"
        self.caches_key = "caches_key"

        self.mutex = threading.Lock()

        self.__loads()


    def __loads(self):
        if not self.cache_file:
            return

        cache_dir = os.path.dirname(self.cache_file)
        if cache_dir and not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)

        if  not os.path.isfile(self.cache_file):
            return

        with open(self.cache_file, "r") as fp:
            buf = fp.read()
            tmp = json.loads(buf)
            try:
                self.caches = tmp.get(self.caches_key)
                self.save_time = tmp.get(self.last_save_time_key)
            except:
                return


    def __dumps(self):
        if not self.cache_file:
            return

        tmp = { }

        with open(self.cache_file, "w") as fp:
            tmp[self.caches_key] = self.caches
            tmp[self.last_save_time_key] = self.save_time
            fp.write(json.dumps(tmp))

    def __saves(self):
        now = time.time()

        if self.save_timeout < 0:
            return

        if float(self.save_time) + self.save_timeout > now:
            return

        self.save_time = now
        self.__dumps()

    def __check_timeout(self):

        if not self.caches:
            return

        if self.timeout < 0:
            return

        tmp = [ ]
        now = time.time()

        for k,(v,t) in self.caches.items():
            if t + self.timeout < now:
                tmp.append(k)

        for k in tmp:
            self.caches.pop(k)


    def get(self, k):
        v = None
        self.mutex.acquire()
        try:
            v = self.get_nolock(k)
        finally:
            self.mutex.release()
        return v

    def get_nolock(self, k):
        if not self.caches:
            return

        self.__check_timeout()

        item = self.caches.get(k)
        if not item:
            return  None

        return item[0]

    def set(self, k, v):
        self.mutex.acquire()
        try:
            self.set_nolock(k, v)
        finally:
            self.mutex.release()


    def set_nolock(self, k, v):
        self.__check_timeout()
        now = time.time()

        self.caches[k] = (v, now)
        self.__saves()


def testkbcache():
    cache = "testlog"
    KV = KvCache(cache, 1, 2)

    data = {"a":"aaaaaaa","b":"bbbbbbbbb"}
    for d in data.keys():
        v = KV.get(d)
        if not v:
            KV.set(d, data.get(d))
            print KV.caches
        time.sleep(2)

    KV.set("c","ccccccccc")
    KV.set("d","ddddddddd")

    print KV.caches

if __name__ == "__main__":
    testkbcache()




