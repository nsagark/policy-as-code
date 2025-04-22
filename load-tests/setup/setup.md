# Setup

This folder contains some Kubernetes resources and a script to start load tests against the Kubernetes API.

## Load test environment

The scale testing was performed using an EC2 ubuntu machine of instance type c6a.48xlarge. 
- CPU: 192 Cores
- Memory: 384 GB
- Disk type: SSD
- Volume size: 100 GiB

k3d was used to run multi node cluster with 3 control-plane and 5 worker nodes.

## Load testing with k6.io

We're using [k6](https://k6.io/) for load testing. It's written in Go, but the tests are written in JavaScript. You can check existing tests or read the [documentation](https://k6.io/docs/). Existing tests are in the `tests/` subfolder.

To start the tests, you can use the `start-rbh.sh` script and provide three parameters:

1. the script you want to execute (e.g., tests/my-test.js)
2. the number of concurrent "users" (in k6, they're called virtual users or vus)
3. the number of overall iterations (they will be distributed across the number of vus)

This will spin up a new namespace (`load-test`) in the target cluster with a service account that has cluster-admin role permissions and spawn K6 with the script you provided. The test file is mounted to the pod from a ConfigMap. Afterward, it will grab the logs from the pod and clean everything up. The logs will be stored in your current folder. 

There is already a util.js file you can use with some custom helper functions (like get the current namespace, build the Kubernetes API base URL etc.) 

K6 thresholds can be used to check if the results of the scale testing meet your requirements and this can be used in the CI tests to pass or fail the build. See [here](https://k6.io/docs/using-k6/thresholds/) for more details. 

## Usage

The instructions below provide guidelines on how the scale testing can be done. 

### Download k3d:
```sh
wget -q -O - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

More details for k3d installation can be found [here](https://k3d.io/v5.4.9/#install-script).

### Create a base cluster using K3d


Create a cluster by setting up embedded etcd for the K3s cluster.


Use the following command if you want to configure the etcd storage limit, this command sets the storage limit to 8GB:
```sh
k3d cluster create scaling --servers 3 --agents=15 --k3s-arg "--disable=metrics-server@server:*" --k3s-node-label "ingress-ready=true@agent:*" --k3s-arg "--etcd-arg=quota-backend-bytes=8589934592@server:*"
```

Note, you can execute into the server node to check the storage setting:
```
docker exec -ti k3d-scaling-server-0 sh
cat /var/lib/rancher/k3s/server/db/etcd/config | tail -2
quota-backend-bytes: 8589934592
```
NOTE: Make sure to disable any firewall on the machine or else the cluster creation can fail. If the sever pods don't come up and you see `too many open files` error in the server logs, please run below command to increase the limit. 

```
sudo prlimit --pid $$ --nofile=1048576:1048576
sudo sysctl fs.inotify.max_user_instances=1280
sudo sysctl fs.inotify.max_user_watches=655360
```

### Install N4K 1.10

```sh
helm repo add nirmata https://nirmata.github.io/kyverno-charts/
helm repo update nirmata

helm install kyverno nirmata/kyverno -f minimal-values.yaml --version=v3.0.29 --namespace kyverno --create-namespace
```

Once the helm chart is deployed, add the patch below to increase the `clientRateLimitBurst` and `clientRateLimitQPS` in the `kyverno-admission-controller` deployment. 

```sh
kubectl patch deployment kyverno-admission-controller -n kyverno --type='json' -p='[{
    "op": "replace", 
    "path": "/spec/template/spec/containers/1/args", 
    "value": [
        "--backgroundServiceAccountName=system:serviceaccount:kyverno:kyverno-background-controller",
        "--servicePort=443",
        "--disableMetrics=false",
        "--otelConfig=prometheus",
        "--metricsPort=8000",
        "--admissionReports=false",
        "--autoUpdateWebhooks=true",
        "--enableConfigMapCaching=true",
        "--enableDeferredLoading=true",
        "--dumpPayload=false",
        "--forceFailurePolicyIgnore=false",
        "--loggingFormat=text",
        "--v=2",
        "--omit-events=PolicyApplied,PolicySkipped,PolicyViolation,PolicyError",
        "--enablePolicyException=false",
        "--protectManagedResources=false",
        "--allowInsecureRegistry=false",
        "--registryCredentialHelpers=default,google,amazon,azure,github",
        "--clientRateLimitBurst=10000",
        "--clientRateLimitQPS=10000"
    ]
}]'

```
### Policy rules used in K6 scale test

The scale test was performed using a `require-labels` policy which checks for `app.kubernetes.io/name` label in the pods. Here is how the rules were generated for testing. 

```sh
for i in $(seq 1 100); do sed "s/xxx/$i/g" policy-template.yaml > require-labels-${i}.yaml;done
```
The `policy-template.yaml` can be found [here](policy-template.yaml)
### Running the K6 scale test

Clone this repo and go to the k6 folder

#### Baseline Test without any policies with 500VUs and 5000 ITERATIONS

```sh
cd robinhood/load-tests/k6
./start-rbh.sh tests/kyverno-pods-rbh-dryrun-baseline.js 500 5000
```

Capture the avg `http_req_duration` and `iterations per second` from the log file. This will give you the baseline metrics without any Kyverno policies

#### Run scale tests with different no of rules

From the repo, go to `extra-policies` folder and deploy the policies. Start with 10 policies/10 rules.

```sh
cd robinhood/load-tests/k6/extra-policies

for i in $(seq 1 10); do kubectl create -f require-labels-${i}.yaml; done
```
Make sure the policies are all in `Ready` state and they are in `Enforce` mode. Next, run the K6 test.

```sh
cd robinhood/load-tests/k6
./start-rbh.sh tests/kyverno-pods-rbh-dryrun.js 500 5000
```

Capture the avg `http_req_duration` and `iterations per second` for different `VUs` and `ITERATIONS`


Repeat the same steps for `20`, `50`, `100` Policies/Rules
