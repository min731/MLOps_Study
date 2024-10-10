># Minikube 설치

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