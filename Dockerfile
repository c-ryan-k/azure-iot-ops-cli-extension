FROM mcr.microsoft.com/cbl-mariner/base/python:3

# working directory
WORKDIR /usr/src/azure-iot-ops

# copy all source to working dir
COPY . .

# create empty kubeconfig to mount later
RUN mkdir /root/.kube
RUN touch /root/.kube/config

# venv
ENV VIRTUAL_ENV=/opt/venv


RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# tox setup
RUN pip install tox
RUN tox r -vv -e python-int --notest 

# run tests
ENTRYPOINT ["tox", "-e", "python-int"]