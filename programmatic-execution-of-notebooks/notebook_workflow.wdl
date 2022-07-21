# Copyright 2022 Verily Life Sciences LLC
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file or at https://developers.google.com/open-source/licenses/bsd
#
# Use WDL to programmatically execute a Jupyter notebook from start to finish. This workflow will:
# - Optionally install a list of Python packages before executing the notebook.
# - Optionally pass parameters to the notebook via Papermill to change its behavior.
#   See also https://papermill.readthedocs.io/.
# - Save the executed ipynb file (containing cell outputs) as a result of the workflow.
# - Also save an HTML copy of the executed ipynb file as a result of the workflow.
#   This allows the notebook outputs to be read in the cloud console immediately.
# - If the notebook created any output files or directories underneath the current working directory,
#   they will also be included in a tar output file.
#
# The notebook is executed on a new, clean VM (as opposed to where you normally run notebooks interactively).
# This is useful not only for reproducibility and provenance, but to specifically confirm that the notebook
# does not depend on any local dependencies (e.g., files or Python/R packages) installed where you normally
# use Jupyter interactively.
#
# NOTE: If an error occurs during notebook execution, the resulting ipynb and html files are still saved, but
# you will need to go look for them in the execution directory of the workflow run.
#
# Coding standard https://biowdl.github.io/styleGuidelines.html is used with newer command body
# style https://github.com/openwdl/wdl/blob/main/versions/1.0/SPEC.md#command-section.

version 1.0

workflow NotebookWorkflow {
    input {
        # This should be the GCS path to a notebook file in the workspace bucket.
        File notebookWorkspacePath
        # See also https://papermill.readthedocs.io/en/latest/usage-cli.html
        String? papermillParameters
        # A space-separated list of pip packages to install.
        String? packagesToPipInstall
        # Use the default Terra image which includes support for both Python and R.
        # See also https://github.com/DataBiosphere/terra-docker/blob/master/terra-jupyter-gatk/CHANGELOG.md
        String dockerImage = 'us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.7'
        Int cpu = 1
        Int memoryGB = 2
        Int diskGB = 10
        Int maxRetries = 0
        Int preemptibleAttempts = 3
    }

    call RunPapermillNotebook {
        input:
            notebookWorkspacePath=notebookWorkspacePath,
            papermillParameters=papermillParameters,
            packagesToPipInstall=packagesToPipInstall,
            dockerImage=dockerImage,
            cpu=cpu,
            memoryGB=memoryGB,
            diskGB=diskGB,
            maxRetries=maxRetries,
            preemptibleAttempts=preemptibleAttempts
    }

    output {
        File outputIpynb = RunPapermillNotebook.outputIpynb
        File outputHtml = RunPapermillNotebook.outputHtml
        File tarOutputs = RunPapermillNotebook.tarOutputs
    }

}

task RunPapermillNotebook {
    input {
        # This should be the GCS path to a notebook file in the workspace bucket.
        File notebookWorkspacePath
        # See also https://papermill.readthedocs.io/en/latest/usage-cli.html
        String papermillParameters = ''
        String? packagesToPipInstall
        # See also https://github.com/DataBiosphere/terra-docker/blob/master/terra-jupyter-gatk/CHANGELOG.md
        String dockerImage = 'us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.7'
        Int cpu = 1
        Int memoryGB = 2
        Int diskGB = 10
        Int maxRetries = 0
        Int preemptibleAttempts = 3
    }
  
    String workDir = 'workdir'
    String notebookOutputFile = basename(notebookWorkspacePath, ".ipynb") + "_out.ipynb"
    String notebookHTMLFile = basename(notebookWorkspacePath, ".ipynb") + "_out.html"
    String tarOutputsFile = 'outputs.tar.gz'

    command <<<
        set -o xtrace
        # For any command failures in this script, return the error.
        set -o errexit
        set -o pipefail
        set -o nounset

        mkdir -p ~{workDir}
        cd ~{workDir}

        ~{if defined(packagesToPipInstall)
          then "pip3 install ~{packagesToPipInstall} "
          else "echo there are no additional packages to pip install "}

        # Execute the notebook using our passed parameter values. If the notebook has an error,
        # don't exit the task immediately, but do return the error code after the HTML version of
        # the executed notebook is captured for easy reading.
        # https://papermill.readthedocs.io/en/latest/usage-execute.html#execute-via-cli
        set +o errexit
        papermill "~{notebookWorkspacePath}" "~{notebookOutputFile}" ~{papermillParameters}
        papermill_exit_code=$?
        set -o errexit

        # Export the notebook to HTML (without rerunning it) to capture provenance.
        jupyter nbconvert --to html --ExtractOutputPreprocessor.enabled=False "~{notebookOutputFile}"
        
        # Create a tar to also capture any outputs written to subdirectories, in addition to the current working directory.
        cd ..
        tar -zcvf ~{tarOutputsFile} --directory ~{workDir} --exclude ~{notebookOutputFile} --exclude ~{notebookHTMLFile} .

        exit ${papermill_exit_code}
    >>>

    output {
        File outputIpynb = workDir + '/' + notebookOutputFile
        File outputHtml = workDir + '/' + notebookHTMLFile
        File tarOutputs = tarOutputsFile
    }

    # See also https://cromwell.readthedocs.io/en/stable/RuntimeAttributes/#recognized-runtime-attributes-and-backends
    # How to configure GPUs https://support.terra.bio/hc/en-us/articles/360055066731
    runtime {
        docker: dockerImage
        memory: memoryGB + ' GB'
        disks: 'local-disk ' + diskGB + ' SSD'
        maxRetries: maxRetries
        preemptible: preemptibleAttempts
        cpu: cpu
    }

    parameter_meta {
        notebookWorkspacePath: {
            help: 'The GCS path to the Jupyter notebook ipynb file to be executed.',
            suggestions: ['TODO path to test notebook in featured workspace.']
        }
        papermillParameters: {
            help: 'An optional space-separated list of papermill parameter command line arguments. See also https://papermill.readthedocs.io/en/latest/usage-cli.html.',
            suggestions: ['-p SOME_NUMBER 42 -p SOME_STRING "update these to match the test notebook from the featured workspace"']
        }
        packagesToPipInstall: {
            help: 'An optional space-separated list of pip packages to install.',
            suggestions: ['fsspec[gcs] imagecodecs']
        }
        dockerImage: {
            help: 'The Terra Jupter Docker image to use. See also https://github.com/DataBiosphere/terra-docker/.',
            suggestions: [
                'us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.7',
                'us.gcr.io/broad-dsp-gcr-public/terra-jupyter-python:1.0.13',
                'us.gcr.io/broad-dsp-gcr-public/terra-jupyter-r:2.1.5'
            ]
        }
        cpu: {help: 'The number of CPUs to use.'}
        memoryGB: {help: 'The amount of RAM in gigabytes to provision.'}
        diskGB: {help: 'The amount of SSD disk space in gigabytes to provision.'}
        maxRetries: {help: 'The number of retries to perform to tolerate transient job failures.'}
        preemptibleAttempts: {help: 'The maximum number of times Terra should request a preemptible machine for this task before using a non-preemptible machine.'}
    }

    meta {
        email: 'terra-solutions-team@google.com'
    }
}
