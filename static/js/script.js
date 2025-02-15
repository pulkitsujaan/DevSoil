// Trigger file explorer when the upload button is clicked
const upload_buttons=document.querySelectorAll("#uploadBtn")
    upload_buttons.forEach(button => {
      button.addEventListener("click", function() {
        document.getElementById("fileInput").click();
    });
        
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
            window.location.href = "/predictB";
        }
        if(prediction_string=='Alluvial Soil'){
            window.location.href = "/predictA";
        }
        if(prediction_string=='Red Soil'){
            window.location.href = "/predictR";
        }
        if(prediction_string=='Clay Soil'){
            window.location.href = "/predictC";
        }

        // Redirect to result.html
        // window.location.href = "/result";
    })
    .catch(error => {
        console.error("Error during file upload:", error);
        alert("Error processing the image.");
    });
}); 




  const alluvail_states = document.querySelectorAll('.alluvial-state');
  
  // Loop through each div and add an event listener
  alluvail_states.forEach(div => {
      div.addEventListener('click', function() {
        let imageElement = div.querySelector('img');
      // Store the clicked div's text in sessionStorage
      sessionStorage.setItem('stateName', div.querySelector('h3').innerText);
      sessionStorage.setItem('statePic', imageElement.src);
      window.location.href = '/AlluvialState';
    });

})
  const black_states = document.querySelectorAll('.black-state');
  
  // Loop through each div and add an event listener
  black_states.forEach(div => {
      div.addEventListener('click', function() {
        let imageElement = div.querySelector('img');
      // Store the clicked div's text in sessionStorage
      sessionStorage.setItem('stateName', div.querySelector('h3').innerText);
      sessionStorage.setItem('statePic', imageElement.src);
      window.location.href = '/BlackState';
    });
  })
  const red_states = document.querySelectorAll('.red-state');
  
  // Loop through each div and add an event listener
  red_states.forEach(div => {
      div.addEventListener('click', function() {
        let imageElement = div.querySelector('img');
      // Store the clicked div's text in sessionStorage
      sessionStorage.setItem('stateName', div.querySelector('h3').innerText);
      sessionStorage.setItem('statePic', imageElement.src);
      window.location.href = '/RedState';
    });
  })
  const clay_states = document.querySelectorAll('.clay-state');
  
  // Loop through each div and add an event listener
  clay_states.forEach(div => {
      div.addEventListener('click', function() {
        let imageElement = div.querySelector('img');
      // Store the clicked div's text in sessionStorage
      sessionStorage.setItem('stateName', div.querySelector('h3').innerText);
      sessionStorage.setItem('statePic', imageElement.src);
      window.location.href = '/ClayState';
    })})





//prediction pages
    const alluvial_predict = document.querySelectorAll('.alluvial-state');
  
    // Loop through each div and add an event listener
    alluvial_predict.forEach(div => {
        div.addEventListener('click', function() {
      
        // Store the clicked div's text in sessionStorage
        sessionStorage.setItem('stateName', div.querySelector('h3').innerText);
        sessionStorage.setItem('statePic', imageElement.src);
        window.location.href = '/predictA';
      })
    });