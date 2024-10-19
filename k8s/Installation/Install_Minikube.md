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

### 7. 애드온 활성화 (*클러스터 지정)

```bash
minikube addons enable dashboard -p jmlim-cluster
minikube addons enable ingress -p jmlim-cluster
minikube addons enable ingress-dns -p jmlim-cluster
# minikube addons enable istio -p jmlim-cluster # 최소 4CPU, 메모리 8GB 필요
# ❗  istio is a 3rd party addon and is not maintained or verified by minikube maintainers, enable at your own risk.
# ❗  istio does not currently have an associated maintainer.
# ❗  Istio needs 8192MB of memory -- your configuration only allocates 2200MB
# ❗  Istio needs 4 CPUs -- your configuration only allocates 2 CPUs
# minikube addons enable istio-provisioner
minikube addons enable kubeflow -p jmlim-cluster
minikube addons enable metallb -p jmlim-cluster
minikube addons enable metrics-server -p jmlim-cluster
# minikube addons enable nvidia-gpu-device-plugin -p jmlim-cluster # KVM driver만 사용 가능
minikube addons enable registry -p jmlim-cluster
minikube addons enable storage-provisioner -p jmlim-cluster
minikube addons enable volumesnapshots -p jmlim-cluster
```
```bash
minikube addons list -p jmlim-cluster
```

### ETC. Docker Desktop 설치 삭제 후, Doker Engine을 Minikube Drive로 설정

```bash
#!/bin/bash

# Docker Engine 설치 (이미 설치되어 있다면 이 단계를 건너뛰세요)
sudo apt-get update
sudo apt-get install -y docker.io

# 현재 사용자를 docker 그룹에 추가 (이미 추가되어 있다면 이 단계를 건너뛰세요)
sudo usermod -aG docker $USER

# Docker 서비스 시작 및 부팅 시 자동 시작 설정
sudo systemctl start docker
sudo systemctl enable docker

# Docker 컨텍스트 확인 및 설정
docker context ls
docker context use default

# Docker Desktop 관련 컨텍스트가 있다면 제거
docker context rm desktop-linux 2>/dev/null || true

# ~/.docker/config.json 파일 수정
# 주의: 이 명령은 기존 config.json 파일을 덮어씁니다.
cat << EOF > ~/.docker/config.json
{
    "auths": {},
    "plugins": {
        "debug": {"hooks": "exec"},
        "scout": {"hooks": "pull,buildx build"}
    },
    "features": {"hooks": "true"}
}
EOF

# DOCKER_HOST 환경 변수 설정
echo 'export DOCKER_HOST=unix:///var/run/docker.sock' >> ~/.bashrc
source ~/.bashrc

# Docker 서비스 재시작
sudo systemctl restart docker

# Minikube 설치 (이미 설치되어 있다면 이 단계를 건너뛰세요)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Minikube 드라이버를 Docker로 설정
minikube config set driver docker

# 변경사항 적용을 위해 새 셸 세션 시작
exec $SHELL

# Minikube 클러스터 시작
minikube start -p my-cluster

# Minikube 상태 확인
minikube status -p my-cluster

# kubectl 설치 (이미 설치되어 있다면 이 단계를 건너뛰세요)
sudo curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# 노드 상태 확인
kubectl get nodes
```