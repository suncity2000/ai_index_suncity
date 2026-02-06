# 🌐 웹서버 배포 가이드

AI Model Observatory를 다양한 웹서버 플랫폼에 배포하는 완전한 가이드입니다.

## 📋 목차

1. [Docker + Nginx 배포 (추천)](#1-docker--nginx-배포-추천)
2. [Railway.app 배포 (무료)](#2-railwayapp-배포-무료)
3. [Render.com 배포 (무료)](#3-rendercom-배포-무료)
4. [AWS EC2 배포](#4-aws-ec2-배포)
5. [Google Cloud Run 배포](#5-google-cloud-run-배포)
6. [Vercel + 외부 API 배포](#6-vercel--외부-api-배포)
7. [전통적인 VPS 배포](#7-전통적인-vps-배포)

---

## 1. Docker + Nginx 배포 (추천)

가장 간단하고 이식성이 좋은 방법입니다.

### 준비물
- Docker 및 Docker Compose 설치
- 서버 (VPS, EC2, 자체 서버 등)

### 배포 단계

#### 1단계: 파일 준비
```bash
# 프로젝트 디렉토리에 모든 파일 복사
ai-observatory/
├── backend_api.py
├── index.html
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

#### 2단계: Docker Compose로 실행
```bash
# 디렉토리 이동
cd ai-observatory

# 컨테이너 빌드 및 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 상태 확인
docker-compose ps
```

#### 3단계: 접속
```
http://your-server-ip
또는
http://your-domain.com
```

#### 중지 및 재시작
```bash
# 중지
docker-compose down

# 재시작
docker-compose restart

# 업데이트 후 재배포
docker-compose down
docker-compose build
docker-compose up -d
```

### 도메인 연결 (선택사항)

#### DNS 설정
1. 도메인 등록업체(Cloudflare, GoDaddy 등)에서 A 레코드 추가
2. 서버 IP 주소를 입력

#### SSL 인증서 (Let's Encrypt)
```bash
# Certbot 설치
sudo apt-get install certbot python3-certbot-nginx

# 인증서 발급
sudo certbot --nginx -d your-domain.com

# 자동 갱신 설정
sudo certbot renew --dry-run
```

---

## 2. Railway.app 배포 (무료)

Railway는 무료 티어로 간단하게 배포할 수 있습니다.

### 배포 단계

#### 1단계: GitHub에 코드 푸시
```bash
# Git 저장소 초기화
git init
git add .
git commit -m "Initial commit"

# GitHub에 푸시
git remote add origin https://github.com/your-username/ai-observatory.git
git push -u origin main
```

#### 2단계: Railway 설정

1. https://railway.app 접속
2. GitHub으로 로그인
3. "New Project" 클릭
4. "Deploy from GitHub repo" 선택
5. ai-observatory 저장소 선택

#### 3단계: 환경 변수 설정 (필요시)
```
PORT=8000
PYTHONUNBUFFERED=1
```

#### 4단계: 배포 완료
Railway가 자동으로 빌드하고 배포합니다.
제공된 URL로 접속: `https://your-app.up.railway.app`

### railway.json 설정 파일 (선택사항)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python backend_api.py",
    "healthcheckPath": "/api/status",
    "healthcheckTimeout": 100
  }
}
```

---

## 3. Render.com 배포 (무료)

Render는 무료 티어로 백엔드를 호스팅할 수 있습니다.

### 배포 단계

#### 1단계: render.yaml 파일 생성
```yaml
services:
  # 백엔드 API
  - type: web
    name: ai-observatory-api
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python backend_api.py
    healthCheckPath: /api/status
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 8000

  # 정적 사이트 (프론트엔드)
  - type: web
    name: ai-observatory-frontend
    env: static
    buildCommand: echo "No build needed"
    staticPublishPath: .
    routes:
      - type: rewrite
        source: /api/*
        destination: https://ai-observatory-api.onrender.com/api/*
    headers:
      - path: /*
        name: Cache-Control
        value: public, max-age=0, must-revalidate
```

#### 2단계: Render.com에서 배포

1. https://render.com 접속
2. GitHub 연결
3. "New +" → "Blueprint" 선택
4. render.yaml을 포함한 저장소 선택
5. 자동 배포 시작

#### 3단계: 접속
```
https://ai-observatory-frontend.onrender.com
```

### 주의사항
- 무료 티어는 15분 비활성 후 슬립 모드 진입
- 첫 요청 시 시작 시간이 소요될 수 있음

---

## 4. AWS EC2 배포

프로덕션 환경에 적합한 방법입니다.

### 배포 단계

#### 1단계: EC2 인스턴스 생성
1. AWS 콘솔에서 EC2 서비스 선택
2. "Launch Instance" 클릭
3. Ubuntu 22.04 LTS 선택
4. t2.micro (프리 티어) 또는 t3.small 선택
5. 보안 그룹 설정:
   - SSH (22): 내 IP
   - HTTP (80): 0.0.0.0/0
   - HTTPS (443): 0.0.0.0/0
   - Custom (8000): 0.0.0.0/0 (테스트용)

#### 2단계: 서버 접속 및 설정
```bash
# SSH 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 로그아웃 후 재접속
exit
```

#### 3단계: 코드 배포
```bash
# Git 설치
sudo apt install git -y

# 저장소 클론
git clone https://github.com/your-username/ai-observatory.git
cd ai-observatory

# Docker Compose 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

#### 4단계: 도메인 및 SSL 설정
```bash
# Nginx 설치 (리버스 프록시용)
sudo apt install nginx certbot python3-certbot-nginx -y

# Nginx 설정
sudo nano /etc/nginx/sites-available/ai-observatory

# 아래 내용 붙여넣기:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 설정 활성화
sudo ln -s /etc/nginx/sites-available/ai-observatory /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# SSL 인증서 발급
sudo certbot --nginx -d your-domain.com
```

#### 5단계: 자동 시작 설정
```bash
# systemd 서비스 파일 생성
sudo nano /etc/systemd/system/ai-observatory.service

# 내용:
[Unit]
Description=AI Observatory
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/ai-observatory
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down

[Install]
WantedBy=multi-user.target

# 서비스 활성화
sudo systemctl enable ai-observatory
sudo systemctl start ai-observatory
```

---

## 5. Google Cloud Run 배포

서버리스 환경으로 자동 스케일링이 가능합니다.

### 배포 단계

#### 1단계: Google Cloud SDK 설치
```bash
# gcloud CLI 설치
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

#### 2단계: 프로젝트 설정
```bash
# 프로젝트 생성
gcloud projects create ai-observatory-PROJECT_ID

# 프로젝트 설정
gcloud config set project ai-observatory-PROJECT_ID

# API 활성화
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

#### 3단계: 컨테이너 빌드 및 배포
```bash
# Cloud Build로 이미지 빌드
gcloud builds submit --tag gcr.io/ai-observatory-PROJECT_ID/backend

# Cloud Run에 배포
gcloud run deploy ai-observatory \
  --image gcr.io/ai-observatory-PROJECT_ID/backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --memory 512Mi \
  --cpu 1
```

#### 4단계: 프론트엔드는 Firebase Hosting 사용
```bash
# Firebase CLI 설치
npm install -g firebase-tools

# Firebase 초기화
firebase init hosting

# index.html 배포
firebase deploy --only hosting
```

---

## 6. Vercel + 외부 API 배포

프론트엔드는 Vercel, 백엔드는 별도 서버에 배포합니다.

### 배포 단계

#### 1단계: 백엔드를 Railway/Render에 배포
위의 Railway나 Render 가이드 참고

#### 2단계: Vercel 설정
```bash
# Vercel CLI 설치
npm install -g vercel

# 프로젝트 디렉토리에서
vercel

# 프로덕션 배포
vercel --prod
```

#### 3단계: 환경 변수 설정
Vercel 대시보드에서:
```
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app/api
```

---

## 7. 전통적인 VPS 배포

일반 VPS (DigitalOcean, Linode, Vultr 등)에 배포합니다.

### 배포 단계

#### 1단계: VPS 설정
```bash
# SSH 접속
ssh root@your-vps-ip

# 사용자 생성
adduser aiobs
usermod -aG sudo aiobs
su - aiobs
```

#### 2단계: Python 환경 설정
```bash
# Python 및 필수 패키지 설치
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip nginx -y

# 프로젝트 디렉토리 생성
mkdir ~/ai-observatory
cd ~/ai-observatory

# 가상환경 생성
python3.11 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

#### 3단계: Systemd 서비스 설정
```bash
sudo nano /etc/systemd/system/ai-observatory.service

# 내용:
[Unit]
Description=AI Observatory Backend
After=network.target

[Service]
Type=simple
User=aiobs
WorkingDirectory=/home/aiobs/ai-observatory
Environment="PATH=/home/aiobs/ai-observatory/venv/bin"
ExecStart=/home/aiobs/ai-observatory/venv/bin/python backend_api.py
Restart=always

[Install]
WantedBy=multi-user.target

# 서비스 시작
sudo systemctl daemon-reload
sudo systemctl enable ai-observatory
sudo systemctl start ai-observatory
```

#### 4단계: Nginx 설정
```bash
sudo nano /etc/nginx/sites-available/ai-observatory

# 내용:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /home/aiobs/ai-observatory;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# 활성화
sudo ln -s /etc/nginx/sites-available/ai-observatory /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 보안 설정

### 방화벽 설정 (UFW)
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 환경 변수 보호
```bash
# .env 파일 생성
nano .env

# 내용:
API_KEY=your-secret-key
DATABASE_URL=your-db-url

# 백엔드에서 사용
pip install python-dotenv
```

### HTTPS 강제
nginx.conf에 추가:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}
```

---

## 📊 모니터링

### 로그 확인
```bash
# Docker
docker-compose logs -f backend

# Systemd
sudo journalctl -u ai-observatory -f

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 성능 모니터링
```bash
# Docker 리소스 사용량
docker stats

# 시스템 리소스
htop
```

---

## 🔄 업데이트 프로세스

### Docker 환경
```bash
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

### Systemd 환경
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart ai-observatory
```

---

## 💰 비용 비교

| 플랫폼 | 무료 티어 | 유료 시작가격 | 장점 |
|--------|-----------|---------------|------|
| Railway | 5$/월 크레딧 | 5$/월 | 간편한 배포 |
| Render | Free tier | 7$/월 | 무료 SSL |
| AWS EC2 | 12개월 무료 | 5$/월~ | 확장성 |
| DigitalOcean | - | 4$/월~ | 저렴함 |
| Google Cloud Run | 무료 할당량 | 사용량 기반 | 서버리스 |

---

## ✅ 체크리스트

배포 전 확인사항:
- [ ] 모든 파일이 준비되었는가?
- [ ] requirements.txt가 최신인가?
- [ ] API URL이 올바르게 설정되었는가?
- [ ] 방화벽 규칙이 설정되었는가?
- [ ] SSL 인증서가 설치되었는가?
- [ ] 백업 계획이 있는가?
- [ ] 모니터링이 설정되었는가?

---

## 🆘 문제 해결

### "502 Bad Gateway"
- 백엔드가 실행 중인지 확인: `docker-compose ps` 또는 `systemctl status ai-observatory`
- 포트가 올바른지 확인: nginx.conf의 proxy_pass

### "CORS Error"
- nginx.conf의 CORS 헤더 확인
- 프론트엔드의 API_BASE_URL 확인

### "연결 거부됨"
- 방화벽 확인: `sudo ufw status`
- 백엔드 로그 확인: `docker-compose logs backend`

---

**추천 배포 방법:**
- **빠른 프로토타입**: Railway 또는 Render (무료)
- **프로덕션**: AWS EC2 + Docker (확장성)
- **저렴한 옵션**: VPS + Nginx (월 4$)
- **서버리스**: Google Cloud Run (사용량 기반)

이제 원하는 플랫폼을 선택해서 배포하실 수 있습니다! 🚀
