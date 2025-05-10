// Function to toggle password visibility
function togglePassword() {
    let passwordInput = document.getElementById("password");
    let toggleIcon = document.querySelector(".toggle-password");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.textContent = "🙈"; // Change icon to indicate visibility
    } else {
        passwordInput.type = "password";
        toggleIcon.textContent = "👁️"; // Change icon back
    }
}

// Function to handle redirection after clicking the "Next" button
function redirectToForm() {
    window.location.href = "/Pages/Prediction_page/index.html"; // Redirect to the patient details page
}
