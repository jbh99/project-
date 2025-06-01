import requests
import random

# 초기 지역 코드 데이터 (시/도 단위)
base_region_codes = {
    "11": "서울특별시",
    "26": "부산광역시",
    "27": "대구광역시",
    "28": "인천광역시",
    "29": "광주광역시",
    "30": "대전광역시",
    "31": "울산광역시",
    "36": "세종특별자치시",
    "41": "경기도",
    "42": "강원도",
    "43": "충청북도",
    "44": "충청남도",
    "45": "전라북도",
    "46": "전라남도",
    "47": "경상북도",
    "48": "경상남도",
    "50": "제주특별자치도"
}

# 수작업 코딩된 관광지 데이터 (시/도 및 시군구 단위)
tourist_spots = {
    # 경기도 하위 지역
    "4182000000": ["쁘디프랑스", "자라섬"],
    "4165000000": ["포천 산정호수", "국립수목원(광릉숲)"],
    "4180000000": ["재인폭포 (한탄강 유네스코 세계지질공원)", "연천 호로고루"],
    "4150000000": ["설봉공원", "덕평공룡수목원"],
    "4146100000": ["호암미술관", "에버랜드"],
    "4148000000": ["헤이리 예술마을", "퍼스트가든"],
    "4161000000": ["화담숲", "팔당물안개공원"],
    
    # 부산 하위 지역
    "2617000000": ["부잔 진시장", "부산 자유도매시장"],
    "2644000000": ["맥도생태공원", "신호공원"],
    "2671000000": ["아홉산숲", "국립부산과학관"],
    "2638000000": ["부산현대미술관", "다대포 꿈의 낙조분수"],
    "2614000000": ["송도해수욕장", "송도 구름산책로"],
    "2623000000": ["부산어린이대공원", "선암사"],
    "2620000000": ["국립해양박물관", "흰여울문화마을"],
    "2650000000": ["F1963", "광안리해수욕장"],
    
    # 서울 하위 지역 
    "1111000000": ["경복궁", "청와대"],
    "1114000000": ["남산타워", "명동"],
    "1117000000": ["홍대", "합정역"],
    
    # 인천 하위 지역 
    "2817000000": ["인천대교", "을왕리해수욕장"],
    "2818500000": ["차이나타운", "자유공원"],
    
    # 제주도 하위 지역 
    "5011000000": ["성산일출봉", "섭지코지"],
    "5013000000": ["한라산", "협재해수욕장"]
}

def get_region_hierarchy(appkey, parent_code=None):
    """SK Open API로부터 지역 계층 구조를 가져옵니다 (시/도 및 시군구 단위만)."""
    base_url = "https://apis.openapi.sk.com/puzzle/travel/meta/districts"
    headers = {'Accept': 'application/json', 'appkey': appkey}
    
    try:
        # 최상위 지역(시,도)인 경우
        if not parent_code:
            params = {'type': 'sig', 'offset': 0, 'limit': 100}
        # 하위지역 조회인 경우
        else:
            params = {'type': 'sig', 'offset': 0, 'limit': 100}
        
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status', {}).get('code') == '00':
            contents = data.get('contents', [])
            if parent_code:
                return [item for item in contents if str(item.get('districtCode', '')).startswith(str(parent_code))]
            return contents
        return []
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        print(f"⚠️ 지역 정보를 가져오는 중 오류입니다: {str(e)}")
        return []

def get_tourist_spots(region_code):
    """ 관광지 정보를 가져옵니다."""
    return [{"name": spot, "description": f"{spot} 관광지"} 
            for spot in tourist_spots.get(region_code, [])]

def display_region_info(region_code, region_name, spots):
    """지역 정보와 관광지를 표시합니다."""
    print("\n" + "=" * 50)
    print(f"🏆 [{region_name}] 지역 정보 🏆")
    print("=" * 50)
    
    if spots:
        print("\n🌟 대표 관광지:")
        for i, spot in enumerate(spots, 1):  # 관광지 출력 
            name = spot.get('name', '이름 없음')
            desc = spot.get('description', '설명 없음')
            print(f"{i}. {name}")
            print(f"   - {desc}")
    else:
        print("\n⚠️ 이 지역의 관광지 정보가 없습니다.")

def display_subregions_with_spots(regions, parent_name):
    """하위 지역 목록과 관광지를 함께 표시합니다."""
    print("\n" + "=" * 50)
    print(f"🏆 [{parent_name}] 하위 지역 목록 🏆")
    print("=" * 50)
    
    for region in regions:
        region_code = region.get('districtCode', '')
        region_name = region.get('districtName', '이름 없음')
        
        # 관광지 정보 가져오기 
        spots = get_tourist_spots(region_code)
        
        print(f"\n📍 {region_code}: {region_name}")
        if spots:
            print("   🌟 대표 관광지:")
            for spot in spots:  # 모든 관광지 출력 
                print(f"      - {spot.get('name', '이름 없음')}")
        else:
            print("   ⚠  관광지 정보가 없습니다")

def validate_region_code(region_code, regions):
    """입력된 지역 코드가 유효한지 확인합니다."""
    if not region_code:
        return False
    
    # 최상위 지역 코드 확인
    if len(region_code) == 2 and region_code in base_region_codes:
        return True
    
    # 하위 지역 코드 확인
    for region in regions:
        if region.get('districtCode') == region_code:
            return True
    
    return False

def main():
    print(" 국내 여행지 추천 프로그램 ")
    print("=" * 50)
    
    # 1. appKey 입력
    appkey = input("발급 받은 appKey를 입력하세요: ").strip()
    if not appkey:
        print("appKey를 입력해주세요.")
        return
    
    # 2. 지역 코드 계층적 탐색
    current_code = None
    regions = []
    region_stack = []  # 이전 단계를 저장하기 위한 스택
    
    while True:
        if not current_code:
            # 최상위 지역 선택
            print("\n[시/도 목록]")
            for code, name in base_region_codes.items():
                print(f"{code}: {name}")
            
            region_code = input("\n추천받을 지역 코드를 입력하세요 (2자리 시/도 코드, 종료: q): ").strip()
            
            if region_code.lower() == 'q':
                return
            if region_code not in base_region_codes:
                print("⚠️ 유효하지 않은 코드입니다. 다시 입력해주세요.")
                continue
            
            regions = get_region_hierarchy(appkey, region_code)
            if not regions:
                print("⚠️ 해당 지역 정보를 가져오지 못했습니다.")
                continue
            
            current_code = region_code
            region_name = base_region_codes[region_code]
            
            # 하위 지역과 관광지 함께 출력
            display_subregions_with_spots(regions, region_name)
            
            # 현재 상태 저장 (이전 단계로 돌아가기 위해)
            region_stack.append((current_code, regions))
        else:
            # 하위 지역 목록 표시
            print(f"\n[{base_region_codes.get(current_code[:2], '')} 하위 지역 목록]")
            print("~: 이전 단계로 돌아가기")
            print("q: 프로그램 종료")
            
            for region in regions:
                print(f"{region.get('districtCode', '')}: {region.get('districtName', '')}")
            
            user_input = input("\n상세 코드를 입력하세요 (전체 코드 입력 또는 Enter로 선택 완료): ").strip()
            
            if user_input.lower() == 'q':
                return
            elif user_input == '~':
                if region_stack:
                    current_code, regions = region_stack.pop()
                    continue
                else:
                    print("⚠️ 더 이상 이전으로 돌아갈 수 없습니다.")
                    continue
            elif not user_input:
                break
                
            # 유효하지 않을 경우
            if not validate_region_code(user_input, regions):
                print("⚠️ 유효하지 않은 코드입니다. 다시 입력해주세요.")
                continue
                
            # 관광지 정보 가져오기 (하위 지역은 더 이상 탐색하지 않음)
            region_name = next((r.get('districtName') for r in regions if r.get('districtCode') == user_input), "알 수 없는 지역")
            spots = get_tourist_spots(user_input)
            display_region_info(user_input, region_name, spots)
            
            # 현재 상태 저장 
            region_stack.append((current_code, regions))
            current_code = user_input
    
    # 3. 최종 선택된 지역의 하위 지역 목록
    destinations = []
    for region in regions:
        code = region.get('districtCode', '')
        name = region.get('districtName', '이름 없음')
        destinations.append(f"{code}: {name}")
    
    if not destinations:
        print("⚠️ 추천할 여행지가 없습니다.")
        return
    
    # 4. 결과 출력
    print("\n" + "=" * 50)
    parent_name = base_region_codes.get(current_code[:2], '알 수 없는 지역')
    print(f" [{parent_name}] 지역 목록 ")
    print("=" * 50)
    
    # 모든 지역 출력 
    for dest in destinations:
        print(dest)
    
    # 5. 선택된 지역 목록 중 무작위 추천 
    if destinations:
        print("\n" + "=" * 50)
        random_dest = random.choice(destinations)
        print(f"🎲 무작위 추천 지역: {random_dest}")
            
if __name__ == "__main__":
    main()
