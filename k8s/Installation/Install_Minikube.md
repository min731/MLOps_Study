># Minikube 설치

[Minikube 공식 문서 참고](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)를 참고 하였습니다.

### 1. 패키지 다운로드 및 설치

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

### 2. Docker Driver 설치

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
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
alias k='kubectl'
alias d='docker'
alias mk='minikube'
source ~/.bashrc
```
###  5. GPU 활성화

```bash

# NVIDIA Container Toolkit 설치 확인 및 설치
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2

# NVIDIA Container CLI 정보 확인
nvidia-container-cli info

#Docker 데몬 설정 수정
sudo nano /etc/docker/daemon.json
```

```json
{
  "default-runtime": "nvidia",
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

```bash
# Docker 서비스 재시작
sudo systemctl restart docker

# NVIDIA 런타임 테스트
sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### 6. 클러스터 생성

```bash
# Minikube 클러스터 시작 (2개 노드)
minikube delete
minikube start -p jmlim-cluster --nodes 2 --driver=docker --gpus all --addons=ingress --addons=nvidia-gpu-device-plugin
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/control-plane-
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/master-
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/worker=worker

# Minikube 상태 및 노드 확인
minikube status -p jmlim-cluster
kubectl get nodes

# NVIDIA Device Plugin 설치
# kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.13.0/nvidia-device-plugin.yml

# 각 노드에 GPU 레이블 추가
# kubectl label nodes jmlim-cluster nvidia.com/gpu=present
# kubectl label nodes jmlim-cluster-m02 nvidia.com/gpu=present

# GPU 사용 가능 여부 확인
# kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.metadata.labels.nvidia\.com/gpu"

# NVIDIA Device Plugin 파드 상태 확인
# kubectl get pods -n kube-system -o wide | grep nvidia-device-plugin

# Worker 노드 GPU 테스트를 위한 파드 YAML 생성 및 적용
cat <<EOF > .yaml
apiVersion: v1
kind: Pod
metadata:
  name: nvidia-gpu-test
spec:
  containers:
  - name: nvidia-gpu-test
    image: nvidia/cuda:12.6.0-base-ubuntu22.04
    command: ["nvidia-smi"]
  restartPolicy: Never
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

### 7. 애드온 활성화

```bash
minikube addons enable dashboard
minikube addons enable ingress
minikube addons enable ingress-dns
minikube addons enable istio
# minikube addons enable istio-provisioner
minikube addons enable kubeflow
minikube addons enable metalb
minikube addons enable metrics-server
minikube addons enable nvidia-gpu-device-plugin
minikube addons enable registry
minikube addons enable storage-provisioner
```