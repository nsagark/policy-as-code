# Resource Optimization Policies

This section demonstrates how to use Kyverno to optimize and manage resource utilization in your Kubernetes cluster.

## What You'll Learn

- How to enforce resource quotas and limits
- How to implement pod disruption budgets
- How to optimize resource allocation
- Best practices for resource management

## Policies Included

1. **Resource Quota Policy** (`resource-quota.yaml`)
   - Enforces namespace resource quotas
   - Sets limits for CPU, memory, and pod count
   - Implements tiered quota system (dev/staging/prod)

2. **Resource Limits Policy** (`resource-limits.yaml`)
   - Enforces container resource limits
   - Prevents resource exhaustion
   - Implements best practices for resource requests/limits ratio

3. **Pod Disruption Budget** (`pod-disruption-budget.yaml`)
   - Automatically creates PDBs for deployments
   - Ensures high availability during cluster operations
   - Customizes disruption settings based on environment

## Try It Out

1. Apply the resource quota policy:
```bash
kubectl apply -f resource-quota.yaml
```

2. Create a test namespace with quota:
```bash
kubectl apply -f test-namespace.yaml
```

3. Deploy a workload that complies with quotas:
```bash
kubectl apply -f test-compliant-deployment.yaml
```

4. Try deploying a workload that exceeds quotas (should be blocked):
```bash
kubectl apply -f test-exceeding-deployment.yaml
```

Expected output for exceeding deployment:
```
Error: ... admission webhook "validate.kyverno.svc" denied the request:
policy Resource Quota/check-resource-quota: validation error: resource quota exceeded ...
```

## Best Practices

1. Resource Quotas:
   - Set appropriate quotas based on environment
   - Consider both resource requests and limits
   - Monitor quota utilization

2. Resource Limits:
   - Set realistic CPU and memory limits
   - Use resource requests for proper scheduling
   - Implement proper monitoring and alerting

3. Pod Disruption Budgets:
   - Consider application availability requirements
   - Set appropriate minAvailable/maxUnavailable
   - Test cluster maintenance scenarios

## Cleanup

Remove the policies and test resources:
```bash
kubectl delete -f .
``` 