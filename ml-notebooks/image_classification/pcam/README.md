
# PatchCamelyon Image Classification notebook examples

## About the machine learning task

The examples in this directory use the [PatchCamelyon benchmark](https://www.tensorflow.org/datasets/catalog/patch_camelyon).  It consists of 327.680 color images (96 x 96px) extracted from histopathologic scans of lymph node sections. Each image is annotated with a binary label indicating presence of metastatic tissue.
The machine learning task is to predict whether metastatic tissue is present.

The model uses one of Keras' prebuilt model architectures, [Xception](https://keras.io/api/applications/xception/). The training first does [_transfer learning_](https://en.wikipedia.org/wiki/Transfer_learning), bootstrapping from model weights trained on the ['imagenet'](https://en.wikipedia.org/wiki/ImageNet) dataset, and then runs a fine-tuning stage.

## About the notebook examples

### In-notebook training example

The [01_keras_pcam](./01_keras_pcam.ipynb) notebook shows in-notebook model training (rather than calling out to a cloud service to do the training).

It works on all notebook platforms without requiring access to [Vertex AI](https://cloud.google.com/vertex-ai), or any other Google Cloud Platform (GCP) services aside from Cloud Storage (GCS).  It shows how to build a Keras image classification model, and how to do _transfer learning_ and model _fine-tuning_.

Given the size of the dataset and model architecture, this example requires an 8-core notebook VM, and the notebook should use an attached GPU to run in a reasonable time frame.  On CWB Terra, you can use the default GATK image customized to use 8 CPUs and 1 GPU.

### Using Vertex AI Training, and the Vertex Experiments API

The [02_1_vertex_ai_pcam](./02_1_vertex_ai_pcam.ipynb) and [02_2_vertex_ai_pcam](./02_2_vertex_ai_pcam.ipynb) notebooks show how to run different types of Vertex AI training jobs.
On [Terra](http://app.terra.bio), this notebook requires a ['native' GCP project](https://support.terra.bio/hc/en-us/articles/360051229072-Accessing-advanced-GCP-features-in-Terra).

The notebooks show:

- [Vertex AI Training](https://cloud.google.com/vertex-ai/docs/training/custom-training) via both a training _script_ and a _package_.
- How to set up and use a [Managed Tensorboard](https://cloud.google.com/vertex-ai/docs/experiments/tensorboard-overview) instance to track training progress.
- How to upload and [deploy](https://cloud.google.com/vertex-ai/docs/predictions/deploy-model-api) a trained model to a scalable _Endpoint_ that autoscales up as you hit it with traffic; how to do traffic splitting for A/B testing or canarying.
- How to configure and run a hyperparameter tuning job (and what the Keras-based training code should look like to support this).
- How to configure and run a multi-node distributed training job (and what the training code should do to support this option).
- How to use the **Experiments API** to create an _Experiment_, log info about the training runs (metrics, params, etc.) to the [Metadata Server](https://cloud.google.com/vertex-ai/docs/ml-metadata/introduction), and how to access and analyze the logged data.

### Using Vertex Pipelines

[Vertex Pipelines](https://cloud.google.com/vertex-ai/docs/pipelines) lets you codify your machine learning workflow, supporting workflow reproducibility, composability, collaboration, and more.

On [Terra](http://app.terra.bio), these notebooks similarly require a ['connected' GCP project](https://support.terra.bio/hc/en-us/articles/360051229072-Accessing-advanced-GCP-features-in-Terra).

The [03_vertex_pipelines_pcam](./03_vertex_pipelines_pcam.ipynb) notebook shows, in addition to the concepts introduced in the notebook above:

- how to use the [KFP SDK](https://www.kubeflow.org/docs/components/pipelines/sdk/install-sdk/) to build pipelines
- use of [‘first-party’ components]((https://github.com/kubeflow/pipelines/tree/master/components/google-cloud/google_cloud_pipeline_components)) that wrap calls to Vertex AI services
- building and using ‘lightweight’ Python-based custom components; how to generate `yaml` files for the component definitions that can be put under version control and shared.
- step caching (very useful for iterative development)
- pipeline control structures: conditionally deploy a model if its metrics are sufficiently good
