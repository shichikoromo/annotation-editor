FROM jupyter/base-notebook:python-3.10

RUN pip install ipywidgets

WORKDIR /home/jovyan/work
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8777", "--allow-root", "--NotebookApp.token=''"]
