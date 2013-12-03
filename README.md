SCM Prompt
==========

Bash prompt with support for SCM distrubuted systems: **GIT** &amp; **Mercurial**

Features
--------

![Features](http://i.imgur.com/UJeAyy9.png)

- Support for GIT
- Support for Mercurial
- Pull and Push indicator
- New, Added, Modificated and Conflicts indicators
- Time on each command
- Return code of last command
- Full path to current working directory
- Indicate in red when running as root

Instalation
-----------

1. Create `.bash` directory: `mkdir -p ~/.bash`
2. `cd ~/.bash`
3. Clone this repository: `git clone https://github.com/wavesoftware/scmprompt.git scmprompt`
4. Install into your Bash RC: `echo '. ~/.bash/scmprompt/scmprompt.sh' >> ~/.bashrc`

Copy & Paste install
--------------------

```bash
mkdir -p ~/.bash
cd ~/.bash
git clone https://github.com/wavesoftware/scmprompt.git scmprompt
echo '. ~/.bash/scmprompt/scmprompt.sh' >> ~/.bashrc
```

Update to newest version
------------------------

```bash
cd ~/.bash/scmprompt
git pull
```

