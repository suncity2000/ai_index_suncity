# 🚀 AI Model Observatory - 빠른 시작 가이드

## 📌 이 프로젝트는 무엇인가요?

전 세계 AI 모델(ChatGPT, Claude, Gemini 등)의 성능과 국가별 AI 역량을 실시간으로 비교할 수 있는 대시보드입니다.

**라이브 데모**: [여기에 배포된 URL을 입력하세요]

---

## 🎯 비개발자를 위한 3단계 배포

### 1️⃣ GitHub에 파일 올리기 (5분)

1. GitHub.com 접속하여 로그인
2. 오른쪽 위 `+` → `New repository` 클릭
3. 이름 입력: `ai-model-observatory`
4. `Create repository` 클릭
5. `Upload files` 클릭하여 모든 파일 드래그 앤 드롭
6. `Commit changes` 클릭

### 2️⃣ Railway.app에서 배포 (5분)

1. https://railway.app 접속
2. `Login with GitHub` 클릭
3. `New Project` → `Deploy from GitHub repo`
4. 방금 만든 `ai-model-observatory` 선택
5. 자동 배포 시작! (2-3분 대기)
6. `Settings` → `Generate Domain` 클릭
7. 생성된 URL 복사!

### 3️⃣ 완료! 🎉

생성된 URL을 브라우저에 입력하면 웹사이트가 나타납니다!

**예시**: `https://ai-observatory.up.railway.app`

---

## 📁 파일 설명

```
ai-model-observatory/
├── 📄 index.html              # 웹사이트 화면
├── 🐍 backend_api.py          # 데이터 수집 프로그램
├── 📋 requirements.txt        # 필요한 라이브러리 목록
├── 🐳 Dockerfile              # Docker 설정
├── 🔧 docker-compose.yml      # 전체 시스템 설정
├── ⚙️ nginx.conf              # 웹서버 설정
├── 🚂 railway.json            # Railway 배포 설정
├── 🎨 render.yaml             # Render 배포 설정
└── 📖 README.md               # 이 파일
```

---

## 🔄 업데이트 방법

배포 후 내용을 수정하려면:

1. GitHub 저장소 접속
2. 수정할 파일 클릭
3. 연필 아이콘(✏️) 클릭하여 편집
4. 하단 `Commit changes` 클릭
5. Railway/Render가 자동으로 재배포!

---

## 💰 비용

- **Railway**: 월 $5 크레딧 무료 제공 (충분함!)
- **Render**: 완전 무료 (15분 후 슬립 모드)

---

## 📊 기능

### ✨ 주요 기능

- 💬 **LLM 모델 비교**: GPT-5, Claude Opus 4.5, Gemini 3 Pro 등
- 🎨 **이미지 생성 모델**: Midjourney, DALL-E, Stable Diffusion 등
- 🎬 **비디오 생성 모델**: Sora, Runway, Pika 등
- 🌍 **국가별 AI 순위**: 10개국 AI 역량 비교
- 💡 **트렌드 인사이트**: 최신 AI 발전 동향

### 🔄 자동 업데이트

- 5분마다 최신 데이터 자동 수집
- 실시간 성능 점수 업데이트
- 국가별 순위 변동 추적

---

## 🆘 문제 해결

### "사이트가 안 열려요"

1. Railway/Render 대시보드에서 배포 상태 확인
2. 녹색 체크 표시가 있는지 확인
3. URL을 정확히 입력했는지 확인

### "데이터가 안 보여요"

1. 브라우저에서 F12 누르기
2. Console 탭에서 에러 확인
3. 5분 정도 기다린 후 새로고침

### "너무 느려요"

- Render 무료 플랜은 15분 후 슬립 모드
- Railway 사용 추천 (더 빠름)

---

## 🎓 더 알아보기

- **상세 배포 가이드**: `GITHUB-DEPLOY-GUIDE.md` 참고
- **기술 문서**: `DEPLOYMENT.md` 참고
- **API 통합**: `API-Integration-Guide.md` 참고

---

## 📞 도움 받기

- **Railway 지원**: https://discord.gg/railway
- **Render 포럼**: https://community.render.com/
- **GitHub Issues**: 이 저장소에서 Issue 생성

---

## 📜 라이선스

MIT License - 자유롭게 사용 및 수정 가능

---

## 🙏 감사 인사

데이터 제공:
- Artificial Analysis
- Arena AI (LMSYS)
- OpenRouter
- Stanford HAI

---

## ⭐ 이 프로젝트가 도움이 되었다면?

GitHub에서 ⭐ 스타를 눌러주세요!

---

**Made with ❤️ for everyone**

코딩을 몰라도 누구나 배포할 수 있는 프로젝트입니다.
