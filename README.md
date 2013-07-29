SCM Prompt
==========

Bash prompt with support for SCM distrubuted systems: **GIT** &amp; **Mercurial**

Features
--------

![Features](http://i.imgur.com/UJeAyy9.png)

- Support for GIT
- Support for Mercurial
- Time on each command
- Return code of last command
- Full path to current working directory
- Indicate in red when running as root

Instalation
-----------

1. Locate `git-remote-hg` script and ensure is executable path. For example, Ubuntu:
    1. Locate: `dpkg -L | grep contrib | grep git-remote-hg`
    2. Make execable: `sudo chmod +x <path_to_git_remote_hg>/git-remote-hg`
    3. Link to bin directory: `sudo ln -s <path_to_git_remote_hg>/git-remote-hg /usr/local/bin/git-remote-hg`
2. Create `.bash` directory: `mkdir -p ~/.bash`
3. `cd ~/.bash`
3. Clone this repository: `git clone https://github.com/wavesoftware/scmprompt.git scmprompt`
4. `cd scmprompt`
5. `git submodule init`
6. `git submodule update`
7. Write `. ~/.bash/scmprompt/scmprompt.sh` to `~/.bashrc`
