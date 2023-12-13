"""
Shows how to load a Kubernetes config from within a cluster. This script
must be run within a pod. You can start a pod with a Python image (for
example, `python:latest`), exec into the pod, install the library, then run
this example.

If you get 403 errors from the API server you will have to configure RBAC to
add permission to list pods by applying the following manifest:

---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pods-list
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]

---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pods-list
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
roleRef:
  kind: ClusterRole
  name: pods-list
  apiGroup: rbac.authorization.k8s.io

Documentation: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
"""

from kubernetes import client, config

def main():
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")
        # print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")


if __name__ == '__main__':
    main()