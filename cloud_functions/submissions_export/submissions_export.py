import firecloud.api as fapi
import os
import pandas as pd
from datetime import datetime
import pandas_gbq


def get_workflow_metadata(namespace, workspace, submission_id, workflow_id):
    r = fapi.get_workflow_metadata(namespace, workspace, submission_id, workflow_id)
    if r.status_code == 200:
        return r.json()
    else:
        print(f'Error retrieving workflow id {workflow_id} with error {r.text}')


def get_workflow_entity_name(workflow):
    try:
        return workflow['workflowEntity']['entityName']
    except KeyError:
        return 'N/A'


def load_one_submission(namespace, workspace, submission_id):
    r = fapi.get_submission(namespace, workspace, submission_id)
    TIME_FORMAT_STRING = '%Y-%m-%dT%H:%M:%S.%fZ'
    df = ''
    if r.status_code == 200:
        data = []
        headers = ['submissionId','workflowId','entityName', 'status', 'cost','start', 'end', 'duration', 'submitter']
        workflows = r.json()['workflows']
        submitter = r.json()['submitter']
        print(f'Loading workflows for submission {submission_id}:')
        for workflow in workflows:
            cost = workflow.get('cost') or 0.0
            status = workflow['status']
            workflow_id = workflow['workflowId']
            entity_name = get_workflow_entity_name(workflow)
            wf_metadata = get_workflow_metadata(namespace, workspace, submission_id, workflow_id)
            start = datetime.strptime(wf_metadata['start'], TIME_FORMAT_STRING)
            end = datetime.strptime(wf_metadata['end'], TIME_FORMAT_STRING)
            duration = str(end-start)
            data.append([submission_id, workflow_id, entity_name, status, cost, start, end, duration, submitter])
        return pd.DataFrame(data=data, columns=headers)
    else:
        print(f'Error retrieving submission id {submission_id} with error {r.text}')


def load_all_submissions(namespace, workspace, all_submission_ids):
    dfs = []
    for submission_id in all_submission_ids:
        dfs.append(load_one_submission(namespace, workspace, submission_id))
    return pd.concat(dfs)


def list_submissions(namespace, workspace):
    r = fapi.list_submissions(namespace, workspace)
    df = ''
    all_submission_ids = []
    if r.status_code == 200:
        data = []
        headers = ['submissionId', 'userComment', 'submissionDate', 'numComplete', 'numFailed']
        for submission in r.json():
            submissionId = submission['submissionId']
            userComment = submission['userComment']
            submissionDate = submission['submissionDate']
            workflowStatuses = submission['workflowStatuses']
            numComplete = workflowStatuses.get('Succeeded') or 0
            numFailed = workflowStatuses.get('Failed') or 0
            data.append([submissionId, userComment, submissionDate, numComplete, numFailed])
            all_submission_ids.append(submissionId)
        data.sort(key=lambda x: x[2], reverse=True) # Sort by submissionDate
        df = pd.DataFrame(data=data, columns=headers)
    else:
        print(f'Error listing submissions for {namespace}/{workspace} with error {r.text}')
    return all_submission_ids, df


def main(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    namespace = os.environ['WORKSPACE_NAMESPACE']
    workspace = os.environ['WORKSPACE_NAME']
    bigquery_project_id = os.environ['BIGQUERY_PROJECT_ID']
    table_id = os.environ['TABLE_ID']
    all_submission_ids, _df = list_submissions(namespace, workspace)
    submission_df = load_all_submissions(namespace, workspace, all_submission_ids)
    submission_df.to_gbq(table_id, project_id=bigquery_project_id, if_exists='replace')
    return 'Success'
