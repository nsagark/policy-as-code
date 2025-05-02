# Network Policy Generation Policy

This policy automatically generates a default-deny NetworkPolicy for all new namespaces, implementing a zero-trust networking model by default.

## Policy Overview

The policy `add-network-policy.yaml` creates a default-deny NetworkPolicy whenever a new namespace is created. This ensures that all new namespaces start with a secure networking configuration.

## How It Works

1. The policy watches for new namespace creation events
2. When a new namespace is created, it automatically generates a NetworkPolicy named `default-deny`
3. The generated NetworkPolicy blocks all ingress and egress traffic by default

## Usage

1. Apply the policy:
```bash
kubectl apply -f add-network-policy.yaml
```

2. Create a new namespace:
```bash
kubectl create ns test-namespace
```

3. Verify the NetworkPolicy was created:
```bash
kubectl get netpol -n test-namespace
```

Expected output:
```
NAME           POD-SELECTOR   AGE
default-deny   <none>         8s
```

## Policy Details

The policy:
- Applies to all new namespaces
- Creates a NetworkPolicy named `default-deny`
- Implements a zero-trust model by default
- Can be customized through namespace labels

## Security Benefits

- Enforces network isolation by default
- Prevents accidental exposure of services
- Implements the principle of least privilege
- Provides a secure baseline for new namespaces

## Cleanup

To remove the policy:
```bash
kubectl delete -f add-network-policy.yaml
```

Note: This will not remove existing NetworkPolicies from namespaces. 