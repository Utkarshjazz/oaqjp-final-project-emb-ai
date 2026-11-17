"""Flask web interface for the emotion detection application."""

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector as detect_emotion


app = Flask(__name__)
INVALID_TEXT_MESSAGE = "Invalid text! Please try again!"


@app.route("/", methods=["GET"])
def home():
    """Render the emotion detection page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route():
    """Analyze the submitted text and return a readable summary."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return INVALID_TEXT_MESSAGE

    result = detect_emotion(text_to_analyze)
    if result["dominant_emotion"] is None:
        return INVALID_TEXT_MESSAGE

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. The dominant emotion is "
        f"{result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
