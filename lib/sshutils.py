import os
import sys
import socket
import subprocess


class SSHCommand():
    def __init__(self, key_path):
        self.key_path = key_path

    def cmdexec(self, remote_host, cmd):
        ssh_cmd = "ssh  -t -o CheckHostIP=no -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ubuntu@%s -i %s %s" % (remote_host, self.key_path, cmd)
        output = subprocess.check_output(ssh_cmd, shell=True,
            stderr=subprocess.STDOUT)
        return (output,'','')

if __name__ == '__main__':
    if len(sys.argv) > 0:
        key_path = sys.argv[1]
    else:
        key_path = '/root/test.pem'
    
    sc = SSHCommand(key_path)
    print sc.cmdexec("10.50.0.6", "uptime")




