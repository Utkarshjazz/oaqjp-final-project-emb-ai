"""Unit tests for the Watson emotion detection client."""

import json
import unittest
from unittest.mock import patch

from EmotionDetection import emotion_detector
from EmotionDetection.emotion_detection import EMOTIONS, MODEL_ID, SERVICE_URL


class FakeResponse:
    """Small response object that matches the requests response fields used here."""

    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


class EmotionDetectionTests(unittest.TestCase):
    """Check emotion parsing, dominant scores, and blank-response handling."""

    def make_response(self, dominant):
        """Build a service response with the selected emotion as the maximum."""
        scores = {emotion: 0.1 for emotion in EMOTIONS}
        scores[dominant] = 0.9
        body = {"emotionPredictions": [{"emotion": scores}]}
        return FakeResponse(200, json.dumps(body))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_required_examples_have_expected_dominant_emotions(self, post):
        """Each course example maps to its expected dominant emotion."""
        examples = (
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear"),
        )

        for statement, dominant in examples:
            with self.subTest(statement=statement):
                post.return_value = self.make_response(dominant)
                result = emotion_detector(statement)
                self.assertEqual(result["dominant_emotion"], dominant)
                self.assertEqual(set(result), {*EMOTIONS, "dominant_emotion"})

        post.assert_called_with(
            SERVICE_URL,
            json={"raw_document": {"text": examples[-1][0]}},
            headers={"grpc-metadata-mm-model-id": MODEL_ID},
            timeout=30,
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_none_for_every_value(self, post):
        """A blank-input response uses the required all-None result shape."""
        post.return_value = FakeResponse(400, "")

        result = emotion_detector("")

        self.assertEqual(
            result,
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_transport_error_returns_none_result(self, post):
        """A service transport error does not crash the caller."""
        import requests

        post.side_effect = requests.RequestException("service unavailable")

        result = emotion_detector("hello")

        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
