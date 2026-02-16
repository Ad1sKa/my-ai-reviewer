import streamlit as st
from huggingface_hub import InferenceClient

# 1. Настройка страницы и стилей
st.set_page_config(page_title="ReviewAI | Vitebsk Pro", page_icon="🚀", layout="wide")

# Кастомный CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 4em;
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
    }
    .result-area {
        background-color: #1e222d;
        padding: 25px;
        border-radius: 20px;
        border-left: 5px solid #00f2fe;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Подключение ключа
hf_token = st.secrets["HF_TOKEN"]

# 3. Интерфейс
st.title("🤖 ReviewAI Pro")
st.write("### Генератор отзывов и ответов для бизнеса 🇧🇾")
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📝 Настройка задачи")
    
    # ИСПРАВЛЕННЫЙ ВЫБОР: Теперь тут два четких варианта
    action = st.selectbox("Что нужно сделать?", 
                         ["Написать новый отзыв (от клиента)", 
                          "Ответить на отзыв (от владельца)"])
    
    style = st.select_slider("Стиль текста:", 
                            options=["Вежливый", "Дружелюбный", "Официальный", "Острый"])
    
    text_input = st.text_area("Суть ситуации (детали):", 
                             placeholder="Например: Клиент недоволен долгой доставкой пиццы.",
                             height=150)
    
    generate_btn = st.button("СГЕНЕРИРОВАТЬ ✨")

with col2:
    st.subheader("🚀 Готовый результат")
    if generate_btn:
        if text_input:
            with st.spinner('🧙‍♂️ ИИ формулирует идеальный текст...'):
                try:
                    client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)
                    
                    # Улучшенная инструкция для ИИ
                    if "от клиента" in action:
                        instruction = f"Напиши качественный отзыв о заведении от лица клиента. Тон: {style}. Детали: {text_input}."
                    else:
                        instruction = f"Напиши вежливый и профессиональный ответ владельца бизнеса на отзыв клиента. Тон: {style}. Суть отзыва: {text_input}."
                    
                    response = client.chat_completion(
                        messages=[{"role": "user", "content": instruction}],
                        max_tokens=500
                    )
                    
                    final_text = response.choices[0].message.content
                    
                    st.success("Готово!")
                    st.markdown(f'<div class="result-area">{final_text}</div>', unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Ошибка: {str(e)}")
        else:
            st.warning("⚠️ Введите детали в поле слева!")

st.markdown("---")
st.caption("© 2024 ReviewAI Startup | Витебск | Твой путь в IT начался!")
