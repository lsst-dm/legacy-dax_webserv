#!/bin/bash -ex

echo "Image serve tests..."

curl --fail -o /tmp/calexp_i6_out.fits "https://lsst-lsp-int.ncsa.illinois.edu/api/image/v1/DC_W13_Stripe82?ds=calexp&ra=37.644598&dec=0.104625&filter=r"

echo "Meta serve tests..."
curl --fail -o /tmp/table_metadata.json "https://lsst-lsp-int.ncsa.illinois.edu/api/meta/v1/db/1/1/tables/1/"
