"""
==============================================================
  TESbot  —  בונה צ'אטבוט לעסקים  (גרסת Python / Streamlit)
==============================================================
"""

import streamlit as st

# ---------- הגדרות עמוד ----------
st.set_page_config(page_title="TESbot — בונה צ'אטבוט", page_icon="💬", layout="wide")

# ---------- עיצוב (CSS) ----------
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@500;700;800&family=Assistant:wght@400;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Assistant', sans-serif; direction: rtl; }
  .main { background: #F7F6F2; }
  h1, h2, h3 { font-family: 'Rubik', sans-serif; color: #1A2238; }
  .hero-title { font-size: 40px; font-weight: 800; line-height: 1.15; margin-bottom: 6px; }
  .hero-title .hl { color: #FF6B5C; }
  .hero-sub { font-size: 18px; color: #4A5169; margin-bottom: 8px; }
  .badge { display:inline-block; background:#E6F7F1; color:#0c8a63; font-weight:700;
           font-size:13px; padding:5px 13px; border-radius:999px; margin-bottom:14px; }
  .stButton button { background:#1A2238; color:#fff; border:none; border-radius:10px;
                     font-family:'Rubik'; font-weight:600; }
  .stButton button:hover { background:#0f1626; color:#fff; }
  .panel-title { font-family:'Rubik'; font-weight:700; font-size:20px; color:#1A2238;
                 margin: 4px 0 12px; }
  div[data-testid="stChatMessage"] { border-radius: 14px; }
</style>
""", unsafe_allow_html=True)

# ---------- ערכי ברירת מחדל (מספרה לדוגמה) ----------
DEFAULT_BIZ = {
    "name": "מספרת רוני",
    "phone": "050-1234567",
    "hours": "א׳–ה׳ 09:00–19:00, ו׳ 09:00–14:00",
    "address": "הרצל 25, תל אביב",
}
DEFAULT_QA = [
    {"keys": "שעות, פתוח, סגור, מתי", "ans": "שעות הפעילות שלנו: {hours} 🕐"},
    {"keys": "מחיר, כמה עולה, תספורת, מחירון", "ans": "תספורת גבר 80₪ · תספורת אישה 120₪ · צבע 250₪ 💇"},
    {"keys": "כתובת, איפה, מיקום, להגיע", "ans": "אנחנו ב-{address} 📍"},
    {"keys": "תור, לקבוע, להזמין, פגישה", "ans": "לקביעת תור חייגו {phone} ונשמח לארח אתכם 📅"},
]

# ---------- אתחול הזיכרון ----------
if "qa" not in st.session_state:
    st.session_state.qa = [dict(x) for x in DEFAULT_QA]
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- כותרת עליונה ----------
st.markdown('<div class="badge">● בלי קוד · מוכן בכמה דקות</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">צ\'אטבוט לעסק שלך, <span class="hl">בלי לכתוב קוד</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">ממלאים פרטים ושאלות מימין — ומדברים עם הבוט החי משמאל.</div>', unsafe_allow_html=True)
st.divider()

# ---------- שני טורים ----------
col_form, col_chat = st.columns([1, 1], gap="large")

# =========== טור הטופס ===========
with col_form:
    st.markdown('<div class="panel-title">🏪 פרטי העסק</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    name = c1.text_input("שם העסק", DEFAULT_BIZ["name"])
    phone = c2.text_input("טלפון", DEFAULT_BIZ["phone"])
    hours = st.text_input("שעות פעילות", DEFAULT_BIZ["hours"])
    address = st.text_input("כתובת", DEFAULT_BIZ["address"])

    st.markdown('<div class="panel-title">❓ השאלות שהבוט יענה עליהן</div>', unsafe_allow_html=True)
    st.caption("בכל שאלה: מילים שהלקוח עשוי לכתוב (מופרדות בפסיק), והתשובה שהבוט ייתן. "
               "אפשר להשתמש ב-{hours} {address} {phone} כדי לשלב פרטים.")

    remove_index = None
    for i, item in enumerate(st.session_state.qa):
        with st.container(border=True):
            item["keys"] = st.text_input("מילים שהלקוח עשוי לכתוב", item["keys"], key=f"keys_{i}")
            item["ans"] = st.text_area("התשובה של הבוט", item["ans"], key=f"ans_{i}", height=70)
            if st.button("🗑️ הסר שאלה", key=f"rm_{i}"):
                remove_index = i
    if remove_index is not None:
        st.session_state.qa.pop(remove_index)
        st.rerun()

    if st.button("➕ הוספת שאלה"):
        st.session_state.qa.append({"keys": "", "ans": ""})
        st.rerun()

# ---------- המוח של הבוט ----------
def fill(text):
    return (text.replace("{hours}", hours).replace("{address}", address)
                .replace("{phone}", phone).replace("{name}", name))

def bot_reply(message):
    m = message.strip().lower()
    for item in st.session_state.qa:
        words = [w.strip().lower() for w in item["keys"].split(",") if w.strip()]
        for w in words:
            if w and w in m:
                return fill(item["ans"])
    return ("לא בטוח/ה שהבנתי 🤔 אפשר לשאול על: שעות, מחירים, כתובת, קביעת תור.\n"
            f"או להתקשר: {phone}")

# =========== טור הצ'אט ===========
with col_chat:
    st.markdown(f'<div class="panel-title">💬 הבוט החי של {name}</div>', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.session_state.messages.append(
            {"role": "assistant", "content": f"שלום! 👋 הגעתם ל{name}. איך אפשר לעזור?"}
        )

    chat_box = st.container(height=420)
    with chat_box:
        for msg in st.session_state.messages:
            avatar = "💬" if msg["role"] == "assistant" else "🧑"
            with st.chat_message(msg["role"], avatar=avatar):
                st.write(msg["content"])

    with st.form("chat_form", clear_on_submit=True):
        fc1, fc2 = st.columns([4, 1])
        user_text = fc1.text_input("הודעה", placeholder="כתבו הודעה לבוט...",
                                   label_visibility="collapsed")
        sent = fc2.form_submit_button("שליחה ➤")
    if sent and user_text.strip():
        st.session_state.messages.append({"role": "user", "content": user_text})
        st.session_state.messages.append({"role": "assistant", "content": bot_reply(user_text)})
        st.rerun()

    if st.button("🔄 התחל שיחה מחדש"):
        st.session_state.messages = []
        st.rerun()