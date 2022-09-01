# Programmatic execution of notebooks

In general, we run Jupyter notebooks **interactively**, but sometimes its useful to run them **programmatically**. Some use cases include:

* A researcher might want to ensure their notebooks run with a known, clean virtual machine configuration without having to guess about the state of the machine they use for interactive analysis (e.g., use the workflow to test that the notebook has no unaccounted for dependencies on locally installed Python packages, R packages, or on local files).
* A researcher might want to run a notebook with many different sets of parameters, all in parallel.
* A researcher might have a long running notebook (e.g., taking hours or even days) that they wish to run on a machine separate from where they are working interactively.
* A researcher might have a notebook that they want to run programmatically but do not wish to take the time to port it to a workflow.

## [notebook_workflow.wdl](./notebook_workflow.wdl)

Use WDL to programmatically execute a Jupyter notebook from start to finish. The notebook is executed on a new, clean
virtual machine (as opposed to where you normally run notebooks interactively).
This is useful not only for reproducibility and provenance, but to specifically confirm that the notebook
does not depend on any local dependencies (e.g., files or Python/R packages) installed where you normally
use Jupyter interactively.

This workflow will:
* Optionally install a list of Python packages before executing the notebook.
  * This is because a kernel restart is often necessary to make use of Python packages installed during notebook execution time.
  * For R package dependencies, have the notebook install them at the beginning of the notebook.
* Optionally pass parameters to the notebook via [Papermill](https://papermill.readthedocs.io/) to change its behavior.
* Save the executed `ipynb` file (containing cell outputs) as a result of the workflow.
* Also save an `html` copy of the executed ipynb file as a result of the workflow. This allows the notebook outputs to be read in the cloud console immediately.
* If the notebook created any output files or directories underneath the current working directory, they will also be included in a tar output file.

Details and limitations:
* If an error occurs during notebook execution, the resulting `ipynb` and `html` files are still saved, but
you will need to go look for them in the execution directory of the workflow run.
* This workflow was originally written for [app.terra.bio](https://app.terra.bio) and Google Cloud, but should run successfully on any Cromwell installation.
* Environment variables `OWNER_EMAIL`, `WORKSPACE_BUCKET`, `WORKSPACE_NAME`, and `WORKSPACE_NAMESPACE` are not currently available, but this may change [in the future](https://www.google.com/url?q=https://support.terra.bio/hc/en-us/community/posts/4411972716443-Make-workspace-environment-variables-available-in-workflow-configuration&sa=D&source=docs&ust=1661812248047678&usg=AOvVaw0jzAJVDbmwco9I4jFIu85L). For now, if your notebook uses those, ensure that you can also inject the desired value via [Papermill](https://papermill.readthedocs.io/) parameters.
* It is not compatible with notebooks written to run on [Hail](https://hail.is/) clusters.

## [dsub_notebook.py](./dsub_notebook.py)

Use `dsub_notebook.py` to execute Jupyter notebooks from the Terra Workspace terminal command line.  As with `notebook.wdl`,
`dsub_notebook.py` executes Jupyter notebooks on a new, clean virtual machine independent of any local dependencies installed where you normally use
Jupyter interactively.

This script will:
* Optionally install a list of Python packages before executing the notebook.
  * This is because a kernel restart is often necessary to make use of Python packages installed during notebook execution time.
  * For R package dependencies, have the notebook install them at the beginning of the notebook.
* Optionally pass parameters to the notebook via [Papermill](https://papermill.readthedocs.io/) to change its behavior.
* Save the executed `ipynb` file containing cell outputs.

Details and limitations:
* If an error occurs during notebook execution, the resulting `ipynb` files are still saved, but
you will need to go look for them in the output directory of the workflow run.

## Demonstration notebook [ProgrammaticExecutionDemo.ipynb](./ProgrammaticExecutionDemo.ipynb)

We have included a notebook to demonstrate how to programmatically execute a notebook using  `notebook.wdl` or
`dsub_notebook.py` and parameterize it using Papermill parameters. The notebook, `ProgrammaticExecutionDemo.ipynb`:

* Generates a set of normally distributed samples
* Plots a histogram of these samples
* Saves the samples to a CSV file
* Saves the histogram plot to a PNG filegenerates

You can control the execution of this notebook with these Papermill parameters:

* `MEAN` and `STD_DEV` set the mean and standard deviation of the normal distribution from which we are sampling.
* `SAMPLES` sets the number of generated samples.  
* `HISTOGRAM_BINS` sets the number of bins used in the histogram.
* `OUTPUT_FILE_BASENAME` is the basename of the CSV and PNG output files. 

All of these parameters have reasonable defaults, so you don't need to specify them all.

### Setup

In a new Terra Workspace, open the terminal and run the following from `/home/jupyter`:

1. Ensure dsub is installed in your cloud environment:

```
pip3 install --upgrade dsub
```

2. Copy `ProgrammaticExecutionDemo.ipynb` to `${WORKSPACE_BUCKET}/notebooks`:
```
export GITHUB_DIR="https://raw.githubusercontent.com/DataBiosphere/terra-examples/main/programmatic_execution_of_notebooks" && \
wget -O /tmp/ProgrammaticExecutionDemo.ipynb ${GITHUB_DIR}/ProgrammaticExecutionDemo.ipynb && \
gsutil cp /tmp/ProgrammaticExecutionDemo.ipynb ${WORKSPACE_BUCKET}/notebooks
```

3. Copy `dsub_notebook.py` to `/home/jupyter`:
```
wget -O ${HOME}/dsub_notebook.py ${GITHUB_DIR}/dsub_notebook.py
```

### Execute a notebook using `dsub_notebook.py`

Use multiple instance of the `--parameters` flag to set individual Papermill parameters:

```
python3 ${HOME}/dsub_notebook.py \
--notebook_to_run=${WORKSPACE_BUCKET}/notebooks/DemoQCResultsWithParameters.ipynb \
--parameters "MEAN 3" \
--parameters "STD_DEV 2" \
--nodry_run
```

In the command output, you'll see a `dstat` command you can run to see the status of your job.

Once the `dsub` job is  finished, successfully or not, you can find the fully rendered, timestamped notebook in the `Analyses`
tab of your workspace. This fully rendered notebook and all resulting files will also be written to the output path on
Cloud Storage, which defaults to `${WORKSPACE_BUCKET}/dsub/results/<NOTEBOOK>/<USER>/<DATE>/<TIME>`.

Try setting an invalid value, for example `--parameters "STD_DEV -1"` to see what happens when an error occurs during notebook
execution. You'll find the fully rendered, timestamped notebook in the expected location, but it will contain an error message
similar to what you'd see in the interactive Jupyter environment.

### Execute a notebook using `notebook_workflow.wdl`:

TODO