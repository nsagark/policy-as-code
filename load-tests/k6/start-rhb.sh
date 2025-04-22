#!/usr/bin/env bash

set -euo pipefail

NAMESPACE="load-test"

if [[ $# -lt 3 ]]; then
        echo "Usage: $0 <script> <vus> <iterations>" 1>&2
        echo "Example: $0 tests/my-test.js 10 100" 1>&2
        exit 1
fi

SCRIPT="$1"
VUS="$2"
ITERATIONS="$3"

if [[ $ITERATIONS -lt $VUS ]]; then
        echo "iterations must be greater or equal to vus" 1>&2
        exit 1
fi

echo "Deploying namespace..."
kubectl create ns "$NAMESPACE"

echo "Deploying RBAC..."
kubectl apply -n "$NAMESPACE" -f rbac.yaml

# copy the script to a temp file under a common name
# so that we can reference always to the same name in the pod
SCRIPT_DIR=$(mktemp -d)
NEW_SCRIPT_PATH="${SCRIPT_DIR}/script.js"

cp "$SCRIPT" "$NEW_SCRIPT_PATH"

echo "Creating configmap..."
kubectl create configmap -n "$NAMESPACE" load-test --from-file="$NEW_SCRIPT_PATH" --from-file="tests/util.js" --from-literal="vus=$VUS" --from-literal="iterations=$ITERATIONS"

rm -rf "$SCRIPT_DIR"

echo "Deploying k6 job..."
kubectl apply -n "$NAMESPACE" -f job.yaml

echo "Waiting for the job to be completed..."
kubectl wait -n "$NAMESPACE" --for=condition=complete --timeout=-1s jobs/load-test

echo "Extracting logs and summary..."
kubectl logs -n "$NAMESPACE" jobs/load-test > "$(basename "$SCRIPT")-${VUS}vu-${ITERATIONS}it-logs.txt"

echo "Clean up job and configmap..."
kubectl delete -n "$NAMESPACE" jobs load-test
kubectl delete -n "$NAMESPACE" configmap load-test
kubectl delete clusterrolebinding load-test

echo "Clean up..."
kubectl delete ns "$NAMESPACE"
