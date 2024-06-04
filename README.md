# Pi4-K3s-IoT-Monitoring-System

This repository contains a project for setting up a K3s cluster using Raspberry Pi 4 devices. The cluster includes a deployment of Pods running RabbitMQ, Telegraf, InfluxDB, and an RTSP Receiver. This setup demonstrates the capability of resource-constrained devices to run a fully functional edge computing environment.

## 준비물
- k8s의 클러스터 및 K3s가 설치된 클러스터 테스트 환경
- 1Master 2Worker 노드의 Raspberry Pi4 3대로 구축된 Cluster
- Raspberry Pi Camera가 장착된 디바이스
- Raspbian OS 64-bit가 설치된 Raspberry Pi 4B

## 작동 방법

### 1. node 조회
```bash
$ sudo kubectl get node
```

### 2. Namespace 생성
```bash
$ sudo kubectl apply -f namespace.yaml
```

### 3. RabbitMQ pod 배포
```bash
$ sudo kubectl apply -f rabbitmq-deployment.yaml
```

### 4. InfluxDB 배포 및 서비스 배포
```bash
$ sudo kubectl apply -f influxdb-deployment.yaml
```

### 5. InfluxDB 접속 및 초기 설정
```bash
웹 브라우저에서 http://<포트포워딩 한 Cluster의 외부 접근 주소>:8086/에 접속하여 초기 설정을 진행
```

### 6. Telegraf Config ConfigMap 배포 (연결을 위한 InfluxDB hash 수정)
```bash
sudo kubectl apply -f telegraf-configmap.yaml
```

### 7. Telegraf 배포
```bash
sudo kubectl apply -f telegraf-deployment.yaml
```

### 8-A. 클라이언트 PC에서 Python 실행 (A와 B중에서 선택, 둘다 동시 실행은 불가)
```python
python3 monitor_GUI.py
```

### 8-B. 클라이언트 PC에서 Node.js 실행
```bash
cd dev/node
npm install
node server.js
```

### 9. Raspberry Pi 1에서 카메라 실행
```bash
bash camera.sh
```

### 10. Raspberry Pi 1에서 데이터 리소스 정보 발행
```python
python Pi4-K3s-IoT-Monitoring-System/src/cluster/Rasp-Produer/producer_app.py
```

### 11. GUI에서 실시간 영상 및 시스템 리소스 보기
GUI에서 Start Stream 버튼을 클릭하여 실시간 영상을 받고 시스템 리소스를 모니터링합니다.
<br><br><br><br>
## K3s 리소스 제거
### 네임스페이스 삭제 - 네임스페이스 내의 모든 리소스(Pods, Deployments, Services 등)
```bash
sudo kubectl delete namespace monitoring
```


