FROM ubuntu:14.04
MAINTAINER Frank Tran (http://anhcuong.github.io)
RUN apt-get update && \
    apt-get install --no-install-recommends -y software-properties-common && \
    apt-add-repository ppa:ansible/ansible && \
    apt-get update && \
    apt-get install -y ansible git vim
ADD ansible /var/tmp/ansible
RUN chmod 400 /var/tmp/ansible
CMD tail -F /var/log/ansible.log