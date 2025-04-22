# Private Repostitory for Robinhood Proof-of-Value (PoV)

## Deliverables

### Validation Policy

A sample validation policy to block `delete` operations with `--grace-period=0` and `--force`:

* [deny-force-delete](Policies/deny-force-delete/README.md)

### Mutation Policy

A sample mutation policy used to configure an ECR registry region:

* [mutate-registry](Policies/mutate-registry/README.md)

### Policy e2e tests with Kyverno Chainsaw

Automated e2e tests with Kyverno Chainsaw to test policy behaviors are available for each policy:

* [deny-force-delete](Policies/deny-force-delete/.chainsaw-test/chainsaw-test.yaml)
* [mutate-registry](Policies/mutate-registry/.chainsaw-test/chainsaw-test.yaml)

These tests are run on each commit with a CI action:

* [CI workflows](.github/workflows/E2Etests.yml)

### Deploying policies with ArgoCD

Automated deployment of policies to ArgoCD managed clusters:

* [argocd](argocd/README.md)

### Upgrade between different versions of Kyverno and OSS & N4K


Test upgrade between diffeent versions of Kyverno and also between various versions of N4K and OSS. Run chainsaw tests after each upgrade:

* [upgrade-tests](upgrade-tests/README.md)

### Load and Scale tests with K6.io

Automated load and scale tests with K6.io:

* [load-tests](load-tests/README.md)