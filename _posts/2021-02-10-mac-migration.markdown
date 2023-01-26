---
title: "MacBook migration"
layout: post
date: 2021-02-10 11:20
image: /assets/images/ciguena.jpg
tag:
- Apple
- Mac
- Time-saving
- Tools
category: blog
author: jaime
---

I just got a new laptop after 7 years holding to my old Mac. I changed is hard drive few years ago after an unfortunate soft-drink spill, I put some nice stickers on it, changed its battery even. Lately it has been slowing down just too much and is lacking space and power, so it was time to get a new one. I postponed the migration cause I have many installed brew formulae (or formulas?), tweaked `rc` files and little bits of configuration here and there that I was worried I would lose.

I didn't want to use TimeMachine cause it has sometimes failed to back up, sometimes getting stuck on "preparing backup", a problem that pops up every year when Apple releases a new macOS software update. I also have a lot of rubbish on the desktop that I have not yet filtered out, I don't want to back that up and I don't want to obsessively clean my desktop either.

### Basic Expectations

Ultimately I would like to back up my installed applications with `brew` and `mac`, my `.tmux`, `.tigrc`, `.vimrc`, `bash_profile` and other configurations that took me so long to tweak to my liking. As well as other settings that I am not aware of but that affect the behaviour of the applications I use.

I would also like to keep a folder named `/code` where I keep a series of subfolders with repositories to github and gitlab. I would like to save some script files under `/usr/bin` as well.

### New Installation

I will write now the steps I followed using the following tools: [brew](http://brew.sh), [pip3](https://pip.pypa.io/en/stable/installing/), [mackup](https://github.com/lra/mackup), [rsync](https://linux.die.net/man/1/rsync). The assumption is that you have them installed.

The original MacBook will be called *M1* and the new one *M2*. Let's start with your applications.

Brew is not only THE package manager on Mac but also a tool that allows you to set up your Mac to a known configuration. It uses a feature called **bundle** that allows you to backup your configuration to a file and use it on another computer. On M1 run:

```sh
brew bundle dump --file=~/Dropbox/brewfile
```

That will dump the configuration on a file in Dropbox and will sync it on M2. You may use whichever mechanism you want to sync that file, throughout this tutorial I use only Dropbox.

The contents of the Brewfile look like below and contain [mas](https://github.com/mas-cli/mas) applications too!. You may also spend some time deleting formulae or apps you don't use anymore.

```sh
# It has common taps
tap "homebrew/bundle"
tap "homebrew/cask"
#etc
# ... brew formulae
brew "alpine"
brew "docbook"
#etc
# ... and mas applications
mas "Keynote", id: 409183694
mas "Kindle", id: 405399194
mas "Slack", id: 803453959
mas "Xcode", id: 497799835
#etc
```

On M2 simply run the command below and it will install everything, prompting you when user confirmation is needed. Be patient as the installation will take several minutes.

```sh
brew bundle -vf ~/Dropbox/brewfile
``` 

We may have installed some python packages on M1 that we want to move to M2. Pip allows you to export the current environment, just use **pip3** and dump everything on a pipfile:

```sh
pip3 freeze > ~/Dropbox/pipfile
```

On M2 you can install the packages again using that file:

```sh
pip3 install -r ~/Dropbox/pipfile
```

Now we want to install the configuration files that we took time to polish. For that we will use **mackup**. 

On M1 run `mackup backup` to backup your dotfiles. You will see your home folder now has symlinks to the backup, in my case I use Dropbox but there are other options.

```sh
 0 drwxr-xr-x   3 jaime  staff     96 Feb  9 21:53 .tmux/
 0 lrwxr-xr-x   1 jaime  staff     40 Feb  9 12:15 .tmux.conf@ -> /Users/jaime/Dropbox/Mackup/.tmux.conf
 0 drwxr-xr-x   5 jaime  staff    160 Feb  9 12:15 .vim/
24 -rw-------   1 jaime  staff  11526 Feb 10 10:40 .viminfo
 0 lrwxr-xr-x   1 jaime  staff     36 Feb  9 12:15 .vimrc@ -> /Users/jaime/Dropbox/Mackup/.vimrc
 0 drwxr-xr-x   4 jaime  staff    128 Feb 10 10:12 .vscode/
 0 lrwxr-xr-x   1 jaime  staff     40 Feb  9 12:15 .wget-hsts@ -> /Users/jaime/Dropbox/Mackup/.wget-hsts
 0 lrwxr-xr-x   1 jaime  staff     37 Feb  9 12:15 .yarnrc@ -> /Users/jaime/Dropbox/Mackup/.yarnrc
```

Now on M2 run `mackup restore`. That's it, now your vim configuration is back how it was on M1, your settings for emacs... whatever you have tweaked. 

Lastly, it might be that we have some folders we want a hard copy off. You can of course move them around with a USB or something, but with one command you might do exactly thr same thing. 

In my case I have a folder structure nested from one root folder called `/code`. I keep everything there, code or not, usually on git repositories. It looks like this:

```sh
└── code
    ├── ASDF
    ├── CBOR
    ├── COAP-EXPLORER
    ├── CORE
```

Inside each capitalized folder I keep repositories, for example for ASDF:

```sh
ASDF ~ tree
.
├── 2020-10-12-hallway
│   ├── ASDF-2020-10-12-unoffical-hallway-01.pdf
│   ├── README.md
│   ├── onedm-asdf-hallway-2020-10-12-gaps-and-proposed-features.pdf
│   └── slides
│       └── ASDF-2020-10-12-SDF-intro.pdf
├── SDF
│   ├── README.md
│   ├── sdf-feature.cddl
│   ├── sdf-framework.cddl
│   ├── sdf-framework.jso.json
│   ├── sdf-validation.cddl
│   ├── sdf-validation.jso.json
│   ├── sdf.html
│   ├── sdf.jso.json-unidiff
│   ├── sdf.md
│   └── sdf.txt
```

Therefore what I want is to simply copy everything as it is from M1 to M2. For that we have the fantastic tool called **rsync**. Remote Sync or rsync allows you to transfer, mirror, sync or compress files and it's the most common tool to move files from one server to another (over ssh). 

Both machines are on the same wifi, with M2 having 192.168.1.3 as IP address. I just run the command:

```sh
rsync -av ~/code/ 192.168.1.3:jaime/
```

That will copy all folders, git branches and configurations as they are to the new Mac over wifi. Which I find pretty fast and cool.

There might be other little quirks and things to be done but after this, your new Mac has the same applications, files and configurations as the old one. 

### TL,DR

Run this on M1:
```sh
brew bundle dump --file=~/Dropbox/brewfile
pip freeze > ~/Dropbox/pipfile
```

This on M2:
```sh
brew bundle -vf ~/Dropbox/Brewfile
pip install -r ~/Dropbox/pipfile
```

And this on M1 again:
```sh
rsync -av ~/code/ 192.168.1.3:jaime/
```
