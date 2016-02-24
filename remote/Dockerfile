FROM ubuntu:14.04
MAINTAINER Frank Tran (http://anhcuong.github.io)
RUN apt-get update && \
	apt-get install -y openssh-server vim
ADD ansible.pub /var/tmp/ansible.pub
RUN mkdir -p /root/.ssh/ && cat /var/tmp/ansible.pub > /root/.ssh/authorized_keys
CMD /etc/init.d/ssh start && tail -F /var/log