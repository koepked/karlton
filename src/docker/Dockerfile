FROM centos
MAINTAINER Dan Koepke

# System setup
RUN yum -y install openmpi openmpi-devel openssh-server openssl openssl-devel \
                   bzip2-devel zlib-devel openssl wget
RUN yum -y groupinstall "Development Tools"
ADD custom.sh /etc/profile.d/custom.sh

# Munge
RUN wget https://github.com/dun/munge/archive/munge-0.5.11.tar.gz
RUN tar -xf munge-0.5.11.tar.gz
RUN cd munge-munge-0.5.11 && ./configure --prefix=/usr --sysconfdir=/etc \
    --localstatedir=/var --libdir=/usr/lib64 && make && make install
RUN chmod 0700 /etc/munge/
RUN chmod 0711 /var/lib/munge/
RUN chmod 0700 /var/log/munge/
RUN chmod 0755 /var/run/munge/
RUN dd if=/dev/urandom bs=1 count=1024 > /etc/munge/munge.key
RUN chmod 0600 /etc/munge/munge.key

# SLURM
RUN wget http://www.schedmd.com/download/archive/slurm-15.08.2.tar.bz2
RUN tar -xf slurm-15.08.2.tar.bz2
RUN cd slurm-15.08.2 && ./configure --prefix=/usr --sysconfdir=/etc \
    && make && make install
ADD slurm.conf /etc/slurm.conf
RUN useradd -M slurm
RUN usermod -L slurm
RUN mkdir /var/spool/slurm
RUN chown slurm:slurm var/spool/slurm
RUN mkdir /var/log/slurm
RUN chown slurm:slurm var/log/slurm

# SSH
ENV HOME /root
RUN mkdir -p /root/.ssh
ADD ssh-config /root/.ssh/config
RUN chmod 600 /root/.ssh/config
RUN /usr/bin/ssh-keygen -f /root/.ssh/id_rsa -t rsa -N ''
RUN cp /root/.ssh/{id_rsa.pub,authorized_keys}
RUN /usr/bin/ssh-keygen -A
ADD touch_nodes.py /root/touch_nodes.py
EXPOSE 22

# Add mpi examples
#ADD example /karlton/example
