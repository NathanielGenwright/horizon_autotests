from selenium import webdriver

from .ui import Container

__all__ = [
    'App',
    'Page'
]


browsers = {
    'firefox': webdriver.Firefox,
    'phantom': webdriver.PhantomJS,
    'Chrome': webdriver.Chrome,
}


class App(object):

    def __init__(self, url, browser, *args, **kwgs):
        self.app_url = url.strip('/')
        self.webdriver = browsers[browser](*args, **kwgs)

    def open(self, url):
        self.webdriver.get(self.app_url + url)

    def quit(self):
        self.webdriver.quit()


class Page(Container):

    url = None

    def __init__(self, app):
        self.app = app
        self.webdriver = app.webdriver
        self.webelement = self.webdriver
