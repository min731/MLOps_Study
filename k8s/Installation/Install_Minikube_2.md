https://claude.ai/chat/b782e6b2-356c-4537-9772-b6b925f2ebb8

```bash
minikube start -p jmlim-cluster \
  --driver=docker \
  --nodes=2 \
  --cpus=8 \
  --memory=5120 \
  --disk-size=50g \
  --kubernetes-version=v1.25.16 \
  --gpus=all \
  --addons=ingress \
  --addons=nvidia-gpu-device-plugin

# label 설정
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/control-plane-
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/master-
kubectl label node jmlim-cluster-m02 node-role.kubernetes.io/worker=worker

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

# 기본 애드온
minikube addons enable dashboard -p jmlim-cluster
minikube addons enable ingress -p jmlim-cluster
minikube addons enable ingress-dns -p jmlim-cluster
minikube addons enable metallb -p jmlim-cluster
minikube addons enable metrics-server -p jmlim-cluster
minikube addons enable registry -p jmlim-cluster
minikube addons enable storage-provisioner -p jmlim-cluster
minikube addons enable volumesnapshots -p jmlim-cluster

# MetalLB IP 범위 설정
minikube addons configure metallb -p jmlim-cluster
# 입력해야 할 IP 범위 예시 (minikube ip 명령어로 확인한 IP 기준):
# - 시작 IP: 192.168.49.2
# - 종료 IP: 192.168.49.10

# 노드 상태 확인
kubectl get nodes
# 파드 상태 확인
kubectl get pods -A
# GPU 인식 확인
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.1/nvidia-device-plugin.yml
kubectl get pods -n kube-system | grep nvidia

# 대시보드 접속
minikube dashboard -p jmlim-cluster

# 클러스터 정보 확인
kubectl cluster-info
```