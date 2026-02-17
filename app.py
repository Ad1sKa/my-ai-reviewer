import streamlit as st
from huggingface_hub import InferenceClient

# 1. Настройка страницы (профессиональный заголовок)
st.set_page_config(page_title="ReviewAI Pro", page_icon="✨", layout="wide")

# Подключение ключа
hf_token = st.secrets["HF_TOKEN"]

# 2. Обновленные словари (только нужные языки)
languages = {
    "Русский": {"title": "ReviewAI Pro", "subtitle": "Генератор отзывов нового поколения", "task": "Настройка", "style": "Стиль", "details": "Суть ситуации", "btn": "СГЕНЕРИРОВАТЬ ✨", "opt1": "Написать отзыв (клиент)", "opt2": "Ответить на отзыв (владелец)"},
    "English": {"title": "ReviewAI Pro", "subtitle": "Next-gen review generator", "task": "Settings", "style": "Style", "details": "Details", "btn": "GENERATE ✨", "opt1": "Write review (customer)", "opt2": "Reply to review (owner)"},
    "Беларуская": {"title": "ReviewAI Pro", "subtitle": "Генератар водгукаў новага пакалення", "task": "Налады", "style": "Стыль", "details": "Сутнасць сітуацыі", "btn": "ЗГЕНЕРАВАЦЬ ✨", "opt1": "Напісаць водгук (кліент)", "opt2": "Адказаць на водгук (уладальнік)"},
    "Polski": {"title": "ReviewAI Pro", "subtitle": "Generator opinii nowej generacji", "task": "Ustawienia", "style": "Styl", "details": "Szczegóły", "btn": "GENERUJ ✨", "opt1": "Napisz opinię (klient)", "opt2": "Odpowiedz na opinię (właściciel)"},
    "Deutsch": {"title": "ReviewAI Pro", "subtitle": "Bewertungs-Generator Pro", "task": "Einstellungen", "style": "Stil", "details": "Details", "btn": "GENERIEREN ✨", "opt1": "Bewertung schreiben", "opt2": "Auf Bewertung antworten"},
    "Français": {"title": "ReviewAI Pro", "subtitle": "Générateur d'avis Pro", "task": "Paramètres", "style": "Style", "details": "Détails", "btn": "GÉNÉRER ✨", "opt1": "Écrire un avis", "opt2": "Répondre à l'avis"},
    "Español": {"title": "ReviewAI Pro", "subtitle": "Generador de reseñas Pro", "task": "Tarea", "style": "Estilo", "details": "Detalles", "btn": "GENERAR ✨", "opt1": "Escribir reseña", "opt2": "Responder reseña"}
}

# 3. ПРОФЕССИОНАЛЬНЫЙ ДИЗАЙН (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .stApp { background: #0f111a; }
    
    /* Карточки блоков */
    div[data-testid="stVerticalBlock"] > div:has(div.stTextArea) {
        background: rgba(255, 255, 255, 0.03);
        padding: 30px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    /* Красивая кнопка */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: 700;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
    }

    /* Поле результата */
    .result-area {
        background: rgba(99, 102, 241, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #e2e8f0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Выбор языка в боковой панели
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    lang_choice = st.selectbox("Language / Язык:", list(languages.keys()))
    t = languages[lang_choice]
    st.divider()
    st.caption("ReviewAI v3.0 Premium")

# 5. Основной интерфейс
st.title(t["title"])
st.markdown(f"<p style='font-size: 1.2rem; color: #94a3b8;'>{t['subtitle']}</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")with col1:
    st.subheader(f"📝 {t['task']}")
    action = st.selectbox("Тип текста", [t["opt1"], t["opt2"]], label_visibility="collapsed")
    
    style = st.select_slider(t["style"], options=["Вежливый", "Дружелюбный", "Официальный", "Дерзкий"])
    
    text_input = st.text_area(t["details"], placeholder="Введите детали здесь...", height=180)
    generate_btn = st.button(t["btn"])

with col2:
    st.subheader("🚀 Result")
    if generate_btn:
        if text_input:
            with st.spinner('⚡ Анализируем и пишем...'):
                try:
                    client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)
                    
                    # УСИЛЕННЫЙ ПРОМПТ (Запрет матов и только выбранный язык)
                    system_instruction = (
                        f"You are a professional copywriter. Write a text in {lang_choice} language ONLY. "
                        "STRICT RULES: 1. No swear words or profanity. 2. No English words in the final text. "
                        f"3. Style: {style}. 4. Task: {action} based on these details: {text_input}. "
                        "Write directly the text of the review or response, no introductions."
                    )
                    
                    response = client.chat_completion(
                        messages=[{"role": "user", "content": system_instruction}], 
                        max_tokens=600,
                        temperature=0.7
                    )
                    final_text = response.choices[0].message.content
                    
                    st.markdown(f'<div class="result-area">{final_text}</div>', unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.error(f"Упс! Что-то пошло не так. Проверьте токен или интернет.")
        else:
            st.warning("⚠️ Пожалуйста, напишите детали ситуации!")
