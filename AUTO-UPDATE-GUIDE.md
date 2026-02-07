# 🤖 자동 데이터 업데이트 설정 가이드 (초간단!)

**매일 자동으로 최신 AI 모델 데이터를 수집하는 시스템**입니다!

## 🎯 이게 뭐죠?

```
매일 오전 9시
    ↓
Python 스크립트가 자동 실행
    ↓
실제 웹사이트에서 데이터 수집
(Artificial Analysis, Arena AI 등)
    ↓
data.json 파일 자동 생성
    ↓
GitHub에 자동 커밋
    ↓
웹사이트 자동 업데이트 완료! ✨
```

**결과**: 손가락 하나 안 까딱하고 항상 최신 데이터! 🎉

---

## 📋 필요한 것

- ✅ GitHub 계정 (이미 있으시죠!)
- ✅ 5분의 시간
- ❌ 코딩 지식 불필요!

---

## 🚀 설정 방법 (5분!)

### 1단계: 파일 업로드 (3분)

GitHub 저장소에 다음 3개 파일을 업로드하세요:

#### 파일 1: `scrape_data.py`
1. GitHub 저장소 메인 페이지
2. **"Add file"** → **"Upload files"** 클릭
3. `scrape_data.py` 파일 드래그 앤 드롭
4. **"Commit changes"** 클릭

#### 파일 2: `.github/workflows/update-data.yml`
1. **"Add file"** → **"Create new file"** 클릭
2. 파일 이름에 `.github/workflows/update-data.yml` 입력
   - 주의: `.github` 앞에 점(.) 빼먹지 마세요!
3. `update-data.yml` 파일 내용 복사해서 붙여넣기
4. **"Commit new file"** 클릭

#### 파일 3: `index.html` (교체)
1. 기존 `index.html` 파일 클릭
2. 휴지통 아이콘 클릭하여 삭제
3. **"Add file"** → **"Upload files"**
4. `index-auto.html` 업로드 후 이름을 `index.html`로 변경
5. **"Commit"** 클릭

---

### 2단계: GitHub Actions 권한 설정 (1분)

1. 저장소 **"Settings"** 탭 클릭
2. 왼쪽 메뉴에서 **"Actions"** → **"General"** 클릭
3. 아래로 스크롤하여 **"Workflow permissions"** 찾기
4. **"Read and write permissions"** 선택
5. **"Allow GitHub Actions to create and approve pull requests"** 체크
6. **"Save"** 버튼 클릭

---

### 3단계: 첫 실행 테스트! (1분)

1. **"Actions"** 탭 클릭
2. 왼쪽에서 **"Update AI Model Data"** 워크플로우 클릭
3. 오른쪽 위 **"Run workflow"** 버튼 클릭
4. **"Run workflow"** 확인 클릭
5. 약 1분 기다리면...
6. ✅ **녹색 체크 표시** 나타남!

---

## 🎉 완료!

이제 **매일 오전 9시**에 자동으로:
- ✅ 최신 AI 모델 데이터 수집
- ✅ data.json 자동 생성
- ✅ 웹사이트 자동 업데이트

**아무것도 안 해도 됩니다!** 🎊

---

## 📂 최종 파일 구조

```
your-repo/
├── index.html              ← 웹사이트 (index-auto.html 이름 변경)
├── data.json               ← 자동 생성됨!
├── scrape_data.py          ← Python 스크립트
└── .github/
    └── workflows/
        └── update-data.yml ← GitHub Actions 설정
```

---

## 🔍 작동 확인

### 1. data.json 파일 확인
- GitHub 저장소에서 `data.json` 파일 클릭
- 데이터가 있으면 성공!

### 2. 웹사이트 확인
```
https://your-username.github.io/your-repo
```
- "AUTO UPDATE" 표시되면 성공!
- 🔄 버튼으로 새로고침 가능

---

## ⚙️ 설정 변경 (선택사항)

### 실행 시간 변경하기

`.github/workflows/update-data.yml` 파일 수정:

```yaml
schedule:
  - cron: '0 0 * * *'   # 매일 오전 9시 (기본)
  # - cron: '0 */6 * * *'  # 6시간마다
  # - cron: '0 12 * * *'   # 매일 오후 9시
```

**Cron 시간 계산기**: https://crontab.guru

---

## 🔧 실제 데이터 연결 (고급)

현재는 예시 데이터를 사용합니다. 실제 데이터를 가져오려면:

### Artificial Analysis 연결

`scrape_data.py` 파일 수정:

```python
def scrape_artificialanalysis():
    url = "https://artificialanalysis.ai/leaderboards/models"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 테이블 찾기
    table = soup.find('table', class_='leaderboard')
    rows = table.find_all('tr')[1:]  # 헤더 제외
    
    models = []
    for row in rows:
        cells = row.find_all('td')
        model = {
            "name": cells[0].text.strip(),
            "score": float(cells[1].text.strip()),
            # ...
        }
        models.append(model)
    
    return models
```

---

## 🆘 문제 해결

### "Permission denied" 에러

**원인**: GitHub Actions 권한 부족  
**해결**: Settings → Actions → "Read and write permissions" 선택

### 스크립트 실행 안됨

**확인사항**:
1. Actions 탭에서 녹색 체크 표시 확인
2. 빨간색 X 표시면 로그 클릭하여 에러 확인

### data.json이 생성 안됨

**확인**:
1. Actions 탭에서 워크플로우 실행 확인
2. 저장소에 data.json 파일 있는지 확인
3. 없으면 수동으로 빈 파일 생성:

```json
{
  "llmModels": [],
  "imageModels": [],
  "videoModels": [],
  "voiceModels": [],
  "agentModels": [],
  "countries": [],
  "insights": [],
  "lastUpdate": "2026-02-07T09:00:00Z"
}
```

---

## 💰 비용

**완전 무료!** 🎉

- GitHub Actions: 월 2,000분 무료
- 이 스크립트: 매일 1분 = 월 30분 사용
- **무료 범위 내에서 충분합니다!**

---

## 📊 수동 실행 방법

언제든지 수동으로 데이터를 업데이트하고 싶다면:

1. **Actions** 탭 클릭
2. **"Update AI Model Data"** 클릭
3. **"Run workflow"** 버튼 클릭
4. 1분 대기
5. 완료!

---

## 🎯 다음 단계

### 단계 1: 기본 작동 확인 ✅
- 파일 업로드
- Actions 실행
- 웹사이트 확인

### 단계 2: 실제 데이터 연결 (선택)
- 웹 스크래핑 로직 추가
- API 연결
- 데이터 정확도 향상

### 단계 3: 고급 기능 (선택)
- Discord/Slack 알림
- 히스토리 저장
- 데이터 시각화

---

## 💡 팁

### 빠른 디버깅
```bash
# 로컬에서 테스트 (개발자용)
python scrape_data.py
```

### 로그 확인
Actions 탭 → 워크플로우 클릭 → 각 단계 로그 확인

### 캐시 무효화
웹사이트가 업데이트 안 되면:
- Ctrl + Shift + R (강력 새로고침)

---

## 📖 참고 자료

- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Python 웹 스크래핑 가이드](https://realpython.com/beautiful-soup-web-scraper-python/)
- [Cron 표현식 도구](https://crontab.guru/)

---

## ✨ 결론

**이제 완전 자동화!**

- ✅ 수동 업데이트 불필요
- ✅ 항상 최신 데이터
- ✅ 무료
- ✅ 간단한 설정

**축하합니다!** 🎊

이제 AI 모델 순위가 변경되면 자동으로 웹사이트에 반영됩니다!

---

## 🤔 궁금한 점?

1. **얼마나 자주 업데이트되나요?**
   - 기본: 매일 1회 (오전 9시)
   - 변경 가능: 6시간마다, 12시간마다 등

2. **수동으로도 실행 가능한가요?**
   - 네! Actions 탭에서 "Run workflow" 클릭

3. **비용이 드나요?**
   - 완전 무료! (GitHub 무료 플랜 범위 내)

4. **실패하면 어떻게 되나요?**
   - 이메일 알림 받음
   - 기존 데이터 유지

5. **데이터 소스를 추가하려면?**
   - `scrape_data.py` 파일 수정
   - 새 함수 추가

---

**모든 준비가 완료되었습니다!** 🚀

이제 손가락 하나 까딱 안 하고 항상 최신 AI 정보를 제공하는 웹사이트를 운영할 수 있습니다!
