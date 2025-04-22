# Mutate ECR Region

Mutate ECR region based on in-cluster ConfigMap.

**NOTE**: This policy requires Kyverno v1.11 and above

## Install

```sh
kubectl apply -f policies/mutate-registry/
```

## Test

### Pod with a ECR image

```sh
kubectl run test --image=844333597536.dkr.ecr.us-west-1.amazonaws.com/kyverno-demo:v1 --dry-run=server -o yaml | grep "image: "
  - image: 844333597536.dkr.ecr.us-west-2.amazonaws.com/kyverno-demo:v1
```

### Pod with a non-ECR image

```sh
kubectl run test --image=nginx --dry-run=server -o yaml | grep "image: "
  - image: nginx
```

### Deployment with a ECR image

```sh
kubectl create deploy test --image=844333597536.dkr.ecr.us-west-1.amazonaws.com/kyverno-demo:v1 --dry-run=server -o yaml | grep "image: "
      - image: 844333597536.dkr.ecr.us-west-2.amazonaws.com/kyverno-demo:v1
```

### Deployment with an init container

Use a deployment with 2 containers:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      initContainers:
      - image: 844333597536.dkr.ecr.us-west-1.amazonaws.com/kyverno-demo:v1
        name: init-1
      containers:
      - image: aws_account_id.dkr.ecr.us-west-2.amazonaws.com/my-repository:tag
        name: container-1
```

```sh
kubectl create -f /tmp/deploy.yaml --dry-run=server -o yaml | grep "image: "
      - image: 844333597536.dkr.ecr.us-west-2.amazonaws.com/kyverno-demo:v1
      - image: 844333597536.dkr.ecr.us-west-2.amazonaws.com/kyverno-demo:v1
```
