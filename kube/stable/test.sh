#!/bin/bash -ex

echo "Meta serve tests..."
curl --fail -o /tmp/table_metadata.json "https://lsst-lsp-stable.ncsa.illinois.edu/api/meta/v1/db/1/1/tables/1/"
