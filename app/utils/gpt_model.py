from openai import OpenAI
import os
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_style_tag_from_gpt(captions: List[str]) -> str:
    prompt = (
        "아래 이미지 설명을 참고해서 스타일을 다음 중 하나로 분류해줘:\n"
        "- 메인: 신랑/신부 단독 혹은 둘이 중심이 되는 사진\n"
        "- 커플: 자연스러운 커플의 분위기가 느껴지는 사진\n"
        "- 풍경: 배경 위주, 사람보다는 풍경이 중심인 사진\n\n"
        f"이미지 설명들: {captions}\n\n"
        "이 이미지에 가장 적합한 스타일 태그 하나만 선택해서 말해줘. 반드시 '메인', '커플', '풍경' 중 하나여야 해.\n"
        "스타일 태그:"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 이미지 스타일 분류 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        temperature=0
    )
    
    style_tag = response.choices[0].message.content.strip()
    print(f"[GPT Response] style_tag: {style_tag}")  # ✅ 결과 확인용 로그
    return style_tag

def get_photo_order_from_gpt(photo_data: list[dict]) -> list[int]:
    prompt_lines = ["다음 사진들을 청첩장의 자연스러운 순서로 정렬해줘.\nID 순서만 콤마로 반환해줘.\n"]

    for photo in photo_data:
        prompt_lines.append(f"{photo['id']}. 스타일: {photo['style']}, 설명: {photo['caption']}")
    
    prompt_lines.append("\n배치 순서:")

    prompt = "\n".join(prompt_lines)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 청첩장 구성 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.7
    )

    result = response.choices[0].message.content.strip()
    print(f"[GPT Response] photo order: {result}")
    
    try:
        return list(map(int, result.replace("[", "").replace("]", "").split(",")))
    except Exception:
        return []