import web
import webvirt

urls = (
    '/', 'handlers.Index'
        )

if __name__ == '__main__':
    app = web.application(urls, webvirt.handlers.classes)
    app.run()
