import streamlit as st


def load_custom_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top right, rgba(37, 99, 235, 0.18), transparent 34%),
                radial-gradient(circle at top left, rgba(124, 58, 237, 0.14), transparent 28%),
                #070b14;
            color: #f8fafc;
        }

        .block-container {
            max-width: 1380px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3 {
            letter-spacing: -0.04em;
        }

        .hero {
            padding: 2.5rem 0 2.2rem 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.16);
            margin-bottom: 2rem;

            position: relative;
            overflow: hidden;
        }

        .hero-title {
            font-size: 3.7rem;
            line-height: 1.04;
            color: #f8fafc;
            margin-bottom: 1rem;
        }

        .hero-copy {
            max-width: 850px;
            color: #a8b3c7;
            font-size: 1.08rem;
            line-height: 1.75;
            margin-bottom: 1.35rem;
        }

        .gradient-word {
            background: linear-gradient(90deg, #60a5fa, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero::before {
            content: "";
            position: absolute;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(59,130,246,0.18), transparent 70%);
            top: -250px;
            right: -120px;
            pointer-events: none;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.45rem 0.9rem;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.82);
            border: 1px solid rgba(96, 165, 250, 0.35);
            color: #93c5fd;
            font-size: 0.82rem;
            font-weight: 700;
            margin-bottom: 1.25rem;
        }

        .hero h1 {
            font-size: 3.7rem;
            line-height: 1.04;
            max-width: 900px;
            color: #f8fafc;
            margin-bottom: 1rem;
        }

        .hero .gradient-word {
            background: linear-gradient(90deg, #60a5fa, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            max-width: 850px;
            color: #a8b3c7;
            font-size: 1.08rem;
            line-height: 1.75;
            margin-bottom: 1.35rem;
        }

        .chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            margin-top: 1.2rem;
        }

        .chip {
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(148, 163, 184, 0.18);
            color: #cbd5e1;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .section-title {
            font-size: 1.55rem;
            font-weight: 800;
            margin: 1.6rem 0 1rem 0;
            color: #f8fafc;
        }

        div[role="radiogroup"] {
            gap: 1rem;
        }

        div[role="radiogroup"] > label {
            min-width: 360px;
            padding: 1rem 1.25rem;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.15);
            box-shadow: 0 18px 45px rgba(0, 0, 0, 0.18);
            transition: all 0.2s ease;
        }

        div[role="radiogroup"] > label:hover {
            border-color: rgba(96, 165, 250, 0.55);
            transform: translateY(-1px);
        }

        div[role="radiogroup"] input {
            display: none;
        }

        div[role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.95), rgba(124, 58, 237, 0.92));
            border-color: rgba(147, 197, 253, 0.65);
        }

        .glass-card {
            padding: 1.55rem;
            border-radius: 22px;
            background: rgba(15, 23, 42, 0.58);
            backdrop-filter: blur(18px);
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.22);
            margin-bottom: 1.1rem;
        }

        .card-heading {
            font-size: 1.35rem;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 0.25rem;
        }

        .card-subtitle {
            color: #94a3b8;
            font-size: 0.95rem;
            margin-bottom: 1.1rem;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            width: 100%;
            min-height: 3rem;
            border-radius: 14px;
            border: 1px solid rgba(147, 197, 253, 0.25);
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            color: white;
            font-weight: 700;
            box-shadow: 0 14px 32px rgba(37, 99, 235, 0.22);
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            border-color: rgba(255, 255, 255, 0.35);
        }

        div[data-testid="stFileUploader"] {
            border: 1px dashed rgba(148, 163, 184, 0.28);
            border-radius: 18px;
            padding: 1rem;
            background: rgba(2, 6, 23, 0.32);
        }

        .stTextInput input {
            border-radius: 14px;
            background: rgba(15, 23, 42, 0.9);
        }

        div[data-testid="stExpander"] {
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            background: rgba(15, 23, 42, 0.52);
        }

        hr {
            border-color: rgba(148, 163, 184, 0.14);
        }

        .chat-user {
            margin-top: 1rem;
            margin-bottom: 0.75rem;
            padding: 1rem 1.2rem;
            border-radius: 18px;
            background: rgba(37, 99, 235, 0.14);
            border: 1px solid rgba(96, 165, 250, 0.22);
            color: #e2e8f0;
        }

        .chat-bot {
            margin-bottom: 1.5rem;
            padding: 1rem 1.2rem;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.14);
            color: #f8fafc;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )