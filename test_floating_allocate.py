import re
import time
import traceback

from lib.sshtest import SSHInstanceTest

class FloatingAllocate(SSHInstanceTest):

    def main(self):
        _allocate_result = False
        _release_result = False

        try:
            addr = self.allocate_address()
            if addr.public_ip:
                _allocate_result = True
                self.release_address(address=addr.public_ip)
                _release_result = True
            
        except Exception, e:
            self.log(e.message)
            tb = traceback.format_exc()
            self.log(tb)

        self.add_result(test_name=self.__class__.__name__+'_allocate', result=_allocate_result)
        self.add_result(test_name=self.__class__.__name__+'_release', result=_release_result)

if __name__ == '__main__':
    o = FloatingAllocate()
    o.main()
    o.emit_results()


