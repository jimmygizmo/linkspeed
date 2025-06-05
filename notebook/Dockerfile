FROM quay.io/jupyter/minimal-notebook:python-3.11
# This notebook base image with Python 3.11 is required for MapBox.
# MapBox libraries or dependencies thereof have an incompatibility with Python 3.12 at the moment.

# Custom settings like dark them as default
COPY overrides.json /opt/conda/share/jupyter/lab/settings/

COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /home/linkspeed/workspace

COPY traffic.ipynb /home/linkspeed/workspace/

EXPOSE 8888

# NOTE: Compose file has notebook start options required for our large response payloads. Use the compose CMD.
#CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]

# For reference, here is the Compose start command showing those important options:
#    command: [
#      "start-notebook.sh",
#      "--NotebookApp.token=''",
#      "--NotebookApp.password=''",
#      "--ServerApp.iopub_data_rate_limit=10000000",
#      "--ServerApp.rate_limit_window=10.0",
#      "--LabApp.default_url='/lab/tree/traffic.ipynb'",
#    ]

