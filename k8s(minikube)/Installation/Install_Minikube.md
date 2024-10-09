># Minikube 설치

[Minikube 공식 문서 참고](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)를 참고 하였습니다.

### 1. 패키지 다운로드 및 설치

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

### 2. Docker Driver 설치

```bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce-cli
sudo chmod 644 ~/다운로드/docker-desktop-amd64.deb
sudo apt install ./docker-desktop-amd64.deb
systemctl --user enable docker-desktop
```

### 3. Kubectl 설치

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
```

### 4. Alias 적용

```bash
nano ~/.bashrc
# alias k='kubectl'
# alias d='docker'
# alias mk='minikube'
source ~/.bashrc
```

### 5. 클러스터 생성

```bash
minikube start --nodes 2 -p jmlim-cluster
minikube status -p jmlim-cluster
kubectl get nodes
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/control-plane-
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/master-
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/worker=worker
```

###  6. GPU 활성화

```bash

# NVIDIA Container Toolkit 설치 확인 및 설치
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# NVIDIA Container CLI 정보 확인
nvidia-container-cli info

# Minikube 클러스터 시작 (2개 노드)
minikube start -p jmlim-cluster --nodes 2 --driver=docker --container-runtime=docker
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/control-plane-
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/master-
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/worker=worker

# Minikube 상태 및 노드 확인
minikube status -p jmlim-cluster
kubectl get nodes

# NVIDIA Device Plugin 설치
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.13.0/nvidia-device-plugin.yml

# 각 노드에 GPU 레이블 추가
kubectl label nodes jmlim-cluster nvidia.com/gpu=present
kubectl label nodes jmlim-cluster-m02 nvidia.com/gpu=present

# GPU 사용 가능 여부 확인
kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.metadata.labels.nvidia\.com/gpu"

# NVIDIA Device Plugin 파드 상태 확인
kubectl get pods -n kube-system -o wide | grep nvidia-device-plugin

# Worker 노드 GPU 테스트를 위한 파드 YAML 생성 및 적용
cat <<EOF > worker-gpu-test.yaml
apiVersion: v1
kind: Pod
metadata:
  name: worker-gpu-test
spec:
  containers:
  - name: cuda-container
    image: nvidia/cuda:11.6.2-base-ubuntu20.04
    command: ["nvidia-smi"]
    resources:
      limits:
        nvidia.com/gpu: 1
  nodeSelector:
    kubernetes.io/hostname: jmlim-cluster-m02
EOF

kubectl apply -f worker-gpu-test.yaml

# 파드 상태 및 로그 확인
kubectl get pods -o wide
kubectl logs worker-gpu-test

# 문제 해결을 위한 추가 명령어
# 각 노드의 GPU 상태 확인
minikube ssh -p jmlim-cluster -- nvidia-smi
minikube ssh -p jmlim-cluster -n jmlim-cluster-m02 -- nvidia-smi

# 노드 로그 확인
minikube logs -p jmlim-cluster
minikube logs -p jmlim-cluster -n jmlim-cluster-m02
```