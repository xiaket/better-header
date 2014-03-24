#!/usr/bin/env python
#coding=utf-8
"""
Author:         Xia Kai <xiaket@corp.netease.com/xiaket@gmail.com>
Filename:       pylib.py
Date created:   2014-02-12 13:11
Last modified:  2014-03-24 10:57
Modified by:    Xia Kai <xiaket@corp.netease.com/xiaket@gmail.com>

Description:
    python code for better-header.
Changelog:
"""
py_header = """#!/usr/bin/env python
#coding=%(encoding)s\n\"\"\"
Author:         %(author)s
Filename:       %(filename)s
Date created:   %(cdate)s
Last modified:  %(date)s
Modified by:    %(modified_by)s

Description:
%(description)s
Changelog:
%(changelog)s
\"\"\"
"""

sh_header = """#!/usr/bin/env bash
#
# Author:         %(author)s
# Filename:       %(filename)s
# Date created:   %(cdate)s
# Last modified:  %(date)s
# Modified by:    %(modified_by)s
#
# Description:
# %(description)s
# Changelog:
# %(changelog)s
"""
import os
import re
import vim
from collections import defaultdict
from copy import copy
from datetime import datetime
from itertools import groupby


ENCODING = 'utf-8'
CURRENT_BUFFER = vim.current.buffer
SUFFIX = CURRENT_BUFFER.name.split("/")[-1].split(".")[-1]
FILENAME = os.path.basename(os.path.realpath(CURRENT_BUFFER.name))
AUTHOR = vim.eval("g:BHAUTHOR")
KEYWORDS = {
    'Author': 'author',
    'Filename': 'filename',
    'Date created': 'cdate',
    'Last modified': 'date',
    'Description': 'description',
    'Changelog': 'changelog',
    'Maintained by': 'modified_by',
    'Modified by': 'modified_by',
    'Usage': 'description',
}
STRIPS = "\t #:"


# utility functions.
def debug(message):
    if bool(int(vim.eval("g:BHDebug"))):
        print str(message)

def print_debug_info():
    debug("#"*40)
    debug("start of debug info")
    debug("filename: %s" % FILENAME)
    debug("has write access: %s" % has_write_access())
    debug("has header: %s" % has_header())

    debug("suffix: %s" % SUFFIX)
    if suffix_is_supported():
        debug("loaded header: %s" % globals()["%s_header" % SUFFIX])
    else:
        debug("suffix not supported")

    debug("end of debug info")
    debug("#"*40)

# helper functions, hide details from worker functions.
def modified():
    """ function to get buffer modification status. :help :redir."""
    vim.command("redir => b:BHmodified")
    vim.command("silent set modified?")
    vim.command("redir END")
    buffer_status = vim.eval("b:BHmodified").strip()
    debug("buffer status: %s" % buffer_status)
    return buffer_status == 'modified'

def suffix_is_supported():
    """
    This function would:
        1. get enabled suffix from global settings.
        2. make sure current suffix header is loaded.
        3. return whether current suffix is supported.
    """
    if SUFFIX not in vim.eval("g:BHEnabledSuffix"):
        # Early return here.
        return False

    # Make sure header of current suffix is defined.
    if bool(int(vim.eval("exists('g:BH%sHeader')" % SUFFIX))):
        header = vim.eval("g:BH%sHeader" % SUFFIX)
        globals()["%s_header" % SUFFIX] = header
    elif ("%s_header" % SUFFIX) not in globals():
        # Header not found in user's vimrc and this plugin.
        return False
    return True

def has_write_access():
    """whether we can write to the buffer."""
    filepath = CURRENT_BUFFER.name
    if not os.path.exists(filepath):
        # file does not exist, so this is a new buffer, we shall check
        # whether we have write access to the directory.
        return os.access(os.path.split(filepath)[0], os.W_OK)
    else:
        # existing file, check whether we have write access to it.
        return os.access(filepath, os.W_OK)

def should_do_write():
    """Whether we should add/update header for this buffer. """
    if not suffix_is_supported():
        return False

    if not has_write_access():
        return False

    # Files under exclude_dir should be exempted from writing.
    filepath = CURRENT_BUFFER.name
    file_dir = filepath.rsplit('/', 1)[0]
    exclude_dirs = vim.eval("g:BHExcludeDir")
    exclude_dirs = [os.path.realpath(os.path.expanduser(_dir)) for _dir in exclude_dirs]
    for dirname in exclude_dirs:
        if file_dir.startswith(dirname):
            debug("File in BHExcludeDir, do not write header.")
            return False

    # whitelist: files directly inside BHIn will have a header.
    in_list = vim.eval("g:BHIn")
    for dirname in in_list:
        dirname = os.path.realpath(os.path.expanduser(dirname))
        if file_dir == dirname:
            debug("File in BHIn, do write.")
            return True

    # whitelist: files under BHUnder or its sub-dir will have a header.
    under_list = vim.eval("g:BHUnder")
    for dirname in under_list:
        dirname = os.path.realpath(os.path.expanduser(dirname))
        if filepath.startswith(dirname):
            debug("File under BHUnder, do write.")
            return True

    debug("default, do not write header.")
    return False

def has_header():
    """
    determine whether this buffer is already equipped with a nice header.

    if we have more than two keywords in the first 7 lines, then it's
    safe to say that this buffer has a header.
    """
    header_content = ("\n".join(CURRENT_BUFFER[:7])).lower()
    return sum(1 for keyword in KEYWORDS if header_content.find(keyword.lower()) != -1) >= 2

def fix_sh_header_with_sharp(data_dict):
    debug("fixing sh header with #")
    for key in data_dict:
        if data_dict[key].find("\n") != -1:
            # new line in value.
            new_lines = []
            lines = data_dict[key].splitlines()
            for line in lines:
                if not line.startswith("#") and line.strip():
                    new_lines.append("# %s" % line)
                else:
                    new_lines.append(line)
            data_dict[key] = '\n'.join(new_lines)

def render_header(header_dict={}):
    """ render header with provided header and dictionary."""
    header = globals().get("%s_header" % SUFFIX).rstrip()
    debug("rendering header.")
    debug("header: %s" % header)
    debug("header_dict: %s" % header_dict)
    data_dict = defaultdict(str)
    data_dict.update({
        'encoding': ENCODING,
        'filename': FILENAME,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'cdate': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'modified_by': AUTHOR,
        'author': AUTHOR,
    })
    debug("updated dict(stage 1): %s" % data_dict)
    keywords = copy(KEYWORDS)
    more_keywords = vim.eval("g:BHKeywords")
    keywords.update(more_keywords)

    # update data_dict with user provided key-value pairs.
    for key in header_dict:
        if not key in keywords:
            continue
        data_dict[keywords[key]] = header_dict[key]
    debug("updated dict(stage 2): %s." % data_dict)

    # if we are editing an shell script, and there are line seps in the comment, add a # if we have to.
    if SUFFIX == "sh":
        fix_sh_header_with_sharp(data_dict)

    rendered_header = header % data_dict
    debug("rendered header: %s" % rendered_header)
    return rendered_header

def prepend_header(rendered_header):
    """ adding header to the beginning of buffer. """
    debug("adding header")
    _range = CURRENT_BUFFER.range(0, 0)
    _range.append(rendered_header.split("\n"))

def extract_comment_py():
    """extract comment from a python script."""
    debug("extract comment from a python script.")
    for line in CURRENT_BUFFER[:3]:
        if re.search(r"coding[:=]\s*([-\w.]+)", line):
            pattern = re.compile(r"coding[:=]\s*(?P<encoding>[-\w.]+)")
            globals()['ENCODING'] = pattern.search(line).group('encoding')
            debug("found encoding: %s" % globals()['ENCODING'])

    lines = list(CURRENT_BUFFER)
    for (i, iline) in enumerate(lines[:10]):
        # find """ or ''' in the first few lines.
        if '"""' in iline or "'''" in iline:
            # find the end of it.
            breaker = '"""' if '"""' in iline else "'''"
            for j, jline in enumerate(lines[i+1:]):
                if breaker in jline:
                    # found it, format the comment a little bit.
                    if j == 0:
                        # in the same line, this is a one line comment.
                        return [jline[jline.index(breaker)+3:jline.rindex(breaker)]]
                    else:
                        lines[i] = lines[i][lines[i].index(breaker)+3:]
                        lines[i+j+1] = lines[i+j+1][:lines[i+j+1].rindex(breaker)]
                        return lines[i:i+j+1]
            else:
                # end of the comment is not found.
                return
    else:
        # comment might start with #
        return extract_comment_sh(python_style=True)

def extract_comment_sh(python_style=False):
    """extract comment from a shell script."""
    if not python_style:
        debug("extract comment from a shell script.")
    lines = list(CURRENT_BUFFER)
    if lines[0].startswith("#!"):
        lines = lines[1:]

    if python_style and re.search(r"coding[:=]\s*([-\w.]+)", lines[0]):
        # strip encoding line.
        lines = lines[1:]

    for i, line in enumerate(lines):
        if not line.startswith("#"):
            break
    else:
        i += 1
    return [line.lstrip("# ") for line in lines[:i]]

def parse_tab_in_comment(comment):
    """get tab separated key-value pairs."""
    line_has_tab = [line.find("\t") != -1 for line in comment]
    if not any(line_has_tab):
        return {}, comment

    comment_dict = {}
    debug("parsing tabs in comment")
    consecutive_true_count = max(len(list(v)) for k, v in groupby(line_has_tab) if k)
    # need to have 3 consecutive tab formatted lines.
    if consecutive_true_count >= 3:
        # for these lines, split by tab, strip non-alphabets.
        for line in copy(comment):
            if line.find("\t") != -1:
                key, value = line.rsplit("\t", 1)
                key = key.strip(STRIPS)
                value = value.strip(STRIPS)
                if re.compile(r'[0-9]{2,4}[ -.][0-9]{2}[ -.][0-9]{2}( [0-9]{2}:[0-9]{2}(:[0-9]{2})?)?').match(key):
                    # if key is a datetime obj, ignore it.
                    continue
                debug("tab || found %s: %s" % (key, value))
                comment_dict[key] = value
                comment.remove(line)
    return comment_dict, comment

def parse_space_in_comment(comment):
    """get space separated key-value pairs."""
    max_spaces_dict = {}
    for line in comment:
        if (not line.strip()) or line.find(" ") == -1:
            # empty line or line do not have spaces in it.
            continue
        max_spaces_dict[line] = max(len(list(v)) for k, v in groupby(line) if k == " ")

    sep = [(line.index(" " * count) + count) for line, count in max_spaces_dict.items()]
    sep.sort()
    count_dict = {len(list(v)):k for k, v in groupby(sep)}

    if max(count_dict.keys()) < 3:
        return {}, comment

    comment_dict = {}
    # more than 3 lines following the same pattern, extract from it.
    sep_position = count_dict[max(count_dict.keys())] - 1
    debug("found boundary: %s" % sep_position)

    def line_match_pattern(line, position, prev_line=None, next_line=None, recursive=True):
        """
        for a line to match a pattern, its next line or its prev line must
        also match the pattern. Notice that the function would call itself
        to see if its next/prev line matches the pattern. So we used a flag
        to stop it from going deeper into the loop.
        """
        if line.strip() and len(line) <= position + 1:
            return False
        if not (line[position] == " " and line[position+1] != " "):
            # The line itself must match the pattern.
            return False
        if (prev_line is None) and (next_line is None) and recursive:
            print("##### Bad way to call this function. ####")
            return False

        if not recursive:
            # If we do not go deeper, then the current line just match the pattern.
            return True

        if prev_line and prev_line.strip() and not (line_match_pattern(prev_line, position, recursive=False)):
            return False

        if next_line and next_line.strip() and not (line_match_pattern(next_line, position, recursive=False)):
            return False

        return True

    comment_copy = copy(comment)
    for index, line in enumerate(comment_copy):
        if (not line.strip()) or line.find(" ") == -1 or len(line) < sep_position:
            # empty line, or line has no space, or line to short.
            continue
        if index == 0:
            if line_match_pattern(line, sep_position, next_line=comment_copy[1]):
                key = line[:sep_position].strip(STRIPS)
                value = line[sep_position:].strip(STRIPS)
                debug("space || found %s: %s" % (key, value))
                comment_dict[key] = value
                comment.remove(line)
            else:
                debug("First line, but it does not match")
            continue
        elif index == len(comment_copy)-1:
            if line_match_pattern(line, sep_position, prev_line=comment_copy[-1]):
                key = line[:sep_position].strip(STRIPS)
                value = line[sep_position:].strip(STRIPS)
                debug("space || found %s: %s" % (key, value))
                comment_dict[key] = value
                comment.remove(line)
            else:
                debug("last line, but it does not match")
            continue
        elif line_match_pattern(line, sep_position, prev_line=comment_copy[index-1], next_line=comment_copy[index+1]):
            key = line[:sep_position].strip(STRIPS)
            value = line[sep_position:].strip(STRIPS)
            debug("space || found %s: %s" % (key, value))
            comment_dict[key] = value
            comment.remove(line)
    return comment_dict, comment

def parse_keyword_in_comment(comment):
    """Using a predefined keyword list to distinguish keywords from contents."""
    debug("into keyword.")
    debug(comment)
    comment_str = ('\n'.join(comment)).lower()
    comment_dict = {}

    more_keywords = vim.eval("g:BHKeywords")
    keywords = copy(KEYWORDS)
    keywords.update(more_keywords)

    keywords = sorted(
        [keyword for keyword in keywords if comment_str.find(keyword.lower()) != -1],
        lambda x, y: cmp(comment_str.index(x.lower()), comment_str.index(y.lower()))
    )
    debug("Found keywords in the original header: %s" % keywords)
    if not keywords:
        return {}, comment

    def get_content(comment, keyword, next_keyword=None):
        debug("into get content")
        for index, line in enumerate(comment):
            if line.lower().find(keyword.lower()) != -1:
                break

        if next_keyword:
            for jndex, line in enumerate(comment):
                if line.lower().find(next_keyword.lower()) != -1:
                    break
        else:
            jndex = len(comment)
        # content in comment[index:jndex-1], further purify it.
        re.I = True
        line_re = re.compile(r"(?P<key>%s)?:?\s*(?P<value>.*)" % keyword)
        re.I = False
        
        first_line = line_re.match(comment[index]).group('value')
        return '\n'.join([first_line] + comment[index+1:jndex-1])

    for i, keyword in enumerate(keywords):
        if i == len(keywords) - 1:
            comment_dict[keyword] = get_content(comment, keyword)
        else:
            comment_dict[keyword] = get_content(comment, keyword, keywords[i+1])
    return comment_dict, comment

def read_comment(comment):
    """get key-value pairs in the comment and return as a dict."""
    comment_dict = {}

    debug("parse tab in comment.")
    comment_dict_from_tab, comment = parse_tab_in_comment(comment)
    debug("parsed dict: %s." % comment_dict_from_tab)
    comment_dict.update(comment_dict_from_tab)

    debug("parse space in comment.")
    comment_dict_from_space, comment = parse_space_in_comment(comment)
    debug("parsed dict: %s." % comment_dict_from_space)
    comment_dict.update(comment_dict_from_space)

    debug("parse keyword in comment.")
    comment_dict_from_keyword, comment = parse_keyword_in_comment(comment)
    debug("parsed dict: %s." % comment_dict_from_keyword)
    comment_dict.update(comment_dict_from_keyword)
    # keyword based separation.
    return comment_dict

# main functions:
def add_header(force=False):
    """add header for this buffer."""
    print_debug_info()
    if not force:
        if not should_do_write():
            return

        on_enter = vim.eval("exists('b:BHENTERED')")
        if on_enter == '0':
            vim.command("let b:BHENTERED = '1'")
        else:
            # variable exist, this function has been run on this buffer, so quit.
            return

    if not has_header() and suffix_is_supported():
        debug("This buffer do not have any header, add it.")
        prepend_header(render_header())

def modify_header():
    """ we would extract info from sh and py scripts."""

    print_debug_info()
    if not bool(int(vim.eval("g:BHModify"))):
        return

    if not should_do_write():
        debug("should not write this buffer.")
        return

    if not has_header():
        debug("This file has no header.")
        return add_header()

    # only if the suffix is supported and we have a method to strip the comment.
    if not (("extract_comment_%s" % SUFFIX) in globals() and suffix_is_supported()):
        return

    comment = globals()["extract_comment_%s" % SUFFIX]()
    debug("comment: %s" % str(comment))
    if not comment:
        debug("comment is empty")
        return

    comment_dict = {}

    if len(comment) < 3:
        # Less than 3 lines of original comment, put them in Description part.
        comment_dict['Description'] = '\n'.join(comment)
    else:
        comment_dict = read_comment(comment)
    if "" in comment_dict:
        del comment_dict[""]
    new_header_dict = read_comment(globals().get("%s_header" % SUFFIX).rstrip().splitlines())
    debug("new")
    debug(set(new_header_dict.keys()))
    debug(set(comment_dict.keys()))
    debug("end")
    if not set(new_header_dict.keys()) == set(comment_dict.keys()):
        return prepend_header(render_header(comment_dict))
    else:
        debug("do not modify header since we already have the same header.")

def update_header():
    """update data in header with variable substitution."""
    print_debug_info()
    if not should_do_write():
        debug("should not write this buffer.")
        return

    if not (has_header() or suffix_is_supported()):
        # This file do not have a header, or it's format is unknown, quit.
        debug("cannot add header to a script of unknown format.")
        return

    # if current buffer is not modified, do not bother to update it's date.
    if not modified():
        debug("Buffer not modified, just quit")
        return

    row, column = vim.current.window.cursor
    header_template = globals().get("%s_header" % SUFFIX).rstrip()

    # if line has the keyword, find the current for the keyword, get the line, re-render it and fill it in.
    head = CURRENT_BUFFER[:10]
    head_content = '\n'.join(head)

    more_updates = vim.eval("g:BHUpdates")

    update = {
        'Maintained by': AUTHOR,
        'Modified by': AUTHOR,
        'Last modified': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'Filename': FILENAME,
    }
    update.update(more_updates)
    for index, line in enumerate(head):
        for keyword in update:
            if line.find(keyword) != -1:
                original_line = [_line for _line in header_template.splitlines() if _line.find(keyword) != -1]
                if original_line:
                    original_line = original_line[0]
                else:
                    continue
                debug("original line: %s" % original_line)
                debug("line to be replaced: %s" % line)
                rendered_line = original_line % {KEYWORDS[keyword]: update[keyword]}
                debug("rendered line: %s" % rendered_line)
                CURRENT_BUFFER[index] = rendered_line

    vim.current.window.cursor = (row, column)
