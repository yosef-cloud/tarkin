import re
import time
from lib.sshtest import SSHInstanceTest

class InstanceIO(SSHInstanceTest):
    def main(self):
        _result = False

        keyname = self.get_new_key_pair()
        self.log('Set up instance')
        instance = self.setup_ssh_instance(keyname, inst_type='m1.large')
        bonnie_time=None
        host=None
        if instance:
            output = self.ssh_cmd_simple(instance, keyname, 'sudo apt-get install -y bonnie++')
            self.log(output)
        
            sw = self.get_stopwatch()
            output = self.ssh_cmd_simple(instance, keyname, 'bonnie++')
            bonnie_time = sw.stop()
            self.log(output)
            if len(output[0])>40:
                _result = True
            if _result:
                host = '.'.join(instance.private_ip_address.split('.')[:2])
                self.counter_increment(**{"VM_count_bonnie-%s" % host: 1,"bonnie_time-%s" % host: bonnie_time})
            self.terminate(instance)
            self.delete_key_pair(keyname)
 


           # delete keypair
        self.add_result(test_name=self.__class__.__name__, result=_result,bonnie_time=bonnie_time, host=host)


if __name__ == '__main__':
    o = InstanceIO()
    o.main()
    o.emit_results()
    o.emit_counters()
