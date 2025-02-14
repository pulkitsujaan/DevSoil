// Trigger file explorer when the upload button is clicked
document.getElementById("uploadBtn").addEventListener("click", function() {
    document.getElementById("fileInput").click();
});

// Handle the file selection event
document.getElementById("fileInput").addEventListener("change", function() {
    let file = this.files[0];

    if (!file) {
        console.log("No file selected!");
        alert("No file selected!");
        return;
    }

    console.log("File selected: ", file);

    let formData = new FormData();
    formData.append("file", file);

    // Convert image to Base64 and store in sessionStorage
    let reader = new FileReader();
    reader.onload = function (e) {
        sessionStorage.setItem("uploadedImage", e.target.result); // Store Base64 image
        console.log("Image saved to sessionStorage.");
    };
    reader.readAsDataURL(file); // Convert image to Base64

    // Send file via POST request to Flask
    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())  // Convert response to JSON
    .then(data => {
        prediction_string = Object.values(data).toString();
        console.log("Prediction result:", prediction_string);
        // console.log("Prediction result:", data);

        sessionStorage.setItem("prediction", JSON.stringify(data));


        if(prediction_string=='Black Soil'){
            window.location.href = "/blacksoil";
        }
        if(prediction_string=='Alluvial Soil'){
            window.location.href = "/alluvialsoil";
        }
        if(prediction_string=='Red Soil'){
            window.location.href = "/redsoil";
        }
        if(prediction_string=='Clay Soil'){
            window.location.href = "/claysoil";
        }

        // Redirect to result.html
        // window.location.href = "/result";
    })
    .catch(error => {
        console.error("Error during file upload:", error);
        alert("Error processing the image.");
    });
});



