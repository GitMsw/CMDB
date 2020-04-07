#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 通过os和sys模块的配合，将当前客户端所在目录设置为工作目录，如果不这么做，会无法导入其它模块；
# handler模块是核心代码模块，在core目录中，我们一会来实现它。
# 以后调用客户端就只需要执行python main.py 参数就可以了
import os
import sys

BASE_DIR = os.path.dirname(os.getcwd())
sys.path.append(BASE_DIR)  # 主路径

from core import handler

if __name__ == '__main__':
    handler.ArgvHandler(sys.argv)

