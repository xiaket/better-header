简介
====

这个插件会更新你的shell/python脚本的header, 使你的脚本便于维护. 你也可以在.vimrc里添加你自己需要的header.

这个插件拓展了Francisco Piedrafita的header.vim的功能: <http://www.vim.org/scripts/script.php?script_id=1142>

具体逻辑是:

  1. 如果文件后缀名不是py/sh, 则不添加/更新header.
  2. 如果没权限写文件, 则不添加/更新header.
  3. 如果待编辑文件的全路径以var, mnt等开头, 不添加/更新header.
  4. 如果待编辑文件的目录是指定目录(例如~), 一定添加/更新header.
  5. 如果待编辑文件的目录是指定目录的子目录, 一定添加/更新header.
  6. 默认不添加/更新header.

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
以这些名字开头的目录下的文件我们不会去看是否添加header.

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

如果你需要添加你自己需要的header, 你需要:

1. 在.vimrc中修改BHEnabledSuffix, 添加你所需要的后缀名(例如c)
```
let g:BHEnabledSuffix = ['py', 'sh', 'c']
```
2. 在.vimrc中写这个后缀名的header, 变量名为BHxxxHeader, 其中xxx为你的header的名字(小写), 此处我们添加BHcHeader:
```
let g:BHcHeader = "/*\nAuthor:         %(author)s\nFilename:       %(filename)s\nDate created:   %(cdate)s\nLast modified:  %(date)s\n\nDescription:\n\n*/\n#include <stdio.h>\n#include <stdlib.h>\n#include <ctype.h>"
```
好吧, 看起来不那么直观, 这个我没法fix了.

使用
====

我经常编写的脚本包括shell和python. 因此, 这两个脚本的header被我硬编码在插件里了. 按照上面的说明, 我修改了我的.vimrc, 添加了我的名字.

本插件默认不写header, 所以你需要修改BHIn和BHUnder, 加入自己希望写header的地方. 对于我, 我经常在~下面写草稿, 这个目录下的内容我希望写header. 这一点我也写到默认值里了, 因此BHIn我不需要修改. 至于BHUnder, 我将日常修改的代码库加到了这个项:
```
let g:BHUnder = ['~/.xiaket/share/repos/ntes-repos', '~/.xiaket/share/Dropbox/mercurial', '~/.xiaket/share/Dropbox/my.repos']
```

TODO
----

English translation.
