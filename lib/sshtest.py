import random
import string
import time

import subprocess

from novatest import NovaEC2Test
from sshutils import SSHCommand

DEFAULT_INSTANCE_TYPE = 'm1.tiny'

class SSHInstanceTest(NovaEC2Test):
    def __init__(self):
        NovaEC2Test.__init__(self)
        self.kp_path = None
        self.connect_api()
        
    def get_new_key_pair(self):
        kn = 'tk'+''.join([random.choice(string.ascii_lowercase+string.digits) for _ in range(8)])
        kp =  self.create_key_pair(kn)
        kp.save('/tmp/')
        return kn

    def setup_pingable_instance(self, key_name=None, **argv):
        """ This implementation waits till VM is pingable """

        # insert key shit
        instance = self.launch_instance(key_name=key_name, **argv)
        if self.block_until_running(instance) and self.block_until_ping(instance):
            self.log('instance %s is pingable' % instance.id)
            return instance
        else:
            self.log('instance %s is NOT pingable' % instance.id)
            return None



    def setup_ssh_instance(self, key_name=None, **argv):
        """ This implementation waits till VM is ssh ready"""

        # insert key shit
        instance = self.launch_instance(key_name=key_name, **argv)
        if (self.block_until_running(instance) and 
           self.block_until_ping(instance) and 
           self.block_until_ssh(instance, key_name)):
            self.log('instance %s is pingable' % instance.id)
            return instance
        else:
            self.log('instance %s is NOT pingable' % instance.id)
            return None

 
    def ssh_cmd_simple(self, instance, key_name, cmd):
        ssh = SSHCommand('/tmp/%s.pem' % key_name)
        self.log('Sending command [%s] to %s' % (cmd, instance.private_ip_address))
        return ssh.cmdexec(instance.private_ip_address, cmd)

    # todo: cleanup the /tmp files        
    

    def block_until_ssh(self, instance, key_name, timeout=300):
        start_time = time.time()
        result = False
        while(time.time() < start_time + timeout):
            try:
                if self.ssh_cmd_simple(instance, key_name, "true"):
                    result = True
                    break
                else:
                    time.sleep(1)
            except subprocess.CalledProcessError, e:
                time.sleep(1)
        return result


