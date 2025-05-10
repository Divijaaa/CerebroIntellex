document.addEventListener("DOMContentLoaded", function () {
    // Retrieve stored prediction results
    const prediction = localStorage.getItem("stroke_prediction") || "Not Available";
    const probability = localStorage.getItem("stroke_probability") || "N/A";

    // Display results
    document.getElementById("resultText").innerText = `Stroke Risk Prediction: ${prediction}`;
    document.getElementById("probabilityText").innerText = `Probability: ${probability}`;

    // Navigation functions
    window.goBack = function () {
        window.location.href = "/Pages/Prediction_page/index.html";
    }

    window.goNext = function () {
        window.location.href = "/Pages/Upload_image_page/upload.html";
    }
});
