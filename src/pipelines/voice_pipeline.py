from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


# Load encoder once (cached)
@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


# 🎤 Convert audio → embedding
def get_voice_embedding(audio_bytes):
    try:
        if audio_bytes is None:
            return None

        encoder = load_voice_encoder()

        # Load audio safely
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        if audio is None or len(audio) == 0:
            return None

        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()

    except Exception as e:
        st.error(f'Voice recog error: {e}')
        return None


# 🎯 Identify single speaker
def identify_speaker(new_embedding, candidates_dict, threshold=0.7):

    if new_embedding is None or not candidates_dict:
        return None, 0.0

    new_embedding = np.array(new_embedding)

    # Avoid division by zero
    if np.linalg.norm(new_embedding) == 0:
        return None, 0.0

    new_embedding = new_embedding / np.linalg.norm(new_embedding)

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:

            stored_embedding = np.array(stored_embedding)

            if np.linalg.norm(stored_embedding) == 0:
                continue

            stored_embedding = stored_embedding / np.linalg.norm(stored_embedding)

            # Cosine similarity
            similarity = np.dot(new_embedding, stored_embedding)

            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, float(best_score)

    return None, float(best_score)


# 🎙️ Process bulk audio (multiple speakers)
def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.7):

    try:
        if audio_bytes is None:
            return {}

        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        if audio is None or len(audio) == 0:
            return {}

        # Split into speech segments
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        for start, end in segments:

            # Ignore very short clips
            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio[start:end]

            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results

    except Exception as e:
        st.error(f'Bulk process error: {e}')
        return {}