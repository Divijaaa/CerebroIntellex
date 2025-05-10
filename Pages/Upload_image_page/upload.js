
document.addEventListener("DOMContentLoaded", function () {
    let selectedFile = null;
    let selectedType = "CT";  // Default to CT

    window.switchTab = function (type) {
        document.querySelectorAll('.tab-option').forEach(tab => tab.classList.remove('active'));
        
        selectedType = type;  // Set selected type
        
        if (type === 'CT') {
            document.getElementById('ctTab').classList.add('active');
        } else if (type === 'MRI') {
            document.getElementById('mriTab').classList.add('active');
        }
    };

    function triggerUpload() {
        document.getElementById('fileInput').click();
    }
    window.triggerUpload = triggerUpload;

    document.getElementById("fileInput").addEventListener("change", function (event) {
        selectedFile = event.target.files[0];
        if (selectedFile) {
            document.getElementById("uploadBox").innerHTML = `<p>${selectedFile.name}</p>`;

            // Store the image locally for display on results.html
            const reader = new FileReader();
            reader.onload = function (e) {
                localStorage.setItem("uploaded_image", e.target.result);
                localStorage.setItem("selectedType", selectedType); // Store CT/MRI
            };
            reader.readAsDataURL(selectedFile);
        }
    });

    document.getElementById("nextButton").addEventListener("click", function () {
        if (!selectedFile) {
            alert("Please upload an image before proceeding.");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        // Use different API endpoints for CT and MRI
        let apiUrl = selectedType === "CT" 
            ? "http://127.0.0.1:8001/classify" 
            : "http://127.0.0.1:8003/classify-mri";  // Updated MRI URL

        fetch(apiUrl, {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            console.log("API Response:", result);

            // Store stroke results
            localStorage.setItem("strokeType", result.prediction || "N/A");
            localStorage.setItem("strokeConfidence", result.confidence || "N/A");

            // Redirect to results page
            window.location.href = "/Pages/Classification_results_page/results.html";
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Failed to upload and classify the image. Please try again.");
        });
    });
});
