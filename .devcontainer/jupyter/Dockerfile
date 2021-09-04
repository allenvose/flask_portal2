# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.168.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
FROM jupyter/scipy-notebook:latest


# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
WORKDIR /home/allenvose/projects/siriusfederal/
COPY *.devcontainer/jupyter/requirements.txt .devcontainer/noop.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt

# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
# #     && apt-get -y install --no-install-recommends <your-package-list-here>
#     && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
#     #
#     # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
#     && apt-get -y install git procps lsb-release \
#     && apt-get -y install nano \
#     #
#     # Install pylint
#     && pip --disable-pip-version-check --no-cache-dir install pylint \

#     # Clean up
#     && apt-get autoremove -y \
#     && apt-get clean -y \
#     && rm -rf /var/lib/apt/lists/*

