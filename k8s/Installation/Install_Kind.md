># Kind 설치

[Kind 공식 문서 참고](https://kind.sigs.k8s.io/docs/user/quick-start/#installing-with-go-install)를 참고 하였습니다.

### 1. kind 패키지 다운로드 및 설치

```bash
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

### 2. kubectl 패키지 다운로드 및 설치

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

### 3. 클러스터 설치

```yaml
# kind 클러스터 설정 파일
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4

# 네트워킹 설정
networking:
  apiServerAddress: "0.0.0.0"  # API 서버가 모든 인터페이스에서 리스닝
  # apiServerPort: 6443  # API 서버 포트

# 노드 설정
nodes:
# 컨트롤 플레인 (마스터) 노드
- role: control-plane
  image: kindest/node:v1.26.15
  extraPortMappings:
  - containerPort: 6443  # Kubernetes API 서버
    hostPort: 6443
    listenAddress: "0.0.0.0"
    protocol: TCP
  - containerPort: 80  # HTTP 트래픽 (Ingress)
    hostPort: 80
    listenAddress: "0.0.0.0"
    protocol: TCP
  - containerPort: 443  # HTTPS 트래픽 (Ingress)
    hostPort: 443
    listenAddress: "0.0.0.0"
    protocol: TCP
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"  # Ingress 준비 레이블 추가

# 워커 노드
- role: worker
  image: kindest/node:v1.26.15
  extraPortMappings:
  - containerPort: 30000  # NodePort 서비스 범위 시작
    hostPort: 30000
    listenAddress: "0.0.0.0"
    protocol: TCP
  - containerPort: 31000  # NodePort 서비스 추가 포트 예시
    hostPort: 31000
    listenAddress: "0.0.0.0"
    protocol: TCP
```

```bash
kind create cluster --name my-cluster --config kind-config.yaml
kubectl cluster-info
kubectl get nodes
kubectl get pods --all-namespaces
kubectl label node jmlim-cluster-worker node-role.kubernetes.io/control-plane-
kubectl label node jmlim-cluster-worker node-role.kubernetes.io/master-
kubectl label node jmlim-cluster-worker node-role.kubernetes.io/worker=worker
```

### 4. GPU 활성화

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```