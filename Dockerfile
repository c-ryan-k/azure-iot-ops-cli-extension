FROM mcr.microsoft.com/cbl-mariner/base/python:3

# install ca-certificates for curl
RUN yum update -y && \
 yum -y install ca-certificates shadow-utils && \
 yum clean all

# install kubectl for tests
RUN curl -LO https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl && mv ./kubectl /usr/local/bin

# working directory
WORKDIR /usr/src/azure-iot-ops

# copy all source to working dir
COPY . .

# create empty kubeconfig to mount later as a file
RUN mkdir -p /root/.kube && touch /root/.kube/config 

# tox setup
RUN pip install tox==4.12.1 --no-cache-dir

# switch from root user
RUN groupadd -r testers && useradd -r -g testers tester
USER tester

# run tests
ENTRYPOINT ["tox", "r", "-vv", "-e", "python-int", "--", "--durations=0"]