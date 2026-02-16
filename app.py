import streamlit as st
from huggingface_hub import InferenceClient

# 1. Настройка внешнего вида
st.set_page_config(page_title="ReviewAI Pro", page_icon="⭐", layout="wide")

# Кастомный дизайн
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-image: linear-gradient(to right, #FF4B4B, #FF8F8F);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); opacity: 0.9; }
    .result-box {
        background-color: #1e222d;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #3e4452;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Боковая панель
with st.sidebar:
    st.title("⚙️ Настройки")
    st.markdown("Для работы нужен ключ от Hugging Face")
    hf_token = st.text_input("Вставь свой токен (hf_...):", type="password")
    st.markdown("[Как получить ключ?](https://huggingface.co)")
    st.divider()
    st.caption("Версия: 1.2 Global Edition")

# 3. Основной контент
st.title("✨ ReviewAI: Генератор текстов на базе ИИ")
st.write("Создавайте отзывы и ответы клиентам, которые повышают лояльность.")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📝 Параметры текста")
    option = st.selectbox("Что нужно сделать?", 
                         ["Написать отзыв о товаре/услуге", 
                          "Написать ответ на отзыв клиента"])
    
    tone = st.select_slider("Тон текста", 
                           options=["Вежливый", "Дружелюбный", "Официальный", "Юмористический"])
    
    details = st.text_area("Детали (что именно произошло?):", 
                          height=150, 
                          placeholder="Пример: Пицца Маргарита была очень вкусной, но курьер опоздал на 20 минут и не извинился.")

with col2:
    st.subheader("🚀 Готовый результат")
    if st.button("СГЕНЕРИРОВАТЬ ТЕКСТ"):
        if not hf_token:
            st.error("❌ Сначала вставь токен в панель слева!")
        elif not details:
            st.warning("⚠️ Опиши детали в левом поле!")
        else:
            with st.spinner('🧙‍♂️ Нейросеть подбирает лучшие слова...'):
                try:
                    # Инициализация клиента
                    client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)
                    
                    # Формируем запрос
                    prompt = f"Напиши {option} на русском языке. Тон: {tone}. Суть: {details}. Пиши как обычный человек, без лишнего пафоса."
                    
                    # Исправленный метод генерации (Chat Completion)
                    response = client.chat_completion(
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=500
                    )
                    
                    result = response.choices[0].message.content
                    
                    # Красивый вывод
                    st.success("Готово!")
                    st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Произошла техническая заминка: {str(e)}")

st.markdown("---")
st.caption("© 2024 ReviewAI Стартап. Теперь ты можешь зарабатывать на этом!")