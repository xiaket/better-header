" Default user. please override this in your vimrc.
if !exists("g:BHAUTHOR")
    let g:BHAUTHOR = 'Your name <yourname@example.com>'
endif

" Enabled suffix. please override in your vimrc, and with each new suffix, 
" set a xx_header in your vimrc.
if !exists("g:BHEnabledSuffix")
    let g:BHEnabledSuffix = ['py', 'sh']
endif

" We would not write header for files under these directories.
if !exists("g:BHExcludeDir")
    let g:BHExcludeDir = ['usr', 'mnt', 'var', 'private', 'Volumes', 'opt']
endif

" We would write header for files in these directories.
if !exists("g:BHIn")
    let g:BHIn = ['~']
endif

" We would write header for files under these directories.
if !exists("g:BHUnder")
    let g:BHUnder = []
endif

if !exists("g:BHDebug")
    let g:BHDebug = "0"
endif

python << EOF
py_header = """#!/usr/bin/env python
#coding=utf-8\n\"\"\"
Author:         %(author)s
Filename:       %(filename)s
Date created:   %(cdate)s
Last modified:  %(date)s

Description:


\"\"\"
"""

sh_header = """#!/usr/bin/env bash
#
# Author:         %(author)s
# Filename:       %(filename)s
# Date created:   %(cdate)s
# Last modified:  %(date)s
#
# Description:
#

"""
import os
import vim
from datetime import datetime

def debug(message):
    if bool(int(vim.eval("g:BHDebug"))):
        print message

def suffix_is_supported(filepath):
    """
    This function would:
        1. get supported_suffix from global settings.
        2. make sure current suffix header is loaded.
        3. return whether current suffix is supported.
    """
    suffix = filepath.split("/")[-1].split(".")[-1]
    debug("Get file suffix: %s" % suffix)
    supported_suffix = vim.eval("g:BHEnabledSuffix")

    if suffix not in supported_suffix:
        # Early return here.
        debug("Suffix not in supported_suffix: %s" % suffix)
        return False

    # Make sure current suffix is defined.
    if bool(int(vim.eval("exists('g:BH%sHeader')" % suffix))):
        debug("Loading user specified suffix: %s" % suffix)
        header = vim.eval("g:BH%sHeader" % suffix)
        globals()["%s_header" % suffix] = header
    elif ("%s_header" % suffix) not in globals():
        # Header not found in user's vimrc and this plugin.
        debug("User want to enable this suffix but not header is found.")
        return False
    debug("Header found for this suffix: %s." % suffix)
    return True
            
def should_do_write(filepath):
    """这个函数判断我们是否应该给这个buffer添加/更新header.
    """
    if not suffix_is_supported(filepath):
        debug("suffix not supported.")
        return False

    if not os.path.exists(filepath):
        # file does not exist, so this is a new buffer, we shall check
        # whether we have write access to the directory.
        directory = os.path.split(filepath)[0]
        if not os.access(directory, os.W_OK):
            # If we do not have write access to the directory, we give up.
            debug("No permission, no write.")
            return False
    else:
        # existing file, check whether we have write access to it.
        if not os.access(filepath, os.W_OK):
            # no permission, do nothing.
            debug("No permission, no write.")
            return False

    # Files under exclude_dir should be exempted from writing.
    file_dir = filepath.rsplit('/', 1)[0]
    exclude_dirs = vim.eval("g:BHExcludeDir")
    exclude_dirs = [os.path.realpath(os.path.expanduser(_dir)) for _dir in exclude_dirs]
    for dirname in exclude_dirs:
        if file_dir.startswith(dirname):
            debug("File in BHExcludeDir, do write not.")
            return False

    # 白名单: BHIn下的目录下的文件我们都要写header.
    in_list = vim.eval("g:BHIn")
    for dirname in in_list:
        dirname = os.path.realpath(os.path.expanduser(dirname))
        if file_dir == dirname:
            debug("File in BHIn, do write.")
            return True

    # 白名单: BHUnder下的目录和子目录下的文件我们都写header.
    under_list = vim.eval("g:BHUnder")
    for dirname in under_list:
        dirname = os.path.realpath(os.path.expanduser(dirname))
        if filepath.startswith(dirname):
            debug("File under BHUnder, do write.")
            return True

    debug("default, do write not.")
    return False

def add_header(force=False):
    current_buffer = vim.current.buffer
    filename = os.path.basename(os.path.realpath(current_buffer.name))
    if not force:
        if not should_do_write(current_buffer.name):
            return

        on_enter = vim.eval("exists('b:BHENTERED')")
        if on_enter == '0':
            vim.command("let b:BHENTERED = '1'")
        else:
            # variable exist, this function has been run on this buffer, so quit.
            return

    author = vim.eval("g:BHAUTHOR")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    header = current_buffer[:7]
    header_content = "\n".join(header)
    if not "Last modified" in header_content:
        suffix = filename.split(".")[-1]
        if suffix_is_supported(current_buffer.name):
            debug("adding header")
            str_tmplt = globals().get("%s_header" % suffix).rstrip()
            str_content = str_tmplt % {
                'author': author,
                'filename': filename,
                'date': date,
                'cdate': date,
            }
            _range = current_buffer.range(0, 0)
            _range.append(str_content.split("\n"))

def update_header():
    current_buffer = vim.current.buffer
    filename = os.path.basename(os.path.realpath(current_buffer.name))

    header = current_buffer[:7]
    header_content = "\n".join(header)
    if not ("Last modified" in header_content and should_do_write(current_buffer.name)):
        # No previous header, and we should not write header, so no nothing.
        debug("No previous header and cannot do write.")
        return

    author = vim.eval("g:BHAUTHOR").replace("/", "\\/")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    row, column = vim.current.window.cursor
    vim.command("silent! 1,8 s/Filename.*/Filename:       %s/e" % filename)
    vim.command("silent! 1,8 s/Last modified:.*/Last modified:  %s/e" % date)
    vim.command("silent! 1,8 s/Modified by:.*/Modified by:    %s/e" % author)
    vim.current.window.cursor = (row, column)
    debug("Header updated.")
EOF

" call these function when these events are triggered.
autocmd bufread,bufnewfile * python add_header()
autocmd bufwritepre * python update_header()

" added a command to write header manually.
command BHeader python add_header(force=True)
