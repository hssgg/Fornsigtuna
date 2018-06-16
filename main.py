#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"
#
# MIT License
#
# Copyright (c) 2018 liantian
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import marshal
import re

from flask import send_file, request, render_template
from flask import Flask, request, jsonify, make_response

with open("zh-Hant.marshal", 'rb') as cf:
    hantRep, Pattern_str = marshal.load(cf)
    hantPattern = re.compile(Pattern_str)
    del Pattern_str
with open("zh-Hans.marshal", 'rb') as cf:
    hansRep, Pattern_str = marshal.load(cf)
    hansPattern = re.compile(Pattern_str)
    del Pattern_str
with open("zh-cn.marshal", 'rb') as cf:
    cnRep, Pattern_str = marshal.load(cf)
    cnPattern = re.compile(Pattern_str)
    del Pattern_str
with open("zh-hk.marshal", 'rb') as cf:
    hkRep, Pattern_str = marshal.load(cf)
    hkPattern = re.compile(Pattern_str)
    del Pattern_str
with open("zh-tw.marshal", 'rb') as cf:
    twRep, Pattern_str = marshal.load(cf)
    twPattern = re.compile(Pattern_str)
    del Pattern_str

app = Flask(__name__)
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    app.config['DEBUG'] = True


@app.errorhandler(404)
def page_not_found(e):
    return "Error : 404 - Page Not Found", 404


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api', methods=['POST'])
def api():
    text = request.values.get('text', "parameter 'text' is empty\n")
    lang = request.values.get('lang', "parameter 'lang' is empty\n")
    html = request.values.get('html', False)

    lang = lang.decode("utf-8").lower()
    if not (lang in (u"zh-hans", u"zh-cn", u"zh-tw", u"zh-hk", u"zh-hant")):
        response = make_response(jsonify(error="parameter 'lang' is error\n"))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response

    # print(bool(html))
    # print(type(text))

    if isinstance(text, str):
        text = text.decode("utf-8")
    if not isinstance(text, unicode):
        response = make_response(jsonify(error="text is not utf-8 encode\n"))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response

    if lang == u"zh-hans":
        result = hansPattern.sub(lambda m: hansRep[re.escape(m.group(0))], text)
    elif lang == u"zh-hant":
        result = hantPattern.sub(lambda m: hantRep[re.escape(m.group(0))], text)
    elif lang == u"zh-cn":
        result = cnPattern.sub(lambda m: cnRep[re.escape(m.group(0))], text)
    elif lang == u"zh-hk":
        result = hkPattern.sub(lambda m: hkRep[re.escape(m.group(0))], text)
    elif lang == u"zh-tw":
        result = twPattern.sub(lambda m: twRep[re.escape(m.group(0))], text)
    else:
        result = text

    if not bool(html):
        response = make_response(jsonify(result=result, lang=lang, text=text, html=bool(html)))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response
    else:
        return render_template("result.html", result=result)
