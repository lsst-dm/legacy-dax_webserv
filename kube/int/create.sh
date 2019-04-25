#!/bin/bash -ex
DAX_NAMESPACE=${DAX_NAMESPACE:-'dax-int'}

# kubectl create -f dax-webserv-datasets-volume.yaml
# kubectl create -f dax-webserv-datasets-claim.yaml --namespace $DAX_NAMESPACE
kubectl create -f dax-webserv-deployment.yaml --namespace $DAX_NAMESPACE
kubectl create -f dax-webserv-service.yaml --namespace $DAX_NAMESPACE
kubectl create -f dax-webserv-ingress.yaml --namespace $DAX_NAMESPACE
