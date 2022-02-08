# Copyright 2021 Verily Life Sciences LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import json
import os
import subprocess

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing import image_dataset_from_directory

# DEBUG_LABELS = [
#     "females",
#     "gynandromorph",
#     "intersex",
#     "males",
#     "multiple-males",
#     "multiple-nonmales",
# ]
# PATCH_CAMELYON_LABELS = ['non_metastatic', 'metastatic']


def generate_camelyon_datasets(batch_size):
    ds, ds_info = tfds.load("patch_camelyon", with_info=True, as_supervised=True)

    # Get the train, validation and test datasets
    training_data = ds["train"]
    validation_data = ds["validation"]
    test_data = ds["test"]

    # shuffle train_data
    buffer_size = 1000
    training_data = training_data.shuffle(buffer_size)

    # batch and prefetch
    training_data = training_data.batch(batch_size).prefetch(1)
    validation_data = validation_data.batch(batch_size).prefetch(1)
    test_data = test_data.batch(batch_size).prefetch(1)

    return (training_data, validation_data, test_data, ds_info)


def generate_debug_datasets(
    num_replicas, copy_datap, input_data, input_data_dir, batch_size, image_size
):
    if copy_datap:
        # copy and unzip the dataset to the local file system
        local_dir = "."
        copy_data(input_data, local_dir)
        data_dir = f"{local_dir}/model_data/training_data"
        print(f"training data dir: {data_dir}")

        (training_set, validation_set) = create_debug_datasets(
            data_dir, batch_size, num_replicas, image_size
        )
    else:
        (training_set, validation_set) = create_debug_datasets(
            input_data_dir,
            batch_size,
            num_replicas,
            image_size,
        )
    return (training_set, validation_set)


def create_debug_datasets(dir_path, base_batch_size, num_acc, image_size):
    print(f"in create_datasets with base batch size {base_batch_size} and num_acc {num_acc}")
    training_set = image_dataset_from_directory(
        dir_path,
        shuffle=True,
        batch_size=(base_batch_size * num_acc),
        image_size=image_size,
        labels="inferred",
        validation_split=0.15,
        subset="training",
        seed=1337,
    )

    validation_set = image_dataset_from_directory(
        dir_path,
        shuffle=True,
        batch_size=(base_batch_size * num_acc),
        image_size=image_size,
        labels="inferred",
        validation_split=0.15,
        subset="validation",
        seed=1337,
    )
    return (training_set, validation_set)


def get_model_dirs(save_dir, checkpoint_dir):
    """Defines utility functions for model saving.

    In a multi-worker scenario, the chief worker will save to the
    desired model directory, while the other workers will save the model to
    temporary directories. It’s important that these temporary directories
    are unique in order to prevent multiple workers from writing to the same
    location. Saving can contain collective ops, so all workers must save and
    not just the chief.
    """

    def _is_chief(task_type, task_id):
        return (task_type == "chief" and task_id == 0) or task_type is None

    tf_config = os.getenv("TF_CONFIG")
    if tf_config:
        tf_config = json.loads(tf_config)

        if not _is_chief(tf_config["task"]["type"], tf_config["task"]["index"]):
            save_dir = os.path.join(save_dir, "worker-{}").format(tf_config["task"]["index"])
            checkpoint_dir = os.path.join(checkpoint_dir, "worker-{}").format(
                tf_config["task"]["index"]
            )

    print(f"Setting save_dir to: {save_dir}")
    print(f"Setting checkpoint_dir to: {checkpoint_dir}")

    return (save_dir, checkpoint_dir)


def copy_data(gcs_path, local_path):
    # copy the zip file with the model data
    local_file = f"{local_path}/model_data.zip"
    print(f"copying data from {gcs_path} to {local_file}")
    copyres = subprocess.run(  # noqa: F841
        [
            "gsutil",
            "-m",
            "cp",
            gcs_path,
            local_file,
        ],
        # capture_output=True,
    )
    # print(f"gsutil result: {copyres}")
    # then unzip
    print("unzipping file....")
    import zipfile

    target_dir = local_path
    with zipfile.ZipFile(local_file, "r") as f:
        f.extractall(target_dir)


def define_callbacks(log_dir, checkpoint_dir):
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, update_freq=300)
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_dir,
        #     save_weights_only=True,
        monitor="val_accuracy",
        mode="max",
        save_freq="epoch"
        #     save_best_only=True
    )
    return (tensorboard_callback, model_checkpoint_callback)


def generate_metrics(validation_set, model, num_classes):
    ma = tf.keras.metrics.AUC()
    mp = tf.keras.metrics.Precision()
    mr = tf.keras.metrics.Recall()

    all_preds = []
    all_labels = []

    for images, labels in validation_set.take(len(validation_set)):
        predictions = model.predict(images)
        y_preds = np.argsort(predictions, axis=1)[:, -1:]
        # print(predictions)
        all_preds += list(y_preds.flatten())
        all_labels += list(labels.numpy())
        onehot_labels = tf.keras.utils.to_categorical(labels, num_classes=num_classes)
        # print(onehot_labels)
        ma.update_state(onehot_labels, predictions)
        mp.update_state(onehot_labels, predictions)
        mr.update_state(onehot_labels, predictions)
    return (ma, mp, mr, all_preds, all_labels)
