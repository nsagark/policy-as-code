# Image Verification Policies

This section demonstrates how to use Kyverno to verify container images using cosign signatures and attestations. Using the Cosign project, OCI images may be signed to ensure supply chain security is maintained

## Prerequisites

- cosign CLI tool installed
- A container registry that supports OCI artifacts
- Sample signed images (provided in examples)

## What You'll Learn

- How to verify container image signatures
- How to check image attestations
- How to enforce registry requirements
- How to implement supply chain security

## Policies Included

1. **Signature Verification** (`signature-verification.yaml`)
   - Verifies container image signatures using cosign
   - Enforces signature requirements for specific registries
   - Shows how to handle multiple signing authorities

2. **Attestation Verification** (`attestation-verification.yaml`)
   - Verifies image attestations (SBOM, vulnerability scans)
   - Demonstrates predicate matching
   - Shows integration with vulnerability scanners

3. **Registry Requirements** (`registry-verification.yaml`)
   - Enforces allowed registries
   - Implements registry mirror configurations
   - Shows how to handle private registries

## Try It Out

1. Generate a test key pair (for demo purposes):
```bash
cosign generate-key-pair
```

2. Apply the signature verification policy:
```bash
kubectl apply -f signature-verification.yaml
```

3. Try deploying a signed image:
```bash
kubectl apply -f test-signed-deployment.yaml
```

4. Try deploying an unsigned image (should be blocked):
```bash
kubectl apply -f test-unsigned-deployment.yaml
```

Expected output for unsigned image:
```
Error: ... admission webhook "validate.kyverno.svc" denied the request:
policy Signature Verification/verify-image-signature: validation error: ...
```

## Cleanup

Remove the policies and test resources:
```bash
kubectl delete -f .
```

## Notes

- For production use, consider using KMS or cloud provider key management services
- Implement proper key rotation and management procedures
- Consider using policy exceptions for development/testing environments 
