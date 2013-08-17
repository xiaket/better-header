For English translation, jump to <https://github.com/xiaket/better-header#introduction>

简介
====

这个插件会更新你的shell/python脚本的header, 使你的脚本便于维护. 你也可以在.vimrc里添加你自己需要的header.

例如, 你在安装这个插件后, 在你的home目录下写一个新的python文件(newfile.py), 你会发现这个文件有了一个良好的header:

```
#!/usr/bin/env python
#coding=utf-8
"""
Author:         尊姓大名 <yourname@example.com>
Filename:       newfile.py
Date created:   2013-08-17 20:43
Last modified:  2013-08-17 20:43

Description:

"""
```

写一个新的shell文件也有类似的效果. 更舒心的是, header里上次更新时间和文件名这两个字段会自动更新.

这个插件拓展了Francisco Piedrafita的header.vim的功能: <http://www.vim.org/scripts/script.php?script_id=1142>

具体逻辑是:

  1. 如果文件后缀名不是py/sh, 则不添加/更新header.
  2. 如果没权限写文件, 则不添加/更新header.
  3. 如果待编辑文件的全路径以var, mnt等开头, 不添加/更新header.
  4. 如果待编辑文件的目录是指定目录(例如~), 添加/更新header.
  5. 如果待编辑文件的目录是指定目录的子目录, 添加/更新header.
  6. 默认不添加/更新header.
  7. 写文件时, 自动更新header里的文件名和修改时间.

安装
====

请先检查自己的vim是否支持python, 因为这个插件的逻辑大都用python编写:

```
vim --version | grep "+python"
```

如果你能看到这儿有输出, 那么你的编辑器支持python, 你能继续了.  :)

按通常的pathogen方式安装:

```
cd ~/.vim/bundle
git clone https://github.com/xiaket/better-header.git
```

最后, 在你的.vimrc中添加你的联系方式:

```
let g:BHAUTHOR = '尊姓大名 <yourname@example.com>'
```

配置
====

插件默认的配置包括:

1. BHAUTHOR:
```
let g:BHAUTHOR = '尊姓大名 <yourname@example.com>'
```

2. BHEnabledSuffix:
```
let g:BHEnabledSuffix = ['py', 'sh']
```
即, 对于py和sh结尾的文件, 我们会去看是否需要添加/更新header.

3. BHExcludeDir:
```
let g:BHExcludeDir = ['usr', 'mnt', 'var', 'private', 'Volumes', 'opt']
```
以这些名字开头的目录(一般都是系统目录)下的文件我们不会去看是否添加header.

4. BHIn:
```
let g:BHIn = ['~']
```
这个列表中的目录下的文件(不包括子目录), 我们会添加/更新header.

5. BHUnder:
```
let g:BHUnder = []
```
这个列表中的目录下的文件(包括子目录), 我们会添加/更新header.

6. BHDebug:
```
let g:BHDebug = "0"
```
是否开debug, 默认关闭. debug输出是我在python代码中直接print出来的. 查看的话请在vim中输入:messages


自定义Header
============

如果你需要添加你自己想要的header:

1. 在.vimrc中修改BHEnabledSuffix, 添加你所需要的后缀名(例如c)
```
let g:BHEnabledSuffix = ['py', 'sh', 'c']
```

2. 在.vimrc中写这个后缀名的header, 变量名为BHxxxHeader, 其中xxx为你的header的名字, 此处我们添加BHcHeader:
```
let g:BHcHeader = "/*\nAuthor:         %(author)s\nFilename:       %(filename)s\nDate created:   %(cdate)s\nLast modified:  %(date)s\n\nDescription:\n\n*/\n#include <stdio.h>\n#include <stdlib.h>\n#include <ctype.h>"
```
好吧, 看起来不那么直观, 这个我没法fix了. 内容里的%(author)s这样的内容会被替换. author对应作者, filename是文件名, cdate是创建时间, date是修改时间.

3. 如果你需要覆盖插件里的header, 可以直接在.vimrc里编写你需要的BHshHeader或BHpyHeader.

使用
====

我经常编写的脚本包括shell和python. 因此, 这两个脚本的header被我硬编码在插件里了.

按照安装说明, 我修改了我的.vimrc, 添加了我的名字.

本插件默认不写header, 所以你需要修改BHIn和BHUnder, 加入自己希望写header的地方. 对于我个人, 我经常在~下面写草稿, 这个目录下的内容我希望写header. 这一点我也写到默认值里了, 因此BHIn我不需要修改. 至于BHUnder, 我将日常修改的代码库加到了这个列表:
```
let g:BHUnder = ['~/.xiaket/share/repos/ntes-repos', '~/.xiaket/share/Dropbox/mercurial', '~/.xiaket/share/Dropbox/my.repos']
```

Introduction
------------

This vim plugin will update the header of your shell/python script, improving its readability and maintainablity. You could also add your header for your favourite language.

As an example, after you've installed this plugin, after writing a new python file(a newfile.py for the time being), you will find the file is pre-filled with a nicely formatted header:

```
#!/usr/bin/env python
#coding=utf-8
"""
Author:         尊姓大名 <yourname@example.com>
Filename:       newfile.py
Date created:   2013-08-17 20:43
Last modified:  2013-08-17 20:43

Description:

"""
```

And that works for shell(.sh files) too. What's more, the 'Last modified' and the 'Filename' fields are automatically updated upon file write.

This plugin is inspired by header.vim, originally written by Francisco Piedrafita: <http://www.vim.org/scripts/script.php?script_id=1142>

Some rationale:

  1. If filename does not ends in py/sh, do not add/update file header.
  2. If we have no write access to the file, do nothing.
  3. If the file is under some system directories, do not add/update file header.
  4. If the file is in some specific directory, add file header for new file, and update file header on write.
  5. If the file is under some specific directory, add/update file header(This would include child-directories).
  6. By default, do not add/update file header.
  7. Filename and modification time would be updated on file write.

Installation
============

1. Please make sure your vim has python support, for this plugin is written in python.
```
vim --version | grep "+python"
```
If you can see some output header, then you may proceed.  :)

2. Install using pathogen:
```
cd ~/.vim/bundle
git clone https://github.com/xiaket/better-header.git
```

3. Last by not the least, add your name in your .vimrc:
```
let g:BHAUTHOR = 'Your name <yourname@example.com>'
```

Configuration
=============

Default configurations for this plugin:

1. BHAUTHOR:
```
let g:BHAUTHOR = '尊姓大名 <yourname@example.com>'
```

2. BHEnabledSuffix:
```
let g:BHEnabledSuffix = ['py', 'sh']
```
We will add custom header file only for files end with these suffixes.

3. BHExcludeDir:
```
let g:BHExcludeDir = ['usr', 'mnt', 'var', 'private', 'Volumes', 'opt']
```
We will do nothing for files under these directories(usually system folders).

4. BHIn:
```
let g:BHIn = ['~']
```
Files under directories(not including their child directories) in this list will have a nice header.

5. BHUnder:
```
let g:BHUnder = []
```
Files under directories(including their child directories) in this list will have a nice header.

6. BHDebug:
```
let g:BHDebug = "0"
```
Debug options, it is closed by default. To enable it, change this to 1. Those debug outputs are printed in my python code. Enter ':messages' in your vim to read them.

Customize Header
================

If you wish to add your own header, you need to:

1. Modify BHEnabledSuffix in your .vimrc, add your suffix(take c for example here).
```
let g:BHEnabledSuffix = ['py', 'sh', 'c']
```

2. Add your header in your .vimrc. The name of the variable should be BHxxxHeader, for example:
```
let g:BHcHeader = "/*\nAuthor:         %(author)s\nFilename:       %(filename)s\nDate created:   %(cdate)s\nLast modified:  %(date)s\n\nDescription:\n\n*/\n#include <stdio.h>\n#include <stdlib.h>\n#include <ctype.h>"
```
This %(author)s thingy will be replaced. Well, it's clumsy to use \n as new line. however, I'm not sure there is a way to fix that.

3. If you wish to override the default header in this plugin, just write your own BHshHeader or BHpyHeader in your .vimrc.

Usage
=====

I play with shell and python script on a daily basis. Thus the header for these scripts are hardcoded in this plugin.

I followed the installation instruction above, added my name in my .vimrc. By default, this plugin does not write header, so you need to modify your BHIn and BHUnder, add folder of your own choice. I start writing new script in ~ most of the time, so I hope files under this directory should start with a nice header. Oh, but not it's child directories, for I store many things in my ~. As I'm the author of this script, BHIn include ~ by default, so no need to change that. So I only need to add my personal repositories in BHUnder:
```
let g:BHUnder = ['~/.xiaket/share/repos/ntes-repos', '~/.xiaket/share/Dropbox/mercurial', '~/.xiaket/share/Dropbox/my.repos']
```

And that's all set. I enjoyed this plugin.
