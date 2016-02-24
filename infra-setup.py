#!/usr/bin/python
import os, time
from docker import Client
import yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader

current_dir = os.path.dirname(os.path.realpath(__file__))
tmpl_dir = os.path.join(current_dir, "templates")
cli = Client(base_url='unix://var/run/docker.sock')
remote_masters = []
remote_workers = []

def create_control():	
	print "===Creating ansible control==="
	control = cli.create_container(
		image='anhcuong/ansible-control', name='ansible_control',
		volumes=['/ansible'],
		host_config=cli.create_host_config(binds=[current_dir+":/ansible"]),
		detach=True,
		working_dir='/ansible'		
	)
	cli.start(container=control["Id"])
	pass

def create_master(m):
	print "===Creating ansible remote - master group==="	
	for i in range(1, int(m)):
		print "==Creating master %d==" %i
		control = cli.create_container(
			image='anhcuong/ansible-remote', name='ansible_master%d' %i ,			
			detach=True			
		)
		response=cli.start(container=control["Id"])		
		print(response)
	pass

def create_worker(n):
	print "===Creating ansible remote - worker group==="
	for i in range(1, int(n)):
		print "==Creating worker %d==" %i
		control = cli.create_container(
			image='anhcuong/ansible-remote', name='ansible_worker%d' %i ,			
			detach=True			
		)
		cli.start(container=control["Id"])		
	pass

def clean_docker():
	for container in cli.containers(all=True):
		if container["Names"][0].startswith("/ansible"):			
			cli.remove_container(container=container["Id"], force=True)

def collect_remote_master_ips():
	for container in cli.containers():
		if container["Names"][0].startswith("/ansible_master"):
			remote_masters.append([container["Names"][0], container["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]])
	print remote_masters
	pass

def collect_remote_worker_ips():
	for container in cli.containers():
		if container["Names"][0].startswith("/ansible_worker"):
			remote_workers.append([container["Names"][0], container["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]])
	print remote_workers
	pass

def render_template(config, template_name, outfile):
    env = Environment(loader=FileSystemLoader(tmpl_dir))
    template = env.get_template(template_name)
    with open(outfile, 'w') as f:
        f.write(template.render(config))

if __name__ == "__main__":
	master_num = os.getenv('MASTER_NUM', 3)
	worker_num = os.getenv('WORKER_NUM', 0)
	clean_docker()
	create_control()
	create_master(master_num)
	create_worker(worker_num)
	print "===Wait for control to collect all remote data==="	
	time.sleep(5)
	collect_remote_master_ips()
	collect_remote_worker_ips()
	print "===Rendering hostfile from j2 templates==="	