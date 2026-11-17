# Final project

Emotion detection web application for customer feedback. It sends text to the
embedded Watson NLP EmotionPredict service and displays scores for anger,
disgust, fear, joy, and sadness, plus the dominant emotion.

The starter project was provided by IBM Developer Skills Network and is
licensed under Apache-2.0; see [LICENSE](LICENSE).

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python server.py
```

Open <http://localhost:5000>. Enter text and select **Run Emotion Detection**.
Blank input displays `Invalid text! Please try again!`.

## Check the package, tests, and code quality

```bash
python -c 'from EmotionDetection import emotion_detector; print(emotion_detector("I love this new technology."))'
python -m unittest -v
python -m pylint server.py
```

The unit tests mock the remote service, so they run without a network connection.
The web application itself uses the course-provided Watson endpoint.
Live inference was unavailable in the preparation environment: the latest request timed out, and an earlier attempt failed DNS resolution. See [SUBMISSION_STATUS.md](SUBMISSION_STATUS.md) and `submission_evidence/` for the recorded attempts and offline verification; no live prediction is claimed.
