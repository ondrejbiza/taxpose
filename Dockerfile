FROM nvidia/cuda:11.3.0-cudnn8-devel-ubuntu20.04

# I forgot what problem this solved:)
ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True

# 'tzdata' have an annoying prompt.
RUN apt update ; DEBIAN_FRONTEND=noninteractive TZ="America/New_York" apt install -y tzdata

# Utilities.
RUN apt update ; apt install -y nano git cmake wget htop software-properties-common curl build-essential dpkg

# Install additional packages for python3.8.
RUN apt update ; apt install -y python3.8-dev python3.8-distutils

# Install pip.
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
# pip version 22 deprecated '*' (e.g. >=2.*) and hence breaks everything.
# Same thing for setuptools, I'm not sure what is the last working version.
RUN pip install pip==21 setuptools==63

# SSH -- fixing a problem in determined ai.
RUN apt update && apt install -y openssh-server apache2 supervisor
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor

# # Display.
# RUN apt update && apt install -y ffmpeg libsm6 libxext6

# # Virtual display. TODO: Some dependency opens a dialog window for region selection.
# # RUN apt update && apt install -y xvfb xserver-xephyr vnc4server
# RUN apt update ; apt install -y xfce4 xfce4-goodies tightvncserver
# RUN pip install pyvirtualdisplay

# Install TAX-Pose.
RUN pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install torch-scatter==2.0.9 torch-sparse==0.6.15 torch-cluster==1.6.0 torch-spline-conv==1.2.1 pyg_lib==0.1.0 -f https://data.pyg.org/whl/torch-1.11.0+cu113.html
RUN pip install fvcore iopath
RUN pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py38_cu113_pyt1110/download.html
RUN pip install --pre dgl -f https://data.dgl.ai/wheels/cu113/repo.html
RUN pip install --pre dglgo -f https://data.dgl.ai/wheels-test/repo.html
RUN git clone https://github.com/ondrejbiza/taxpose.git
WORKDIR /taxpose
RUN pip install -e .
WORKDIR /

# Install R-NDF.
RUN git clone https://github.com/anthonysimeonov/relational_ndf.git
WORKDIR /relational_ndf
RUN pip install numpy cython
RUN apt update ; apt install -y libffi-dev
RUN pip install -e .
WORKDIR /
