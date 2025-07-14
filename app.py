from flask import Flask, render_template, request
import random
from difflib import SequenceMatcher

app = Flask(__name__)

PROMPT_OUTPUT_PAIRS = [
    {
        "prompt": "Describe a birthday party.",
        "output": "Cake, candles, balloons, and everyone singing together in one loud happy mess."
    },
    {
        "prompt": "Describe a traffic jam.",
        "output": "Cars stuck, horns blaring, drivers staring at their watches helplessly."
    },
    {
        "prompt": "Describe a rainy day.",
        "output": "Umbrellas pop open, streets shine wet, and chai smells even better than usual."
    },
    {
        "prompt": "Describe a school exam.",
        "output": "Papers on desks, silence all around, and pencils moving like machines."
    },
]

current_prompt = {"value": ""}

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    user_guess = ""
    output = ""

    if request.method == "POST":
        if "refresh" in request.form:
            # If New Round button clicked, skip evaluation
            result = ""
        else:
            user_guess = request.form["guess"]
            real_prompt = current_prompt["value"]
            similarity = SequenceMatcher(None, user_guess.lower(), real_prompt.lower()).ratio()
            score = int(similarity * 100)
            result = f"🎯 Real Prompt: {real_prompt}\n🧠 Similarity Score: {score}%"

    pair = random.choice(PROMPT_OUTPUT_PAIRS)
    current_prompt["value"] = pair["prompt"]
    output = pair["output"]

    return render_template("index.html", output=output, result=result)

if __name__ == "__main__":
    app.run(debug=True)
