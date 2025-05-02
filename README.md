# Kyverno Workshop: Kubernetes Policy Management

## Workshop Overview
This workshop provides hands-on experience with Kyverno, a Kubernetes-native policy engine. Through practical exercises, you'll learn how to implement and manage various types of policies in your Kubernetes clusters.

## Prerequisites
- A running Kubernetes cluster (minikube, kind, or any other distribution)
- `kubectl` configured to access your cluster
- Helm installed
- Basic understanding of Kubernetes concepts

## Workshop Duration
- Total Duration: 4 hours
- Breaks: 15 minutes after each hour

## Workshop Agenda

### Session 1: Introduction to Kyverno (45 minutes)
1. What is Kyverno?
   - Policy engine overview
   - Key features and benefits
   - Use cases

2. Installation and Setup
   ```bash
   # Add Kyverno Helm repository
   helm repo add kyverno https://kyverno.github.io/kyverno/
   helm repo update

   # Install Kyverno
   helm install kyverno kyverno/kyverno -n kyverno --create-namespace

   # Verify installation
   kubectl get pods -n kyverno
   ```

3. Basic Concepts
   - Policy types
   - Policy enforcement modes
   - Policy reports

### Session 2: Basic Policy Implementation (60 minutes)

#### Exercise 1: Label Validation Policy
1. Create a policy to enforce team labels on pods:
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: require-labels
   spec:
     validationFailureAction: enforce
     rules:
     - name: check-team
       match:
         any:
         - resources:
             kinds:
             - Pod
       validate:
         message: "Team label is required"
         pattern:
           metadata:
             labels:
               team: "?*"
   ```

2. Test the policy:
   ```bash
   # Create a pod without team label (should fail)
   kubectl run nginx --image=nginx

   # Create a pod with team label (should succeed)
   kubectl run nginx-labelled --image=nginx --labels=team=dev
   ```

3. Check policy reports:
   ```bash
   kubectl get policyreport
   ```

#### Exercise 2: Resource Validation
1. Create a policy to enforce resource limits:
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: require-resource-limits
   spec:
     validationFailureAction: enforce
     rules:
     - name: check-resource-limits
       match:
         any:
         - resources:
             kinds:
             - Pod
       validate:
         message: "CPU and memory limits are required"
         pattern:
           spec:
             containers:
             - resources:
                 limits:
                   cpu: "?*"
                   memory: "?*"
   ```

2. Test the policy with different resource configurations

### Session 3: Advanced Policy Features (60 minutes)

#### Exercise 3: Image Verification
1. Create a policy to verify image signatures:
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: verify-images
   spec:
     rules:
     - name: verify-signature
       match:
         any:
         - resources:
             kinds:
             - Pod
       verifyImages:
       - imageReferences:
         - "ghcr.io/kyverno/test-verify-image:signed-cert"
         failureAction: Enforce
         attestors:
         - entries:
           - certificates:
               cert: |-
                 -----BEGIN CERTIFICATE-----
                 # Your certificate here
                 -----END CERTIFICATE-----
   ```

2. Test with signed and unsigned images

#### Exercise 4: Network Policy Generation
1. Create a policy to generate network policies:
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: generate-network-policy
   spec:
     rules:
     - name: generate-default-deny
       match:
         resources:
           kinds:
           - Namespace
       generate:
         kind: NetworkPolicy
         name: default-deny
         namespace: "{{request.object.metadata.name}}"
         data:
           spec:
             podSelector: {}
             policyTypes:
             - Ingress
             - Egress
   ```

2. Test the generated network policies

### Session 4: Integration and Best Practices (45 minutes)

#### Exercise 5: ArgoCD Integration
1. Configure ServerSideDiff
2. Set up resource tracking
3. Handle ownership conflicts

#### Exercise 6: Troubleshooting
1. Common issues and solutions
2. Performance optimization
3. Resource management

## Hands-on Lab (30 minutes)
Create a comprehensive policy set that:
1. Enforces pod security standards
2. Validates resource requests/limits
3. Generates network policies
4. Verifies image signatures

## Assessment Criteria
Participants will be evaluated based on:
1. Successful implementation of policies
2. Understanding of policy types
3. Troubleshooting skills
4. Integration capabilities

## Resources
- [Kyverno Documentation](https://kyverno.io/docs/)
- [Policy Examples](https://kyverno.io/policies/)
- [Community Support](https://kyverno.io/community/)

## Troubleshooting Guide

### Common Issues and Solutions

1. **CRD Check Failures**
   ```bash
   # Verify RBAC permissions
   kubectl auth can-i create clusterpolicy --as system:serviceaccount:kyverno:kyverno
   
   # Check CRD installation
   kubectl get crd clusterpolicies.kyverno.io
   ```

2. **Sync Failures**
   ```bash
   # Enable ServerSideDiff
   kubectl patch deployment kyverno -n kyverno --type=json -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--enableServerSideDiff"}]'
   ```

3. **Resource Management Issues**
   ```bash
   # Check resource status
   kubectl get policyreport
   kubectl get clusterpolicy
   ```

4. **Performance Issues**
   ```bash
   # Monitor Kyverno metrics
   kubectl port-forward -n kyverno svc/kyverno-svc-metrics 9090:9090
   ```

## Next Steps
1. Explore advanced policy features
2. Implement custom policies for your use case
3. Join the Kyverno community
4. Contribute to the project

## Feedback
Please provide feedback on:
1. Workshop content
2. Exercise difficulty
3. Time allocation
4. Additional topics to cover 
