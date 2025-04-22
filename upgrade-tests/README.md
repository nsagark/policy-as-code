## Upgrade tests across different versions of N4K & Kyverno OSS

This repository contains a Chainsaw test that automates testing of the following upgrade sequence:

```sh
OSS 1.10 --> N4K 1.10 --> N4K 1.11 --> OSS 1.11
```

The test uses YAML manifests to emulate the ArgoCD upgrade which will render manifests from a helm chart.

The steps followed at each installation are:

## Pre-Requisites

1. Install a cluster on Kind

2. All tests are run on Kubernetes v1.28

3. Install Chainsaw 

4. Install Go

5. Install CRD

## Installation, Upgrade and Testing Steps

1. All versions are installed using *.yaml files created using helm templates.

2. For install/ upgrade, we use the following command on each .yaml file to the corresponding release.

```sh
kubectl apply -f <filename.yaml> --server-side=true
```

3. After installing Kyverno, we wait for sometime for all the pods to come up properly.

4. Once all the pods are up and running, we use a policy `require-run-as-nonroot` to validate Kyverno functionality.

5. Chainsaw tests are run on the cluster to validate the policies for both positive and negative test cases for each version of Kyverno.

6. A successful run implies that each version mentioned above is installed properly, Kyverno pods are brought up and the policies that are configured at the first step are working through the upgrade.

## Assumptions

1. We introduced a sleep in the code to give enough time for the pods to come up properly after each upgrade.

2. Cronjobs are deleted after upgrading from each N4K version to clear the completed pods.

## Sample Run

https://github.com/nirmata/robinhood-pov/actions/runs/9529404982/job/26268121426