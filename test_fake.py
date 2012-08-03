
from lib.novatest import NovaEC2Test
from random import random
import time

class Fake(NovaEC2Test):
    def main(self):
        _result = False
        sw = self.get_stopwatch()
        time_to_done = None
        if time.sleep(2 + random()) == None:
            time_to_done = sw.stop()
            _result = True
        self.add_result(test_name=self.__class__.__name__, result=_result, time_to_done=time_to_done)

if __name__ == '__main__':
    o = Fake()
    o.main()
    o.emit_results()

