#!/bin/bash

kubectl create namespace platform

helm repo add signoz https://charts.signoz.io
helm repo update

helm install signoz signoz/signoz \
  -n platform