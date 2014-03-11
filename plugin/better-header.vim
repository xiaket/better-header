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

augroup betterheader
    " call these function when these events are triggered.
    autocmd!
    py import sys
    exe 'python sys.path.insert(0, "' . escape(expand('<sfile>:p:h'), '\') . '")'
    py from pylib import add_header, modify_header, update_header
    autocmd bufnewfile * python add_header()
    autocmd bufread * python modify_header()
    autocmd bufwritepre * python update_header()
augroup END

" added a command to write header manually.
command BHeader python add_header(force=True)
command BHChange python modify_header()
