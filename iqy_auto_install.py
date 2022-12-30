#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import time
from pywinauto.application import Application


def grant_privilege():
    # 提权
    os.environ.update({"__COMPAT_LAYER": "RUnAsInvoker"})


def start_app(path):
    """launch application"""
    return Application().start(path, timeout=10, retry_interval=3)


def get_window_title(app):
    """get the window title text"""
    for w in app.windows():
        window_title = w.window_text()
        if window_title:
            window_title = window_title.replace('\n', r'\n').replace('\r', r'\r')

        # 不够严谨
        if "安装" in window_title:
            return window_title


# todo: 条件判断
def close_window(dlg):
    """close the window"""
    dlg.close()


def main(app, dest_path):
    # 获取窗口标题
    window_title = get_window_title(app)
    dlg = app[window_title]

    # 点击子窗口的阅读协议
    dlg.child_window(title_re=r'阅读.同意').click()

    # 输入自定义的安装路径
    dlg.child_window(class_name="Edit").set_edit_text(dest_path)

    # 点击子窗口的立即安装
    dlg.child_window(title="立即安装", class_name="Button").click()

    # 关闭窗口
    # close_window(dlg)


if __name__ == '__main__':
    path = r'C:\Users\zhboat\Downloads\iqy.exe'
    dest_path = r'C:\Software\IQY'

    grant_privilege()

    if not os.path.exists(path):
        print('Please check the package!')

    app = start_app(path)
    time.sleep(5)
    main(app, dest_path)
