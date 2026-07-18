# Self-made-hhjoj

Open-source and free online judge system with a question bank. The overall programming languages are only Python and HTML.

# About the question bank

The question bank contains a classic programming problem — Two Sum, as well as the online GESP March 2023 Level 1 C++ exam paper<br>
And we will update the question bank daily; the question bank folder is located in the tk/ folder of this repository.
- # How to run?

  First, your computer must have Python version 3.8 or higher installed.  [Click here to download the Windows version](https://mirrors.aliyun.com/python-release/windows/python-3.8.10.exe)（Must）<br>
  Secondly, please install GCC/JAVA/NODEJS yourself.<br>Click here to download[windows-Mingw](https://github.com/brechtsanders/winlibs_mingw/releases/download/12.4.0posix-12.0.0-msvcrt-r1/winlibs-i686-posix-dwarf-gcc-12.4.0-mingw-w64msvcrt-12.0.0-r1.7z)   [windows-zulujdk](https://cdn.azul.com/zulu/bin/zulu17.66.19-ca-jdk17.0.19-win_x64.msi)
  [windows-nodejs](https://nodejs.org/dist/v20.20.2/node-v20.20.2-x64.msi)<br>
  (Optional, but if not installed, only Python can be used in the OJ)<br>
  Second, run main.py, and then run oj/judge_core.py.<br>
  After that, you can open your browser and visit 127.0.0.1:1279 to view the OJ, or visit 17.0.0.1:8080 to view the judging interface.

# About how Linux runs
For Linux distributions with the apt command such as Ubuntu, Debian, and Linux Mint, simply enter sudo apt install gcc-14 g++-14 node npm openjdk-17-jdk in the command line terminal. Regarding why Python is not included, it is because the Linux system itself comes with Python pre-installed
# How to run macOS
install Homebrew：<br>
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"<br>
 install:<br>
  brew install python<br>
  brew install gcc<br>
  brew install node<br>
  brew install openjdk@17<br>
  sudo ln -sfn $(brew --prefix)/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk<br>
  echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc<br>
  echo 'export JAVA_HOME="/opt/homebrew/opt/openjdk@17"' >> ~/.zshrc<br>
  source ~/.zshrc<br>
Regarding why there is Python, it is because macOS does not come with Python pre-installed (**older versions used to have Python 2.7 pre-installed between macOS versions 10.8 and 12.3, the system did indeed come with Python 2.7 pre-installed. However, this version has long officially end-of-life, and Apple has removed it in subsequent system updates)<br>
# How to add a question?
Please copy and paste voluntarily, and change the title.
# This program is completely cross-platform
Supports Windows 7~Windows 11, Linux, macOS<br>
As long as your computer can install/use Python and a browser, you can use this OJ<br>



