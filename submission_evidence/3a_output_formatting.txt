"""Emotion detection client for the embedded Watson NLP service."""

import json

import requests


SERVICE_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result():
    """Return the required result shape when the service has no prediction."""
    result = {emotion: None for emotion in EMOTIONS}
    result["dominant_emotion"] = None
    return result


def emotion_detector(text_to_analyze):
    """Return scores for the five emotions and the strongest emotion."""
    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            SERVICE_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )
    except requests.RequestException:
        return _empty_result()

    if response.status_code != 200:
        return _empty_result()

    try:
        response_data = json.loads(response.text)
        emotion_scores = response_data["emotionPredictions"][0]["emotion"]
        result = {emotion: emotion_scores[emotion] for emotion in EMOTIONS}
    except (IndexError, KeyError, TypeError, json.JSONDecodeError):
        return _empty_result()

    result["dominant_emotion"] = max(EMOTIONS, key=result.__getitem__)
    return result
