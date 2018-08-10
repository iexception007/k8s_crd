# custom resource define(crd) project
This project is the crd lib. 
function:
1. create
2. delete
3. update
# create the crd on the k8s cluster.
``` bash
kubectl create -f kuryrnet.yaml
kubectl create -f cluster2.yaml
```
1. kuryrnet.yaml
``` yaml
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: kuryrnets.openstack.org
spec:
  group: openstack.org
  version: v1
  scope: Cluster
  names:
    plural: kuryrnets
    singular: kuryrnet
    kind: KuryrNet
    shortNames:
    - kn
---
apiVersion: "openstack.org/v1"
kind: KuryrNet
metadata:
  name: cluster1
spec:
  ovs_bridge: br-int
  pod_security_groups: id_of_secuirity_group_for_pods
  pod_subnet: id_of_subnet_for_pods
  project: id_of_project
  service_subnet: id_of_subnet_for_k8s_services
```
2. cluster2.yaml
```yaml
apiVersion: "openstack.org/v1"
kind: KuryrNet
metadata:
  name: cluster2
spec:
  ovs_bridge: br-int
  pod_security_groups: 111111
  pod_subnet: 222222
  project: 333333
  service_subnet: 444444
```
# search th crd
``` bash
kubectl get crd
kubectl get kuryrnets
kubectl edit kuryrnets cluster2
```
# search api_token
``` bash
kubectl -n kube-system get secret {replicaset-controller-token-*}
kubectl -n kube-system describe secret {replicaset-controller-token-*} | grep -E '^token' | cut -f2 -d':' | tr -d ' '

kubectl -n kube-system edit clusterrole replicaset-controller
- apiGroups:
  - ""
  resources:
  - customresourcedefinition
  verbs:
  - '*'
- apiGroups:
  - openstack.org
  resources:
  - kuryrnets
  verbs:
  - '*'
```
# testing the connect.
```
APISERVER=$(kubectl config view | grep server | cut -f 2- -d ":" | tr -d " ")
TOKEN=$(kubectl describe secret $(kubectl get secrets | grep {replicaset-controller-token-*} | cut -f1 -d ' ') | grep -E '^token' | cut -f2 -d':' | tr -d '\t')
curl $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure

curl https://192.168.1.191:6443/api/v1/namespaces/default/pods --header "Authorization: Bearer $TOKEN" --insecure
curl https://192.168.1.191:6443/apis/openstack.org/v1/namespaces/*/kuryrnetes/cluster1 --header "Authorization: Bearer $TOKEN" --insecure
curl https://192.168.1.191:6443/apis/openstack.org/v1/kuryrnetes/cluster1 --header "Authorization: Bearer $TOKEN" --insecure

```
# k8s python lib base operate
```python
from kubernetes import client, config

config.load_kube_config()

#print config.configuration.api_key['authorization']
v1 = client.CoreV1Api()
print("List pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
```
# create crd and search crd and delete crd.
1. create_cluster_custom_object(group, version, plural, body)  
2. patch_cluster_custom_object(group, version, plural, name, body)  
3. delete_cluster_custom_object(group, version, plural, name, body  