from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from utils import check_login, register_user
from forms import LoginForm, RegisterForm
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json

app = Flask(__name__)
app.secret_key = "supersecret123"  

# Load DialoGPT model & tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Load predefined responses
def load_responses():
    with open("data.json", "r") as file:
        return json.load(file)

responses = load_responses()
conversation_history = []

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if check_login(username, password):
            session['user'] = username
            return redirect(url_for('chat_page'))  # 👈 Redirect to chatbot page directly
        else:
            flash("Invalid credentials. Try again.")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if register_user(username, password):
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Username already taken. Try another one.")
            return redirect(url_for('register'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/chat')
def chat_page():
    if 'user' in session:
        return render_template("chat.html", user=session['user'])  # 👈 Pass user to template
    return redirect(url_for('login'))




@app.route("/get", methods=["POST"])
def chat():
    global conversation_history
    try:
        user_input = request.form.get("msg", "").strip()
        if not user_input:
            return jsonify({"response": "Please type something!"})

        if user_input.lower() in responses:
            return jsonify({"response": responses[user_input.lower()]})

        conversation_history.append(f"User: {user_input}")

        chat_prompt = "\n".join(conversation_history) + "\nAI:"
        input_ids = tokenizer.encode(chat_prompt, return_tensors="pt")

        output_ids = model.generate(
            input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
        )

        response = tokenizer.decode(output_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        conversation_history.append(f"AI: {response}")

        if len(conversation_history) > 12:
            conversation_history = conversation_history[-6:]

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})




if __name__ == '__main__':
    app.run(debug=True)
