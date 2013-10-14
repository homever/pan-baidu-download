#!/usr/bin/env python2
#!coding=utf-8

import sys
import os
import json

from bddown_help import *
from bddown_core import BaiduDown


def execute_command(args=sys.argv[1:]):
    if not args:
        print usage()
        sys.exit(1)

    command = args[0]
    if command.startswith('-'):
        if command in ('-h', '--help'):
            print show_help()
        elif command in ('-V', '-v', '--version'):
            print 'V1.01'
        else:
            usage()
            sys.exit(1)
        sys.exit(0)

    commands = {
        'help':         show_help,
        'download':     download,
        'show':         show,
        'config':       config
    }

    if command not in commands.keys():
        usage()
        sys.exit(1)
    elif '-h' in args or '--help' in args:
        print command_help[args[0]]
    else:
        commands[command](args[1:])


def download(links, limit=None):
    for link in links:
        bd = BaiduDown(link)
        if not limit:
            cmd = "aria2c -c -o '%s' -s5 -x5 %s '%s'" % (bd.filename, limit, bd.link)
        else:
            cmd = "aria2c -c -o '%s' -s5 -x5 '%s'" % (bd.filename, bd.link)
        os.system(cmd)
    sys.exit(0)


def show(links):
    if not len(links):
        print command_help['show']
    for link in links:
        bd = BaiduDown(link)
        print bd.filename, '\n', bd.link, '\n'
    sys.exit(0)


def config(argv):
    try:
        configure = json.load(file('config.json'))
        for i in configure:
            print "%-10s: %s" % (i, configure[i])
        sys.exit(0)
    except IOError, e:
        print sys.stderr >> "config.json不存在"
        print sys.stderr >> "Exception: %s" % str(e)
        sys.exit(1)


if __name__ == '__main__':
    execute_command()