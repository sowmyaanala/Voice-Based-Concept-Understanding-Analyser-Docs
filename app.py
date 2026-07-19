import streamlit as st
import librosa
import matplotlib.pyplot as plt
import tempfile
from pdf_report import create_pdf
from speech_to_text import speech_to_text

from semantic_eval import semantic_similarity
from audio_utils import analyze_audio
from scoring_engine import evaluate_understanding

st.set_page_config(page_title="Voice-Based Concept Understanding Analyser")

st.title("🎤 Voice-Based Concept Understanding Analyser")
st.write("Automated evaluation of spoken conceptual explanations using AI.")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "Upload Student Audio (WAV)",
        type=["wav", "mp3"]
    )

with col2:
    st.subheader("Concept Reference")
    st.write(
        "Machine Learning is a subset of Artificial Intelligence "
        "that enables systems to learn from data."
    )

if uploaded_file:

    st.success("Audio uploaded successfully!")

    st.audio(uploaded_file)

    # Save uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_file.close()

    audio_path = temp_file.name

    # Load audio
    y, sr = librosa.load(audio_path)

    # Draw waveform
    fig, ax = plt.subplots(figsize=(10,3))
    ax.plot(y)
    ax.set_title("Audio Waveform")
    st.subheader("Audio Visualization")
    st.pyplot(fig)

# Save waveform image
    plt.savefig("waveform.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    if st.button("Analyze Concept Understanding"):
        st.success("Analysis Completed")
        import os
        st.write("Saved file:", audio_path)
        st.write("File size:", os.path.getsize(audio_path), "bytes")

    transcript = speech_to_text(audio_path)

    reference = """
    Machine Learning is a subset of Artificial Intelligence
    that enables systems to learn from data.
    """

    similarity = semantic_similarity(transcript, reference)

    audio = analyze_audio(audio_path)

    fillers = [
        "um",
        "uh",
        "like",
        "actually",
        "basically",
        "you know",
        "so"
    ]

    words = transcript.lower().split()

    filler_count = sum(words.count(f) for f in fillers)

    filler_ratio = filler_count / max(len(words), 1)

    score, level, color = evaluate_understanding(
        similarity,
        filler_ratio,
        audio
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Transcribed Explanation")
        st.write(transcript)

    with right:
        st.subheader("Final Evaluation")
        st.metric("Score", f"{score}/100")
        st.markdown(
            f"<h3 style='color:{color}'>{level}</h3>",
            unsafe_allow_html=True
        )

    st.subheader("Evaluation Summary")

    st.write(f"Semantic Similarity : {similarity:.2f}")
    st.write(f"Filler Word Ratio : {filler_ratio:.2f}")
    st.write(f"Pause Ratio : {audio['pause_ratio']:.2f}")
    st.write(f"Confidence : {audio['rms_energy']:.4f}")
    st.write(f"Final Score : {score}/100")
    st.write(f"Understanding Level : {level}")

    create_pdf(
        transcript,
        similarity,
        filler_ratio,
        audio["pause_ratio"],
        audio["rms_energy"],
        score,
        level
    )

    with open("report.pdf", "rb") as pdf:
        st.download_button(
            "📄 Download PDF Report",
            pdf,
            "Evaluation_Report.pdf"
        )