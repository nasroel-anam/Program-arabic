# ✅ Langkah 1: Install pustaka yang diperlukan
!pip install streamlit pyngrok camel-tools -q


# ✅ Langkah 2: Simpan isi aplikasi ke file Streamlit (app.py)
%%writefile app.py
import streamlit as st
from camel_tools.utils.charmap import CharMapper
from camel_tools.utils.normalize import (
    normalize_unicode, normalize_alef_ar, normalize_alef_maksura_ar,
    normalize_teh_marbuta_ar
)
from camel_tools.utils.dediac import dediac_ar
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.sentiment import SentimentAnalyzer

st.title("Aplikasi Analisis Teks Arab - CAMeL Tools")

menu = st.sidebar.selectbox("Pilih Fitur", [
    "Buckwalter Mapping", "Normalisasi",
    "Buang Harakat", "Tokenisasi",
    "Sentimen Analisis"
])

sentence = st.text_area("Masukkan Kalimat Arab", "هَلْ ذَهَبْتَ إِلَى المَكْتَبَةِ؟")

if menu == "Buckwalter Mapping":
    ar2bw = CharMapper.builtin_mapper('ar2bw')
    sent_bw = ar2bw(sentence)
    st.write("Buckwalter Mapping:")
    st.code(sent_bw)

elif menu == "Normalisasi":
    step1 = normalize_alef_ar(sentence)
    step2 = normalize_alef_maksura_ar(step1)
    step3 = normalize_teh_marbuta_ar(step2)
    step4 = normalize_unicode(step3)
    st.write("Setelah Normalisasi:")
    st.code(step4)

elif menu == "Buang Harakat":
    sent_dediac = dediac_ar(sentence)
    st.write("Tanpa Harakat:")
    st.code(sent_dediac)

elif menu == "Tokenisasi":
    tokens = simple_word_tokenize(sentence)
    st.write("Token:")
    st.write(tokens)

elif menu == "Sentimen Analisis":
    sa = SentimentAnalyzer.pretrained()
    result = sa.predict([sentence])[0]
    st.write("Prediksi Sentimen:")
    st.success(result)


# ✅ Langkah 3: Masukkan Authtoken ngrok Anda
# Ganti dengan token Anda sendiri jika ini file dibagikan ke publik
!ngrok config add-authtoken "2zaEALdIikHP3MjTSLfE8IPfo1z_6avudhCZ4oGc2pGDZZZSv"


# ✅ Langkah 4: Jalankan aplikasi dan buat link web
from pyngrok import ngrok

# Jalankan streamlit di background
!streamlit run app.py &>/content/log.txt &

# Buat link publik
public_url = ngrok.connect(addr="8501")
print("🔗 Akses aplikasi web Anda di link berikut:")
print(public_url)
