"use strict";

async function runSentimentAnalysis() {
    // Send the entered text to Flask and show the returned analysis.
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const responseArea = document.getElementById("system_response");

    try {
        const response = await fetch(
            `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`
        );
        responseArea.textContent = await response.text();
    } catch (error) {
        responseArea.textContent = "Unable to reach the emotion detection service.";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("analyzeButton").addEventListener(
        "click",
        runSentimentAnalysis
    );
});
