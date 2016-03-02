buildenv:
	cd control/ && docker build -t anhcuong/ansible-control .  
	cd remote/ && docker build -t anhcuong/ansible-remote .
	apt-get install -y python-pip 
	pip install -r requirements.txt
	chmod +x infra-setup.py	
ansible:
	./infra-setup.py
destroy:
	./infra-setup.py destroy
elasticsearch:
	docker exec -it ansible_control bash -c "ansible-playbook -e @cluster.yml elasticsearch.yml"
	
	
