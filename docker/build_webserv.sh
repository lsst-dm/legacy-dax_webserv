#!/bin/sh

# LSST Data Management System
# Copyright 2016 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.


# Create a base image with only stack prerequisites
# @author  Brian Van Klaveren, SLAC

set -e

DEFAULT_TAG="webserv/webserv:webserv_latest"

usage() {
  cat << EOD

  Usage: $(basename "$0") [options]

  This command builds a base image which includes only stack prerequisites.

  Available options:
    -h          this message
    -D          Docker Tag name. Defaults to $DEFAULT_TAG
    -E          EUPS tag. Defaults to dax_latest.

EOD
}

# get the options
while getopts hD:E: c; do
    case $c in
            h) usage ; exit 0 ;;
            D) TAG="$OPTARG" ;;
            E) EUPS_TAG="$OPTARG" ;;
            p) PUSH=1 ;;
            \?) usage ; exit 2 ;;
    esac
done

shift "$((OPTIND-1))"

if [ $# -ne 0 ] ; then
    usage
    exit 2
fi

if [ -z $TAG ]  ; then
    # Use defeault tag
    TAG=$DEFAULT_TAG
fi

if [ $EUPS_TAG ]  ; then
    EUPS_TAG="EUPS_TAG=$EUPS_TAG"
fi

# Build the release image

printf "Building base image with tag: %s\n" $TAG

docker build --no-cache ${EUPS_TAG:+"--build-arg"} $EUPS_TAG --tag="$TAG" webserv
