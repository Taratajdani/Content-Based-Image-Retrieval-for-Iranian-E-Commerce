const uploadBtn = document.getElementById('uploadBtn');
const captureBtn = document.getElementById('captureBtn');
const imageUpload = document.getElementById('imageUpload');
const cameraPreview = document.getElementById('cameraPreview');
const canvas = document.getElementById('canvas');
const imagePreview = document.getElementById('imagePreview');
const message = document.getElementById('message');
const resultsDiv = document.getElementById('results');
const loadingDiv = document.getElementById('loading')
let imageBlob = null;


window.addEventListener('beforeunload', function (event) {
  sessionStorage.clear();
});


uploadBtn.addEventListener('click', () => {
    imageUpload.click();
});

imageUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        displayImage(file);
    }
});


captureBtn.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraPreview.srcObject = stream;
        cameraPreview.style.display = 'block';
        cameraPreview.play();

        const takePicture = async() =>{
            const context = canvas.getContext('2d');
            canvas.width = cameraPreview.videoWidth;
            canvas.height = cameraPreview.videoHeight;
            context.drawImage(cameraPreview, 0, 0, canvas.width, canvas.height);
            cameraPreview.style.display = 'none';
            cameraPreview.pause();
            cameraPreview.srcObject.getTracks().forEach(track => track.stop());

            canvas.toBlob((blob) => {
                displayImage(blob);
            }, 'image/jpeg');
        }

         const takePictureBtn = document.createElement('button')
         takePictureBtn.innerText='Take Picture'
         imagePreview.appendChild(takePictureBtn)

        takePictureBtn.addEventListener('click', takePicture);
    } catch (err) {
        message.innerText = 'Error accessing camera: ' + err;
    }
});

function displayImage(fileOrBlob){
  const reader = new FileReader();
  reader.onload = function (e) {
    imagePreview.style.display = 'block';
    const img = document.createElement('img');
    img.src = e.target.result;
    imagePreview.innerHTML = '';
    imagePreview.appendChild(img);
    imageBlob = fileOrBlob;


    preprocessAndProcess(imageBlob)
  }
   reader.readAsDataURL(fileOrBlob);
}


async function preprocessAndProcess(blob){
    message.innerText = '';
    loadingDiv.style.display = 'block';
    const formData = new FormData();
     formData.append('image', blob, 'image.jpg');
    try {
        const response = await fetch('http://localhost:5000/api/process_image/', {
            method: 'POST',
            body: formData
            });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        loadingDiv.style.display = 'none';
        if (data.quality === 'low') {
            message.innerText = 'Image quality is low, please try another picture.';
        }
          else if(data.results.length > 0){
           message.innerText = 'Here are the top 10 results:'
           displayResults(data.results)
         }else{
            message.innerText= 'No similar picture could be found, try searching via keywords';
            window.location.href = "https://www.digikala.com/search/";
          }

    } catch (error) {
        console.error('Error during processing:', error);
        loadingDiv.style.display = 'none';
        message.innerText = `Error during processing: ${error}`;
    }
}


function displayResults(results) {
    resultsDiv.innerHTML = '';
    resultsDiv.style.display = 'flex';
    resultsDiv.style.flexWrap = 'wrap';
    results.forEach(result => {
    const img = document.createElement('img')
    img.src = result.image_url
    img.onclick = () => {window.open(result.product_url)}
    resultsDiv.appendChild(img)
  });
}