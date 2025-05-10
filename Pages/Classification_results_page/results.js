
document.addEventListener("DOMContentLoaded", function () {
    // Retrieve stored values
    const strokeType = localStorage.getItem("strokeType") || "N/A";
    const strokeConfidence = localStorage.getItem("strokeConfidence") || "N/A";
    const uploadedImage = localStorage.getItem("uploaded_image") || "";
    const selectedType = localStorage.getItem("selectedType") || "CT";  // Default to CT

    // Convert confidence to 4 decimal places if it's a valid number
    const roundedConfidence = isNaN(strokeConfidence) ? "N/A" : parseFloat(strokeConfidence).toFixed(4);

    // Update UI for Classification Results
    document.getElementById("strokeType").textContent = strokeType;
    document.getElementById("confidence").textContent = `${roundedConfidence}%`;
    document.getElementById("imageType").textContent = selectedType;  // Display CT/MRI

    // Display uploaded image
    if (uploadedImage) {
        const imgElement = document.getElementById("uploadedImage");
        imgElement.src = uploadedImage;
        imgElement.style.display = "block";
    }

    // Show MRI Segmentation button only if MRI was selected
    const segmentationButton = document.getElementById("mriSegmentationButton");
    if (selectedType === "MRI") {
        segmentationButton.style.display = "block";
    } else {
        segmentationButton.style.display = "none";  // Hide button for CT images
    }

    // MRI Segmentation Button Click Handler
    segmentationButton.addEventListener("click", async function () {
        if (!uploadedImage) {
            alert("No uploaded image found!");
            return;
        }

        // Convert base64 image back to a file object
        function dataURLtoBlob(dataURL) {
            const byteString = atob(dataURL.split(',')[1]);
            const mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0];
            const ab = new ArrayBuffer(byteString.length);
            const ia = new Uint8Array(ab);
            for (let i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            return new Blob([ab], { type: mimeString });
        }
        
        const blob = dataURLtoBlob(uploadedImage);
        
        const file = new File([blob], "uploaded_mri.png", { type: "image/png" });

        // Create form data
        const formData = new FormData();
        formData.append("file", file);
        formData.append("stroke_type", strokeType); // Send stroke type to FastAPI

        try {
            const apiResponse = await fetch("http://127.0.0.1:8004/segment/", {
                method: "POST",
                body: formData
            });

            if (!apiResponse.ok) throw new Error("Segmentation failed!");

            // Convert response into an image URL and store it in localStorage
            const imageBlob = await apiResponse.blob();  // Get the image as a blob
            const imageUrl = URL.createObjectURL(imageBlob); // Create a URL for the image


            // Store segmented image and stroke type in localStorage
            const reader = new FileReader();
            reader.readAsDataURL(imageBlob);
            reader.onloadend = function() {
                localStorage.setItem("segmentedImage", reader.result);
            };

            localStorage.setItem("segmentedBlob", await imageBlob.text());
            localStorage.setItem("strokeType", strokeType);

            // Redirect to seg-results.html
            window.location.href = "/Pages/Segmentation_page/seg-results.html";
        } catch (error) {
            console.error("Error during segmentation:", error);
            alert("Segmentation failed! Check the console for details.");
        }
    });
});
