
from lib.novatest import NovaEC2Test

class SpawnSpeed(NovaEC2Test):
    """Uses counter to measure average spawn speed per node"""
    def main(self):
        self.connect_api()
        _result = False
        instance = self.launch_instance(inst_type='m1.large')
        sw = self.get_stopwatch()
        time_till_running = None
        time_till_ping = None
        if self.block_until_running(instance):
            time_till_running = sw.stop()
            if self.block_until_ping(instance):
                time_till_ping = sw.stop()
                _result = True
        self.add_result(test_name=self.__class__.__name__, result=_result, time_till_running=time_till_running, time_till_ping=time_till_ping, ip=instance.private_ip_address)
        host=None
	if _result:
   	    host = '.'.join(instance.private_ip_address.split('.')[:2])
	    self.counter_increment(**{"VM_count-%s" % host: 1,"time_till_ping-%s" % host: time_till_ping})
        self.terminate(instance)

if __name__ == '__main__':
    o = SpawnSpeed()
    o.main()
    o.emit_results()
    o.emit_counters()
