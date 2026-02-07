#!/usr/bin/env python3
import json
import requests
import os
from datetime import datetime

def scrape_artificialanalysis():
    print("📊 Artificial Analysis API에서 실제 데이터 수집 및 매핑 중...")
    
    api_key = aa_nlHXrHmYGAApxkFnjBrBFcYPegOsmqKZ
    if not api_key:
        print("❌ API 키를 찾을 수 없습니다.")
        return []

    # API v2 엔드포인트
    url = "https://artificialanalysis.ai/api/v2/data/llms/models" 
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            api_data = response.json()
            # API 응답의 'data' 리스트를 가져옵니다.
            raw_models = api_data.get('data', [])
            
            # 1. 지능 지수(Intelligence Index) 기준 내림차순 정렬
            raw_models.sort(
                key=lambda x: x.get('evaluations', {}).get('artificial_analysis_intelligence_index') or 0, 
                reverse=True
            )
            
            models = []
            for index, item in enumerate(raw_models[:15]): # 상위 15개 모델 추출
                evals = item.get('evaluations', {})
                pricing = item.get('pricing', {})
                creator = item.get('model_creator', {})
                
                # 가격 등급 계산 (100만 토큰당 가격 기준)
                price_val = pricing.get('price_1m_blended_3_to_1') or 0
                if price_val == 0: price_str = "Free"
                elif price_val < 0.5: price_str = "$"
                elif price_val < 2.0: price_str = "$$"
                elif price_val < 10.0: price_str = "$$$"
                else: price_str = "$$$$"

                # 데이터 매핑
                models.append({
                    "rank": index + 1,
                    "name": item.get('name'),
                    "company": creator.get('name', 'Unknown'),
                    "score": evals.get('artificial_analysis_intelligence_index') or 0,
                    "price": price_str,
                    "usage": 98 - (index * 2), # 순위에 따른 가상 사용률
                    "color": "#00fff2" if index < 3 else "#a78bfa",
                    "url": f"https://artificialanalysis.ai/models/{item.get('slug')}",
                    "isKorean": creator.get('name') in ["Naver", "Wrtn", "Upstage", "Kakao"],
                    "newFeatures": ["API Live"] if index < 5 else []
                })
            
            print(f"✅ 실제 모델 {len(models)}개 매핑 완료!")
            return models
        else:
            print(f"❌ API 오류: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
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
