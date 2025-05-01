# Kyverno Workshop - KCD Austin

Welcome to the Kyverno Workshop! This hands-on workshop will guide you through various Kyverno policy implementations and best practices.

## Prerequisites

- Kubernetes cluster (v1.16 or higher)
- kubectl CLI tool
- Kyverno installed on the cluster ([Installation Guide](https://kyverno.io/docs/installation/))
- cosign (for image verification demo)

## Workshop Structure

This workshop is organized into the following sections:

1. **Mutation Policies**
   - Learn how to modify Kubernetes resources on-the-fly
   - Implement automatic label injection
   - Add default resource limits

2. **Generation Policies**
   - Automatically create companion resources
   - Network policies generation
   - ConfigMap/Secret generation

3. **Image Verification**
   - Implement container image verification using cosign
   - Enforce signed container images
   - Verify image attestations

4. **Resource Optimization**
   - Set and enforce resource quotas
   - Implement resource limits
   - Best practices for resource management

## Getting Started

Each section contains:
- README with detailed instructions
- Sample policies
- Example resources to test the policies
- Expected outcomes

Navigate to each directory to get started with the specific topic:

```bash
# Start with mutation policies
cd 01-mutation-policies

# Move to generation policies
cd 02-generation-policies

# Explore image verification
cd 03-image-verification

# Learn about resource optimization
cd 04-resource-optimization
```

## Additional Resources

- [Kyverno Documentation](https://kyverno.io/docs/)
- [Kyverno GitHub Repository](https://github.com/kyverno/kyverno)
- [Policy Examples](https://kyverno.io/policies/) 