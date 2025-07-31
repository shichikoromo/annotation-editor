FROM jupyter/base-notebook:python-3.10

RUN pip install --no-cache-dir spacy ipywidgets 
RUN pip install jupyterlab

WORKDIR /home/jovyan

CMD ["jupyter-lab",  "--allow-root", "--no-browser", "--ip=0.0.0.0", "--port=8888", "--NotebookApp.token=''", "--NotebookApp.password=''"]
