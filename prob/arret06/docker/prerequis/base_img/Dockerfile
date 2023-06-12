FROM alpine:latest

#install python
ENV PYTHONUNBUFFERED=1
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories
RUN apk add --update --no-cache python3 postgresql-dev gcc python3-dev musl-dev && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN apk add build-base
RUN pip3 install psycopg2

RUN apk add openssh
RUN apk add udev-init-scripts-openrc

#install fortune and remove default files
RUN apk add fortune
RUN cd /usr/share/fortune; rm *

#copy predefined fortune files
COPY fortune/fortunes /usr/share/fortune
COPY fortune/people /usr/share/fortune

#process fortune files
RUN cd /usr/share/fortune; strfile -c % fortunes fortunes.dat; strfile -c % people people.dat

#install openrc (used to start sshd)
RUN apk add openrc

#install sshd (openssh) and enable sshd service
RUN apk add openssh

#copy ssh keys to enable password-less entry
COPY ssh/sshkeys/id_rsa /root/.ssh/id_rsa
COPY ssh/sshkeys/id_rsa.pub /root/.ssh/id_rsa.pub

#copy authorized_keys and known hosts
COPY ssh/authorized_keys /root/.ssh/authorized_keys
COPY ssh/known_hosts /root/.ssh/known_hosts

#copy ssh host keys to ensure continuity of access with different containers
COPY ssh/sshhostkeys /etc/ssh

#add root passwd (root)
COPY ssh/shadow /etc/shadow

#ensure file permissions
RUN chmod 644 /usr/share/fortune/*

RUN chmod 600 /root/.ssh/*
RUN chmod 644 /root/.ssh/*.pub 
RUN chmod 644 /root/.ssh/authorized_keys

RUN chmod 600 /etc/ssh/ssh_host*
RUN chmod 644 /etc/ssh/ssh_host*.pub

RUN chmod 640 /etc/shadow

#disable password authentication
RUN echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

VOLUME [ "/sys/fs/cgroup" ]
