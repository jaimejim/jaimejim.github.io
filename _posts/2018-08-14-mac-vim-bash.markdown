---
title: "Vim and Bash Profiles Setup"
layout: post
date: 2018-08-14 18:14
image: /assets/images/disaster.jpg
tag:
- Apple
- Mac
- Vim
- Time-saving
blog: true
star: true
---

A month ago my Mac SSD drive died due to a water spill. Apparently this is a common problem that will manifest itself even if in a [delayed fashion](https://www.ifixit.com/Wiki/MacBook_water_damage_-_The_definitive_guide). That is, if the spill does not automatically destroy your computer, like it did to mine, the corrosion process will occur when you combine electricity, metal, water and oxygen. it might take a week or two, but it does happen.

In my case it immediately killed the SSD drive (which is exposed in Mac) and forced me to replace it. While [Time Machine](https://en.wikipedia.org/wiki/Time_Machine_(macOS)) works pretty well, in my case I hadn't set it up properly and "*Back up while on battery power was not enabled*", thus losing few months worth of material. Nevertheless this was useful to do a fresh installation and reset of common configuration files like **.vimrc**, **.bash_profiles**. I thought of leaving them here in case someone is curious, together with the brew formulae I find fundamental:



``` bash
#.bash_profile

##########
# Terminal
##########

alias ln='ln -v'
alias ...='../..'
alias ..='cd ..'
alias ...='cd ../../../'
alias ....='cd ../../../../'
alias .....='cd ../../../../'
alias l='ls'
alias l.='ls -d .* --color=auto'
alias lh='ls -Alh'
alias h="history | cut -c 8-"
alias cp='cp -iv'
alias mv='mv -iv'
alias mkdir='mkdir -pv'
alias ll='ls -FGlAhp'
alias less='less -FSRXc'
alias c='clear'

######
# GIT
######

# git status
alias gs='git status'
# copy the current branch name
alias gcb='git rev-parse --abbrev-ref HEAD | pbcopy'
# open a pull request, requires Hub to be installed (hub.github.com)
alias gpr='git request-pull'
# open url of the current repository
alias gh="git-open"
# Pull all files from underlying repositories
# alias pa='/usr/local/bin/git-pull-all'
alias pa='~/../../usr/local/bin/git-pull-all'

##########
# Assorted
##########

# PDF to TEXT on folder
alias pdf-all='find . -name \*.pdf -exec pdftotext "{}" \;'

# Todo lists
alias todo="todotxt-machine"

# Autojump with j
[ -f /usr/local/etc/profile.d/autojump.sh ] && . /usr/local/etc/profile.d/autojump.sh

# DOCKER commands
alias dstop='docker stop $(docker ps -a -q)'
alias dremove='docker rm $(docker ps -a -q)'

# Better diff
alias diff='colordiff'

# Brew cleanup
alias brewup='brew update; brew upgrade; brew prune; brew cleanup; brew doctor'

##############
# Network Info
##############

# netCons:      Show all open TCP/IP sockets
alias netCons='lsof -i'             
# lsock:        Display open sockets
alias lsock='sudo /usr/sbin/lsof -i -P'   
# lsockU:       Display only open UDP sockets
alias lsockU='sudo /usr/sbin/lsof -nP | grep UDP'
# lsockT:       Display only open TCP sockets
alias lsockT='sudo /usr/sbin/lsof -nP | grep TCP'
# ipInfo0:      Get info on connections for en0
alias ipInfo0='ipconfig getpacket en0'
# ipInfo1:      Get info on connections for en1
alias ipInfo1='ipconfig getpacket en1'        
# openPorts:    All listening connections
alias openPorts='sudo lsof -i | grep LISTEN'
# showBlocked:  All ipfw rules inc/ blocked IPs
alias showBlocked='sudo ipfw list'

###########
# Colouring
###########

# Add color to ls
export CLICOLOR=1
export LSCOLORS=Exfxcxdxbxegedabagacad

# Tell grep to highlight matches
export GREP_OPTIONS='--color=auto'

# Shell color
export TERM="xterm-color"
PS1='\[\e[0;33m\]\u\[\e[0m\]@\[\e[0;32m\]\h\[\e[0m\]:\[\e[0;34m\]\w\[\e[0m\]\$ '

```

``` vim
# .vimrc

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 " Quick Shortcuts:
 "   ,w    : save
 "   ,q    : quit
 "   j j   : exit insert
 "    *    : search current word
 " space   : search forwards
 " , space : search back
 "   , tn  : new tab
 "   ,tc   : close tab
 "   ,tl   : toggle
 "   ,te   : open in this path
 "   ,ss   : enable spell check
 "    F3   : Paste Mode
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" With a map leader it's possible to do extra key combinations
" like <leader>w saves the current file
let mapleader = ","
let g:mapleader = ","

" Fast saving
nmap <leader>w :w!<cr>

" Fast quitting
nmap <leader>q :q<cr>

" Mapping jj to Escape form Insert Mode
:imap jj <Esc>


let g:rehash256 = 1
let g:molokai_original = 1
" colorscheme molokai
" colorscheme spring-night

" Activate pathogen
execute pathogen#infect()
syntax on
filetype plugin indent on

" Enable neocomplete
let g:neocomplete#enable_at_startup = 1

" Saves when focus is lost
set autowrite

" Set to auto read when a file is changed from the outside
set autoread

" Enable syntax highlighting
syntax enable


" Map <Space> to / (search) and <Space>-<Space> to ? (backwards search)
map <space> /
map <leader><space> ?


""""""""""""""""""""""""""""""
" => Markdown Section
""""""""""""""""""""""""""""""
au BufNewFile,BufFilePre,BufRead *.md set filetype=markdown

""""""""""""""""""""""""""""""
" => Golang Section
""""""""""""""""""""""""""""""
" \t => go test
autocmd FileType go nmap <leader>t  <Plug>(go-test)

" \r => go run
autocmd FileType go nmap <leader>r  <Plug>(go-run)

" run :GoBuild or :GoTestCompile based on the go file (i.e., src or test)
function! s:build_go_files()
  let l:file = expand('%')
  if l:file =~# '^\f\+_test\.go$'
    call go#cmd#Test(0, 1)
  elseif l:file =~# '^\f\+\.go$'
    call go#cmd#Build(0)
  endif
endfunction

autocmd FileType go nmap <leader>b :<C-u>call <SID>build_go_files()<CR>

autocmd FileType go nmap <leader>c <Plug>(go-coverage)

autocmd FileType go nmap <leader>d <Plug>(go-def)

autocmd FileType go nmap <leader>gb <Plug>(go-doc-browser)

au FileType go nmap <leader>e <Plug>(go-rename)

" let all lists be of type quickfix
let g:go_list_type = "quickfix"

" when formatting on save, also make the necessary fixes to the import decl
let g:go_fmt_command = "goimports"

autocmd BufNewFile,BufRead *.go setlocal noexpandtab tabstop=4 shiftwidth=4

" golang tagbar
let g:tagbar_type_go = {  
    \ 'ctagstype' : 'go',
    \ 'kinds'     : [
        \ 'p:package',
        \ 'i:imports:1',
        \ 'c:constants',
        \ 'v:variables',
        \ 't:types',
        \ 'n:interfaces',
        \ 'w:fields',
        \ 'e:embedded',
        \ 'm:methods',
        \ 'r:constructor',
        \ 'f:functions'
    \ ],
    \ 'sro' : '.',
    \ 'kind2scope' : {
        \ 't' : 'ctype',
        \ 'n' : 'ntype'
    \ },
    \ 'scope2kind' : {
        \ 'ctype' : 't',
        \ 'ntype' : 'n'
    \ },
    \ 'ctagsbin'  : 'gotags',
    \ 'ctagsargs' : '-sort -silent'
\ }

nmap <F8> :TagbarToggle<CR>

" clang-format short-cut
"map <C-K> :pyf /Users/tfossati/bin/clang-format.py<cr>
"imap <C-K> <c-o>:pyf /Users/tfossati/bin/clang-format.py<cr>

autocmd BufNewFile,BufRead *.{c,cpp,h} setlocal expandtab tabstop=2 shiftwidth=2

""""""""""""""""""""""""""""""
" => Other Vim Settings
""""""""""""""""""""""""""""""
set ruler

" airline smart tab line
let g:airline#extensions#tabline#enabled = 1

```

``` sh

:~/$ brew list
autojump	gdbm		hub		lynx		p11-kit		tig
bash-completion	gettext		icu4c		mackup		python		tree
cask		ghi		libffi		nettle		python@2	wget
colordiff	git		libidn2		nmap		readline	xz
coreutils	gmp		libtasn1	node		ripgrep
emacs		gnutls		libunistring	openssl		sqlite

```
