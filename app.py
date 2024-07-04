import random
from flask import Flask, render_template, request, jsonify, url_for
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import spacy

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

# Load intents and other necessary data
with open('intents.json', 'r') as file:
    intents = json.load(file)

# Load saved model and other preprocessing artifacts
model = load_model('chatbot_model (1).h5')

with open('words.pkl', 'rb') as f:
    words = pickle.load(f)
print(f"Length of words list after loading: {len(words)}")  # Debug statement

with open('classes.pkl', 'rb') as f:
    classes = pickle.load(f)

lemmatizer = WordNetLemmatizer()
nlp = spacy.load('en_core_web_sm')

# Function to clean up input sentence
def clean_up_sentence(sentence):
    doc = nlp(sentence)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return tokens

# Function to convert sentence into bag of words array
def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)  # Ensure the bag length matches the number of features expected by the model
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"Found in bag: {w}")

    # Pad or truncate bag to match expected input shape (974 features)
    if len(bag) < 974:
        bag = bag + [0] * (974 - len(bag))
    else:
        bag = bag[:974]

    return np.array(bag)

# Function to predict intent from user input
def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    print(f"Shape of generated bag: {p.shape}")  # Debug statement
    # Ensure the bag length matches the expected input shape
    if len(p) < 974:
        p = np.pad(p, (0, 974 - len(p)), 'constant')
    else:
        p = p[:974]
    print(f"Shape of padded/truncated bag: {p.shape}")  # Debug statement
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Route for main page
@app.route('/')
def home():
    css_url = url_for('static', filename='styles.css')
    js_url = url_for('static', filename='scripts.js')
    background_url = url_for('static', filename='background.jpg')
    print(f'CSS URL: {css_url}, JS URL: {js_url}, Background URL: {background_url}')
    return render_template('index.html', background_url=background_url)

# Route to handle chatbot interactions
@app.route('/chat', methods=['POST'])
def chat():
    try:
        msg = request.json['message']  # Adjust to match your JS code
        print(f"Received message: {msg}")

        # Predict intent and get response
        ints = predict_class(msg, model)
        print(f"Intent prediction: {ints}")

        res = get_response(ints, intents)
        print(f"Generated response: {res}")

        return jsonify({'message': res})

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'message': 'Error: Please try again later'})

# Function to fetch appropriate response based on predicted intent
def get_response(ints, intents_json):
    if ints:
        tag = ints[0]['intent']
        for i in intents_json['intents']:
            if i['tag'] == tag:
                responses = i['responses']
                # Shuffle responses and return a random one
                random.shuffle(responses)
                return responses[0]  # Adjust to return different responses as needed
    return "I'm sorry, I don't understand. Could you please rephrase?"

if __name__ == '__main__':
    app.run(debug=True, port=4000)



