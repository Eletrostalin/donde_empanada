window.handleRegistration = async function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrf_token')
            }
        });

        const result = await response.json();

        if (result.success) {
            showNotification(result.message); // Уведомление
            setTimeout(() => {
                location.reload(); // Перезагрузка страницы после уведомления
            }, 2000);
        } else {
            showModal('error-modal', result.message); // Показываем модалку с ошибкой
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showModal('error-modal', 'Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.');
    }
}

// Обработчик авторизации
window.handleLogin = async function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrf_token')
            }
        });

        const result = await response.json();

        if (result.success) {
            showNotification(result.message); // Уведомление
            setTimeout(() => {
                location.reload(); // Перезагрузка страницы
            }, 2000);
        } else {
            showModal('login-required-modal', 'Неверная связка логин/пароль. Пожалуйста, попробуйте снова.'); // Показываем модалку с ошибкой
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showModal('login-required-modal', 'Неверная связка логин/пароль. Пожалуйста, попробуйте снова.');
    }
}

// Обработчик добавления маркера
window.handleAddMarker = async function(event) {
    event.preventDefault();  
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrf_token')
            }
        });

        const result = await response.json();

        if (result.success) {
            showNotification(result.message); 
            setTimeout(() => {
                location.reload();  
            }, 2000);
        } else {
            showModal('error-modal', result.message); // Показываем модалку с ошибкой
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showModal('error-modal', 'Произошла ошибка при добавлении точки. Пожалуйста, попробуйте снова.');
    }
}

// Обработчик формы "Я хозяин"
window.showOwnerInfoForm = function() {
    showNotification('Идет добавление точки, пожалуйста подождите'); // Уведомление

    setTimeout(() => {
        const addMarkerForm = document.getElementById('add-marker-form');
        const formData = new FormData(addMarkerForm);

        fetch(addMarkerForm.action, {
            method: addMarkerForm.method,
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrf_token')
            }
        }).then(response => response.json())
        .then(result => {
            if (result.success) {
                document.getElementById('location_id').value = result.location_id; // сохраняем id локации
                openModal('owner-info-modal');
            } else {
                showModal('error-modal', `Ошибка добавления локации: ${result.message}`); // Показываем модалку с ошибкой
            }
        }).catch(error => {
            console.error('Ошибка:', error);
            showModal('error-modal', 'Произошла ошибка при добавлении локации. Пожалуйста, попробуйте снова.');
        });

        closeModal('add-marker-modal');
    }, 2000); // Ожидание перед выполнением логики
}