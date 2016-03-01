# Introduction
Ansible playbook to setup playground for distributed tools on cluster of dockers.

# Prerequisite
- python2.7
- [docker](https://docs.docker.com/installation/), at least version 1.10.2, API version 1.22
- [make](http://stackoverflow.com/questions/11934997/how-to-install-make-in-ubuntu/) 

# How to run
- The cluster includes one control docker with many remote dockers
- The remote workers divide into 2 groups: master and worker. All of them can be controlled by ansible running from control docker
- Edit .env file to input number of masters(default=3) and workers(default=0) you want to run
- Let your number of your master is odd because many distributed tools use odd size for their leader election algorithm.
- Remember to setup ansible cluster first before you can try out other tools-cluster.

```sh
# Install dependencies
make buildenv
# Set number of workers and machines
source .env
```

## Ansible cluster

```sh
# Create playground for ansible
make ansible

# Try out ansible commands
docker exec -it ansible_control bash
ansible all -m shell -a "ls -la"

```

## Elasticsearch cluster

```sh
make elasticsearch
docker exec -it ansible_control bash
export TERM=xterm
ansible-playbook elasticsearch.yml
	 
```