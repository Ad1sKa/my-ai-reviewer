import streamlit as st
from huggingface_hub import InferenceClient

# 1. Загружаем секретный токен из настроек
hf_token = st.secrets["HF_TOKEN"]

st.set_page_config(page_title="ReviewAI Pro", page_icon="⭐")

st.title("🤖 ReviewAI: Твой помощник по отзывам")
st.write("Витебск, ИИ теперь на связи! Генерируй ответы за секунды.")

# 2. Интерфейс
option = st.selectbox("Что нужно сделать?", ["Написать отзыв", "Ответить клиенту"])
tone = st.select_slider("Тон текста", options=["Вежливый", "Дружелюбный", "Официальный"])
details = st.text_area("Детали (что произошло?):", placeholder="Например: Вкусная пицца, но везли долго.")

# 3. Работа с ИИ
if st.button("СГЕНЕРИРОВАТЬ ✨", use_container_width=True):
    if details:
        with st.spinner('Нейросеть думает...'):
            try:
                # Подключаемся к модели
                client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)
                prompt = f"Напиши {option} на русском языке. Тон: {tone}. Суть: {details}. Пиши коротко и по делу."
                
                response = client.chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                
                st.success("Готово!")
                st.write(response.choices.message.content)
                st.balloons()
            except Exception as e:
                st.error(f"Ошибка: {e}")
    else:
        st.warning("⚠️ Сначала напиши подробности!")
