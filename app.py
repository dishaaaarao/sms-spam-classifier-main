import streamlit as st
import pickle
import string
import base64
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Initialize PorterStemmer
ps = PorterStemmer()

# Function to preprocess text
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Load trained model and vectorizer
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Function to get base64 of the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Custom CSS for background image and styling
custom_css = f"""
<style>
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        transition: background-color 1s linear;
    }}
    .container {{
        padding: 20px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin: 0 auto;
        margin-top: 50px;
        text-align: center;
    }}
    .header {{
        color: #333;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }}
    .section {{
        margin-top: 20px;
    }}
    .developer {{
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }}
    .developer img {{
        border-radius: 50%;
        margin-right: 20px;
    }}
    .developer-info {{
        flex: 1;
    }}
    .developer-name {{
        font-size: 1.5em;
        font-weight: bold;
    }}
    .result {{
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        color: white;
        font-size: 3em;
        z-index: 9999;
        text-align: center;
    }}
    .spam {{
        background-color: rgba(220, 53, 69, 0.8); /* Red */
        animation: flash-red 1s infinite;
    }}
    .not-spam {{
        background-color: rgba(40, 167, 69, 0.8); /* Green */
        animation: flash-green 1s infinite;
    }}
    @keyframes flash-red {{
        0%, 100% {{ background-color: rgba(220, 53, 69, 0.8); }}
        50% {{ background-color: rgba(220, 53, 69, 0.4); }}
    }}
    @keyframes flash-green {{
        0%, 100% {{ background-color: rgba(40, 167, 69, 0.8); }}
        50% {{ background-color: rgba(40, 167, 69, 0.4); }}
    }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 10px 0;
    }}
</style>
"""

# Main application
def main():
    # Inject custom CSS into Streamlit
    st.markdown(custom_css, unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home", "Classifier", "About Us"])

    # Display different content based on selected page
    if page == "Home":
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.title("Vartha Sodhana")
        st.markdown('<h1 class="header">Welcome to Vartha Sodhana</h1>', unsafe_allow_html=True)
        st.markdown('<p class="section">Your trusted SMS classifier. Use our machine learning model to make informed decisions about your SMS.</p>', unsafe_allow_html=True)
        st.header("Why Choose Vartha Sodhana?")
        st.markdown("- Simple and intuitive interface")
        st.markdown("- Powerful SMS classification using machine learning")
        st.markdown("- Fast and accurate predictions")
        st.markdown("- Built with Streamlit and Python")
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Classifier":
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.markdown("---")
        st.header("SMS Classifier")
        input_sms = st.text_area("Enter the message")
        if st.button('Predict'):
            # Preprocess text
            if 'adhaar' in input_sms or 'atm pin' in input_sms or 'bank' in input_sms or 'otp' in input_sms or 'congrajulations' in input_sms or 'congrats' in input_sms:
                result=1
            else:
                try:
                    transformed_sms = transform_text(input_sms)
                    # Vectorize text
                    vector_input = tfidf.transform([transformed_sms])
                    # Predict
                    print('this is vector: ',vector_input.shape)
                    result = model.predict(vector_input)[0]
                except Exception as e:
                    print(e)
                    result=0
            # result=1
            # Display result
            if result == 1:
                st.markdown('<div class="result spam">', unsafe_allow_html=True)
                st.write("Prediction: Spam")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result not-spam">', unsafe_allow_html=True)
                st.write("Prediction: Not Spam")
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "About Us":
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.markdown("---")
        st.header("About Us")
        st.write("This page provides information about Vartha Sodhana.")
        st.write("Created with Streamlit and Python.")
        st.write("Welcome to our machine learning project. Here are the profiles of our amazing developers:")

        # Developer profiles
        developers = [
            {
                "name": "Disha Rao",
                "role": "Developer",
                "bio": "3rd year Student at Srinivas Institute of Technology",
                "image": r"C:\Users\LENOV0\Downloads\disha.jpeg"
            },
            {
                "name": "Chaithrashree CS",
                "role": "Developer",
                "bio": "3rd year Student at Srinivas Institute of Technology",
                "image": r"C:\Users\LENOV0\Downloads\chaithra.jpeg"
            }
        ]

        guide = {
            "name": "Shana Santhosh",
            "role": "Guide",
            "bio": "Project Guide and Mentor",
            "image": r"C:\Users\LENOV0\Downloads\mam.jpeg"  
        }

        for developer in developers:
            st.markdown('<div class="developer">', unsafe_allow_html=True)
            st.image(developer["image"], width=100)
            st.markdown('<div class="developer-info">', unsafe_allow_html=True)
            st.markdown(f'<p class="developer-name">{developer["name"]}</p>', unsafe_allow_html=True)
            st.write(f"**Role:** {developer['role']}")
            st.write(developer["bio"])
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Guide profile
        st.markdown('<div class="developer">', unsafe_allow_html=True)
        st.image(guide["image"], width=100)
        st.markdown('<div class="developer-info">', unsafe_allow_html=True)
        st.markdown(f'<p class="developer-name">{guide["name"]}</p>', unsafe_allow_html=True)
        st.write(f"**Role:** {guide['role']}")
        st.write(guide["bio"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer">By Disha Rao and Chaithrashree CS</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
