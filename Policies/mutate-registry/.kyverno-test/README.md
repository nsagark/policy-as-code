# Kyverno CLI tests for mutate-registry Policy

This section details the Kyverno CLI tests for the mutation policy to update image region for ECR images.

The test validates the `mutation-registry.yaml` policy for both positive and negative test using the Kyverno CLI tests for the following resources:

1. Deployments
2. CronJobs
3. A Pod using an init container

`values.yaml` has the region information from the configmap which is passed to the test file. The bad and good resources are passed using the `resources.yaml` file. 

After applying the policy, each resource is validated against it's `patchedResource` to validate whether the ecr region is updated or not. Correct images with ecr in their image with the wrong region is updated with the correct region from configmap.