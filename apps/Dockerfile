# Build a docker image from latest YaCy sources

# Base image : latest stable official jdk image from Docker (Debian based)
FROM openjdk:latest

# Install needed packages not in base image
RUN apt-get update && apt-get install -yq curl python3

# trace java version
RUN java -version

# set current working dir
WORKDIR /opt

# All in one step to reduce image size growth :
# - install ant and git packages
# - clone main YaCy git repository (we need to clone git repository to generate correct version when building from source)
# - Compile with ant
# - remove unnecessary and size consuming .git directory
# - remove ant and git packages

# Possible alternative : copy directly your current sources an remove git clone command from the following RUN
# COPY . /opt/yacy_search_server/

RUN apt-get update && \
	apt-get install -yq ant git && \
	git clone https://github.com/yacy/yacy_search_server.git && \
	ant compile -f /opt/yacy_search_server/build.xml && \
	rm -rf /opt/yacy_search_server/.git && \
	apt-get purge -yq --auto-remove ant git && \
	apt-get clean

# Install IPFS
RUN apt-get install golang-go -y && \
  wget https://dist.ipfs.io/go-ipfs/v0.4.14/go-ipfs_v0.4.14_linux-amd64.tar.gz -O go-ipfs.tar.gz  && \
  tar xvfz go-ipfs.tar.gz && \
  rm go-ipfs.tar.gz && \
  cp go-ipfs/ipfs /usr/local/bin/ipfs



# Set initial admin password : "docker" (encoded with custom yacy md5 function net.yacy.cora.order.Digest.encodeMD5Hex())
RUN sed -i "/adminAccountBase64MD5=/c\adminAccountBase64MD5=MD5:e672161ffdce91be4678605f4f4e6786" /opt/yacy_search_server/defaults/yacy.init
RUN sed -i "/adminAccountForLocalhost=/c\adminAccountForLocalhost=true" /opt/yacy_search_server/defaults/yacy.init

# Intially enable HTTPS : this is the most secure option for remote administrator authentication
#RUN sed -i "/server.https=false/c\server.https=true" /opt/yacy_search_server/defaults/yacy.init

# Create user and group yacy : this user will be used to run YaCy main process // --no-create-home
RUN adduser --system --group  --disabled-password yacy

# Set ownership of yacy install directory to yacy user/group
RUN chown yacy:yacy -R /opt/yacy_search_server

# Expose HTTP and HTTPS default ports
EXPOSE 8090 8443

# Set data volume : yacy data and configuration will persist even after container stop or destruction
# VOLUME ["/opt/yacy_search_server/DATA"]

# Add python script
ADD yacyexec.py /usr/local/bin/
ADD yacyexec.sh /usr/local/bin/
RUN chmod a+x /usr/local/bin/yacyexec.py
RUN chmod a+x /usr/local/bin/yacyexec.sh

# Next commands run as yacy as non-root user for improved security

USER yacy
# Init IPFS for yacy user
RUN /usr/local/bin/ipfs init

# Start yacy as a foreground process (-f) to display console logs and to wait for yacy process
#CMD ["/bin/sh","/opt/yacy_search_server/startYACY.sh","-f"]
#CMD ["/usr/local/bin/ipfs", "daemon"]
#CMD ["/usr/local/bin/ipfs", "cat", "/ipfs/QmS4ustL54uo8FzR9455qaxZwuMiUhyvMcX9Ba8nUH4uVv/readme"]
#CMD ["/usr/bin/curl","http://toto.com"]
ENTRYPOINT ["/bin/bash", "-c",  "/usr/local/bin/yacyexec.py \"$@\"", "--"] # "/usr/bin/python3",
#ENTRYPOINT ["/bin/bash", "-c",  "/usr/local/bin/yacyexec.sh \"$@\"", "--"]
#ENTRYPOINT /bin/bash -c /usr/local/bin/yacyexec.sh "$@"
#ENTRYPOINT /usr/local/bin/yacyexec.py
#CMD ["http://toto.com"] # default parameter for ENTRYPOINT
