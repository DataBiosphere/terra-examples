## Programmatic execution of notebooks

Generally, Jupyter notebooks are run interactively in a Terra analysis environment, but sometimes it's useful to run them programmatically.  

For example:

* A researcher might want to ensure their notebooks run with a known, clean virtual machine configuration to confirm it has no unresolved dependencies on locally installed Python packages, R packages, or on local files.
* A researcher might want to run a notebook with many different sets of parameters, all in parallel.
* A researcher might have a long running notebook (e.g., taking hours or even days) that they wish to run on a machine separate from where they are working interactively.
* A researcher might have a notebook that they want to run programmatically but do not wish to take the time to port it to a workflow.

In this workspace, we demonstrate two ways to run notebooks programmatically:

* `dsub_notebook.py`: A Python script launched via the Terra workspace terminal.
* `notebook_workflow.wdl`: A WDL workflow that launches Jupyter notebooks via the Terra workflows tab.

Both of these tools use [Papermill](https://papermill.readthedocs.io/) to run notebooks on clean, newly allocated virtual machines. You can pass parameters to the notebook using [Papermill parameters](https://papermill.readthedocs.io/en/latest/usage-parameterize.html) to configure your notebook's behavior.

## Instructions

### Setup

Before you begin, create your own editable copy (clone) of this WORKSPACE. Click the round circle with three dots in the upper right corner of this page and choose "Clone".

Then, navigate to the analyses tab and open `1-setup.ipynb` in playground mode.

Select `Cell > Run All` from the Jupyter menu bar to install all required dependencies.

### Papermill parameters

You can use Papermill parameters to configure the behavior of your notebooks.  For example, open `2-programmatic_execution_demo.ipynb` and look at the parameters available to you in the Papermill parameters cell.

* `MEAN` and `STD_DEV` set the mean and standard deviation of the normal distribution from which we are sampling.
* `SAMPLES` sets the number of generated samples.  
* `HISTOGRAM_BINS` sets the number of bins used in the histogram.
* `OUTPUT_FILE_BASENAME` is the basename of the CSV and PNG output files. 

Don't edit these parameters directly in the notebook: we'll demonstrate how to use `dsub_notebook.py` and `notebook_workflow.wdl` to set these parameters and customize your notebook's run.

### `dsub_notebook.py`

You can use `dsub_notebook.py` to execute Jupyter notebooks directly from the Terra workspace terminal or in a script.

#### Run `2-programmatic_execution_demo.ipynb`

First, navigate to the Terra workspace terminal.

Then, select the notebook you wish to run and assign it to an environment variable for convenience. In this case, we've selected `2-programmatic_execution_demo.ipynb`.

```
export NOTEBOOK_TO_RUN=${WORKSPACE_BUCKET}/notebooks/2-programmatic_execution_demo.ipynb
```

Now, launch `dsub_notebook.py`.  Use multiple instance of the `--parameters` flag to set individual Papermill parameters:

```
python3 ${HOME}/dsub_notebook.py \
--notebook_to_run=${NOTBOOK_TO_RUN} \
--parameters "MEAN 3" \
--parameters "STD_DEV 2" \
--nodry_run
```

In the command output, you'll see a `dstat` command you can run to see the status of your job.

Once the `dsub` job is  finished, successfully or not, you can find the fully rendered, timestamped notebook in the `Analyses`
tab of your workspace. This fully rendered notebook and any files emitted by the notebook will also be written to the output path on
Cloud Storage, which defaults to `${WORKSPACE_BUCKET}/dsub/results/<NOTEBOOK>/<USER>/<DATE>/<TIME>`.

Try setting an invalid value, for example `--parameters "STD_DEV -1"` to see what happens when an error occurs during notebook
execution. You'll find the fully rendered, timestamped notebook in the expected location, but it will contain an error message
similar to what you'd see in the interactive Jupyter environment.

#### Run `3-explore_sample_qc_results.ipynb`

`3-explore_sample_qc_results.ipynb` produces QC reports from detailed QC analyses which were previously run on three different datasets.

Choose one of these three values for the parameter `DATASET`:

  * `simons` - [The Simons Genome Diversity Project](https://www.simonsfoundation.org/simons-genome-diversity-project/)
  * `thousand_genomes` - [1000 Genomes Phase 3](https://www.internationalgenome.org/category/phase-3/)
  * `platinum_genomes` DeepVariant Platinum Genomes

In this example, we'll generate a QC analysis report for 1000 Genomes Phase 3:

```
export NOTEBOOK_TO_RUN=${WORKSPACE_BUCKET}/notebooks/3-explore_sample_qc_results.ipynb
```

```
python3 ${HOME}/dsub_notebook.py \
--notebook_to_run=${NOTEBOOK_TO_RUN} \
--parameters "DATASET thousand_genomes" \
--nodry_run
```

In the command output, you'll see a `dstat` command you can run to see the status of your job.

Once the `dsub` job is  finished, successfully or not, you can find the fully rendered, timestamped notebook in the `Analyses`
tab of your workspace. This fully rendered notebook and any files emitted by the notebook will also be written to the output path on
Cloud Storage, which defaults to `${WORKSPACE_BUCKET}/dsub/results/<NOTEBOOK>/<USER>/<DATE>/<TIME>`.

### `notebook_worfklow.wdl`

Alternatively, you can execute Jupyter notebooks via a workflow using `notebook_workflow.wdl`.

#### Run `2-programmatic_execution_demo.ipynb`

First, navigate to the Workflows tab and open `notebook_workflow`.

Now, configure the following inputs:

* Set `notebookWorkspacePath` using the GCS URL for the notebook. You can find this by first clicking the folder icon on the data tab to browse bucket files and then selecting `notebooks > 2-programmatic_execution_demo.ipynb` to view the GCS URL.
* Set `papermillParameters` using multiple instances of the `-p` flag to specify parameters in a single, space-separated string.  For example, if you'd like to set MEAN to 2 and STD_DEV to 0.5, you'd use:

```
-p MEAN 2 -p STD_DEV 0.5
```

Finally, click Run Analysis. You can follow the progress of your job as you would any other workflow, using the Job History tab. Upon completion of the job, you can find its outputs including the fully rendered, timestamped notebook, an HTML preview of the notebook, and the outputs of the job in the outputs tab of the [Job Manager](https://job-manager.dsde-prod.broadinstitute.org/).

#### Run `3-explore_sample_qc_results.ipynb`

`3-explore_sample_qc_results.ipynb` produces QC reports from detailed QC analyses which were previously run on three different datasets.

First, navigate to the Workflows tab and open `notebook_workflow`.

Now, configure the following inputs:

* Set `notebookWorkspacePath` using the GCS URL for the notebook. You can find this by first clicking the folder icon on the data tab to browse bucket files and then selecting `notebooks > 3-explore_sample_qc_results.ipynb` to view the GCS URL.
* Set `papermillParameters` using multiple instances of the `-p` flag to specify parameters in a single, space-separated string.  In this notebook, you can choose one of these three values for the parameter `DATASET`:

  * `simons` - [The Simons Genome Diversity Project](https://www.simonsfoundation.org/simons-genome-diversity-project/)
  * `thousand_genomes` - [1000 Genomes Phase 3](https://www.internationalgenome.org/category/phase-3/)
  * `platinum_genomes` DeepVariant Platinum Genomes

Finally, click Run Analysis. You can follow the progress of your job as you would any other workflow, using the Job History tab. Upon completion of the job, you can find its outputs including the fully rendered, timestamped notebook, an HTML preview of the notebook, and the outputs of the job in the outputs tab of the [Job Manager](https://job-manager.dsde-prod.broadinstitute.org/).

## Notebooks

### A note on time and cost estimates

`dsub_notebook.py` and `notebook_workflow.wdl` launch new virtual machine instances to execute notebooks. Generally, it takes a few minutes to provision and configure new machine instances.

**IMPORTANT**: `dsub_notebook.py` and `notebook_workflow.wdl` are tools that enable you to run *your own* notebooks. The cost estimates provided here are strictly for the setup and demo notebooks we've included in this workspace. Using these tools to run your own notebooks will vary in cost depending on the configuration and number of VM instances you use to run your notebooks.

**Notebook 1-setup.ipynb**: Installs `dsub_notebook.py` and its dependencies.

Environment: Default Terra environment [v2.2.8](us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.8)

Computer Power:  Standard VM

| Runtime  | Value |
| --- | --- |
| Environments | Default (GATK 4.2.4.0 Python3.7.12 R 4.2.1) |
| CPU Minimum| 1|
| Disksize Minimum | 50 GB |
| Memory Minimum | 3.75 GB |

This notebook runs in a few seconds on the Standard VM configuration, and costs less than US$0.01 to run.

**Notebook 2-programmatic_execution_demo.ipynb**:  Demonstrates how to execute a notebook using `notebook.wdl` or `dsub_notebook.py` and configure its behavior using Papermill parameters.

* Generates a set of normally distributed samples
* Plots a histogram of these samples
* Saves the samples to a CSV file
* Saves the histogram plot to a PNG filegenerates

Environment: Default Terra environment [v2.2.8](us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.8)

Computer Power:  Standard VM

| Runtime  | Value |
| --- | --- |
| Environments | Default (GATK 4.2.4.0 Python3.7.12 R 4.2.1) |
| CPU Minimum| 1|
| Disksize Minimum | 50 GB |
| Memory Minimum | 3.75 GB |

This notebook runs in a few seconds on the Standard VM configuration, and costs less than US$0.01 to run.

**Notebook 3-explore_sample_qc_resulst.ipynb**:  Demonstrates how to execute a notebook using `notebook.wdl` or `dsub_notebook.py` and configure its behavior using Papermill parameters.

This notebook produces QC reports from detailed QC analyses which were previously run on three different datasets:

* [The Simons Genome Diversity Project](https://www.simonsfoundation.org/simons-genome-diversity-project/)
* [1000 Genomes Phase 3](https://www.internationalgenome.org/category/phase-3/)
* DeepVariant Platinum Genomes

Environment: Default Terra environment [v2.2.8](us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.8)

Computer Power:  Standard VM

| Runtime  | Value |
| --- | --- |
| Environments | Default (GATK 4.2.4.0 Python3.7.12 R 4.2.1) |
| CPU Minimum| 1|
| Disksize Minimum | 50 GB |
| Memory Minimum | 3.75 GB |

This notebook runs in a few minutes on the Standard VM configuration, and costs less than US$0.01 to run.
 
## Workflows 

### notebook_workflow.wdl

`notebook_workflow.wdl` executes a Jupyter notebook using Papermill on a new virtual machine instance.

Workflow inputs and outputs depends on the notebook you're running, but no additional inputs are required for the demonstration notebooks `2-programmatic_notebook_execution_demo.ipynb` nor `3-explore_sample_qc_results.ipynb`.  `2-programmatic_notebook_execution_demo.ipynb` outputs a CSV file containing samples from a user-configured normal distribution and a PNG file containing a histogram plot of the distribution.  `3-explore_sample_qc_results.ipynb` outputs a CSV file detailing the anomalies found in the QC analysis.

The workflow should complete in under 30min and cost less than US$0.01 to run.

For helpful hints on controlling Cloud costs, see this article ([click here to view](https://support.terra.bio/hc/en-us/articles/360029748111)).       


### Contact information

For help with Terra accounts setup, for help navigating the Terra environment, or to submit Terra feedback, please use the hamburger menu at the top left of this page and click Support then Terra Support Home for Terra documentation or Contact Us to ask a question directly to the Terra support team.

For help with `dsub_notebook.py`, `notebook_workflow.wdl`, or issues with the example notebooks, please file an issue on our [GitHub repository issues page](https://github.com/DataBiosphere/terra-examples/issues). 