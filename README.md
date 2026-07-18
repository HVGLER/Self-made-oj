# Self-made-hhjoj
[the English vesion readme?](https://github.com/HVGLER/Self-made-oj/blob/main/README_en.md)<br>
开源免费的判题系统，有题库。整体编程语言只有Python 和 html

# 关于题库

题库里面有经典的编程题————两数之和，还有在线GESP2023年03月的试卷<br>
并且我们会每日更新题库,题库文件夹在本仓库的  tk/  文件夹。

- # 咋运行？

  首先，你的电脑要安装Python3.8以上的Python版本  [点我下载windows版](https://mirrors.aliyun.com/python-release/windows/python-3.8.10.exe)（必须）<br>
  其次，GCC/JAVA/NODEJS请自行安装<br>点我下载[windows-Mingw](https://github.com/brechtsanders/winlibs_mingw/releases/download/12.4.0posix-12.0.0-msvcrt-r1/winlibs-i686-posix-dwarf-gcc-12.4.0-mingw-w64msvcrt-12.0.0-r1.7z)   [windows-zulujdk](https://cdn.azul.com/zulu/bin/zulu17.66.19-ca-jdk17.0.19-win_x64.msi)

  [windows-nodejs](https://nodejs.org/dist/v20.20.2/node-v20.20.2-x64.msi)<br>

  （可选，只不过如果不安装，oj里面的编程语言只有Python能用）<br>
  第二，运行main.py，然后再运行oj/judge_core.py<br>
  之后就可以打开浏览器，访问127.0.0.1:1279查看oj啦，也可以访问127.0.0.1:8080查看判题接口。

  # 关于linux咋运行

  Ubuntu、debian、linuxmint等有apt命令的linux直接在命令行终端输入  sudo apt install gcc-14 g++-14 nodejs npm  openjdk-17-jdk  关于为什么没有python，因为linux系统本身就自带python。

  # 关于macos咋运行

  安装Homebrew：<br>

  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"<br>

  安装组件:<br>

  brew install python<br>

  brew install gcc<br>

  brew install node<br>

  brew install openjdk@17<br>

  sudo ln -sfn $(brew --prefix)/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk<br>

  echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc<br>
  echo 'export JAVA_HOME="/opt/homebrew/opt/openjdk@17"' >> ~/.zshrc<br>
  source ~/.zshrc<br>

  关于为什么有python，因为macos不自带python（**旧版本曾预装 Python 2.7**：在 macOS 10.8 至 12.3 版本期间，系统确实预装了 Python 2.7。但这个版本官方早已停止维护，苹果也在后续系统中将其移除了）<br>

# 咋加题目？

请自觉复制粘贴，改题目

# 关于我为啥要搞GithubPages
因为在电脑上安装好了这个oj，可以快捷的访问oj，并且在github的加持下不必我多说。

# 本程序完全跨平台

支持windows7~windows11，linux，macos<br>

只要你的电脑能安装/使用python和浏览器，就能使用这个oj<br>
