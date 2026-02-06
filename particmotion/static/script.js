function updateForceInputs() {
  const type = document.getElementById("force_type").value;
  const container = document.getElementById("force-params");
  let html = "";

  if (type === "constant") {
    html = '<label>Force (F) [N]:</label><input type="number" id="F" value="">';
  } else if (type === "sinusoidal") {
    html = '<label>Amplitude (F0) [N]:</label><input type="number" id="F0" value="">' +
           '<label>Angular Frequency (ω) [rad/s]:</label><input type="number" id="omega" value="">';
  } else if (type === "linear") {
    html = '<label>Slope (k) [N/s]:</label><input type="number" id="k" value="">';
  } else if (type === "exponential") {
    html = '<label>Initial Force (F0) [N]:</label><input type="number" id="F0" value="">' +
           '<label>Decay Constant (τ) [s]:</label><input type="number" id="tau" value="">';
  }
  container.innerHTML = html;
}

function calculate() {
  console.log("Calculation started..."); 
  
  const mode = document.getElementById("mode").value;
  const mass = document.getElementById("mass").value;
  const v0 = document.getElementById("v0").value;
  const t = document.getElementById("t").value;
  const force_type = document.getElementById("force_type").value;

  const data = { mode, mass, v0, t, force_type };

  
  if (force_type === "constant") data.F = document.getElementById("F").value;
  if (force_type === "sinusoidal") {
    data.F0 = document.getElementById("F0").value;
    data.omega = document.getElementById("omega").value;
  }
  if (force_type === "linear") data.k = document.getElementById("k").value;
  if (force_type === "exponential") {
    data.F0 = document.getElementById("F0").value;
    data.tau = document.getElementById("tau").value;
  }

  console.log("Sending data:", data);

  fetch("/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) throw new Error("Server error: " + response.status);
    return response.json();
  })
  .then(result => {
    console.log("Result received:", result);
    const box = document.getElementById("result-box");
    
    document.getElementById("result-text").innerText = 
      `Final velocity: ${result.v} m/s\nMomentum: ${result.p} kg·m/s`;
    box.classList.add("glow");
    const graphImg = document.getElementById("force-graph");
if (result.graph) {
    graphImg.src = "data:image/png;base64," + result.graph;
    graphImg.style.display = "block";
}
    
  })
  .catch(error => {
    console.error("Error details:", error);
    document.getElementById("result-text").innerText = "Error: " + error.message;
  });
}
function resetForm() {
  
    
    document.getElementById("mass").value = "";
    document.getElementById("v0").value = "";
    document.getElementById("t").value = "";
    
   
    document.getElementById("mode").selectedIndex = 0;
    document.getElementById("force_type").selectedIndex = 0;
    
    
    updateForceInputs();
    
    
    const resultText = document.getElementById("result-text");
    const resultBox = document.getElementById("result-box");
    const plotImg = document.getElementById("force-graph");
   
    resultText.innerText = "Waiting for calculations...";
    resultBox.classList.remove("glow");
    if (plotImg) {
        plotImg.style.display = "none";
        plotImg.src = "";
    }
    

    
    

    console.log("Form has been reset!");
    
    
}




window.onload = function() {
    resetForm();
};