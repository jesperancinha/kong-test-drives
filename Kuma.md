# Installing Kuma

```shell
curl -L https://docs.konghq.com/mesh/installer.sh | VERSION=2.6.0 sh -
cd kong-mesh-2.6.0/bin
export PATH=$(pwd):$PATH
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## Resources

-  [Install kumactl](https://docs.konghq.com/mesh/latest/production/install-kumactl/)
-  [Install and Set Up kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
