from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    image = request.files["food_image"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image.filename
    )

    image.save(filepath)

    img = Image.open(filepath)

    prompt = """
    Analyze this meal image.

    Return the result exactly like this:

    🍛 Food:
    ...

    🔥 Estimated Calories:
    ...

    💪 Protein:
    ...

    🍚 Carbohydrates:
    ...

    🥑 Fat:
    ...

    ⭐ Health Score:
    ...

    💡 Healthy Suggestion:
    ...

    Keep the response concise and user friendly.
    """

    response = model.generate_content([prompt, img])

    return render_template(
        "result.html",
        result=response.text
    )

if __name__ == "__main__":
    app.run(debug=True)

