># Cuda 설치

[참고 자료](https://ingu627.github.io/tips/install_cuda_linux/)

### 1. 기존 설치된 관련 파일 삭제 (CUDA, cuDNN 관련 파일)
```bash
echo "Removing existing CUDA and cuDNN files..."
sudo apt-get --purge remove "*cublas*" "*cufft*" "*curand*" "*cusolver*" "*cusparse*" "*npp*" "*nvjpeg*" "cuda*" "libcudnn*" -y
sudo apt-get autoremove -y
sudo apt-get autoclean
sudo rm -rf /usr/local/cuda*

### 2. Nvidia Driver 설치
echo "Installing NVIDIA Driver..."
sudo apt-get update
sudo apt-get install -y nvidia-driver-560

### 3. CUDA 설치
echo "Installing CUDA 12.6..."

### CUDA repository 추가
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub
sudo sh -c 'echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64 /" > /etc/apt/sources.list.d/cuda.list'

### CUDA 설치
sudo apt-get update
sudo apt-get install -y cuda-12-6

### 4. cuDNN 설치
echo "Installing cuDNN..."
sudo apt-get install -y libcudnn8 libcudnn8-dev

### 5. 환경 변수 설정 (CUDA와 cuDNN 경로 추가)
echo "Configuring environment variables..."
echo 'export PATH=/usr/local/cuda-12.6/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export CUDNN_PATH=/usr/include' >> ~/.bashrc
source ~/.bashrc

### 6. 설치 확인
echo "Verifying installations..."

### NVIDIA 드라이버 확인
nvidia-smi

### CUDA 컴파일러 버전 확인
nvcc --version

### cuDNN 버전 확인
cat /usr/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
echo "Installation completed successfully!"
```

