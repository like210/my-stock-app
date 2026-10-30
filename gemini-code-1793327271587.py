import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 디자인 스타일 지정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="주식 가격 조회기",
    page_icon="📈",
    layout="centered"
)

# 따뜻한 톤(크림/노란색/웜톤 스타일)을 적용하기 위한 CSS 설정
st.markdown("""
    <style>
    /* 전체 배경색 지정 */
    .stApp {
        background-color: #FAF8F5;
    }
    
    /* 카드 및 입력창 스타일 개선 */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #F0EAE1;
    }
    
    /* 헤더 스타일 */
    h1 {
        color: #4A3E3D;
    }
    p {
        color: #6E6259;
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. 메인 화면 타이틀 및 안내 문구
# -----------------------------------------------------------------------------
st.title("📈 간단 주식 가격 조회기")
st.write("원하는 주식의 종목 코드를 입력하시면 최근 1년간의 주가 흐름을 따뜻한 차트로 보여드립니다.")


# -----------------------------------------------------------------------------
# 3. 사용자 입력 받기
# -----------------------------------------------------------------------------
# 기본값으로 삼성전자(005930.KS)를 지정합니다.
ticker_symbol = st.text_input(
    label="종목 코드를 입력하세요 (예: 한국 005930.KS, 미국 AAPL, TSLA)",
    value="005930.KS"
).strip().upper()


# -----------------------------------------------------------------------------
# 4. yfinance 데이터 가져오기 및 시각화
# -----------------------------------------------------------------------------
if ticker_symbol:
    try:
        # yfinance를 통해 데이터 불러오기 (최근 1년치: period='1y')
        ticker_data = yf.Ticker(ticker_symbol)
        df = ticker_data.history(period="1y")

        if df.empty:
            st.error("입력한 종목 코도의 데이터를 찾을 수 없습니다. 코드를 확인해주세요.")
        else:
            # 주식 주요 지표 계산
            current_price = df['Close'].iloc[-1]           # 가장 최근 종가 (현재가)
            price_1y_ago = df['Close'].iloc[0]             # 1년 전 종가
            change_rate = ((current_price - price_1y_ago) / price_1y_ago) * 100  # 1년 등락률(%)

            # 종목 이름 가져오기 (정보가 없으면 입력한 코드 사용)
            info = ticker_data.info
            stock_name = info.get('shortName', ticker_symbol)

            # 지표 카드를 2개 컬럼으로 나누어 표시
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label=f"현재가 ({stock_name})",
                    value=f"{current_price:,.2f}"
                )
            with col2:
                st.metric(
                    label="1년 등락률",
                    value=f"{change_rate:+.2f}%",
                    delta=f"{change_rate:+.2f}%"
                )

            # -----------------------------------------------------------------
            # 5. Plotly 꺾은선 차트 생성
            # -----------------------------------------------------------------
            fig = go.Figure()

            # 꺾은선 라인 추가 (따뜻한 주황/브라운 톤 적용)
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='종가',
                line=dict(color='#E07A5F', width=2.5),
                hovertemplate='날짜: %{x|%Y-%m-%d}<br>주가: %{y:,.2f}<extra></extra>'
            ))

            # 차트 레이아웃 설정
            fig.update_layout(
                title=dict(
                    text=f"<b>{stock_name} 최근 1년 주가 추이</b>",
                    font=dict(size=18, color="#4A3E3D")
                ),
                xaxis_title="날짜",
                yaxis_title="주가",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#FFFDF9",
                hovermode="x unified",
                margin=dict(l=20, r=20, t=50, b=20),
                xaxis=dict(
                    showgrid=True,
                    gridcolor="#F0EAE1",
                    color="#4A3E3D"
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#F0EAE1",
                    color="#4A3E3D"
                )
            )

            # Streamlit 화면에 Plotly 차트 출력
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("데이터를 불러오는 중 오류가 발생했습니다. 종목 코드를 다시 확인해 주세요.")