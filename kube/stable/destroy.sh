#!/bin/bash -x
DAX_NAMESPACE=${DAX_NAMESPACE:-'dax-stable'}

kubectl delete ingress dax-webserv-ingress --namespace $DAX_NAMESPACE
kubectl delete service dax-webserv-service --namespace $DAX_NAMESPACE
kubectl delete deployment dax-webserv-deployment --namespace $DAX_NAMESPACE
kubectl delete pvc dax-webserv-datasets-claim --namespace $DAX_NAMESPACE
kubectl delete pv dax-prod-webserv-datasets-volume
