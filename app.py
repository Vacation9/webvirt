#!/usr/bin/python2
import web
import webvirt

urls = (
    '/', 'Index',
    '/auth', 'Auth',
    '/list', 'List',
    '/login', 'Login',
    '/console', 'Console'
        )

if __name__ == '__main__':
    app = web.application(urls, webvirt.urls.classes)
    app.run()
