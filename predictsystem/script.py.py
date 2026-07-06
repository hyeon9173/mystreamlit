import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 깨짐 방지 및 세련된 미니멀 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 페이지 설정
st.set_page_config(
    page_title="대기오염 리스크 관리 시스템", 
    layout="wide"
)

# --- 💾 [백엔드 데이터] 대기업 반도체 공장 가상 센서 데이터셋 ---
@st.cache_data
def load_big_company_data():
    data = {
        "농도_황산화물(mg/m3)": [12.5, 14.1, 11.8, 13.5, 15.2],
        "농도_먼지(mg/m3)": [5.2, 6.1, 4.8, 5.5, 6.4],
        "농도_질소산화물(mg/m3)": [35.4, 38.2, 33.1, 36.8, 41.0],
        "배출유량(m3/h)": [80000, 82000, 79000, 81000, 83000]
    }
    return pd.DataFrame(data)

big_df = load_big_company_data()

# 대기업 데이터의 평균값 추출
avg_sox_conc = big_df["농도_황산화물(mg/m3)"].mean()
avg_dust_conc = big_df["농도_먼지(mg/m3)"].mean()
avg_nox_conc = big_df["농도_질소산화물(mg/m3)"].mean()
avg_big_flow = big_df["배출유량(m3/h)"].mean()


# --- ⚙️ [백엔드 로직 1] 유량 연산 및 스케일링 함수 ---
def calculate_kg_emission(concentration, big_flow_rate, scale_percent, operating_hours):
    our_estimated_flow = big_flow_rate * (scale_percent / 100.0)
    total_kg = concentration * our_estimated_flow * operating_hours * 1e-6
    return total_kg


# --- ⚙️ [백엔드 로직 2] 법정 부과금 산출 함수 ---
def calculate_realistic_fine(basic_inputs, excess_inputs, is_over_limit, violation_count):
    prices = {"황산화물": 500, "먼지": 770, "질소산화물": 2130}
    yearly_index = 5.8234
    company_size_coeff = 0.3 
    
    results = {}
    total_sum = 0
    
    violation_coeff = 1.0 if violation_count == 1 else (1.2 if violation_count == 2 else 1.4)

    for key in ["황산화물", "먼지", "질소산화물"]:
        fine_basic = basic_inputs[key] * prices[key] * yearly_index * 0.5
        fine_excess = 0
        if is_over_limit:
            fine_excess = excess_inputs[key] * prices[key] * yearly_index * company_size_coeff * violation_coeff
            
        total_item = int(fine_basic + fine_excess)
        results[key] = {"기본": int(fine_basic), "초과": int(fine_excess), "합계": total_item}
        total_sum += total_item
        
    results["총액"] = total_sum
    return results


# ---------------- 🖤 모노톤 에센셜 UI 디자인 시작 ----------------

with st.sidebar:
    st.markdown("### **우리 공장 조건 입력**")
    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1.5px solid #111111;'>", unsafe_allow_html=True)
    
    our_hours = st.number_input("이번 달 공장 가동 시간 (hour)", min_value=1, value=120)
    
    scale_ratio = st.slider(
        "대기업 대비 공장 설비 규모 (%)", 
        min_value=1, max_value=100, value=10,
        help="벤치마킹 대상 대기업 생산라인 대비 당사 공장의 총 배출 유량(설비 용량) 비율입니다. 값이 작을수록 당사의 예상 배출 유량 스케일이 낮게 보정됩니다."
    )
    
    st.markdown("<hr style='margin: 15px 0; border: 0; border-top: 1px solid #CCCCCC;'>", unsafe_allow_html=True)
    st.markdown("**단속 및 기준치 초과 설정**")
    is_over_limit = st.checkbox("배출허용기준 초과 적발 시", value=False)
    
    excess_ratio = 0.0
    violation_count = 1
    
    if is_over_limit:
        excess_ratio = st.slider(
            "순수 초과 배출량 비율 (%)", 
            min_value=0, max_value=100, value=5,
            help="총 배출량 중에서 정부가 허용하는 법적 기준선(농도)을 초과하여 배출된 '벌금 부과 대상 리스크 물질'의 비율을 가정합니다."
        )
        violation_count = st.slider("최근 2년 이내 누적 위반 횟수", 1, 3, 1)

# 💡 [업그레이드 1] 제목 이모티콘 삭제 및 두 행으로 안전하게 나누어 출력
st.markdown("<h2 style='margin-bottom: 0px; font-weight: 700; color: #111111;'>대기업 데이터 기반</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='margin-top: 0px; font-weight: 700; color: #111111;'>중소기업 환경 리스크 예측 시스템</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #666666; font-size: 15px; margin-top: 10px;'>반도체 대기업 센서 데이터(농도/유량)를 벤치마킹하여 당사의 예상 과징금을 실시간 시뮬레이션합니다.</p>", unsafe_allow_html=True)

# 세련된 블랙 라인으로 구분선 교체
st.markdown("<hr style='margin: 15px 0; border: 0; border-top: 2px solid #111111;'>", unsafe_allow_html=True)


# --- 🧠 백엔드 자동 연산 프로세스 가동 ---
our_sox_kg = calculate_kg_emission(avg_sox_conc, avg_big_flow, scale_ratio, our_hours)
our_dust_kg = calculate_kg_emission(avg_dust_conc, avg_big_flow, scale_ratio, our_hours)
our_nox_kg = calculate_kg_emission(avg_nox_conc, avg_big_flow, scale_ratio, our_hours)

input_sox_excess = our_sox_kg * (excess_ratio / 100.0)
input_dust_excess = our_dust_kg * (excess_ratio / 100.0)
input_nox_excess = our_nox_kg * (excess_ratio / 100.0)

basic_inputs = {"황산화물": our_sox_kg, "먼지": our_dust_kg, "질소산화물": our_nox_kg}
excess_inputs = {"황산화물": input_sox_excess, "먼지": input_dust_excess, "질소산화물": input_nox_excess}
results = calculate_realistic_fine(basic_inputs, excess_inputs, is_over_limit, violation_count)


# --- 📊 독립된 행(Row) 기반의 미니멀 KPI 패널 ---
if is_over_limit:
    st.markdown(f"<div style='border: 1px solid #111111; padding: 12px; border-radius: 0px; background-color: #FAFAFA; margin-bottom: 15px; font-size: 14px;'><b>규제 상태:</b> <span style='color: #D32F2F; font-weight: bold;'>{violation_count}차 적발 가중 규제 적용 중</span></div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='border: 1px solid #E0E0E0; padding: 12px; border-radius: 0px; background-color: #FAFAFA; margin-bottom: 15px; font-size: 14px;'><b>규제 상태:</b> <span style='color: #111111; font-weight: bold;'>정상 운영 (기준 준수 예측)</span></div>", unsafe_allow_html=True)

st.metric(label="벤치마킹 예상 총 부담금 (합계)", value=f"{results['총액']:,} 원")

# 세련된 다크그레이 점선 배치
st.markdown("<hr style='margin: 15px 0; border: 0; border-top: 1px dashed #333333;'>", unsafe_allow_html=True)

total_kg = our_sox_kg + our_dust_kg + our_nox_kg
st.metric(label="가동시간 기반 예상 총 배출량", value=f"{total_kg:,.2f} kg")

st.markdown("<br>", unsafe_allow_html=True)


# 탭 구조 설계
tab_report, tab_bench = st.tabs(["비용 산정 리포트", "벤치마킹한 대기업 원본 데이터셋"])

with tab_report:
    st.markdown("<h5 style='font-weight: 600; color: #111111;'>[1] 연동 기준 상세 예측 통계</h5>", unsafe_allow_html=True)
    
    report_df = pd.DataFrame({
        "예상 배출량 (kg)": [our_sox_kg, our_dust_kg, our_nox_kg],
        "기본 부과금": [results["황산화물"]["기본"], results["먼지"]["기본"], results["질소산화물"]["기본"]],
        "초과 부과금 (벌금)": [results["황산화물"]["초과"], results["먼지"]["초과"], results["질소산화물"]["초과"]],
        "최종 합계": [results["황산화물"]["합계"], results["먼지"]["합계"], results["질소산화물"]["합계"]]
    }, index=["황산화물 (SOx)", "먼지 (Dust)", "질소산화물 (NOx)"])
    
    st.dataframe(
        report_df.style.format({
            "예상 배출량 (kg)": "{:,.2f} kg",
            "기본 부과금": "{:,} 원",
            "초과 부과금 (벌금)": "{:,} 원",
            "최종 합계": "{:,} 원"
        }), 
        use_container_width=True
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("<h5 style='font-weight: 600; color: #111111;'>[2] 물질별 비용 구성 시각화 그래프</h5>", unsafe_allow_html=True)
    
    categories = ["황산화물", "먼지", "질소산화물"]
    basic_fines = [results["황산화물"]["기본"], results["먼지"]["기본"], results["질소산화물"]["기본"]]
    excess_fines = [results["황산화물"]["초과"], results["먼지"]["초과"], results["질소산화물"]["초과"]]
    
    # 💡 [업그레이드 2] 대형 모니터에서도 시원하게 보이도록 그래프 크기 극대화 (figsize=(16, 6.5))
    fig, ax = plt.subplots(figsize=(16, 6.5))
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # 💡 [업그레이드 3] 그래프 컬러 모노톤 매칭 (기본=검정색, 초과=회색)
    ax.bar(categories, basic_fines, label="기본 부과금", color="#111111", width=0.25)
    ax.bar(categories, excess_fines, bottom=basic_fines, label="초과 부과금(벌금)", color="#AAAAAA", width=0.25)
    
    # 💡 [업그레이드 4] 축과 테두리 선을 깊이감 있는 짙은 검정 계열로 마감 처리
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#111111')
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_color('#111111')
    ax.spines['bottom'].set_linewidth(1.2)
    
    ax.tick_params(colors='#111111', labelsize=11)
    ax.legend(facecolor='#FFFFFF', edgecolor='#111111', fontsize=11, loc='upper right')
    ax.set_ylabel("부과 금액 (원)", color='#111111', fontsize=11, fontweight='bold')
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    st.pyplot(fig)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("<div style='border-left: 3px solid #111111; padding-left: 10px; color: #444444; font-size: 14px;'><b>비즈니스 가치:</b> 이 시스템은 TMS 측정 장비가 없는 중소기업이 대기업의 평균 배출 농도 패턴을 공유받았다고 가정하여, 가동시간과 기업 규모 비율 조절만으로 잠재적 환경 비용 리스크를 시뮬레이션할 수 있도록 설계되었습니다.</div>", unsafe_allow_html=True)

with tab_bench:
    st.markdown("<h5 style='font-weight: 600; color: #111111;'>[참조 데이터] 대기업 반도체 공장 실시간 센서 데이터셋 (가상)</h5>", unsafe_allow_html=True)
    st.dataframe(big_df, use_container_width=True)

st.markdown("<hr style='margin: 30px 0; border: 0; border-top: 1px solid #111111;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #999999; font-size: 12px;'>© 2026 중소기업 환경안전 상생 예측 시스템 | 대기업 데이터 매핑 기반 알고리즘</p>", unsafe_allow_html=True)