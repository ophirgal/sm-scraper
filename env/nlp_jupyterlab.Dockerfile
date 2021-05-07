
FROM sm-scraper:nlp


# jupyterlab
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get update && apt-get install -y nodejs \
    && jupyter labextension install --no-build \
        @jupyter-widgets/jupyterlab-manager@2.0 \
        jupyter-threejs \
        @jupyterlab/toc \
        @aquirdturtle/collapsible_headings \
        jupyterlab-plotly@4.14.3 \
        plotlywidget@4.14.3 \
    && jupyter lab build


# cleanup
# RUN rm -rf /root/.cache/pip \
#     && rm -rf /var/lib/apt/lists/* \
#     && conda clean -a


