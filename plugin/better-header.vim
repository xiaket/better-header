if !has('python')
    " Poor one.
    finish
endif

" Default user. please override this in your vimrc.
if !exists("g:BHAUTHOR")
    let g:BHAUTHOR = 'Your name <yourname@example.com>'
endif

" Enabled suffix. please override in your vimrc, and with each new suffix, 
" set a xx_header in your vimrc.
if !exists("g:BHEnabledSuffix")
    let g:BHEnabledSuffix = ['py', 'sh']
endif

" a list of keywords. which would be recognized.
if !exists("g:BHKeywords")
    let g:BHKeywords = {}
endif

" whether we would update old headers after we opened an existing file.
if !exists("g:BHModify")
    let g:BHModify = "1"
endif

" name your fields to be updated during a buffer write.
if !exists("g:BHUpdates")
    let g:BHUpdates = {}
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

function BHPyWrapper(action, force)
    " use this function to wrap python code, accelerate startup.
    if !exists("g:BHPathFixed")
        let g:BHPathFixed = "0"
    endif

    if g:BHPathFixed == "0"
        py import sys
        " remove current directory, avoid import problems.
        py sys.path = sys.path[1:]
        exe 'python sys.path.insert(0, "' . escape(expand('<sfile>:p:h'), '\') . '")'
        let g:BHPathFixed = "1"
    endif

    py from pylib import add_header, modify_header, update_header
    if a:action == "add"
        if a:force == "true"
           python add_header(force=True)
        else
           python add_header(force=False)
        endif
    elseif a:action == "modify"
        python modify_header()
    elseif a:action == "update"
        python update_header()
    endif
endfunction

augroup betterheader
    " Remove ALL autocommands for the current group.
    autocmd!

    autocmd bufnewfile * :call BHPyWrapper("add", "false")
    autocmd bufread * :call BHPyWrapper("modify", "nouse")
    autocmd bufwritepre * :call BHPyWrapper("update", "nouse")
augroup END

" added a command to write header manually.
command BHeader call BHPyWrapper("add", "true")
command BHChange call BHPyWrapper("modify", "nouse")
