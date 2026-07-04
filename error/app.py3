import streamlit as st
import pandas as pd
import numpy as np

# 샘플 매물 데이터 생성 (실제 엑셀 파일이 있을 때는 pd.read_excel('data.xlsx')로 교체)
@st.cache_data
def load_sample_data():
    data = {
        '지역': ['정문'] * 25 + ['미대 뒷길'] * 25 + ['후문'] * 25,
        '보증금(만원)': [500, 600, 450, 700, 550, 650, 480, 580, 620, 520, 530, 590, 470, 680, 570, 630, 490, 610, 540, 660, 510, 640, 560, 600, 580] + 
                       [400, 450, 380, 500, 420, 480, 350, 460, 440, 410, 430, 470, 360, 490, 450, 470, 370, 480, 420, 460, 390, 490, 440, 460, 430] + 
                       [800, 900, 750, 950, 850, 920, 780, 880, 860, 820, 830, 890, 770, 980, 870, 930, 790, 910, 840, 960, 810, 940, 860, 900, 880],
        '월세(만원)': [50, 60, 45, 70, 55, 65, 48, 58, 62, 52, 53, 59, 47, 68, 57, 63, 49, 61, 54, 66, 51, 64, 56, 60, 58] + 
                    [40, 45, 38, 50, 42, 48, 35, 46, 44, 41, 43, 47, 36, 49, 45, 47, 37, 48, 42, 46, 39, 49, 44, 46, 43] + 
                    [80, 90, 75, 95, 85, 92, 78, 88, 86, 82, 83, 89, 77, 98, 87, 93, 79, 91, 84, 96, 81, 94, 86, 90, 88],
        '면적(㎡)': [25, 30, 22, 35, 28, 32, 24, 29, 31, 26, 27, 30, 23, 34, 29, 31, 25, 30, 28, 32, 26, 31, 29, 30, 29] + 
                  [20, 25, 18, 28, 22, 26, 19, 24, 23, 21, 22, 25, 19, 27, 23, 25, 20, 25, 22, 26, 21, 26, 23, 25, 23] + 
                  [35, 40, 32, 45, 38, 42, 34, 39, 41, 36, 37, 40, 33, 44, 39, 41, 35, 40, 38, 42, 36, 41, 39, 40, 39],
        '풀옵션': ['O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O'] + 
               ['O', 'X', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O'] + 
               ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        '주차가능': ['O', 'X', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O'] + 
                 ['O', 'O', 'X', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'O', 'X', 'O', 'O', 'X', 'O'] + 
                 ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        '보안시설': ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'] + 
                 ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'] + 
                 ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    }
    return pd.DataFrame(data)

# 밝고 깔끔한 디자인 CSS
st.markdown("""
<style>
    /* 전체 페이지 배경을 밝게 */
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        min-height: 100vh;
    }
    
    /* Streamlit 기본 배경 제거 */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* 제목 스타일 */
    .main-title {
        text-align: center;
        color: #f39c12;
        font-size: 3.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 3px 6px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #f39c12, #e67e22);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 부제목 스타일 */
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        line-height: 1.6;
    }
    
    /* 섹션 제목 */
    .section-title {
        color: #34495e;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.8);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* 입력 필드 스타일 */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        border: 2px solid #e9ecef;
        border-radius: 10px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox > div > div:hover {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        background-color: #ffffff;
    }
    
    /* 슬라이더 스타일 */
    .stSlider > div > div {
        background: linear-gradient(90deg, #3498db, #2ecc71);
    }
    
    /* 슬라이더 컨테이너 배경 */
    .stSlider > div {
        background: rgba(255, 255, 255, 0.8);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2ecc71 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
    }
    
    /* 체크박스 스타일 */
    .stCheckbox > div > label {
        color: #2c3e50 !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    .stCheckbox > div > div {
        margin-bottom: 0.5rem;
        background: rgba(255, 255, 255, 0.9);
        padding: 0.5rem;
        border-radius: 8px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* 체크박스 텍스트 강제 검은색 */
    .stCheckbox label p,
    .stCheckbox label div,
    .stCheckbox label span {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    
    /* 조건 선택 제목도 검은색으로 */
    .condition-title {
        color: #2c3e50 !important;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* 모든 체크박스 관련 텍스트 강제 검은색 */
    div[data-testid="stCheckbox"] label {
        color: #2c3e50 !important;
    }
    
    div[data-testid="stCheckbox"] label p {
        color: #2c3e50 !important;
    }
    
    /* 컬럼 배경 */
    .stColumn {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* 입력 필드 라벨 스타일 */
    .stSelectbox label,
    .stSlider label {
        color: #34495e;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* 전체적인 그림자 효과 제거 */
    .stApp > header {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
    }
    
    /* 사이드바도 밝게 */
    .css-1d391kg {
        background: rgba(248, 249, 250, 0.9);
    }
</style>
""", unsafe_allow_html=True)

# 웹페이지 제목
st.markdown('<h1 class="main-title">🏠 Statistics Project</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">영남대학교 자취생들을 위한 매물 분석 홈페이지입니다.<br>원하는 조건을 자유롭게 검색해보세요!</p>', unsafe_allow_html=True)

# 검색 조건 섹션
st.markdown('<h2 class="section-title">🔍 검색 조건</h2>', unsafe_allow_html=True)

# 2열 레이아웃으로 구성
col1, col2 = st.columns(2)

with col1:
    # 지역 선택
    region = st.selectbox("📍 구역 선택", ["전체", "정문", "미대 뒷길", "후문"])
    
    # 조건 선택 (체크박스로 복수 선택 가능)
    st.markdown('<p class="condition-title">⭐ 조건 선택 (복수 선택 가능)</p>', unsafe_allow_html=True)
    condition_full_option = st.checkbox("풀옵션", value=False)
    condition_parking = st.checkbox("주차가능", value=False)
    condition_security = st.checkbox("보안시설", value=False)

with col2:
    # 보증금 범위 입력
    deposit = st.slider("💰 보증금 (만원)", 0, 1000, (300, 1000))
    
    # 월세 범위 입력
    rent = st.slider("💵 월세 (만원)", 0, 100, (30, 100))

# 데이터 로드
df = load_sample_data()

# 검색 버튼
if st.button("🔍 검색하기", key="search_btn"):
    # 검색 조건에 따른 필터링
    filtered_df = df.copy()
    
    # 지역 필터링
    if region != "전체":
        filtered_df = filtered_df[filtered_df['지역'] == region]
    
    # 보증금 필터링
    filtered_df = filtered_df[(filtered_df['보증금(만원)'] >= deposit[0]) & (filtered_df['보증금(만원)'] <= deposit[1])]
    
    # 월세 필터링
    filtered_df = filtered_df[(filtered_df['월세(만원)'] >= rent[0]) & (filtered_df['월세(만원)'] <= rent[1])]
    
    # 조건 필터링 (복수 선택 가능)
    if condition_full_option:
        filtered_df = filtered_df[filtered_df['풀옵션'] == 'O']
    if condition_parking:
        filtered_df = filtered_df[filtered_df['주차가능'] == 'O']
    if condition_security:
        filtered_df = filtered_df[filtered_df['보안시설'] == 'O']
    
    # 결과 표시
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    ">
        <h3 style="color: #155724; margin-top: 0;">✅ 검색 결과: {len(filtered_df)}개의 매물을 찾았습니다!</h3>
        <p style="color: #155724; margin-bottom: 0.5rem;"><strong>📍 지역:</strong> {region}</p>
        <p style="color: #155724; margin-bottom: 0.5rem;"><strong>⭐ 조건:</strong> {', '.join([cond for cond, selected in [('풀옵션', condition_full_option), ('주차가능', condition_parking), ('보안시설', condition_security)] if selected]) if any([condition_full_option, condition_parking, condition_security]) else '전체'}</p>
        <p style="color: #155724; margin-bottom: 0.5rem;"><strong>💰 보증금:</strong> {deposit[0]}~{deposit[1]}만원</p>
        <p style="color: #155724; margin-bottom: 0;"><strong>💵 월세:</strong> {rent[0]}~{rent[1]}만원</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 매물 카드 표시
    if len(filtered_df) > 0:
        st.markdown('<h2 class="section-title">🏠 검색된 매물</h2>', unsafe_allow_html=True)
        
        # 매물 카드 CSS 추가
        st.markdown("""
        <style>
        .property-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 1px solid #e9ecef;
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .property-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        
        .property-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .property-location {
            background: linear-gradient(135deg, #3498db, #2ecc71);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .property-price {
            font-size: 1.2rem;
            font-weight: 700;
            color: #e74c3c;
        }
        
        .property-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .detail-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .detail-label {
            font-weight: 600;
            color: #7f8c8d;
        }
        
        .detail-value {
            color: #2c3e50;
        }
        
        .condition-badges {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .badge-yes {
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
        }
        
        .badge-no {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 매물 카드 생성
        for idx, row in filtered_df.iterrows():
            total_price = row['보증금(만원)'] + row['월세(만원)']
            
            st.markdown(f"""
            <div class="property-card">
                <div class="property-header">
                    <div class="property-location">📍 {row['지역']}</div>
                    <div class="property-price">총 {total_price:,}만원</div>
                </div>
                
                <div class="property-details">
                    <div class="detail-item">
                        <span class="detail-label">💰 보증금:</span>
                        <span class="detail-value">{row['보증금(만원)']:,}만원</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">💵 월세:</span>
                        <span class="detail-value">{row['월세(만원)']:,}만원</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">📐 면적:</span>
                        <span class="detail-value">{row['면적(㎡)']}㎡</span>
                    </div>
                </div>
                
                <div class="condition-badges">
                    <span class="badge {'badge-yes' if row['풀옵션'] == 'O' else 'badge-no'}">
                        풀옵션: {'O' if row['풀옵션'] == 'O' else 'X'}
                    </span>
                    <span class="badge {'badge-yes' if row['주차가능'] == 'O' else 'badge-no'}">
                        주차: {'O' if row['주차가능'] == 'O' else 'X'}
                    </span>
                    <span class="badge {'badge-yes' if row['보안시설'] == 'O' else 'badge-no'}">
                        보안: {'O' if row['보안시설'] == 'O' else 'X'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            border: 1px solid #f5c6cb;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            margin-top: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
            <h3 style="color: #721c24; margin-top: 0;">😔 검색 결과가 없습니다</h3>
            <p style="color: #721c24; margin-bottom: 0;">다른 조건으로 다시 검색해보세요!</p>
        </div>
        """, unsafe_allow_html=True)
