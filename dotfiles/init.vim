set tabstop=2
set shiftwidth=2
set expandtab
set smartindent

" round indentation to multiples of 'shiftwidth' when shifting text
" (so that it behaves like Ctrl-D / Ctrl-T):
set shiftround

" reproduce the indentation of the previous line:
set autoindent
" keep indentation produced by 'autoindent' if leaving the line blank:
"set cpoptions+=I
" a stricter alternative which works better for the C language:
"set cindent
" use language‐specific plugins for indenting (better):
filetype plugin indent on
