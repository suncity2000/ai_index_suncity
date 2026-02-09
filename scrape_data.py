#!/usr/bin/env python3
import json
import requests
import os
from datetime import datetime

# 공통 설정
API_BASE_URL = "https://artificialanalysis.ai/api/v2/data"
# [주의] 깃허브에 올릴 때는 보안을 위해 아래 줄을 사용하세요.
# API_KEY = os.environ.get('AI_MODELS_KEY')
API_KEY = "aa_nlHXrHmYGAApxkFnjBrBFcYPegOsmqKZ"

# 한국 기업 목록 로드
def load_korean_companies():
    try:
        with open('korean_companies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('companies', [])
    except Exception as e:
        print(f"⚠️ korean_companies.json 로드 실패: {e}")
        return ["Naver", "Wrtn", "Upstage", "Kakao", "Samsung", "LG", "SK Telecom", "KT"]

def fetch_api_data(endpoint):
    """API 엔드포인트에서 데이터를 가져오는 공통 함수"""
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print(f"❌ API 오류 ({endpoint}): {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 네트워크 에러 ({endpoint}): {e}")
        return []

def is_korean_company(creator_name, korean_list):
    """한국 기업 여부 확인"""
    return any(kr.lower() in creator_name.lower() for kr in korean_list)

def map_llm_data(items, korean_list):
    """LLM 모델 데이터 매핑 (상위 20개, 풍부한 평가 데이터 포함)"""
    mapped_list = []
    for index, item in enumerate(items[:20]):
        creator = item.get('model_creator', {})
        creator_name = creator.get('name', 'Unknown')
        evals = item.get('evaluations', {})

        # 점수 추출 (다양한 키 이름 시도)
        score = evals.get('artificial_analysis_intelligence_index', 0)
        coding_score = (
            evals.get('artificial_analysis_coding_index', 0) or
            evals.get('coding', 0) or
            evals.get('humaneval', 0) or 0
        )
        math_score = (
            evals.get('artificial_analysis_math_index', 0) or
            evals.get('math', 0) or
            evals.get('gsm8k', 0) or 0
        )

        # 속도 (토큰/초)
        speed = item.get('median_output_tokens_per_second', 0) or 0

        # 가격 ($/백만 토큰)
        input_price = item.get('input_cost_per_million', 0) or 0
        output_price = item.get('output_cost_per_million', 0) or 0

        # 가성비 점수: 종합점수 / 출력가격 * 10 (가격이 0이면 점수 그대로)
        if output_price > 0:
            value_score = round(score / output_price * 10, 2)
        else:
            value_score = round(score * 100, 2)

        mapped_list.append({
            "name": item.get('name', 'Unknown'),
            "company": creator_name,
            "score": score,
            "codingScore": coding_score,
            "mathScore": math_score,
            "speed": speed,
            "inputPrice": input_price,
            "outputPrice": output_price,
            "valueScore": value_score,
            "color": "#00fff2" if index < 3 else "#a78bfa",
            "url": f"https://artificialanalysis.ai/models/{item.get('slug', '')}",
            "isKorean": is_korean_company(creator_name, korean_list)
        })
    return mapped_list

def map_media_data(items, korean_list):
    """미디어 모델 데이터 매핑 (상위 20개)"""
    mapped_list = []
    for index, item in enumerate(items[:20]):
        creator = item.get('model_creator', {})
        creator_name = creator.get('name', 'Unknown')

        categories = item.get('categories', [])
        specialty = categories[0].get('style_category', 'General') if categories else "General"

        score = item.get('elo', 0)
        num_ratings = item.get('num_ratings', 0) or item.get('total_votes', 0) or 0
        release_date = item.get('release_date', '') or ''

        mapped_list.append({
            "name": item.get('name', 'Unknown'),
            "company": creator_name,
            "score": score,
            "specialty": specialty,
            "numRatings": num_ratings,
            "releaseDate": release_date,
            "color": "#00fff2" if index < 3 else "#a78bfa",
            "url": f"https://artificialanalysis.ai/models/{item.get('slug', '')}",
            "isKorean": is_korean_company(creator_name, korean_list)
        })
    return mapped_list

def main():
    print("🚀 AI Model Observatory 통합 데이터 수집 시작\n")

    korean_list = load_korean_companies()
    print(f"🇰🇷 한국 기업 목록: {len(korean_list)}개 로드됨")

    # 1. LLM 모델 수집
    print("\n🧠 LLM 데이터 수집 중...")
    llm_raw = fetch_api_data("llms/models")
    llm_models = map_llm_data(llm_raw, korean_list)

    # 2. Text-to-Image 모델 수집
    print("🎨 Text-to-Image 데이터 수집 중...")
    tti_raw = fetch_api_data("media/text-to-image")
    tti_models = map_media_data(tti_raw, korean_list)

    # 3. Text-to-Speech 모델 수집
    print("🎙️ Text-to-Speech 데이터 수집 중...")
    tts_raw = fetch_api_data("media/text-to-speech")
    tts_models = map_media_data(tts_raw, korean_list)

    # 4. Text-to-Video 모델 수집
    print("🎬 Text-to-Video 데이터 수집 중...")
    ttv_raw = fetch_api_data("media/text-to-video")
    ttv_models = map_media_data(ttv_raw, korean_list)

    # 5. Image-to-Video 모델 수집
    print("🎞️ Image-to-Video 데이터 수집 중...")
    itv_raw = fetch_api_data("media/image-to-video")
    itv_models = map_media_data(itv_raw, korean_list)

    # JSON 데이터 생성
    data = {
        "llmModels": llm_models,
        "textToImageModels": tti_models,
        "textToSpeechModels": tts_models,
        "textToVideoModels": ttv_models,
        "imageToVideoModels": itv_models,
        "lastUpdate": datetime.now().isoformat(),
        "metadata": {
            "version": "3.0",
            "source": "Artificial Analysis API v2",
            "apiEndpoints": {
                "llm": "https://artificialanalysis.ai/api/v2/data/llms/models",
                "textToImage": "https://artificialanalysis.ai/api/v2/data/media/text-to-image",
                "textToSpeech": "https://artificialanalysis.ai/api/v2/data/media/text-to-speech",
                "textToVideo": "https://artificialanalysis.ai/api/v2/data/media/text-to-video",
                "imageToVideo": "https://artificialanalysis.ai/api/v2/data/media/image-to-video"
            }
        }
    }

    total = len(llm_models) + len(tti_models) + len(tts_models) + len(ttv_models) + len(itv_models)
    korean_count = sum(1 for m in llm_models + tti_models + tts_models + ttv_models + itv_models if m.get('isKorean'))

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ data.json 생성 완료!")
    print(f"   📊 총 {total}개 모델 (LLM:{len(llm_models)} TTI:{len(tti_models)} TTS:{len(tts_models)} TTV:{len(ttv_models)} ITV:{len(itv_models)})")
    print(f"   🇰🇷 한국 기업 모델: {korean_count}개")

if __name__ == "__main__":
    main()
