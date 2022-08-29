# Programmatic execution of notebooks

In general, we run Jupyter notebooks **interactively**, but sometimes its useful to run them **programmatically**. Some use cases include:

* A researcher might want to ensure their notebooks run with a known, clean VM configuration without having to guess about the state of the workspace VM they use for interactive analysis (e.g., check for no dependence of the notebook on locally installed Python packages, R packages, or on local files).
* A researcher might want to run a notebook with many different sets of parameters, all in parallel.
* A researcher might have a long running notebook (e.g., taking hours or even days) that they wish to run on a machine separate from where they are working interactively.
* A researcher might have a notebook that they want to run programmatically but do not wish to take the time to port it to a workflow.

## [notebook_workflow.wdl](./notebook_workflow.wdl)

Use WDL to programmatically execute a Jupyter notebook from start to finish. This workflow will:
* Optionally install a list of Python packages before executing the notebook.
* Optionally pass parameters to the notebook via Papermill to change its behavior. See also https://papermill.readthedocs.io/.
* Save the executed ipynb file (containing cell outputs) as a result of the workflow.
* Also save an HTML copy of the executed ipynb file as a result of the workflow. This allows the notebook outputs to be read in the cloud console immediately.
* If the notebook created any output files or directories underneath the current working directory, they will also be included in a tar output file.

The notebook is executed on a new, clean VM (as opposed to where you normally run notebooks interactively).
This is useful not only for reproducibility and provenance, but to specifically confirm that the notebook
does not depend on any local dependencies (e.g., files or Python/R packages) installed where you normally
use Jupyter interactively.

NOTE: If an error occurs during notebook execution, the resulting ipynb and html files are still saved, but
you will need to go look for them in the execution directory of the workflow run.
