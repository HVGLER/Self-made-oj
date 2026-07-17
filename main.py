import os
import time
print("正在启动服务器中...")
time.sleep(2)
print("启动成功！请打开浏览器，在地址栏输入127.0.0.1:1279")
a = input("是否让本程序帮你打开？(Y/N)")
if a == 'Y':
    os.system("echo 已打开 && explorer.exe http://127.0.0.1:1279/")

os.system("python -m http.server 1279")