# Kuma - Kong Test Drives - jesperancinha

## How to install Kumactl

-  [Official Kumactl Installation Manual](https://kuma.io/docs/2.6.x/production/install-kumactl/)

```shell
curl -L https://kuma.io/installer.sh | VERSION=2.6.1 sh -
```

```shell
cd ~/kuma-2.6.1/bin; \
export PATH=$(pwd):$PATH; \
cd ~
```

## How to install Kubectl

- [Official Kubectl Installation Manual](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

```shell
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

##### Remove all

```shell
kubectl delete pods --all -A
```

## Install Kind

https://kuma.io/docs/2.6.x/quickstart/kubernetes-demo/

```shell
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-amd64
[ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-arm64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

## Install Cluster

https://kuma.io/docs/2.6.x/quickstart/kubernetes-demo/

```shell
kind create cluster --name=mesh-zone
```

## Loading script

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
