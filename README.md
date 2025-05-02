# Nirmata Kyverno Operator and N4K Upgrade Guide

This guide provides step-by-step instructions for upgrading Nirmata Kyverno Operator and N4K (Nirmata Enterprise for Kyverno) from v1.11.4-n4k.nirmata.9 to latest version of 1.13 via Argo CD

## Prerequisites

- Access to the Kubernetes cluster
- Argo CD access
- Argo CD CLI 
- Backup of existing resources

## Upgrade Steps

### 1. Backup Existing Resources

Before proceeding with the upgrade, ensure you have backups of:
- ClusterPolicies
- PolicyReports
- ClusterCleanupPolicies
- PolicyExceptions
- Kyverno CRDs
- Nirmata Kyverno Operator CRDs
- PolicyReports (Optional)


```bash
kubectl get cpol,cleanpol,ccleanpol,polex -o yaml > allPolBkp.yaml
kubectl get polr -A -o yaml > bkpPolr.yaml
```

### 2. Delete Existing Installation

Remove the current versions of below in Argo CD
- Nirmata Kyverno Operator
- N4K

### 3. Cleanup

Run the cleanup script to from [here](https://github.com/nirmata/nirmata-scripts/tree/main/kyverno_nirmata_cleaunp_new) to ensure all related resources from previous versions are removed:
```bash
# Run cleanup script
chmod + x kyverno_cleanup_latest_nk4_1_10.sh
./kyverno_cleanup_latest_nk4_1_10.sh /home/user/.kube/config  nirmata-system nirmata-kyverno-operator kyverno
```

### 4. Deploying Operator and N4K 1.13.x

#### Nirmata Kyverno Operator

Download this repository and apply the Argo CD application for operator.
```bash

# Login to Argo CD
argocd login <argourl>:<argoport>  --username <user> --password <password> --insecure  # e.g. argocd login 127.0.0.1:8080 --username admin --password password123 --insecure

# Deploy the operation application
kubectl apply -f application-operator.yaml


```

#### N4K
```bash
# Download N4K helm chart
wget https://github.com/nirmata/kyverno-charts/releases/download/kyverno-3.3.14/kyverno-3.3.14.tgz

# Extract and modify values.yaml as needed
tar -xzf kyverno-3.3.14.tgz
```

### 5. Argo CD Deployment

1. Update your Git repository with the new values.yaml files
2. Sync the following applications in Argo CD:
   - Nirmata Kyverno Operator
   - N4K

### 6. Verify Installation

After the sync is complete, verify that:
- Nirmata Kyverno Operator is running in the `nirmata-system` namespace
- N4K is running in the `kyverno` namespace
- All pods are in Running state
- No errors in the logs

### 7. Deploy Policies

Deploy your policies from Git:
```bash
# Apply your policies
kubectl apply -f <path-to-your-policies>
```

## Troubleshooting

If you encounter any issues during the upgrade:
1. Check pod logs for errors
2. Verify all CRDs are properly installed
3. Ensure all required namespaces exist
4. Check Argo CD sync status

## Rollback Procedure

If the upgrade fails:
1. Restore from your backups
2. Reapply the previous version configurations
3. Sync the applications in Argo CD

## Support

For additional support, please contact Nirmata support or refer to the official documentation. 

