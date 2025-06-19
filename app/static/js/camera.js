let captured = false;

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    const video = document.getElementById('video');
    video.srcObject = stream;
  })
  .catch(err => {
    console.error('Erreur webcam :', err);
    alert('Impossible d’accéder à la webcam. Veuillez vérifier les permissions.');
  });

function capture() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  
  const imageInput = document.getElementById('face_image');
  canvas.toBlob(blob => {
    const file = new File([blob], 'temp.jpg', { type: 'image/jpeg' });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    imageInput.files = dataTransfer.files;
    captured = true;
  }, 'image/jpeg');
}

function prepareImage() {
  if (!captured) {
    alert('Veuillez capturer une image avant de soumettre.');
    return false;
  }
  return true;
}