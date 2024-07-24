document.addEventListener('DOMContentLoaded', function() {
    // Обработчик для формы входа
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.headers.get('content-type').includes('application/json')) {
                return response.json();
            } else {
                return response.text().then(text => { throw new Error(text) });
            }
        })
        .then(data => {
            if (data.success) {
                var loginModal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
                loginModal.hide();
                location.reload(); // Перезагрузка страницы после успешного входа
            } else {
                alert('Ошибка входа: ' + data.message + ' 🚫');
            }
        })
        .catch(error => {
            alert('Произошла ошибка: ' + error.message + ' 🚫');
        });
    });

    // Обработчик для формы регистрации
    document.getElementById('registerForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch('/register', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.headers.get('content-type').includes('application/json')) {
                return response.json();
            } else {
                return response.text().then(text => { throw new Error(text) });
            }
        })
        .then(data => {
            if (data.success) {
                location.reload(); // Перезагрузка страницы после успешной регистрации
            } else {
                alert('Ошибка регистрации: ' + data.message + ' 🚫');
            }
        })
        .catch(error => {
            alert('Произошла ошибка: ' + error.message + ' 🚫');
        });
    });
});
