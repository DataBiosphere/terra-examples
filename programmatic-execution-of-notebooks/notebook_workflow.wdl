# Copyright 2022 Verily Life Sciences LLC
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file or at https://developers.google.com/open-source/licenses/bsd
#
# Initial proof of concept version of the papermill notebook execution workflow.
#
# Coding standard https://biowdl.github.io/styleGuidelines.html is used with newer command body
# style https://github.com/openwdl/wdl/blob/main/versions/1.0/SPEC.md#command-section.

version 1.0

workflow NotebookWorkflow {
    call RunPapermillNotebook {}
}

task RunPapermillNotebook {
    input {
        # This should be the GCS path to a notebook file in the workspace bucket.
        File notebookWorkspacePath
        # See also https://papermill.readthedocs.io/en/latest/usage-cli.html
        String papermillParameters
        String? packagesToPipInstall
        # See also https://github.com/DataBiosphere/terra-docker/blob/master/terra-jupyter-python/CHANGELOG.md
        String dockerImage = 'us.gcr.io/broad-dsp-gcr-public/terra-jupyter-python:1.0.6'
        Int cpu = 1
        Int memoryGB = 2
        Int diskGB = 10
        Int maxRetries = 0
        Int preemptibleAttempts = 3
    }
  
    String notebookOutputFile = basename(notebookWorkspacePath, ".ipynb") + "_out.ipynb"
    String notebookHTMLFile = basename(notebookWorkspacePath, ".ipynb") + "_out.html"

    command <<<
        set -o xtrace
        # For any command failures in this script, return the error.
        set -o errexit
        set -o pipefail
        set -o nounset

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
        
        exit ${papermill_exit_code}
    >>>

    output {
        File outputIpynb = notebookOutputFile
        File outputHtml = notebookHTMLFile
        # TODO capture output in subdirectories
        Array[File] outputs = glob("*")
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
}
