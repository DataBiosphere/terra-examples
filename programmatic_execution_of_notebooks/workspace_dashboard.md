## Programmatic execution of notebooks

Generally, Jupyter notebooks are run interactively in a Terra cloud environment, but it's sometimes useful to run them programmatically.  

### Why you might want to run a notebook programmatically

* To run with a known, clean virtual machine configuration to confirm it has no unresolved dependencies on locally installed Python packages, R packages, or on local files.
* To run a notebook with many different sets of parameters, all in parallel.
* To execute a long-running notebook (e.g., taking hours or even days) on a machine separate from where you are working interactively.
* To run a notebook programmatically without porting it to a workflow.

### Two ways to run notebooks programmatically

* Via a Python script launched via the Terra workspace terminal (`dsub_notebook.py`). See [Using the terminal and interactive analysis shell in Terra](https://support.terra.bio/hc/en-us/articles/360041809272-Using-the-terminal-and-interactive-analysis-shell-in-Terra) for step-by-step instructions for launching a Terra worksapce terminal.

* Via a WDL workflow that launches Jupyter notebooks via the Terra workflows tab (`notebook_workflow.wdl`).  See [Getting started running workflows](https://support.terra.bio/hc/en-us/articles/360036379771-Get-started-running-workflows) for details on how to use workflows on Terra.

### Demonstration notebook (proxy for your own)

This workspace includes an example notebook, `2-explore_sample_qc_results.ipynb` that you can run using either option (Python script or WDL). The notebook produces quality control (QC) reports from detailed QC analyses, which were previously run on three different datasets.

### A note on time and cost estimates

Option 1 (`dsub_notebook.py`) and Option 2 (`notebook_workflow.wdl`) both launch new virtual machine instances to execute notebooks. Generally, it takes a few minutes to provision and configure new machine instances.

**IMPORTANT**: `dsub_notebook.py` and `notebook_workflow.wdl` are tools that enable you to run *your own* notebooks. The cost estimates provided here apply only to the setup and demo notebooks we included in this workspace. The cost of using these tools to run your own notebooks will vary depending on the configuration and number of VM instances you use to run your notebooks.

### Configuring analysis parameters in your notebook 

Both of these options use [Papermill](https://papermill.readthedocs.io/) to run notebooks on clean, newly allocated virtual machines.  You can use  [Papermill parameters](https://papermill.readthedocs.io/en/latest/usage-parameterize.html) to configure your notebooks.  For example, open `2-explore_sample_qc_results.ipynb` and look at the parameters available to you in the Papermill parameters cell:

* Use the `DATASET` parameter to select which dataset you'd like to examine (datasets are described below).
* Use the `CSV_OUTPUT_FILE_NAME` parameter to name your CSV output file. If you leave it unset, it will default to `<DATASET>_problem_summary.csv`.

**Don't edit these parameters directly in the notebook!** 
We'll demonstrate how to use `dsub_notebook.py` and `notebook_workflow.wdl` to set these parameters and customize individual notebook runs.

## Before you begin 

If you're new to Terra, we recommend reading this [introduction to workspaces](https://support.terra.bio/hc/en-us/articles/360046095192-Intro-to-workspaces) before following these instructions.

Clone this workspace by following the directions in the [How to clone your own workspace](https://www.google.com/url?q=https://support.terra.bio/hc/en-us/articles/360026130851-How-to-clone-your-own-workspace&sa=D&source=docs&ust=1665875782230262&usg=AOvVaw0mL4ZWxU-6EWHvsbRo9z54) support article.

## Option 1: Run notebooks with the command `dsub_notebook.py`

You can use `dsub_notebook.py` to execute Jupyter notebooks directly from the Cloud environment terminal.

As noted above, the demo notebook (`2-explore_sample_qc_results.ipynb`) produces QC reports from detailed QC analyses which were previously run on three different datasets.

### Install required dependencies

**Step 1:** In your cloned workspace, navigate to the **Analyses tab** and launch a new Jupyter Cloud Environment.  When creating the Jupyter Cloud Environment, you can use the Default Terra environment [v2.2.8](us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.8).

**Step 2:** Once the Cloud Environment is running, open `1-setup.ipynb` in **playground mode**.

**Step 3:** Select `Cell > Run All` from the **Jupyter menu bar** to install all required dependencies.

### Example and code
In this example, we'll generate a QC analysis report for 1000 Genomes Phase 3 by running this command in the Cloud Environment Terminal:

```
python3 ${HOME}/dsub_notebook.py \
--notebook_to_run=${WORKSPACE_BUCKET}/notebooks/2-explore_sample_qc_results.ipynb \
--parameters "DATASET thousand_genomes" \
--nodry_run
```

**Adjusting parameters**    

You can select a dataset by choosing one of these three values for the parameter `DATASET`:
  * `simons` - [The Simons Genome Diversity Project](https://www.simonsfoundation.org/simons-genome-diversity-project/) (As described in the linked document, all data is freely available.)
  * `thousand_genomes` - [1000 Genomes Phase 3](https://www.internationalgenome.org/category/phase-3/) ([Data access policy](https://www.internationalgenome.org/IGSR_disclaimer))
  * `platinum_genomes` DeepVariant Platinum Genomes (Open access)

**Note**: these datasets are all open access


**What to expect**

In the command output, you'll see a `dstat` command you can run to see the status of your job.

Once the `dsub` job is  finished, you will find a fully rendered, time stamped copy of the notebook in the `Analyses` tab of your workspace. This fully rendered notebook and any files created by the notebook as part of the analysis will also be written to the output path on Cloud Storage, which defaults to 

`${WORKSPACE_BUCKET}/dsub/results/<NOTEBOOK>/<USER>/<DATE>/<TIME>`.

You can use the `output_notebook` flag to specify a different path for your rendered notebook, and the `output_path` flag to specify a different path for the output files generated by your notebook.

To see a list of all available flags, run:

```
python3 ${HOME}/dsub_notebook.py –help
```

## Option 2: Run notebooks with WDL (`notebook_worfklow.wdl`)

Alternatively, you can execute Jupyter notebooks via a workflow using `notebook_workflow.wdl`.

**Step 1:** Navigate to the Workflows tab and open `notebook_workflow`.

**Step 2:** Configure the following inputs:

* Set `notebookWorkspacePath` using the GCS URL for the notebook. You can find this by first clicking the folder icon on the data tab to browse bucket files and then selecting `notebooks > 2-explore_sample_qc_results.ipynb` to view the GCS URL.
* Set `papermillParameters` using multiple instances of the `-p` flag to specify parameters in a single, space-separated string.  Choose one of the three values for the parameter `DATASET` described in the previous section, for example:

```
-p DATASET simons
```

**Step 3:** Run the WDL by clicking **Run Analysis**. 

**What to expect**

You can follow the progress of your job as you would any other workflow, using the Job History tab. Upon completion of the job, you can find its outputs including the fully rendered, timestamped notebook, an HTML preview of the notebook, and the outputs of the job in the outputs tab of the [Job Manager](https://job-manager.dsde-prod.broadinstitute.org/).

## Additional information about notebooks, environment requirements and cost estimates

For helpful hints on controlling Cloud costs, see this article ([click here to view](https://support.terra.bio/hc/en-us/articles/360029748111)).       

### Notebook 1-setup.ipynb

**What does it do?**

Installs `dsub_notebook.py` and its dependencies, which are required for Option 1.

#### Jupyter Cloud Environment recommendations

**Application configuration**   
Default Terra environment [v2.2.8](us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.8) (GATK 4.2.4.0 Python3.7.12 R 4.2.1)

**Cloud compute profile**

| Parameter | Value|   
| --- | --- |
| CPU Minimum | 1|
| Memory Minimum | 3.75 GB |

**Persistent disk**   

| Parameter | Value|   
| --- | --- |
| Disk size Minimum | 50 GB |

**Time and cost to run**

This notebook runs in a few seconds on the Standard VM configuration, and costs less than US$0.01 to run.

### Notebook 2-explore_sample_qc_results.ipynb

Note that this is a demo notebook only. If you were running your own notebook programmatically, you would replace the information below with your own notebook analysis. 

**What does it do?**

Demonstrates how to execute a notebook using `notebook.wdl` or `dsub_notebook.py` and configure its behavior using Papermill parameters.

This notebook produces QC reports from detailed QC analyses which were previously run on three different datasets:

* [The Simons Genome Diversity Project](https://www.simonsfoundation.org/simons-genome-diversity-project/)
* [1000 Genomes Phase 3](https://www.internationalgenome.org/category/phase-3/)
* DeepVariant Platinum Genomes

**Jupyter Cloud Environment recommendations**

Default Terra environment [v2.2.8](us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.8)

**Compute Power**

Standard VM

| Runtime  | Value |
| --- | --- |
| Environments | Default (GATK 4.2.4.0 Python3.7.12 R 4.2.1) |
| CPU Minimum | 1|
| Disk size Minimum | 50 GB |
| Memory Minimum | 3.75 GB |

**Time and cost to run**
This demo notebook runs in a few minutes on the Standard VM configuration, and costs less than US$0.01 to run.
 
## Additional information about workflows

### notebook_workflow.wdl

**What does it do?**
`notebook_workflow.wdl` executes a Jupyter notebook using Papermill on a new virtual machine instance.

**Inputs and outputs**
Workflow inputs and outputs depend on the notebook you're running. No additional inputs beyond those specified on the workflows page are required for the demonstration notebook `2-explore_sample_qc_results.ipynb`.  This notebook outputs a CSV file detailing the results of the QC analysis.

**Time and cost to complete**
The workflow should complete in under 30 minutes and cost less than US$0.01 to run.

### Contact information

For help with Terra accounts setup, for help navigating the Terra environment, or to submit Terra feedback, please use the main navigation menu at the top left of this page. Click "Support," then "Terra Support Home" for Terra documentation.  Alternatively, click "Contact Us" to ask a question directly to the Terra support team.

For help with `dsub_notebook.py`, `notebook_workflow.wdl`, or issues with the example notebooks, please file an issue on our [GitHub repository issues page](https://github.com/DataBiosphere/terra-examples/issues). 

### Software license information

Copyright 2022 Verily Life Sciences LLC
Use of this source code is governed by an open-source BSD-style [license](https://developers.google.com/open-source/licenses/bsd).
