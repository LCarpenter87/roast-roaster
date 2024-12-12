import streamlit as st

import base64
import google.generativeai as genai

st.title("🎈 Lets roast some roasts!")
st.write(
    "Share your image of a roast dinner, and I'll let you know how awful it is!"
)

genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
def upload_to_gemini(path, mime_type=None):
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file


textsi_1 = """You are a sassy critical professional Roaster! 
              You will be given roast dinner photos, and you will \"roast that dinner\" 
            you with funny and witty retorts commenting on the quality of the roast dinner!"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 2,
    "top_p": 0.95,
}

model = genai.GenerativeModel(
  model_name='gemini-2.0-flash-exp',
  generation_config=generation_config,
  system_instruction=textsi_1
)

my_file = st.file_uploader("Choose your roast dinner!", type=['jpg'], accept_multiple_files=False )

if my_file is not None:
  col1, col2 = st.columns(2)
  gemini_file = upload_to_gemini(my_file, 'image/jpeg')
  response = model.generate_content([gemini_file, "Roast this Roast!"])
  with col2:
    st.write(response.text)
  with col1:
    st.image(my_file)

