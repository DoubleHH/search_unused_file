# 搜索未使用的对象

## 步骤

1. 搜索所有的对象申明，ag命令如下：
	
	~~~
	ag --objc " *@interface +\w* *:
	~~~
	
	这样可以搜索到所有对象的声明，从声明中可以取出对象类名。

2. 利用对象类名在工程所在文件夹搜索该类名出现过的所有代码行。ag命令如下：

	~~~
	ag --objc -w ObjectName SearchPath
	ag --objc -w JSONModel /Users/xx/XXProject
	~~~

2. 循环判断每个对象是否真的被其他对象或者类使用过（本身类使用自己不算做使用），如果使用过则退出循环。使用过的判断条件如下：
	- 该行不是注释行。注释行分为//和/**/样式（包括内部行）的注释。
	- 该行不是被本身类使用。

### 如何判断不是本身类使用的自己

当一行代码中出现了正在搜索的类名。当自身类使用本身类名时，我们认为不算使用过。那么怎么判断一行代码是非自身类使用？

大家非常直观地会想出，如果当前的代码不在类定义的文件中，就是非本身类了吧...

但这是有漏洞的逻辑，首先一个文件的名字跟本身定义的类可以不一样，其次一个文件可以定义多个类，期间可以相互使用。

完美的逻辑是搜索该代码是在哪个类的声明或实现代码区域使用的。如果是在自身类的声明或者实现区域内，就不算被使用，反之则算使用过。

最终我们的问题变为，如果判断当前代码所在的类名。

#### 判断代码行所在的类名

两种办法

1. 找到该类的定义和实现代码的文件名，起始和结束行，判断一行代码的行数是否在区间内就行；
2. 通过该行代码在文件内按照行数依次往上找，找到类的声明行或者实现行（@interface or @implementation）停止，得到当前代码行所在的类名；

采取第二种方案