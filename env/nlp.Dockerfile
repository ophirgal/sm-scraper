
FROM ubuntu:18.04


# basic os dependencies
RUN apt-get update && apt-get install -y \
            software-properties-common \
        && add-apt-repository universe \
        && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
            curl vim git zip unzip unrar p7zip-full wget \
            apache2 openssl libssl-dev \
            mysql-client mysql-server libmysqlclient-dev

# basic python dependencies
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3 \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
ENV PATH="/opt/miniconda3/bin:${PATH}"
ARG PATH="/opt/miniconda3/bin:${PATH}"
RUN apt-get install -y \
        build-essential \
    && /opt/miniconda3/bin/conda install \
        'jupyterlab==2.2.6' \
        'matplotlib==3.3.2' \
        'pandas==1.2.1' \
        'scipy==1.5.2' \
        'plotly==4.14.3' \
    && /opt/miniconda3/bin/pip install \
        'mysql-connector-python==8.0.23' \
        'mysqlclient==2.0.3' \
        'patool==1.12' \
        'pyunpack==0.2.2'

# nlp dependencies
RUN /opt/miniconda3/bin/pip install \
        'flask==1.1.2' \
        'click==7.1.2' \
    && /opt/miniconda3/bin/conda install -c conda-forge \
        'spacy==3.0.5' \
    && python -m spacy download en_core_web_sm \
    && python -m spacy download en_core_web_trf

RUN /opt/miniconda3/bin/conda install -c conda-forge \
        'scikit-learn==0.24.1'


CMD python3 -m src.nlp.main

## instructions:
# `make nlp`

