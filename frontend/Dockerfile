FROM jupyter/base-notebook:python-3.10

RUN pip install ipywidgets

WORKDIR /home/jovyan/work

CMD ["jupyter", "notebook",  "--allow-root", "--no-browser", "--ip=0.0.0.0", "--port=8888", "--NotebookApp.token=''", "--NotebookApp.password=''"]
