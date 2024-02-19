function adjustInputSize(inputField) {
    inputField.style.height = 'auto';
    inputField.style.height = (inputField.scrollHeight) + 'px';
}


function runScript() {
    fetch('/run-script')
    .then(response => {
        if (response.ok) {
        alert('Python script executed successfully!');
        } else {
        alert('Error executing Python script!');
        }
    });
}


function downloadTextFile() {
    var fileUrl = 'randomtext.txt'; 
    var a = document.createElement('a');
    a.href = fileUrl;
    a.download = 'randomtext.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function startDownload() {
    setTimeout(downloadTextFile, 1000); // Задержка в 1 секунду
}


function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);
    fetch('/upload', {
    method: 'POST',
    body: formData
    })
    .then(response => {
        if (response.ok) {
        alert('File uploaded successfully!');
        } else {
        alert('Error uploading file!');
        }
    })
    .catch(error => console.error('Error:', error));
}



document.getElementById('encryptButton').addEventListener('click', function() {
var inputText = document.getElementById('inputTextf').value;

fetch('/encrypt', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: inputText })  // Виправлений параметр text
})
.then(response => response.json())
.then(data => {
    document.getElementById('encryptedText').value = data.result;
})
.catch(error => console.error('Error:', error));
});


document.getElementById('decryptButton').addEventListener('click', function() {
var inputText = document.getElementById('inputTextn').value;
fetch('/decrypt', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: inputText })  // Виправлений параметр text
})
.then(response => response.json())
.then(data => {
    document.getElementById('decryptedText').value = data.result;
})
.catch(error => console.error('Error:', error));
});
