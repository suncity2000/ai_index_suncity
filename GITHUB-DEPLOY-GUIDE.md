# 🎯 비개발자를 위한 GitHub 배포 완전 가이드

코딩 지식 없이 GitHub만으로 AI Model Observatory를 배포하는 방법입니다!

## 📋 준비물

- ✅ GitHub 계정 (이미 있으시다니 완료!)
- ✅ 다운로드한 프로젝트 파일들
- ✅ 15분의 시간

## 🎬 배포 방법 (가장 쉬운 순서)

1. [Railway.app으로 배포 (추천!)](#방법-1-railwayapp으로-배포-추천)
2. [Render.com으로 배포](#방법-2-rendercom으로-배포)
3. [Vercel로 배포](#방법-3-vercel로-배포-프론트엔드만)

---

## 방법 1: Railway.app으로 배포 (추천!)

### ⏱️ 소요시간: 10분
### 💰 비용: 무료 (월 5$ 크레딧 제공)

### 단계별 가이드

#### 1단계: GitHub에 파일 업로드 📤

1. **GitHub.com 접속**
   - 브라우저에서 https://github.com 열기
   - 로그인

2. **새 저장소(Repository) 만들기**
   - 오른쪽 상단 `+` 버튼 클릭
   - `New repository` 선택
   
   ![New Repository](https://docs.github.com/assets/cb-11427/mw-1440/images/help/repository/repo-create.webp)

3. **저장소 설정**
   ```
   Repository name: ai-model-observatory
   Description: AI 모델 비교 대시보드
   Public 선택 (무료)
   "Add a README file" 체크
   ```
   - `Create repository` 버튼 클릭

4. **파일 업로드**
   - 방금 만든 저장소 페이지에서
   - `Add file` → `Upload files` 클릭
   - 다음 파일들을 드래그 앤 드롭:
     ```
     ✅ backend_api.py
     ✅ index.html
     ✅ requirements.txt
     ✅ Dockerfile
     ✅ docker-compose.yml
     ✅ nginx.conf
     ✅ README.md
     ```
   - 하단에 `Commit changes` 버튼 클릭

   ![Upload Files](https://docs.github.com/assets/cb-33194/mw-1440/images/help/repository/upload-files-button.webp)

#### 2단계: Railway.app 설정 🚂

1. **Railway.app 접속**
   - 브라우저에서 https://railway.app 열기
   - `Login` 클릭
   - `Login with GitHub` 선택
   - GitHub 계정으로 로그인

2. **새 프로젝트 만들기**
   - 대시보드에서 `New Project` 클릭
   - `Deploy from GitHub repo` 선택
   - `ai-model-observatory` 저장소 선택
   
3. **자동 배포 시작!**
   - Railway가 자동으로 감지하고 배포 시작
   - 2-3분 정도 기다리면 완료

4. **URL 확인**
   - 배포 완료 후 `Settings` 탭 클릭
   - `Generate Domain` 클릭
   - 생성된 URL 복사 (예: `ai-observatory.up.railway.app`)

5. **접속 테스트**
   - 생성된 URL을 브라우저에 입력
   - 대시보드가 나타나면 성공! 🎉

### 🎉 완료! 이제 웹사이트가 작동합니다!

---

## 방법 2: Render.com으로 배포

### ⏱️ 소요시간: 15분
### 💰 비용: 완전 무료

### 단계별 가이드

#### 1단계: GitHub에 파일 업로드 (위와 동일)

#### 2단계: render.yaml 파일 추가

1. **GitHub 저장소로 이동**
2. **새 파일 만들기**
   - `Add file` → `Create new file` 클릭
   - 파일 이름: `render.yaml`
   
3. **아래 내용 복사해서 붙여넣기**
   ```yaml
   services:
     # 백엔드 API
     - type: web
       name: ai-observatory-backend
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
     
     # 프론트엔드
     - type: web
       name: ai-observatory-frontend
       env: static
       region: oregon
       plan: free
       buildCommand: echo "Static site"
       staticPublishPath: .
       routes:
         - type: rewrite
           source: /api/*
           destination: https://ai-observatory-backend.onrender.com/api/*
   ```

4. **Commit 버튼 클릭**

#### 3단계: Render.com 설정

1. **Render.com 접속**
   - https://render.com 열기
   - `Get Started` 클릭
   - `GitHub`으로 로그인

2. **Blueprint 배포**
   - `New +` 버튼 클릭
   - `Blueprint` 선택
   - `ai-model-observatory` 저장소 선택
   - `Connect` 클릭

3. **자동 배포 시작**
   - Render가 자동으로 render.yaml 읽고 배포
   - 3-5분 정도 소요

4. **URL 확인**
   - 대시보드에서 `ai-observatory-frontend` 클릭
   - 상단의 URL 확인 (예: `https://ai-observatory-frontend.onrender.com`)

### 🎉 완료!

**주의사항**: 무료 플랜은 15분 비활성화 후 슬립 모드 진입. 첫 접속 시 30초 정도 로딩될 수 있습니다.

---

## 방법 3: Vercel로 배포 (프론트엔드만)

Vercel은 프론트엔드만 무료로 호스팅합니다. 백엔드는 Railway나 Render 필요.

### 단계별 가이드

#### 1단계: 백엔드를 Railway에 먼저 배포
(위의 Railway 가이드 참고)

#### 2단계: Vercel 설정

1. **Vercel.com 접속**
   - https://vercel.com 열기
   - `Sign Up` 클릭
   - `Continue with GitHub` 선택

2. **프로젝트 import**
   - `Add New...` → `Project` 클릭
   - `ai-model-observatory` 선택
   - `Import` 클릭

3. **환경 변수 설정**
   - `Environment Variables` 섹션에서
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-backend.up.railway.app/api`
   - (Railway에서 받은 백엔드 URL 입력)

4. **Deploy 클릭**
   - 2분 정도 기다리면 완료
   - 생성된 URL 확인 (예: `ai-observatory.vercel.app`)

---

## 🔧 배포 후 설정

### 커스텀 도메인 연결 (선택사항)

#### Railway에서:
1. 프로젝트 설정 → `Settings` → `Domains`
2. `Custom Domain` 클릭
3. 본인의 도메인 입력 (예: `ai.yourdomain.com`)
4. DNS 설정에서 CNAME 레코드 추가

#### Render에서:
1. 서비스 클릭 → `Settings` → `Custom Domain`
2. 도메인 입력
3. DNS A 레코드 추가

---

## 📱 업데이트 방법

배포 후 코드를 수정하려면:

### GitHub 웹에서 직접 수정

1. **GitHub 저장소 접속**
2. **수정할 파일 클릭** (예: `backend_api.py`)
3. **연필 아이콘(Edit) 클릭**
4. **코드 수정**
5. **하단 `Commit changes` 클릭**
6. **자동으로 재배포 시작!** ✨

### 파일 다시 업로드

1. **GitHub 저장소 접속**
2. **해당 파일 클릭**
3. **휴지통 아이콘으로 삭제**
4. **`Add file` → `Upload files`로 새 파일 업로드**

---

## 🆘 문제 해결

### "사이트가 열리지 않아요"

**확인 사항:**
1. Railway/Render 대시보드에서 배포 상태 확인
   - 녹색 체크 표시가 있어야 함
   - 빨간색 X 표시면 로그 확인

2. URL이 정확한지 확인
   - 마지막에 슬래시(/) 없이 입력
   - https:// 포함해서 입력

3. 로그 확인
   - Railway: 프로젝트 → `Deployments` → 최신 배포 클릭 → `View Logs`
   - Render: 서비스 클릭 → `Logs` 탭

### "데이터가 안 나와요"

**해결방법:**
1. 브라우저 F12 (개발자 도구) 열기
2. Console 탭에서 에러 확인
3. Network 탭에서 API 요청 확인
   - 빨간색 에러가 있으면 백엔드 문제
   - URL이 잘못되었을 가능성

### "15분 후에 느려져요" (Render 무료 플랜)

**해결방법:**
- 유료 플랜으로 업그레이드 ($7/월)
- 또는 Railway 사용 (무료 크레딧)

---

## 💰 비용 비교

| 플랫폼 | 무료 플랜 | 유료 시작 | 비고 |
|--------|-----------|-----------|------|
| **Railway** | $5 크레딧/월 | $5/월 | 가장 추천! |
| **Render** | 완전 무료 | $7/월 | 슬립 모드 있음 |
| **Vercel** | 무료 | $20/월 | 프론트엔드만 |

---

## ✅ 최종 체크리스트

배포 완료 후 확인:

- [ ] 웹사이트가 열리는가?
- [ ] LLM 모델 탭에 데이터가 보이는가?
- [ ] 이미지/비디오 탭도 작동하는가?
- [ ] 국가 순위가 표시되는가?
- [ ] 인사이트 섹션이 보이는가?
- [ ] "Last updated" 시간이 표시되는가?

모두 체크되면 성공! 🎉

---

## 🎓 추가 학습 자료

더 알아보고 싶다면:

- **GitHub 기본**: https://docs.github.com/ko/get-started
- **Railway 문서**: https://docs.railway.app/
- **Render 문서**: https://render.com/docs

---

## 📞 도움이 필요하면

1. **Railway 커뮤니티**: https://discord.gg/railway
2. **Render 포럼**: https://community.render.com/
3. **GitHub Issues**: 저장소에서 Issue 생성

---

## 🚀 다음 단계

배포가 완료되었다면:

1. ✅ **친구들과 공유하기**
   - URL을 복사해서 전달

2. ✅ **정기 업데이트**
   - 일주일에 한 번 GitHub에서 파일 수정
   - 자동으로 최신 데이터 반영

3. ✅ **커스텀 도메인 연결** (선택사항)
   - 예: `ai-observatory.mywebsite.com`

4. ✅ **모니터링 설정**
   - Railway/Render 대시보드에서 트래픽 확인

---

## 🎉 축하합니다!

비개발자인데도 불구하고 완전한 풀스택 웹 애플리케이션을 배포했습니다!

이제 다음과 같은 것들을 할 수 있습니다:
- ✅ 전 세계 어디서나 접속 가능한 웹사이트 운영
- ✅ 실시간 AI 모델 데이터 제공
- ✅ GitHub로 쉽게 업데이트
- ✅ 자동으로 5분마다 최신 데이터 갱신

**당신은 이제 웹 개발자입니다!** 🎊

---

### 📸 스크린샷으로 보는 Railway 배포 과정

#### 1. GitHub에 저장소 만들기
```
1. github.com 접속
2. 오른쪽 위 + 버튼
3. New repository
4. 이름 입력: ai-model-observatory
5. Create repository 클릭
```

#### 2. 파일 업로드
```
1. Add file 버튼
2. Upload files 클릭
3. 파일 드래그 앤 드롭
4. Commit changes 클릭
```

#### 3. Railway 배포
```
1. railway.app 접속
2. Login with GitHub
3. New Project
4. Deploy from GitHub repo
5. ai-model-observatory 선택
6. Deploy 자동 시작!
```

#### 4. URL 생성
```
1. Settings 탭
2. Generate Domain 클릭
3. URL 복사
4. 브라우저에 붙여넣기
5. 완료! 🎉
```

---

**이 가이드를 북마크하세요!**
나중에 다시 필요할 때 쉽게 찾을 수 있습니다.

**질문이 있으면 언제든 물어보세요!** 😊
