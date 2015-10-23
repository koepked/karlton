FROM centos
MAINTAINER Dan Koepke

# System setup
RUN yum -y install openmpi openmpi-devel openssh-server
RUN yum -y groupinstall "Development Tools"
ADD custom.sh /etc/profile.d/custom.sh

# SSH
ENV HOME /root
RUN mkdir -p /root/.ssh
ADD ssh-config /root/.ssh/config
RUN chmod 600 /root/.ssh/config
RUN /usr/bin/ssh-keygen -f /root/.ssh/id_rsa -t rsa -N ''
RUN cp /root/.ssh/{id_rsa.pub,authorized_keys}
RUN /usr/bin/ssh-keygen -A
EXPOSE 22

# Add mpi examples
ADD example /karlton/example
