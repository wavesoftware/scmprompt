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
git clone https://github.com/wavesoftware/scmprompt.git ~/.bash/scmprompt
echo '. ~/.bash/scmprompt/scmprompt.sh' >> ~/.bashrc
exec bash -l
```

Copy & Paste install for all users
----------------------------------

```bash
sudo git clone https://github.com/wavesoftware/scmprompt.git /usr/lib/scmprompt
sudo bash -c "echo '. /usr/lib/scmprompt/scmprompt.sh' > /etc/profile.d/scmprompt.sh"
exec bash -l
```

Update to newest version
------------------------

```bash
cd <scmprompt-dir>
git pull
```

