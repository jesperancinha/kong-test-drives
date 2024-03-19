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
