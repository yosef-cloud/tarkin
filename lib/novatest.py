import boto
import json
import time

from basetest import BaseTest
import common as utils


# important eventlet stuff
from eventlet import patcher
patcher.monkey_patch(all=True)

DEFAULT_INSTANCE_TYPE = 'm1.tiny'

class NovaEC2Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.ec2_conn = None
        
        pass

    def connect_api(self):
        self.log('Connect to EC API')
        self.ec2_conn = boto.connect_ec2(**utils.get_rc_credentials())

    def get_images(self):
        return self.ec2_conn.get_all_images()

    def get_first_ami(self):
        images = self.get_images()
        for i in images:
            if i.type == 'machine':
                return i

    def get_image(self, ami_name):
        return self.ec2_conn.get_image(ami_name)                

    def launch_instance(self, ami_name=None, inst_type=DEFAULT_INSTANCE_TYPE, key_name=None, security_groups=None):
        if not ami_name:
            self.log('AMI not provided for test, picking first one')
            ami = self.get_first_ami()
        else:
            ami = self.get_image(ami_name)
            self.log('AMI specified %s' % str(ami))

        reservation = ami.run(instance_type=inst_type, key_name=key_name, security_groups=security_groups)
        self.log('New instance: %s' % str(reservation.instances[0]))
        return reservation.instances[0]

    def get_instance_status(self, instance):
        instance.update()
        return instance.state

    def block_until_running(self, instance, timeout=300):
        start_time = time.time()
        result = False
        while(time.time() < start_time + timeout):
            if self.get_instance_status(instance) == 'running':
                result = True
                break
            else:
                time.sleep(1)
        return result

    def block_until_ping(self, instance, timeout=300):
        start_time = time.time()
        result = False
        while(time.time() < start_time + timeout):
            if utils.checkping(instance):
                result = True
                break
            else:
                time.sleep(1)
        return result

    def terminate(self, instance):
        instance.terminate()

    def create_key_pair(self, name):
        return self.ec2_conn.create_key_pair(name)

    def delete_key_pair(self, name):
        return self.ec2_conn.delete_key_pair(name)

    def get_all_key_pairs(self):
        return self.ec2_conn.get_all_key_pairs()

    def create_sg_group(self, name, desc=None):
        return self.ec2_conn.create_security_group(name, desc)

    def delete_sg_group(self, name):
        return self.ec2_conn.delete_security_group(name)

    def auth_sg_group(self, name, src_security_group_name=None, cidr_ip=None,
                              ip_protocol=None, to_port=None, from_port=None):
        return self.ec2_conn.authorize_security_group(name, 
                                                 src_security_group_name=src_security_group_name, 
                                                 cidr_ip=cidr_ip, 
                                                 ip_protocol=ip_protocol,
                                                 to_port=to_port, 
                                                 from_port=from_port)
    def list_sg_groups(self):
        return self.ec2_conn.get_all_security_groups()

    def wait_for_terminated(self, instance, timeout=300):
        start = time.time()
        while(time.time() <= start+timeout): 
            if self.get_instance_status(instance) == 'terminated':
                break
            else:
                time.sleep(1)

    def allocate_address(self):
        return self.ec2_conn.allocate_address()

    def release_address(self, address):
        return self.ec2_conn.release_address(public_ip=address)

    def associate_address(self, instance, address):
        return self.ec2_conn.associate_address(instance, address)

    def disassociate_address(self, address):
        return self.ec2_conn.disassociate_address(address)

    def get_all_addresses(self):
        return self.ec2_conn.get_all_addresses()
