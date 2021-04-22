



FROM ubuntu:18.04

# basic os dependencies
RUN apt-get update && apt-get install -y \
            software-properties-common \
        && add-apt-repository universe \
        && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
            curl vim git zip unzip unrar p7zip-full wget \
            apache2 openssl libssl-dev \
            mysql-client mysql-server libmysqlclient-dev \
    && apt-key adv \
            --keyserver hkp://p80.pool.sks-keyservers.net:80 \
            --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8 \
        && echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > \
            /etc/apt/sources.list.d/pgdg.list \
        && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
            postgresql-9.3 \
            postgresql-client-9.3 \
            postgresql-contrib-9.3 \
            postgresql-server-dev-9.3 \
            libpq-dev

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

# jupyterlab
# RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
#     && apt-get update && apt-get install -y nodejs \
#     && jupyter labextension install --no-build \
#         @jupyter-widgets/jupyterlab-manager@2.0 \
#         jupyter-threejs \
#         @jupyterlab/toc \
#         @aquirdturtle/collapsible_headings \
#         jupyterlab-plotly@4.14.3 \
#         plotlywidget@4.14.3 \
#     && jupyter lab build

RUN /opt/miniconda3/bin/pip install \
        'flask==1.1.2' \
        'psycopg2==2.8.6' \
    && /opt/miniconda3/bin/conda install -c conda-forge \
        'spacy==3.0.5' \
    && python -m spacy download en_core_web_sm \
    && python -m spacy download en_core_web_trf

RUN /opt/miniconda3/bin/conda install -c conda-forge \
        'scikit-learn==0.24.1'

# cleanup
# RUN rm -rf /root/.cache/pip \
#     && rm -rf /var/lib/apt/lists/* \
#     && conda clean -a


CMD python3 -m src.nlp.main

## instructions:
# `make nlp`

