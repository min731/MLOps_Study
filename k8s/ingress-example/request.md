```bash
sudo vi /etc/hosts
192.168.49.2    minikube.jmlim-cluster.com
```

```bash
# HTTP로 요청
# minikube.jmlim-cluster.com(hosts-192.168.49.2(mk ip))-> 31131(nginx-ingress-controller Nodeport Port) -> hello.example.com (kind: ingress Host명) -> service -> deployment
curl -H "Host: hello.example.com" minikube.jmlim-cluster.com:31131
\
# 또는 HTTPS로 요청 (-k 옵션은 인증서 검증을 건너뜁니다)
curl -k -H "Host: hello.example.com" https://minikube.jmlim-cluster.com:30341
```