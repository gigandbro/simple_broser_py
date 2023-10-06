import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QAction, QLineEdit, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class BrowserTab(QWebEngineView):
    def __init__(self, url):
        super().__init__()
        self.setUrl(QUrl(url))

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowIcon(QIcon("your_icon.png"))

        self.browser_tabs = QTabWidget()
        self.setCentralWidget(self.browser_tabs)

        navtb = QToolBar()
        self.addToolBar(navtb)

        back_btn = QAction("◄", self)
        back_btn.setStatusTip("Назад")
        navtb.addAction(back_btn)

        next_btn = QAction("►", self)
        next_btn.setStatusTip("Вперед")
        navtb.addAction(next_btn)

        reload_btn = QAction("🗘", self)
        reload_btn.setStatusTip("Обновить")
        navtb.addAction(reload_btn)

        new_tab_btn = QAction("➕", self)
        new_tab_btn.setStatusTip("Новая вкладка")
        new_tab_btn.triggered.connect(self.add_new_tab)
        navtb.addAction(new_tab_btn)

        close_tab_btn = QAction("✖", self)
        close_tab_btn.setStatusTip("Закрыть вкладку")
        close_tab_btn.triggered.connect(self.close_current_tab)
        navtb.addAction(close_tab_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        self.show()

        self.browser_tabs.tabCloseRequested.connect(self.close_current_tab)
        self.browser_tabs.currentChanged.connect(self.update_urlbar)
        self.browser_tabs.currentChanged.connect(self.update_title)

        back_btn.triggered.connect(self.navigate_back)
        next_btn.triggered.connect(self.navigate_forward)
        reload_btn.triggered.connect(self.reload_current_browser)

        self.add_new_tab()

    def update_title(self):
        current_browser = self.current_browser()
        if current_browser:
            title = current_browser.page().title()
            self.setWindowTitle("%s - gigbrows" % title)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.current_browser().setUrl(q)

    def update_urlbar(self):
        current_browser = self.current_browser()
        if isinstance(current_browser, BrowserTab):
            q = current_browser.url()
            self.urlbar.setText(q.toString())
            self.urlbar.setCursorPosition(0)

    def add_new_tab(self):
        new_tab = self.create_new_tab("https://www.google.com")
        new_tab.loadFinished.connect(self.update_title)
        new_tab.loadFinished.connect(self.update_urlbar)

    def close_current_tab(self):
        current_tab_index = self.browser_tabs.currentIndex()
        if current_tab_index >= 0:
            self.browser_tabs.removeTab(current_tab_index)

    def current_browser(self):
        current_tab_index = self.browser_tabs.currentIndex()
        if current_tab_index >= 0:
            return self.browser_tabs.widget(current_tab_index)
        return None

    def create_new_tab(self, url):
        browser_tab = BrowserTab(url)
        self.browser_tabs.addTab(browser_tab, "New Tab")
        self.browser_tabs.setCurrentWidget(browser_tab)
        return browser_tab

    def navigate_back(self):
        self.current_browser().back()

    def navigate_forward(self):
        self.current_browser().forward()

    def reload_current_browser(self):
        current_browser = self.current_browser()
        if current_browser:
            current_browser.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


