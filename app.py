import streamlit as st
from huggingface_hub import InferenceClient

# 1. Настройка страницы
st.set_page_config(page_title="ReviewAI Global", page_icon="🌍", layout="wide")

# Подключение ключа из Secrets
hf_token = st.secrets["HF_TOKEN"]

# 2. Словари для перевода интерфейса
languages = {
    "Русский": {"title": "🤖 ReviewAI Pro", "subtitle": "Генератор отзывов и ответов", "task": "Настройка задачи", "style": "Стиль текста", "details": "Суть ситуации", "btn": "СГЕНЕРИРОВАТЬ ✨", "opt1": "Написать новый отзыв (от клиента)", "opt2": "Ответить на отзыв (от владельца)"},
    "English": {"title": "🤖 ReviewAI Pro", "subtitle": "Review & Response Generator", "task": "Task Setting", "style": "Text Style", "details": "Details", "btn": "GENERATE ✨", "opt1": "Write a new review (as customer)", "opt2": "Reply to review (as owner)"},
    "Беларуская": {"title": "🤖 ReviewAI Pro", "subtitle": "Генератар водгукаў і адказаў", "task": "Налада задачы", "style": "Стыль тэксту", "details": "Сутнасць сітуацыі", "btn": "ЗГЕНЕРАВАЦЬ ✨", "opt1": "Напісаць новы водгук (ад кліента)", "opt2": "Адказаць на водгук (ад уладальніка)"},
    "Polski": {"title": "🤖 ReviewAI Pro", "subtitle": "Generator opinii i odpowiedzi", "task": "Ustawienie zadania", "style": "Styl tekstu", "details": "Szczegóły", "btn": "GENERUJ ✨", "opt1": "Napisz nową opinię (klient)", "opt2": "Odpowiedz na opinię (właściciel)"},
    "Deutsch": {"title": "🤖 ReviewAI Pro", "subtitle": "Bewertungs-Generator", "task": "Aufgabe", "style": "Stil", "details": "Details", "btn": "GENERIEREN ✨", "opt1": "Neue Bewertung schreiben (Kunde)", "opt2": "Auf Bewertung antworten (Besitzer)"},
    "Français": {"title": "🤖 ReviewAI Pro", "subtitle": "Générateur d'avis", "task": "Tâche", "style": "Style", "details": "Détails", "btn": "GÉNÉRER ✨", "opt1": "Écrire un avis (client)", "opt2": "Répondre à un avis (propriétaire)"},
    "Español": {"title": "🤖 ReviewAI Pro", "subtitle": "Generador de reseñas", "task": "Tarea", "style": "Style", "details": "Detalles", "btn": "GENERAR ✨", "opt1": "Escribir reseña (cliente)", "opt2": "Responder a reseña (dueño)"}
}

# 3. Кастомный CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%; border-radius: 15px; height: 4em;
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white; font-weight: bold; border: none;
    }
    .result-area { background-color: #1e222d; padding: 25px; border-radius: 20px; border-left: 5px solid #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

# 4. Выбор языка
with st.sidebar:
    st.title("🌐 Language / Язык")
    lang_choice = st.selectbox("Select Language:", list(languages.keys()))
    t = languages[lang_choice]
    st.divider()
    st.caption("ReviewAI v2.0 Global")

# 5. Интерфейс
st.title(t["title"])
st.write(f"### {t['subtitle']} 🇧🇾")
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader(f"📝 {t['task']}")
    action = st.selectbox(t["task"], [t["opt1"], t["opt2"]])
    
    # Динамический плейсхолдер
    if action == t["opt1"]:
        placeholder_text = "Например: Пицца была холодной" if lang_choice in ["Русский", "Беларуская"] else "Example: The pizza was cold"
    else:
        placeholder_text = "Например: Клиент написал, что пицца была холодной" if lang_choice in ["Русский", "Беларуская"] else "Example: Customer said the pizza was cold"
    
    style = st.select_slider(t["style"], options=["Вежливый", "Дружелюбный", "Официальный", "Дерзкий"])
    text_input = st.text_area(t["details"], placeholder=placeholder_text, height=150)
    generate_btn = st.button(t["btn"])

with col2:
    st.subheader("🚀 Result")
    if generate_btn:
        if text_input:
            with st.spinner('🔮 AI is working...'):
                try:
                    client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)
                    
                    # Промпт подстраивается под выбранный язык
                    prompt = f"Write a {action} in {lang_choice} language. Tone: {style}. Details: {text_input}. Natural human style."
                    
                    response = client.chat_completion(messages=[{"role": "user", "content": prompt}], max_tokens=500)
                    final_text = response.choices[0].message.content
                    
                    st.success("Success!")
                    st.markdown(f'<div class="result-area">{final_text}</div>', unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("⚠️ Enter details!")
