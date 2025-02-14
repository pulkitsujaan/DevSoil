// Trigger the hidden file input field on button click
document.getElementById("uploadBtn").addEventListener("click", function() {
    document.getElementById("fileInput").click();  // Open file explorer
});

// Listen for the file selection event
document.getElementById("fileInput").addEventListener("change", function() {
    let file = this.files[0];  // Get the first selected file

    // Debugging: Check if file is selected
    if (!file) {
        console.log("No file selected!");
        alert("No file selected!");
        return;
    }

    console.log("File selected: ", file);

    // Create FormData to send the file in the POST request
    let formData = new FormData();
    formData.append("file", file);

    // Debugging: Check if FormData is created correctly
    console.log("FormData created: ", formData);

    // Send file via POST request to Flask
    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => {
        console.log("Response received: ", response);
        return response.json();  // Convert response to JSON
    })
    .then(data => {
        console.log("Prediction result: ", data);  // Check prediction result
    })
    .catch(error => {
        console.error("Error during file upload:", error);  // Log any error
        alert("Error in file upload");
    });
});
