# Automate exporting workflow submissions to BigQuery with Cloud Functions and Cloud Scheduler

There exists [this notebook](https://app.terra.bio/#workspaces/vts-playground/willyn-export-job-submission/notebooks/launch/willyn_get_workflow_data.ipynb) which uses the Firecloud API to list all the submissions of the a workspace and export it to BigQuery. This notebook had to be run manually, which becomes a problem when you need live, up-to-date data in BigQuery. Follow these instructions to create a Cloud Function which can automate the export. 


## Prerequisite setup

1) Create a new [service account](https://cloud.google.com/iam/docs/service-accounts), or choose an existing one. Download the json keyfile for this service account. 
2) Grant this service account BigQuery Data Editor to the destination dataset.
3) Grant this service account BigQuery Job User in the destination project. 
4) Register the service account to Terra using the [register_service_account.py](https://github.com/broadinstitute/firecloud-tools/blob/master/scripts/register_service_account/register_service_account.py) script. 
    ```
    python register_service_account.py -j keyfile.json -e "example@email.com"
    ```
5) Add the registered account to the proper Terra group. Doing so will grant the service account the ability to pull the workflow submission data. 

## Create the Cloud Function
1) Navigate to [Cloud Functions](https://console.cloud.google.com/functions/add) and add a new one. 
2) Choose 1st gen environment, and trigger type "Cloud Pub/Sub". Create a new Pub/Sub topic. 
3) In the runtime section, **choose the service account from the prerequisite step** as the runtime service account. 
4) Set memory, timeout, and autoscaling as needed. See considerations section for more details. 
5) Add the following Runtime environment variables:
    ```
    WORKSPACE_NAMESPACE   The Terra billing project containing the workspace.
    WORKSPACE_NAME        The name of the workspace containing the workflow submissions.
    BIGQUERY_PROJECT_ID   The name of the Google Cloud project holding the destination bigquery table.
    TABLE_ID              The full path of the destination table. Format: `project_id.dataset_id.table_id`
    ```
6) Click next to navigate the code editing section.
7) Choose Python 3.7 as the language. Add the submissions_export.py and requirements.txt files. 
8) Enter "main" as the entry point. 
9) Deploy and test.

## Create the Cron Job with Cloud Scheduler
1) Navigate to [Cloud Scheduler](https://console.cloud.google.com/cloudscheduler) and add a new one.
2) Specify a frequency using the unix-cron format. For example `0 * * * *` will run every hour at minute 0. See [here](https://crontab.guru/every-1-hour) for help. 
3) Choose Pub/Sub as the Target type. Select the pub/sub topic you created above. Write anything for the message body, it will not be used. 
4) Set the retry config appropriately. I went with 1 max retry attempt. 
5) Done! 

## Error handling
Generally all errors in your cloud function will be available in logging. Select your cloud function, and navigate to the logging section. You should be able to see call stacks of errors logged here. 
## Considerations
The script will take several minutes for workspaces with a large number of submissions. For a workspace with ~400 workflows, the script may take ~4 minutes. 
The amount of memory you will need will scale with the number of submissions as well. 