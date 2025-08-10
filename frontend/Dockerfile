FROM jupyter/base-notebook:python-3.10

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install jupyterlab

WORKDIR /home/jovyan

CMD ["jupyter", "lab", "/home/jovyan/editor.ipynb", "--LabApp.default_url=/lab/tree/editor.ipynb", "--no-browser", "--ip=0.0.0.0", "--port=8888", "--NotebookApp.token=''"]