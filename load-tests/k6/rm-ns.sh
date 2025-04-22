(
NAMESPACE=$1

pid=$(ps -ef |grep "kubectl proxy" | grep -v color | awk '{ print $2}')
kill -9 $pid

kubectl proxy &
kubectl get namespace $NAMESPACE -o json |jq '.spec = {"finalizers":[]}' >temp.json
curl -k -H "Content-Type: application/json" -X PUT --data-binary @temp.json 127.0.0.1:8001/api/v1/namespaces/$NAMESPACE/finalize
)

