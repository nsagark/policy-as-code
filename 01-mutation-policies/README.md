# Mutation Policies

This section demonstrates how to use Kyverno mutation policies to automatically modify Kubernetes resources at admission time.

## What You'll Learn

- How to automatically inject labels into resources
- How to set default resource limits
- How to enforce pod security standards

## Policies Included

1. **Label Injection** (`add-labels.yaml`)
   - Automatically adds a label `foo=bar` to all pods, services, configmaps and secrets

2. **Resource Defaults** (`resource-defaults.yaml`)
   - Sets default CPU/memory requests for containers

3. **Pod Security** (`pod-security.yaml`)
   - Adds security context settings
   - Sets non-root user requirements

## Try It Out

1. Apply the label injection policy:
```bash
kubectl apply -f add-labels.yaml
```

2. Create a test pod:
```bash
kubectl apply -f test-pod.yaml
```

3. Verify the labels were added:
```bash
kubectl get pod test-pod -o yaml
```

Expected output will show automatically injected labels:
```yaml
metadata:
  labels:
    foo: bar
```

## Cleanup

Remove the policies and test resources:
```bash
kubectl delete -f .
``` 
