from enum import Enum
import json
import os
import shlex
import subprocess
import time

from absl import app
from absl import flags
from pathlib import Path

class TerraStack(Enum):
    RWB = 1  # All of Us Researcher Workbench
    CWB = 2  # app.terra.bio
    TVC = 3  # multi-cloud Terra

# Infer the technical foundation from environment variables.
terra_stack = None
if "WORKSPACE_CDR" in os.environ:
    terra_stack = TerraStack.RWB
elif "WORKSPACE_BUCKET" in os.environ:
    terra_stack = TerraStack.CWB
else:
    terra_stack = TerraStack.TVC

# TODO: how to keep the Docker tags up to date?
default_docker_image = {
    TerraStack.RWB: 'us.gcr.io/broad-dsp-gcr-public/terra-jupyter-aou:2.1.6',
    TerraStack.CWB: 'us.gcr.io/broad-dsp-gcr-public/terra-jupyter-gatk:2.2.7',
    TerraStack.TVC: 'us-central1-docker.pkg.dev/terra-vdevel-potent-beet-7262/my-repo/rcpu-terra'
}

# Use the TVC autodelete bucket for any defaults.
# This resource was created via notebook setup_cloudtop.ipynb but eventually every workspace should have one.
TVC_AUTODELETE_BUCKET_REFERENCE = 'blob_data_autodelete_after_one_week'

FLAGS = flags.FLAGS

flags.DEFINE_boolean('dry_run', True, 'Dry run - output generated commands only.')

# Papermill flags
flags.DEFINE_integer('start_timeout', 300, 'Papermill start timeout', lower_bound=0)
flags.DEFINE_string('parameters_file', None, 'Papermill parameters file', short_name='f')
flags.DEFINE_multi_string('parameters', None,
                          'Quoted Papermill parameter-value paris to pass to the parameters cell.'
                          'Should take the form "PARAMETER VALUE"', short_name='p')
flags.DEFINE_multi_string('packages_to_install', None,
                          'Optional packages to install using pip3', short_name='i')
flags.DEFINE_string('notebook_to_run', None, 'Notebook to run via papermill')
flags.DEFINE_string('output_notebook', None, 'Output notebook rendered by papermill')

# Environment variables available to notebook
flags.DEFINE_string('output_path', None, 'Write notebook outputs (CSV files, etc.) to this path')

# dsub flags
flags.DEFINE_string('name', None, 'dsub job name')
flags.DEFINE_string('logging', None, 'dsub logging path')
flags.DEFINE_string('image', default_docker_image[terra_stack], 'dsub Docker image')
flags.DEFINE_integer('boot_disk_size', 60, 'dsub boot disk size in GB.')

terra_status = None
terra_auth_status = None
if terra_stack == TerraStack.TVC:
    flags.DEFINE_string('output_bucket_reference', TVC_AUTODELETE_BUCKET_REFERENCE,
                        'The reference name for the destination bucket for results.')
    terra_status = json.loads(subprocess.run('terra status --format json',
                                             capture_output=True, shell=True).stdout.decode('utf-8'))
    terra_auth_status = json.loads(subprocess.run('terra auth status --format json',
                                                  capture_output=True, shell=True).stdout.decode('utf-8'))

# Required flags
flags.mark_flag_as_required('notebook_to_run')

def getPapermillCmd(start_timeout, parameters, has_parameters_file = False):
    parameters_str = ''.join([f'--parameters {p.split(maxsplit=1)[0]} {p.split(maxsplit=1)[1]} '
                              for p in parameters]) if parameters else ''
    parameters_file_str = '--parameters_file ${PARAMETERS_FILE} ' if has_parameters_file else ''
    return ('papermill '
            f'--start-timeout {start_timeout} '
            f'{parameters_str}'
            f'{parameters_file_str}'
            '"${NOTEBOOK_TO_RUN}" '
            '"${OUTPUT_NOTEBOOK}"')

def getPipCmd(packages_to_install):
    return f"pip3 install {' '.join(packages_to_install)}"

def getPetServiceAccount():
    cmd = 'gcloud auth list --format json'
    json_str = subprocess.run(cmd.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
    return json.loads(json_str)[0]['account']

def getDsubCmd(job_name,
               dsub_user,
               logging_path,
               image,
               boot_disk_size,
               papermill_cmd,
               pip_cmd,
               parameters_file,
               notebook_to_run,
               output_notebook,
               output_path,
               unparsed_flags):
    if terra_stack == TerraStack.TVC:
        google_project = terra_status['workspace']['googleProjectId']
        dsub_user = terra_auth_status['userEmail'].split('@')[0]
        service_account = terra_auth_status['serviceAccountEmail']
        env_flags = ''
    else:
        google_project = os.getenv('GOOGLE_PROJECT')
        dsub_user = os.getenv('OWNER_EMAIL').split('@')[0]
        service_account = getPetServiceAccount()
        env_variables = ['GOOGLE_PROJECT',
                         'WORKSPACE_BUCKET',
                         'WORKSPACE_CDR',
                         'WORKSPACE_NAMESPACE',
        ]
        env_flags = '\n'.join([f'--env {v}={os.getenv(v)} \\' for v in env_variables])

    parameters_file_flag = f'\n--input PARAMETERS_FILE={parameters_file} \\' if parameters_file else '' 

    cmd = f"'cd ${{OUTPUT_PATH}} {'&& ' + pip_cmd if pip_cmd else ''} && {papermill_cmd}; true; cp \"${{OUTPUT_NOTEBOOK}}\" ${{OUTPUT_PATH}}'"
    return f'''dsub \\
--name {job_name} \\
--provider google-cls-v2 \\
--boot-disk-size {boot_disk_size} \\
--project {google_project} \\
--network "network" \\
--subnetwork "subnetwork" \\
--service-account {service_account} \\
--user {dsub_user} \\
--zones "us-central1-*" \\
--logging {logging_path} \\
--image {image} \\ 
{env_flags}
--input NOTEBOOK_TO_RUN="{notebook_to_run}" \\ {parameters_file_flag}
--output OUTPUT_NOTEBOOK="{output_notebook}" \\
--output-recursive OUTPUT_PATH={output_path} \\
--command {cmd}
''' + ' '.join(unparsed_flags)

def main(argv):
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    
    job_name = FLAGS.name
    if not job_name:
        job_name = Path(FLAGS.notebook_to_run).stem.replace(' ', '_')
    
    if terra_stack == TerraStack.TVC:
        dsub_user = terra_auth_status['userEmail'].split('@')[0]
        dereference_result = subprocess.run(f'terra resolve --name={FLAGS.output_bucket_reference}',
                                               capture_output=True, shell=True)
        if dereference_result.returncode != 0:
            raise ValueError(f'''Reference name "{FLAGS.output_bucket_reference}" does not resolve to a bucket in the current workspace.
            Use parameter --output_bucket_reference to pass a valid reference name to a bucket in this workspace.
            ''')
        workspace_bucket: str = dereference_result.stdout.decode('utf-8').rstrip()
    else:
        dsub_user = os.getenv('OWNER_EMAIL').split('@')[0]
        workspace_bucket = os.getenv('WORKSPACE_BUCKET')
        
    (job_date, job_time) = timestamp.split('_')

    output_path = FLAGS.output_path
    if not output_path:
        output_path = f'{workspace_bucket}/dsub/results/{job_name}/{dsub_user}/{job_date}/{job_time}'
        
    logging_path = FLAGS.logging
    if not logging_path:
        logging_path = f'{workspace_bucket}/dsub/logs/{job_name}/{dsub_user}/{job_date}/{job_time}'

    papermill_cmd = getPapermillCmd(
            start_timeout=FLAGS.start_timeout,
            parameters=FLAGS.parameters,
            has_parameters_file=FLAGS.parameters_file)

    packages_to_install = FLAGS.packages_to_install
    pip_cmd = getPipCmd(
        packages_to_install=packages_to_install) if packages_to_install else None

    # If the notebook is local, upload it to the output path.
    notebook_to_run = FLAGS.notebook_to_run
    if not notebook_to_run.startswith('gs://'):
        notebook_to_run = os.path.join(output_path, 'input_notebook', os.path.basename(FLAGS.notebook_to_run))

    output_notebook = FLAGS.output_notebook
    if not output_notebook:
        output_notebook = notebook_to_run.replace('.ipynb', f'_{timestamp}.ipynb')

    dsub_cmd = getDsubCmd(
            job_name=job_name,
            dsub_user=dsub_user,
            logging_path=logging_path,
            image=FLAGS.image,
            boot_disk_size=FLAGS.boot_disk_size,
            papermill_cmd=papermill_cmd,
            pip_cmd=pip_cmd,
            parameters_file=FLAGS.parameters_file,
            notebook_to_run=notebook_to_run,
            output_notebook=output_notebook,
            output_path=output_path,
            unparsed_flags=argv[1:]
    )

    print(f'dsub command: {dsub_cmd}')
    if FLAGS.dry_run:
        print('Dry run - exiting.')
        return
    if notebook_to_run != FLAGS.notebook_to_run:
        subprocess.run(f'gsutil cp "{FLAGS.notebook_to_run}" "{notebook_to_run}"', shell=True)
    subprocess.run(shlex.split(dsub_cmd.replace('\\', ''), posix=True))

if __name__ == "__main__":
    app.run(main)
