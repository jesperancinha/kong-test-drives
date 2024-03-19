# Kuma - Kong Test Drives - jesperancinha

## Introduction

To run the examples in this folder you can install these 3 commands (see the [Installation](./Installation.md) file) :

1. kubectl - [Documentation](https://kubernetes.io/docs/tasks/tools/#kubectl)
2. kumactl - [Documentation](https://docs.konghq.com/mesh/latest/production/install-kumactl/)
3. kind - [Documentation](https://kind.sigs.k8s.io/docs/user/quick-start/)

kubectl and kumactl are essential. kind only allows you to quickly setup [K8S](https://kubernetes.io/) in your machine. It is not a requirement. An alternative could be MicroK8S(see the [MicroK8S](./MicroK8S.md) installation notes) or Minikube.

## Loading script

https://kuma.io/docs/2.6.x/quickstart/kubernetes-demo/

```shell
kind create cluster --name=mesh-zone
kumactl install control-plane \
  --set "controlPlane.mode=zone" \
  | kubectl apply -f -
kubectl apply -f https://raw.githubusercontent.com/kumahq/kuma-counter-demo/master/demo.yaml
kubectl wait -n kuma-demo --for=condition=ready pod --selector=app=demo-app --timeout=90s
kubectl get namespace
kubectl get pods --namespace=kuma-demo
kubectl get pods -o wide

kubectl port-forward svc/demo-app -n kuma-demo 5000:5000
kubectl port-forward svc/demo-app -n kuma-demo 6379:6379
kubectl port-forward svc/kuma-control-plane -n kuma-system 5681:5681
```

## Teardown

```shell
kind delete cluster --name=mesh-zone
kubectl delete pods --all -A
```

## How to log

```shell
kubectl exec -it <podname> -c kuma-sidecar -n <namespace> -- sh
wget http://localhost:9901/logging?level=debug --post-data='' -O /tmp/res
kubectl logs -f <podname> -c kuma-sidecar -n <namespace>
kubectl logs -f <podname> -n <namespace>
```

## Resources

-   https://support.konghq.com/support/s/article/How-to-enable-debug-logging-for-kuma-sidecar-without-using-port-forward
-   https://spacelift.io/blog/kubectl-logs
