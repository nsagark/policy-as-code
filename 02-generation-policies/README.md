# Generation Policies

This section demonstrates how to use Kyverno generation policies to automatically create companion resources when certain resources are created.

## What You'll Learn

- How to automatically generate Network Policies
- How to create ConfigMaps for applications
- How to generate Secrets with proper configurations

## Policies Included

1. **Network Policy Generation** (`network-policy-generator.yaml`)
   - Automatically creates a NetworkPolicy for each new namespace
   - Implements zero-trust networking by default
   - Allows customization through namespace labels

2. **ConfigMap Generation** (`configmap-generator.yaml`)
   - Creates application configuration ConfigMaps
   - Demonstrates data synchronization
   - Shows how to use variables and templates

3. **Secret Generation** (`secret-generator.yaml`)
   - Generates necessary Secrets for applications
   - Implements secure defaults
   - Shows integration with external sources

## Try It Out

1. Apply the network policy generator:
```bash
kubectl apply -f network-policy-generator.yaml
```

2. Create a test namespace:
```bash
kubectl apply -f test-namespace.yaml
```

3. Verify the generated NetworkPolicy:
```bash
kubectl get networkpolicy -n test-namespace
```

Expected output:
```bash
NAME                  POD-SELECTOR   AGE
default-deny-all     <none>         1m
allow-same-namespace <none>         1m
```

## Cleanup

Remove the policies and test resources:
```bash
kubectl delete -f .
``` 