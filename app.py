import streamlit as st
from huggingface_hub import InferenceClient

# 1. Настройка страницы
st.set_page_config(page_title="ReviewAI Premium", page_icon="💎", layout="wide")

# Подключение ключа из Secrets
try:
    hf_token = st.secrets["HF_TOKEN"]
except Exception:
    st.error("Критическая ошибка: Токен HF_TOKEN не найден в Secrets!")
    st.stop()

# 2. Объединенные словари (7 языков + динамические подсказки)
languages = {
    "Русский": {
        "title": "ReviewAI Pro", "subtitle": "Профессиональная генерация отзывов",
        "task": "Тип операции", "style": "Тональность", "details": "Детали ситуации",
        "btn": "СОЗДАТЬ ШЕДЕВР ✨", "opt1": "Написать отзыв (Клиент)", "opt2": "Ответить на отзыв (Владелец)",
        "ph1": "Например: Пицца была холодной, а курьер опоздал на час.",
        "ph2": "Например: Клиент пожаловался, что пицца была холодной. Нужно извиниться и предложить скидку."
    },
    "English": {
        "title": "ReviewAI Pro", "subtitle": "Professional Review Generation",
        "task": "Task Type", "style": "Tone", "details": "Details",
        "btn": "GENERATE ✨", "opt1": "Write Review (Customer)", "opt2": "Reply to Review (Owner)",
        "ph1": "Example: The pizza was cold and the delivery was late.",
        "ph2": "Example: Customer complained about cold pizza. Apologize and offer a discount."
    },
    "Беларуская": {
        "title": "ReviewAI Pro", "subtitle": "Прафесійная генерацыя водгукаў",
        "task": "Тып аперацыі", "style": "Тонасць", "details": "Дэталі сітуацыі",
        "btn": "ЗГЕНЕРАВАЦЬ ✨", "opt1": "Напісаць водгук (Кліент)", "opt2": "Адказаць на водгук (Уладальнік)",
        "ph1": "Напрыклад: Піца была халоднай, а кур'ер спазніўся.",
        "ph2": "Напрыклад: Кліент паскардзіўся, што піца была халоднай. Трэба папрасіць прабачэння."
    },
    "Polski": {"title": "ReviewAI Pro", "subtitle": "Generator Opinii Pro", "task": "Zadanie", "style": "Styl", "details": "Szczegóły", "btn": "GENERUJ ✨", "opt1": "Napisz opinię", "opt2": "Odpowiedz", "ph1": "Np. Pizza była zimna.", "ph2": "Np. Klient napisał, że pizza była zimna."},
    "Deutsch": {"title": "ReviewAI Pro", "subtitle": "Bewertungs-Generator", "task": "Aufgabe", "style": "Stil", "details": "Details", "btn": "ERSTELLEN ✨", "opt1": "Bewertung schreiben", "opt2": "Antworten", "ph1": "Z.B. Die Pizza war kalt.", "ph2": "Z.B. Kunde sagte, die Pizza war kalt."},
    "Français": {"title": "ReviewAI Pro", "subtitle": "Générateur d'avis", "task": "Tâche", "style": "Style", "details": "Détails", "btn": "GÉNÉRER ✨", "opt1": "Écrire un avis", "opt2": "Répondre", "ph1": "Ex: La pizza était froide.", "ph2": "Ex: Le client a dit que la pizza était froide."},
    "Español": {"title": "ReviewAI Pro", "subtitle": "Generador Pro", "task": "Tarea", "style": "Estilo", "details": "Detalles", "btn": "GENERAR ✨", "opt1": "Escribir reseña", "opt2": "Responder", "ph1": "Ej: La pizza estaba fría.", "ph2": "Ej: El cliente dijo que la pizza estaba fría."}
}

# 3. ПРЕМИУМ ДИЗАЙН (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    * { font-family: 'Outfit', sans-serif; }
    .stApp { background: radial-gradient(circle at top right, #1e1b4b, #0f172a); }
    
    /* Стеклянные карточки */
    [data-testid="stVerticalBlock"] > div:has(div.stTextArea), .result-container {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px !important;
        padding: 40px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.4);
    }

    /* Кнопка с неоновым свечением */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #ec4899) !important;
        border: none !important;
        border-radius: 16px !important;
        color: white !important;
        font-weight: 800 !important;
        height: 3.8em !important;
        letter-spacing: 1px;
        transition: all 0.4s ease !important;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 35px rgba(236, 72, 153, 0.5);
        color: white !important;
    }

    /* Блок результата */
    .result-area {
        background: rgba(0, 0, 0, 0.2);
        border-left: 4px solid #ec4899;
        padding: 25px;
        border-radius: 12px;
        color: #f1f5f9;
        font-size: 1.15rem;
        line-height: 1.6;
    }
    
    h1 { 
        background: linear-gradient(to right, #fff, #94a3b8); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: 3.5rem !important; 
        font-weight: 800 !important;
    }
    h3 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Сайдбар
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🌐 Settings</h2>", unsafe_allow_html=True)
    lang_choice = st.selectbox("Choose Language:", list(languages.keys()))
    t = languages[lang_choice]
    st.divider()
    st.info("💎 Premium Edition v3.5")

# 5. Основной контент
st.title(t["title"])
st.markdown(f"<p style='font-size: 1.3rem; opacity: 0.8; color: #94a3b8;'>{t['subtitle']}</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown(f"### ⚙️ {t['task']}")
    action = st.selectbox("Action", [t["opt1"], t["opt2"]], label_visibility="collapsed")
    
    # Динамический плейсхолдер в зависимости от выбора действия
    current_placeholder = t["ph1"] if action == t["opt1"] else t["ph2"]
    
    st.markdown(f"**{t['style']}**")
    style = st.select_slider("Style", options=["Вежливый", "Дружелюбный", "Официальный", "Дерзкий"], label_visibility="collapsed")
    
    st.markdown(f"**{t['details']}**")
    text_input = st.text_area("Input", placeholder=current_placeholder, height=200, label_visibility="collapsed")
    
    generate_btn = st.button(t["btn"])

with col2:
    st.markdown("### ✨ Result")
    if generate_btn:
        if text_input:
            with st.spinner('🚀 AI создает идеальный текст...'):
                try:
                    client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)
                    
                    # Промпт с жесткими правилами
                    system_msg = (
                        f"You are a professional copywriting AI. TASK: {action}. LANGUAGE: {lang_choice}. "
                        f"TONE: {style}. CONTEXT: {text_input}. "
                        f"STRICT RULES: 1. Use ONLY the {lang_choice} language. 2. NO profanity/swear words. "
                        "3. Write naturally and human-like. 4. Output ONLY the resulting text, no intros."
                    )
                    
                    response = client.chat_completion(
                        messages=[{"role": "user", "content": system_msg}],
                        max_tokens=600, 
                        temperature=0.8
                    )
                    final_text = response.choices[0].message.content
                    
                    st.markdown(f'<div class="result-area">{final_text}</div>', unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.error("Ошибка соединения с AI. Проверьте токен или лимиты API.")
        else:
            st.warning("⚠️ Пожалуйста, опишите ситуацию!")
