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