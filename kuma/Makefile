install-all: install-kuma install-kubectl install-microk8s
	curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
install-microk8s:
		sudo snap install microk8s --classic
install-kubectl:
	curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" ;\
	sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
install-kuma:
	cd ~; \
	curl -L https://kuma.io/installer.sh | VERSION=2.6.1 sh -
install-planes:
	kumactl install control-plane \
      --set "controlPlane.mode=zone" \
      | kubectl apply -f -
