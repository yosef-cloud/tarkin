import time
from lib.sshtest import SSHInstanceTest
from lib.common import checkpingaddr

class FloatingAssociate(SSHInstanceTest):
    def main(self):
        _assoc_result = False
        _ping_result = False
        _release_result = False
        _disassoc_result = False

        keyname = self.get_new_key_pair()
        instance = self.setup_pingable_instance(keyname)
        self.log("Launching instance")
        if instance:
           time.sleep(5)
           self.log("Attempt to setup floating IPs for instance %s" % instance)
           try:
               addr = self.allocate_address()
               self.log("Allocated ip %s " % addr.public_ip)
               if addr.public_ip:
                   self.log("Associate ip %s to instance %s" % (addr.public_ip, instance))
                   if self.associate_address(instance, addr.public_ip):
                       _assoc_result = True

                       time.sleep(5)

                       # try and ping after some period of time
                       instance.update()

                       self.log("Ping instance at %s" % addr.public_ip)
                       if checkpingaddr(addr.public_ip):
                           _ping_result = True 

                       # disassociate address
                       self.log("Disassociate address: %s " % addr.public_ip)
                       self.disassociate_address(addr.public_ip)

                       time.sleep(1)
                       self.log("Release address: %s " % addr.public_ip)
                       self.release_address(addr.public_ip)

                       time.sleep(1)
                       self.log("Get all addresses and make sure dissociated and released")
                       addrs = self.get_all_addresses()

                       if not addr.public_ip in [x.public_ip for x in addrs]:
                           _release_result = True

                       if len([x.instance_id for x in addrs if x.public_ip == addr.public_ip]) == 0:
                           _disassoc_result = True
 
           except Exception, e:
               print e.message
           
           self.terminate(instance)
           self.delete_key_pair(keyname)
           # delete keypair
        self.add_result(test_name=self.__class__.__name__+'assoc', result=_assoc_result)
        self.add_result(test_name=self.__class__.__name__+'ping', result=_ping_result)
        self.add_result(test_name=self.__class__.__name__+'release', result=_release_result)
        self.add_result(test_name=self.__class__.__name__+'disassoc', result=_disassoc_result)

if __name__ == '__main__':
    o = FloatingAssociate()
    o.main()
    o.emit_results()

