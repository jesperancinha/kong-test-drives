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

## How to install microk8s

This has been Linux tested


#### Installation

```shell
sudo snap install microk8s --classic
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

#### Configuration

```shell
sudo usermod -a -G microk8s jesperancinha
newgrp microk8s
sudo chown -R jesperancinha ~/.kube
```

#### Creating a node

- [Install Kubernetes in Ubuntu](https://ubuntu.com/kubernetes/install)
- [Install a local Kubernetes with MicroK8s](https://ubuntu.com/tutorials/install-a-local-kubernetes-with-microk8s#1-overview)

```shell
microk8s add-node
microk8s join <NODEID>
microk8s kubectl get no
microk8s stop
microk8s reset
microk8s enable dns 
microk8s enable dashboard
microk8s enable storage
microk8s kubectl get all --all-namespaces
token=$(microk8s kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
microk8s kubectl -n kube-system describe secret $token
```

## Install control plane SSH and certificates

#### Create certificate and key

```shell
openssl genrsa -out ca.key 2048
openssl req -new -key ca.key -x509 -days 365 -out ca.crt
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -subj "/CN=kubectl"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365
cat client.crt client.key > client.pem
```

```shell
openssl req -newkey rsa:2048 -nodes -keyout tls.key -out tls.csr
openssl x509 -req -sha256 -days 365 -in tls.csr -signkey tls.key -out tls.crt
kubectl create secret tls my-certificate --cert=tls.crt --key=tls.key
```

```yaml
users:
- name: kubectl
  user:
    client-certificate: /path/to/client.crt
    client-key: /path/to/client.key
```

#### Create a configuration

```shell
kubectl config set-cluster my-cluster --server=https://your-cluster-api-server-address --certificate-authority=ca.crt
kubectl config set-credentials my-user --client-certificate=/path/to/client.crt --client-key=client.key
kubectl config set-context my-context --cluster=my-cluster --user=my-user
kubectl config use-context my-context
```

```shell
kubectl config set-cluster my-cluster --server=https://your-cluster-api-server-address
kubectl config set-credentials my-user
kubectl config set-context my-context --cluster=my-cluster --user=my-user
kubectl config use-context my-context
```
#### Create the control-plane

```shell
kumactl install control-plane \
  --set "controlPlane.mode=zone" \
  | kubectl apply -f -
```

#### Your startup file .bashrc/.zsh

```shell
export KUBECONFIG=~/.kube/config
```

## Loading script

```shell
microk8s reset
microk8s stop
microk8s start
microk8s enable dns 
microk8s enable dashboard
microk8s enable storage
kind create cluster --name=mesh-zone
kumactl install control-plane \
  --set "controlPlane.mode=zone" \
  | kubectl apply -f -
kubectl apply -f https://raw.githubusercontent.com/kumahq/kuma-counter-demo/master/demo.yaml
kubectl wait -n kuma-demo --for=condition=ready pod --selector=app=demo-app --timeout=90s
microk8s.kubectl get nodes
kubectl get namespace
kubectl get pods --namespace=kuma-demo
kubectl get pods -o wide

kubectl port-forward svc/demo-app -n kuma-demo 5000:5000
kubectl port-forward svc/kuma-control-plane -n kuma-system 5681:5681

kind delete cluster --name=mesh-zone
```
