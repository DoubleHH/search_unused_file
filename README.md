# search\_unused\_file

Search unused files in Xcode folder. 找出Xcode工程文件夹下未使用的文件，用于定期清理工程。未使用包括两种，1.没添加到工程；2.添加到工程后，但没使用过。

环境：脚本运行于Mac终端  
使用工具：Terminal + Python的额外工具包[the\_silver\_search](https://github.com/ggreer/the_silver_searcher)  
脚本编写语言：Python   

## 准备工作

打开终端Terminal，并安装[the\_silver\_search](https://github.com/ggreer/the_silver_searcher)，安装命令`brew install ag`。

## Usage

使用方式如下：

~~~
python search_unused_files.py (搜寻的文件夹) (要搜索的文件所在地)
~~~

## 举例说明

一般有两种需求：

1. 检查部分。检查工程内部分问价夹内文件在整个工程是否被使用；
2. 检查全部。检查整个工程内有哪些文件是否被使用；

用实际例子来说明，例如，有如下工程结构:

![](http://i.niupic.com/images/2017/06/25/47O1uT.png)

### 检查部分

想了解 Notify 这个文件夹下在整个 TestProject 工程有哪些文件未被使用，首先 cd 到 脚本所在目录，再运行脚本，具体命令如下：

~~~
cd /Users/user/Downloads/search_unused_file
python search_unused_file.py /Users/user/Desktop/TestProject /Users/user_name/Desktop/TestProject/TestProject/Notify
~~~

user指的是具体你的电脑用户名字

> 注意：如果提示`ag command not found`请参照上方的准备工作部分

最后结果如下：

![](http://i.niupic.com/images/2017/06/25/CGxBFo.png)

可以看到有进度条，最后说明该 Notify 文件夹下有两个文件 WMNotifyView 和 WMNotifyModel 未使用到

### 检查整个

使用和检查部分基本一致，命令行更简单:

~~~
cd /Users/user/Downloads/search_unused_file
python search_unused_file.py /Users/user/Desktop/TestProject
~~~

第二个路径不用传~

![](http://i.niupic.com/images/2017/06/25/QA815V.png)