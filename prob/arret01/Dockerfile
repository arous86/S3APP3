FROM alpine:latest

#install python
ENV PYTHONUNBUFFERED=1
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories
RUN apk add python3

RUN apk add openssh

#install fortune and remove default files
RUN apk add fortune
RUN cd /usr/share/fortune; rm *

#copy predefined fortune files
COPY fortunes /usr/share/fortune
COPY people /usr/share/fortune

#process fortune files
RUN cd /usr/share/fortune; strfile -c % fortunes fortunes.dat; strfile -c % people people.dat

#create /todo directory to hold todo data
RUN mkdir /todo

#copy todo.py
COPY todo.py /usr/local/bin/todo.py

#add scripts to ease use of todo.py
COPY scripts/list_todo.sh /usr/local/bin/list_todo.sh
COPY scripts/add_todo.sh /usr/local/bin/add_todo.sh
COPY scripts/remove_todo.sh /usr/local/bin/remove_todo.sh
COPY scripts/help.sh /usr/local/bin/help.sh
COPY scripts/todo.sh /usr/local/bin/todo.sh

#Add symbolic links to scripts
RUN ln -s /usr/local/bin/list_todo.sh /usr/local/bin/liste
RUN ln -s /usr/local/bin/remove_todo.sh /usr/local/bin/retrait
RUN ln -s /usr/local/bin/add_todo.sh /usr/local/bin/nouveau
RUN ln -s /usr/local/bin/help.sh /usr/local/bin/aide
RUN ln -s /usr/local/bin/todo.sh /usr/local/bin/todo

CMD ["/bin/sh"]
