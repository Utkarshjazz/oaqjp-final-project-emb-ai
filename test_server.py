"""Web route tests for the Flask emotion detector."""

import unittest
from unittest.mock import patch

from server import app


class EmotionDetectorRouteTests(unittest.TestCase):
    """Check the home page, formatted result, and invalid-input response."""

    def setUp(self):
        """Create a fresh Flask test client for each route test."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page_renders(self):
        """The main route serves the provided emotion detector interface."""
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NLP", response.data)
        self.assertIn(b"textToAnalyze", response.data)

    def test_valid_text_returns_formatted_scores(self):
        """The API route includes scores and the dominant emotion."""
        scores = {
            "anger": 0.01,
            "disgust": 0.02,
            "fear": 0.03,
            "joy": 0.9,
            "sadness": 0.04,
            "dominant_emotion": "joy",
        }
        with patch("server.detect_emotion", return_value=scores):
            response = self.client.get(
                "/emotionDetector", query_string={"textToAnalyze": "I love my life"}
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"'joy': 0.9", response.data)
        self.assertIn(b"dominant emotion is joy", response.data)

    def test_blank_text_shows_required_error(self):
        """A blank input receives the exact course-required message."""
        with patch("server.detect_emotion") as detect_emotion:
            response = self.client.get(
                "/emotionDetector", query_string={"textToAnalyze": "   "}
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")
        detect_emotion.assert_not_called()

    def test_service_error_uses_required_error_message(self):
        """A None dominant emotion is rendered as the required error."""
        scores = {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }
        with patch("server.detect_emotion", return_value=scores):
            response = self.client.get(
                "/emotionDetector", query_string={"textToAnalyze": "hello"}
            )

        self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")


if __name__ == "__main__":
    unittest.main()
