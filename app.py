import web
import webvirt

urls = (
    '/', 'Index',
    '/auth/(.*)', 'Auth',
        )

if __name__ == '__main__':
    app = web.application(urls, webvirt.urls.classes)
    app.run()
