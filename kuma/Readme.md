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
```

## How to install microk8s

This has been Linux tested


#### Installation

```shell
sudo snap install microk8s --classic
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
microk8s enable dns 
microk8s enable dashboard
microk8s enable storage
microk8s kubectl get all --all-namespaces
token=$(microk8s kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
microk8s kubectl -n kube-system describe secret $token
```

## Install control plane SSH and certificates


#### Create a configuration

```shell
kubectl config set-cluster my-cluster --server=https://your-cluster-api-server-address --certificate-authority=/path/to/ca.crt
kubectl config set-credentials my-user --client-certificate=/path/to/client.crt --client-key=/path/to/client.key
kubectl config set-context my-context --cluster=my-cluster --user=my-user
kubectl config use-context my-context
```

#### Create the control-plane

```shell
kubectl config set-cluster my-cluster --server=http://<IP> --kubeconfig $HOME/.kube/config
kumactl install control-plane \
  --set "controlPlane.mode=zone" \
  | kubectl apply -f -
```

#### Your startup file .bashrc/.zsh

```shell
export KUBECONFIG=~/.kube/config
```
