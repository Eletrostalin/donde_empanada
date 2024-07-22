document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/register', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrf_token')
        }
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
            alert('Регистрация прошла успешно!');
            var registerModal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
            registerModal.hide();
            var loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
            loginModal.show();
        } else {
            alert('Ошибка регистрации: ' + data.message);
        }
    })
    .catch(error => {
        alert('Произошла ошибка: ' + error.message);
    });
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/login', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrf_token')
        }
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
            alert('Вход выполнен успешно!');
            location.reload(); // Перезагрузка страницы или закрытие модального окна
        } else {
            alert('Ошибка входа: ' + data.message);
        }
    })
    .catch(error => {
        alert('Произошла ошибка: ' + error.message);
    });
});
