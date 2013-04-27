#!/usr/bin/python2 -OO
import web
import webvirt

urls = (
    '/', 'Index',
    '/auth', 'Auth',
    '/list', 'List',
    '/login', 'Login',
    '/logout', 'Logout',
    '/console', 'Console',
    '/vm', 'VM',
    '/create', 'Create'
        )

if __name__ == '__main__':
    app = web.application(urls, webvirt.urls.classes)
    app.run()
