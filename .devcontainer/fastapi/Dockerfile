# [Choice] Python version: 3, 3.8, 3.7, 3.6
ARG VARIANT=3.9
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
WORKDIR /home/allenvose/projects/siriusfederal/
COPY *.devcontainer/fastapi/requirements.txt .devcontainer/noop.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
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
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*


ENV client_id '53fbprwytc23zxwb39ychdpu'
ENV client_secret 'q55maUrEdgjwT2797tvAaMeh'
ENV client_id2 'xuntd8mqcde8by7hkzbjhs2z'
ENV client_secret2 'YuASsPgDXCkQQgFMh7dH5mwU'
ENV smart_api_id '8d3c41e0-9b26-427a-bbcf-784ba88d3741'
ENV smart_api_secret 'cb3f5266-3553-40be-9ea3-2ea0484b79fc'
ENV PYTHONPATH '/home/vscode/fastapi/'
ENV DEBIAN_FRONTEND=

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]