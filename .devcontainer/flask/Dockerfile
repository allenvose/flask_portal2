# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.168.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
WORKDIR /home/allenvose/projects/siriusfederal/
COPY *.devcontainer/flask/requirements.txt .devcontainer/noop.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    #
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    && apt-get -y install git procps lsb-release \
    && apt-get -y install nano \
    #
    # Install pylint
    && pip --disable-pip-version-check --no-cache-dir install pylint \
    && pip --disable-pip-version-check --no-cache-dir install Authlib==0.15.3 Flask \

    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 5000
ENV FLASK_APP run.py
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH '/home/vscode/flask'
ENV DEBUG=True
ENV SECRET_KEY=S3cr3t_K#Key
ENV DB_PASS=ryanlion22
ENV DEBIAN_FRONTEND=

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
