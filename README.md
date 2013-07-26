简介
====

这个插件会更新你的shell/python脚本的header, 使你的脚本便于维护.

这个插件硬编码了python/shell的header. 在它认为合适的时候, 它会添加/更新这个header里的字段.

具体逻辑是:

  0. 默认不添加/更新header.
  1. 如果待编辑文件在某些目录(/Users/xiaket/)下, 一定添加/更新header.
  2. 如果没权限写文件, 则不添加/更新header.
  3. 如果待编辑文件的全路径以var, mnt等开头, 不添加/更新header.
  4. 如果待编辑文件在某些目录下, 一定不添加/更新header.

安装
====

按通常的pathogen方式安装, 在你的.vimrc中添加你的联系方式:

```
HEADER_AUTHOR = "尊姓大名 <yourname@example.com>"
```

TODO
----

English translation.
