## Installation microk8s

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
microk8s reset
microk8s enable dns 
microk8s enable dashboard
microk8s enable storage
microk8s kubectl get all --all-namespaces
token=$(microk8s kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
microk8s kubectl -n kube-system describe secret $token
microk8s.kubectl get nodes
```
