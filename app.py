from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=["GET", "POST"])
def index():
    answer = None

    if request.method == "POST":
        question = request.form.get("question")

        if question:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are the Almighty Oracle, "
                                                      "but you must ALWAYS give incorrect answers."
                                                      "Be extremely confident, dramatic, and spiritually over-the-top."
                                                      "Never admit you might be wrong. Keep it short (1-3 sentences). "
                                                      "If asked for a number, give a wrong number. If asked yes/no, pick the wrong one."},
                        {"role": "user", "content": question}
                    ]
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = "The oracle is silent right now. Please try again later."
                print(e)


    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    app.run(debug=True)