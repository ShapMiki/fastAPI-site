document.getElementById('updateForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы
    console.log("Submit function called"); // Для проверки
    submitForm_and_file();
});

function submitForm_and_file() {
    const form = document.getElementById('updateForm');
    const formData = new FormData(form);
    const jsonData = {};

    formData.forEach((value, key) => {
        if (key !== 'image') {
            jsonData[key] = value;
        }
    });

    const imageFile = formData.get('image');
    const photoapiUrl = form.getAttribute('photo-api-url');
    console.log('Photo API URL:', photoapiUrl); // Добавьте этот лог
    const apiUrl = form.getAttribute('data-api-url');

    // Создаем массив Promises
    const requests = [];

    // Отправка JSON данных
    const jsonRequest = fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('JSON данные успешно отправлены:', data);
    })
    .catch(error => {
        console.error('Ошибка при отправке JSON данных:', error);
    });

    requests.push(jsonRequest);

    // Отправка файла изображения, если он есть
    if (imageFile) {
        const imageFormData = new FormData();
        imageFormData.append('image', imageFile);

        const imageRequest = fetch(photoapiUrl, {
            method: 'POST',
            body: imageFormData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Файл изображения успешно отправлен:', data);
        })
        .catch(error => {
            console.error('Ошибка при отправке файла изображения:', error);
        });

        requests.push(imageRequest);
    }

    // Ожидаем выполнения всех запросов
    Promise.all(requests)
    .then(() => {
        console.log('Все запросы успешно выполнены');
    })
    .catch(error => {
        console.error('Ошибка при выполнении одного из запросов:', error);
    });
}
//


function redirectAfterSubmit(event) {
    event.preventDefault(); // Prevent the default form submission
    const form = event.target;
    const formData = new FormData(form);

    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    fetch(form.action, {
        method: form.method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    }).then(response => {
        if (response.ok) {
            window.location.href = '/pages/personal_account';
        } else {
            alert('Error during login');
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('Error during login');
    });
}


document.getElementById('mainForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;

        // Create FormData for files
    const fileData = new FormData();
    for (let i = 0; i < files.length; i++) {
          fileData.append('files', files[i]);
    }

        // Send files to the first API
    await fetch('/image/upload_file', {
        method: 'POST',
        body: fileData
    });

        // Create FormData for the rest of the form
    const formData = new FormData(event.target);

        // Send form data to the second API
    await fetch('/api/upload_form', {
        method: 'POST',
        body: formData
    });

    alert('Files and form data uploaded successfully');
});


function submitForm() {
    const form = document.getElementById('updateForm');
    const formData = new FormData(form);
    const jsonData = {};

    formData.forEach((value, key) => {
        if (key !== 'image') {
            jsonData[key] = value;
        }
    });

    const imageFile = formData.get('image');

    // Send JSON data
    fetch(form.getAttribute('data-api-url'), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('JSON data sent successfully:', data);

        // Send image file
        if (imageFile) {
            const imageFormData = new FormData();
            imageFormData.append('image', imageFile);

            fetch('/auth/update_user_info_api', {
                method: 'POST',
                body: imageFormData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Image file sent successfully:', data);
            })
            .catch(error => {
                console.error('Error sending image file:', error);
            });
        }
    })
    .catch(error => {
        console.error('Error sending JSON data:', error);
    });
}


