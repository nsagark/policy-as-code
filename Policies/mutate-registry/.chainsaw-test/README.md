# Chainsaw tests for mutate-registry Policy

This section details the Chainsaw tests for the mutation policy to update image region for ECR images.

The test has following steps:

### Step 1:

Apply the configmap that sets the region to `us-west-2`

### Step 2:

Apply the `mutate-registry.yaml` policy and verify that the policy is status is set to `True` and is ready.

### Step 3:

Run the policy against a pod.yaml which has an ecr image set for a certain region. The mutation policy changes the ecr region of the image to the one set from the configmap. The mutated policy is verified against the patched yaml file to validate the policy is working.

### Step 4:

The policy, in this step, is implemented against a manifest without a proper ecr image. The mutation does not impact this manifest and the resource stays the same.