#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
DEST_PATH="$SCRIPT_DIR/datasets"

DATASET_NAME="rowhitswami/nips-papers-1987-2019-updated"

kaggle datasets download -d "$DATASET_NAME" -p "$DEST_PATH" --unzip

# Delete all downloaded files except papers.csv
rm -f "$DEST_PATH/authors.csv"