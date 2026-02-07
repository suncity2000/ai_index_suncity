#!/usr/bin/env python3
import json
import requests
import os
from datetime import datetime

def scrape_artificialanalysis():
    print("📊 Artificial Analysis API에서 실제 데이터 수집 중...")
    
    # 1. 환경 변수에서 키 가져오기 (GitHub Secrets)
    api_key = os.environ.get('AI_MODELS_KEY')
    
    # 로컬 테스트용 (테스트 후 반드시 지우거나 주석 처리하세요)
    # api_key = "여기에_실제_키_입력" 

    if not api_key:
        print("❌ API 키를 찾을 수 없습니다. 환경 변수 설정을 확인하세요.")
        return []

    url = "https://artificialanalysis.ai/api/v2/data/llms/models" 
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(response.json()) # 이 줄이 핵심입니다!
        # 상태 코드가 200일 때만 JSON 분석 시도
        if response.status_code == 200:
            api_data = response.json()
            raw_models = api_data if isinstance(api_data, list) else api_data.get('models', [])
            
            models = []
            for index, item in enumerate(raw_models[:15]):
                models.append({
                    "rank": index + 1,
                    "name": item.get('model_name') or item.get('name', 'Unknown'),
                    "company": item.get('creator_name') or "AI Research",
                    "score": item.get('intelligence_index') or item.get('intelligence_score', 85),
                    "price": "$$$" if (item.get('price_per_1m_tokens', 0) > 10) else "$$",
                    "usage": 90 - index,
                    "color": "#00fff2" if index < 3 else "#a78bfa",
                    "url": f"https://artificialanalysis.ai/models/{item.get('model_slug') or item.get('slug', '')}",
                    "isKorean": False,
                    "newFeatures": ["Verified API"]
                })
            print(f"✅ 실제 모델 {len(models)}개 수집 성공!")
            return models
        else:
            print(f"❌ API 오류 (상태 코드: {response.status_code})")
            return []

    except Exception as e:
        print(f"❌ 데이터 처리 중 에러 발생: {e}")
        return []

# --- 나머지 함수들 (scrape_lmsys_arena, scrape_voice_models 등)은 동일하게 유지 ---

def scrape_lmsys_arena():
    return [{"rank": 1, "name": "Nano Banana Pro", "company": "Google", "score": 95, "price": "$$", "usage": 92, "specialty": "Photorealism", "color": "#f472b6", "url": "https://labs.google/nano", "isKorean": False}]

def scrape_voice_models():
    return [
        {"rank": 1, "name": "ElevenLabs Turbo v3", "company": "ElevenLabs", "score": 96, "price": "$$", "usage": 94, "specialty": "자연스러운 억양", "color": "#a78bfa", "url": "https://elevenlabs.io", "isKorean": False},
        {"rank": 3, "name": "Clova Dubbing", "company": "Naver", "score": 91, "price": "$$", "usage": 78, "specialty": "한국어 특화", "color": "#10b981", "url": "https://clovadubbing.naver.com", "isKorean": True}
    ]

def scrape_agent_services():
    return [{"rank": 1, "name": "Genspark", "company": "Genspark", "score": 93, "price": "Free", "usage": 89, "specialty": "AI 검색 엔진", "color": "#a78bfa", "url": "https://genspark.ai", "isKorean": False}]

def scrape_stanford_hai():
    return [{"rank": 6, "name": "한국", "flag": "🇰🇷", "aiPower": 5700, "investment": 11.8, "adoption": 42.1, "models": 78, "trend": "up"}]

def generate_insights():
    return [{"title": "한국 AI 서비스 약진", "description": "국내 서비스들이 글로벌 톱10 진입 중.", "icon": "🇰🇷", "color": "border-blue-400"}]

def main():
    print("🚀 AI Model Observatory 데이터 수집 시작\n")
    
    data = {
        "llmModels": scrape_artificialanalysis(),
        "imageModels": scrape_lmsys_arena(),
        "videoModels": [{"rank": 1, "name": "Veo 3.1", "company": "Google", "score": 94, "price": "$$$", "usage": 88, "duration": "8s", "color": "#f472b6", "url": "https://deepmind.google/veo/", "isKorean": False}],
        "voiceModels": scrape_voice_models(),
        "agentModels": scrape_agent_services(),
        "countries": scrape_stanford_hai(),
        "insights": generate_insights(),
        "lastUpdate": datetime.now().isoformat(),
        "metadata": {"version": "1.0", "source": "Automated API"}
    }
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ data.json 파일 생성 완료!")

if __name__ == "__main__":
    main()
