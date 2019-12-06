#!/bin/bash

function dc-exec {
    sudo docker-compose exec "$@"
}

echo "[DATACUBE-INGEST] Ingesting sample data..."

echo "[DATACUBE-INGEST] Adding new product definition to datacube..."
dc-exec www datacube product add "/datacube/ingest/dataset_types/ls8_collections_sr_scene.yaml"

echo "[DATACUBE-INGEST] Preparing data for ingestion..."
dc-exec www bash -c "python3 /datacube/ingest/prepare_scripts/usgs_ls_ard_prepare.py /datacube/original_data/LC08*"

echo "[DATACUBE-INGEST] Adding dataset metadata to datacube..."
dc-exec www bash -c "datacube dataset add /datacube/original_data/LC08*/*.yaml --auto-match"

echo "[DATACUBE-INGEST] Ingesting data..."
dc-exec www datacube -v ingest \
    -c "/datacube/ingest/ingestion_configs/ls8_collections_sr_fuente_de_piedra_example.yaml"  \
    --executor multiproc 2

echo "[DATACUBE-INGEST] Data ingestion finished."
