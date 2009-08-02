#!/usr/bin/env python
# encoding: utf-8
"""
Example of Paramiko's SFTP
"""
import sys
import os
import paramiko

def get_host_key(host):
    hostkeytype = None
    hostkey = None
    # try to load host key from known hosts
    try:
        host_keys = paramiko.util.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))
    except IOError:
        host_keys = {}
    if host in host_keys:
        hostkeytype = host_keys[host].keys()[0]
        hostkey = host_keys[host][hostkeytype]
    return hostkeytype, hostkey

def get_private_key(keyfile=None):
    key = None
    keytype = None
    if keyfile is None:
        keyfiles = [os.path.expanduser('~/.ssh/id_%s' % keytype) for keytype in ('dsa', 'rsa')]
    else:
        keyfiles = [keyfile,]
    for kf in keyfiles:
        try:
            key = paramiko.RSAKey.from_private_key_file(kf)
            keytype = 'ssh-rsa'
        except (IOError, paramiko.SSHException), e:
            try:
                key = paramiko.DSSKey.from_private_key_file(kf)
                keytype = 'ssh-dsa'
            except (IOError, paramiko.SSHException), e:
                pass
    if key is None:
        raise paramiko.SSHException('No rsa or dsa keys are available: %s' % e)
    return keytype, key

def get_remote_file(user, host, path, pkeyfile=None):
    hostkeytype, hostkey = get_host_key(host)
    userkeytype, userkey = get_private_key(pkeyfile)
    t = paramiko.Transport((host, 22))
    t.connect(hostkey=hostkey, username=user, pkey=userkey)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(path, os.path.basename(path))
    t.close()

def main(args):
    if len(args) < 3:
        print "sftp.py <user> <host> <remote_path> [pkey]"
        sys.exit(1)
    else:
        user = args[0]
        host = args[1]
        path = args[2]
        if len(args) == 4:
            pkey = args[3]
        else:
            pkey = None
    print "Retrieving %s@%s:%s" % (user, host, path)
    get_remote_file(user, host, path, pkey)

if __name__ == '__main__':
    main(sys.argv[1:])
