# Kyverno Generate Policies Workshop

This workshop covers different types of generate policies in Kyverno. Generate policies are used to create new Kubernetes resources based on certain triggers.

## Workshop Structure

1. **Basic Generate Policies**
   - ConfigMap Generation
   - Secret Generation
   - NetworkPolicy Generation

2. **Advanced Generate Policies**
   - Namespace Provisioning
   - Resource Synchronization
   - Cross-Namespace Resource Generation

## Prerequisites

- Kubernetes cluster with Kyverno installed
- kubectl configured to access the cluster
- Basic understanding of Kubernetes resources

## Workshop Exercises

### 1. Basic Generate Policies

#### 1.1 ConfigMap Generation
- Policy: `configmap-generator.yaml`
- Test: `tests/configmap-generator-test.yaml`
- Description: Generates a ConfigMap when a deployment with specific labels is created

#### 1.2 Secret Generation
- Policy: `secret-generator.yaml`
- Test: `tests/secret-generator-test.yaml`
- Description: Generates a Secret when a namespace with specific labels is created

#### 1.3 NetworkPolicy Generation
- Policy: `network-policy-generator.yaml`
- Test: `tests/network-policy-generator-test.yaml`
- Description: Generates a NetworkPolicy for all new namespaces

### 2. Advanced Generate Policies

#### 2.1 Namespace Provisioning
- Policy: `namespace-provisioner.yaml`
- Test: `tests/namespace-provisioner-test.yaml`
- Description: Creates a complete set of resources when a new namespace is created

#### 2.2 Resource Synchronization
- Policy: `resource-sync.yaml`
- Test: `tests/resource-sync-test.yaml`
- Description: Synchronizes resources across namespaces

## Testing

Each policy includes:
- Kyverno test files
- Chainsaw test files
- Sample resources to trigger the policies

## Running Tests

1. Kyverno Tests:
```bash
kyverno test .
```

2. Chainsaw Tests:
```bash
chainsaw test --test-dir tests/
```

## Additional Resources

- [Kyverno Documentation](https://kyverno.io/docs/)
- [Generate Rules Documentation](https://kyverno.io/docs/writing-policies/generate/) 