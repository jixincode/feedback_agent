#!/bin/bash

PYTHON="/opt/homebrew/bin/python3.11"
SCRIPT="main.py"

if [ ! -f "$PYTHON" ]; then
    echo "错误: Python 3.11 未找到: $PYTHON"
    echo "请确保已安装 Python 3.11"
    exit 1
fi

if [ ! -f "$SCRIPT" ]; then
    echo "错误: 脚本文件未找到: $SCRIPT"
    exit 1
fi

cd "$(dirname "$0")"
$PYTHON $SCRIPT