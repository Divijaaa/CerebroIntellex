document.getElementById("predictionForm").addEventListener("submit", function (event) {
    event.preventDefault();
    // Get values and convert them to float
    const age = parseFloat(document.getElementById("age").value);
    const avg_glucose_level = parseFloat(document.getElementById("avg_glucose_level").value);
    const bmi = parseFloat(document.getElementById("bmi").value);

    // Array to store error messages
    let errors = [];

    // Validate each field separately
    if (isNaN(age) || age <= 0) errors.push("Age must be greater than 0.");
    if (isNaN(avg_glucose_level) || avg_glucose_level <= 0) errors.push("Average Glucose Level must be greater than 0.");
    if (isNaN(bmi) || bmi <= 0) errors.push("BMI must be greater than 0.");

    // If there are errors, show them and stop execution
    if (errors.length > 0) {
        alert(errors.join("\n"));
        return;
    }
    // Collect form data
    const data = {
        age: age,
        avg_glucose_level: avg_glucose_level,
        bmi: bmi,
        hypertension: document.getElementById("hypertension").value === 'yes' ? 1 : 0, // Convert to 1/0
        heart_disease: document.getElementById("heart_disease").value === 'yes' ? 1 : 0, // Convert to 1/0
        ever_married: document.getElementById("ever_married").value.trim().charAt(0).toUpperCase() + document.getElementById("ever_married").value.trim().slice(1).toLowerCase(),
        work_type: document.getElementById("work_type").value.trim().replace(" ", "_").toLowerCase(),
        Residence_type: document.getElementById("Residence_type").value.trim().charAt(0).toUpperCase() + document.getElementById("Residence_type").value.trim().slice(1).toLowerCase(),
        smoking_status: document.getElementById("smoking_status").value.trim().replace(" ", "_").toLowerCase()
    };

    console.log("Collected Data:", JSON.stringify(data));

    // Send request to FastAPI
    fetch("http://127.0.0.1:8080/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log("API Response:", result);

        // Store prediction and patient data in localStorage
        localStorage.setItem("stroke_prediction", result.stroke_prediction);
        localStorage.setItem("stroke_probability", result.stroke_probability);
        localStorage.setItem("patientData", JSON.stringify(data));

        // Redirect to next page
        window.location.href = "/Pages/Prediction_page_results/pred-result.html";
    })
    .catch(error => console.error("Error:", error));
});
