import streamlit as st
from huggingface_hub import InferenceClient

# 1. Настройка страницы и стилей
st.set_page_config(page_title="ReviewAI | Vitebsk Edition", page_icon="🚀", layout="wide")

# Кастомный CSS для крутого дизайна
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 4em;
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4);
    }
    .result-area {
        background-color: #1e222d;
        padding: 25px;
        border-radius: 20px;
        border-left: 5px solid #00f2fe;
        font-size: 18px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Подключение к ИИ через секреты
try:
    hf_token = st.secrets["HF_TOKEN"]
except:
    st.error("⚠️ Ошибка: Токен HF_TOKEN не найден в настройках Secrets!")
    st.stop()

# 3. Интерфейс
st.title("🤖 ReviewAI Pro")
st.write("### Твой персональный ИИ-копирайтер из Витебска 🇧🇾")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Что нужно сделать?")
    action = st.selectbox("Выберите задачу:", 
                         ["Написать новый отзыв", "Ответить на отзыв клиента"])
    
    style = st.select_slider("Стиль текста:", 
                            options=["Вежливый", "Дружелюбный", "Официальный", "Дерзкий"])
    
    text_input = st.text_area("О чем пишем? (детали):", 
                             placeholder="Например: Пицца огонь, но курьер опоздал на полчаса и забыл колу.",
                             height=200)
    
    generate_btn = st.button("СГЕНЕРИРОВАТЬ МАГИЮ ✨")

with col2:
    st.subheader("🚀 Результат")
    if generate_btn:
        if text_input:
            with st.spinner('🔮 Нейросеть подбирает лучшие слова...'):
                try:
                    # Инициализация клиента
                    client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)
                    
                    # Промпт для ИИ
                    prompt = f"Act as a professional copywriter. Write a {action} in Russian language. Tone: {style}. Details: {text_input}. Write naturally like a human."
                    
                    # Запрос к нейросети (исправленный формат)
                    response = client.chat_completion(
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=500
                    )
                    
                    # Извлекаем текст ответа правильно
                    final_text = response.choices[0].message.content
                    
                    # Вывод результата
                    st.success("Готово!")
                    st.markdown(f'<div class="result-area">{final_text}</div>', unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Произошла ошибка: {str(e)}")
        else:
            st.warning("⚠️ Пожалуйста, введите детали в поле слева!")

# Подвал
st.markdown("---")
st.caption("© 2024 ReviewAI Startup | Разработано в 13 лет. Будущее уже здесь.")
