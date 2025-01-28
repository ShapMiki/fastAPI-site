async function submitForm_and_foto() {
    // Останавливаем стандартное поведение формы
    event.preventDefault();

    // Получаем элемент формы
    const form = document.getElementById('updateForm');
    // Создаем объект FormData из формы
    const formData = new FormData(form);

    // Инициализируем пустой объект для хранения JSON данных и переменную для файла изображения
    const jsonData = {};
    let imageFile = null;

    // Перебираем каждую запись в объекте FormData
    formData.forEach((value, key) => {
        // Если ключ равен 'image', сохраняем значение в imageFile
        if (key === 'image') {
            imageFile = value;
        } else {
            // В противном случае сохраняем значение в jsonData
            jsonData[key] = value;
        }
    });

    try {
        // Отправляем JSON данные на сервер
        const jsonResponse = await fetch(form.getAttribute('data-api-url'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
        });

        // Если ответ не ok, выбрасываем ошибку
        if (!jsonResponse.ok) throw new Error('Ошибка при отправке JSON данных');

        // Логируем успешный ответ с JSON данными
        console.log('JSON данные успешно отправлены:', await jsonResponse.json());

        // Если есть файл изображения, отправляем его на сервер
        if (imageFile) {
            const imageFormData = new FormData();
            imageFormData.append('image', imageFile);

            const imageResponse = await fetch(form.getAttribute('photo-api-url'), {
                method: 'POST',
                body: imageFormData,
            });

            // Если ответ не ok, выбрасываем ошибку
            if (!imageResponse.ok) throw new Error('Ошибка при отправке файла изображения');

            // Логируем успешный ответ с файлом изображения
            console.log('Файл изображения успешно отправлен:', await imageResponse.json());
        }

        // Логируем, что все данные успешно отправлены
        console.log('Все данные успешно отправлены!');
    } catch (error) {
        // Логируем любые ошибки, возникшие во время выполнения fetch операций
        console.error('Ошибка при отправке данных:', error);
    }
    window.location.href = '/pages/personal_account';
}
//


let selectedFiles = [];

document.getElementById('fileInput').addEventListener('change', function(event) {
    const files = event.target.files;
    if (selectedFiles.length + files.length > 10) {
        alert('Вы можете загрузить не более 10 файлов.');
        return;
    }
    for (let i = 0; i < files.length; i++) {
        selectedFiles.push(files[i]);
    }
});


async function fetchUploadCarLot(event) {
    event.preventDefault(); // Останавливаем стандартное поведение формы

    const form = document.getElementById('carLotForm');
    const formData = new FormData(form);

    const jsonData = {};
    const imageFiles = selectedFiles; // Берем файлы из глобального selectedFiles

    // Перебираем данные формы, исключая файлы
    formData.forEach((value, key) => {
        if (!key.startsWith('image')) {
            jsonData[key] = value;
        }
    });

    try {
        // Отправляем JSON данные на сервер
        const jsonResponse = await fetch('/cars/add_activ_lot_api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
        });

        if (!jsonResponse.ok) {
            throw new Error(`Ошибка при отправке JSON данных: ${jsonResponse.statusText}`);
        }

        const jsonResult = await jsonResponse.json();
        const carId = jsonResult.car_id;

        console.log('JSON данные успешно отправлены:', jsonResult);

        // Отправка файлов изображений, если они есть
        if (imageFiles.length > 0) {
            const imageFormData = new FormData();
            imageFiles.forEach((file, index) => {
                imageFormData.append(`image${index}`, file);
            });

            try {
                const imageResponse = await fetch(`/images/upload_car_images/${carId}`, {
                    method: 'POST',
                    body: imageFormData,
                });

                if (!imageResponse.ok) {
                    throw new Error(`Ошибка при отправке файлов изображений: ${imageResponse.statusText}`);
                }

                console.log('Файлы изображений успешно отправлены:', await imageResponse.json());
            } catch (error) {
                console.error('Ошибка при отправке файлов изображений:', error);
                alert('Не удалось отправить изображения. Попробуйте снова.');
                return;
            }
        } else {
            console.log('Файлы изображений отсутствуют, отправка пропущена.');
        }

        // Если все данные успешно отправлены
        console.log('Все данные успешно отправлены!');
        window.location.href = '/pages/personal_account';
    } catch (error) {
        console.error('Ошибка при отправке JSON данных:', error);
        alert('Не удалось отправить данные лота. Попробуйте снова.');
    }
}











async function submitFormAndReload(event) {
    event.preventDefault(); // Prevent the default form submission

    const form = document.getElementById('RateForm');
    const formData = new FormData(form);

    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    try {
        const response = await fetch(form.action, {
            method: form.method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        });

        if (response.ok) {
            console.log('Form data sent successfully');
            setTimeout(() => {
                window.location.reload();
            }, 400); // Reload the page after 0.4 seconds
        } else {
            console.error('Error sending form data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


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

/*
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
});*/

/*
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

*/
