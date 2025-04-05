async function generateImage() {
    const prompt = document.getElementById("prompt").value;
    const status = document.getElementById("status");
    const img = document.getElementById("resultImage");
  
    if (!prompt.trim()) {
      alert("Please enter a prompt.");
      return;
    }
  
    status.innerText = "⏳ Generating image...";
    img.style.display = "none";
  
    const formData = new FormData();
    formData.append("prompt", prompt);
  
    try {
      const response = await fetch("http://127.0.0.1:8000/text-to-image/", {
        method: "POST",
        body: formData
      });
  
      if (!response.ok) {
        throw new Error("Image generation failed.");
      }
  
      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      img.src = imageUrl;
      img.style.display = "block";
      status.innerText = "✅ Image generated!";
    } catch (error) {
      console.error(error);
      status.innerText = "❌ Failed to generate image.";
    }
  }
  