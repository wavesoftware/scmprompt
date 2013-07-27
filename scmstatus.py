#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

# change those symbols to whatever you prefer
symbols = {'ahead of': '↑·', 'behind': '↓·', 'prehash':':'}

from subprocess import Popen, PIPE

import sys
import os.path

lib_dir = os.path.dirname(sys.argv[0])
current_dir = os.path.realpath(os.path.curdir)

def get_distance(dir):
    return 0
def get_distance_git():
    return get_distance('.git')
def get_distance_hg():
    return get_distance('.hg')
def get_git():
    gitsym = Popen(['git', 'symbolic-ref', 'HEAD'], stdout=PIPE, stderr=PIPE)
    branch, error = gitsym.communicate()

    error_string = error.decode('utf-8')

    if 'fatal: Not a git repository' in error_string:
        return None

    branch = branch.decode('utf-8').strip()[11:]

    res, err = Popen(['git','diff','--name-status'], stdout=PIPE, stderr=PIPE).communicate()
    err_string = err.decode('utf-8')
    if 'fatal' in err_string:
        return None
    changed_files = [namestat[0] for namestat in res.splitlines()]
    staged_files = [namestat[0] for namestat in Popen(['git','diff', '--staged','--name-status'], stdout=PIPE).communicate()[0].splitlines()]
    nb_changed = len(changed_files) - changed_files.count('U')
    nb_U = staged_files.count('U')
    nb_staged = len(staged_files) - nb_U
    staged = str(nb_staged)
    conflicts = str(nb_U)
    changed = str(nb_changed)
    nb_untracked = len(Popen(['git','ls-files','--others','--exclude-standard'],stdout=PIPE).communicate()[0].splitlines())
    untracked = str(nb_untracked)
    if not nb_changed and not nb_staged and not nb_U and not nb_untracked:
        clean = '1'
    else:
        clean = '0'

    remote = ''

    if not branch: # not on any branch
        branch = symbols['prehash']+ Popen(['git','rev-parse','--short','HEAD'], stdout=PIPE).communicate()[0][:-1]
    else:
        remote_name = Popen(['git','config','branch.%s.remote' % branch], stdout=PIPE).communicate()[0].strip()
        if remote_name:
            merge_name = Popen(['git','config','branch.%s.merge' % branch], stdout=PIPE).communicate()[0].strip()
        else:
            remote_name = "origin"
            merge_name = "refs/heads/%s" % branch

        if remote_name == '.': # local
            remote_ref = merge_name
        else:
            remote_ref = 'refs/remotes/%s/%s' % (remote_name, merge_name[11:])
        revgit = Popen(['git', 'rev-list', '--left-right', '%s...HEAD' % remote_ref],stdout=PIPE, stderr=PIPE)
        revlist = revgit.communicate()[0]
        if revgit.poll(): # fallback to local
            revlist = Popen(['git', 'rev-list', '--left-right', '%s...HEAD' % merge_name],stdout=PIPE, stderr=PIPE).communicate()[0]
        behead = revlist.splitlines()
        ahead = len([x for x in behead if x[0]=='>'])
        behind = len(behead) - ahead
        if behind:
            remote += '%s%s' % (symbols['behind'], behind)
        if ahead:
            remote += '%s%s' % (symbols['ahead of'], ahead)

    if remote == "":
        remote = '.'

    out = [
        'git',
        str(branch),
        str(remote),
        staged,
        conflicts,
        changed,
        untracked,
        clean
    ]
    return out
def get_hg():
    hgprompt = os.path.join(lib_dir, 'hg-prompt', 'prompt.py')
    hg_rev, hg_branch = Popen('hg id -b -n', stdout=PIPE, shell=True).communicate()[0].strip().split(" ")
    hg_rev = hg_rev.replace('+', '←').strip('←')
    try:
        hg_rev = int(hg_rev)
        if hg_rev < 0:
            return None
        hg_rev = str(hg_rev)
    except:
        pass
    hg_counts_cmd = 'hg status | grep -v \'.orig\'| awk \'{arr[$1]+=1} END {for (i in arr) {print i,arr[i]}}\''
    hg_counts = {
        'S': 0, #staged,
        'X': 0, #conflicts,
        'M': 0, #changed,
        '?': 0, #untracked,
        'C': 1  #clean
    }
    if hg_rev.find('←') >= 0:
        hg_counts['X'] = int(Popen('hg resolve --list | wc -l', stdout=PIPE, shell=True).communicate()[0].strip())
    for line in Popen(hg_counts_cmd, stdout=PIPE, shell=True).communicate()[0].strip().split("\n"):
        if line == '':
            continue
        hgst, count = line.split()
        hgst = hgst.replace('!', '?')
        hgst = hgst.replace('A', 'S')
        hgst = hgst.replace('R', 'S')
        hg_counts[hgst] += int(count)
        hg_counts['C'] = 0
    
    if (hg_counts['X']) > 0:
        hg_counts['M'] -= hg_counts['X']
    ahead = 0
    behind = 0
    hg_status = 'hg --config extensions.prompt=%s prompt \'{incoming|count},{outgoing|count}\'' % hgprompt
    hg_status = Popen(hg_status, stdout=PIPE, shell=True).communicate()[0].strip().split(",")
    ahead = hg_status[1]
    behind = hg_status[0]
    if ahead == '':
        ahead = 0
    if behind == '':
        behind = 0
    remote = ''
    if behind:
        remote += '%s%s' % (symbols['behind'], behind)
    if ahead:
        remote += '%s%s' % (symbols['ahead of'], ahead)

    if remote == "":
        remote = '.'
    
    out = [
        'hg',
        '%s:%s' % (hg_branch, hg_rev),
        remote,
        str(hg_counts['S']), #staged,
        str(hg_counts['X']), #conflicts,
        str(hg_counts['M']), #changed,
        str(hg_counts['?']), #untracked,
        str(hg_counts['C'])  #clean
    ]
    return out

git = get_git()
hg = get_hg()
out = None
if git == None and hg == None:
    sys.exit(0)
if git == None and hg != None:
    out = hg
if git != None and hg == None:
    out = git        
if git != None and hg != None:
    gint = get_distance_git()
    hint = get_distance_hg()
    if gint < hint:
        out = git
    else:
        out = hg
print("\n".join(out))
