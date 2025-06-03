FROM quay.io/jupyter/minimal-notebook:latest

# Custom settings like dark them as default
COPY overrides.json /opt/conda/share/jupyter/lab/settings/

# Copy requirements and install
COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir -r /tmp/requirements.txt


WORKDIR /home/linkspeeds/workspace


EXPOSE 8888


# By default starts Jupyter Lab. Classic Notebook is also available.
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]

