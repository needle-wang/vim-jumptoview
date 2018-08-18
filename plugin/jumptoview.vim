" File:          jumptoview.vim
" Author:        needle wang<needlewang2011@gmail. com

let s:save_cpo = &cpo
set cpo&vim

if exists("loaded_jumptoview")
    finish
endif
let loaded_jumptoview = 1

if !exists('g:jumptoview_patterns_prefix')
    let g:jumptoview_patterns_prefix = ''
endif

if !exists('g:jumptoview_template_prefix')
    let g:jumptoview_template_prefix = 'templates'
endif

if !exists('g:jumptoview_grep_cmd')
    let g:jumptoview_grep_cmd = 'vimgrep'
endif

if !exists('g:jumptoview_open_cmd')
    let g:jumptoview_open_cmd = 'tabnew'
endif

python3 << EOF

import vim
from jumptoview import get_view_from_url

def gotoview():
    line = vim.current.line
    settings = {}
    settings['buffername'] = vim.current.buffer.name
    settings['grep'] = vim.eval('g:jumptoview_grep_cmd')
    settings['open'] = vim.eval('g:jumptoview_open_cmd')
    settings['templates'] = vim.eval('g:jumptoview_template_prefix')
    settings['prefix'] = vim.eval('g:jumptoview_patterns_prefix')
    vim.command(get_view_from_url(line, settings))

EOF

autocmd FileType python nnoremap <silent> gO :py3 gotoview()<CR>

let &cpo = s:save_cpo
