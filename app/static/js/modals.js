// Открытие модального окна по указанному идентификатору
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    } else {
        console.error(`Modal with ID ${modalId} not found`);
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    } else {
        console.error(`Modal with ID ${modalId} not found`);
    }
}

// Открытие модального окна для входа
function showLoginModal() {
    openModal('login-modal');
}

// Закрытие модального окна для входа
function closeLoginForm() {
    closeModal('login-modal');
}

// Закрытие модального окна для регистрации
function closeRegistrationForm() {
    closeModal('registration-modal');
}

// Закрытие модального окна для добавления маркера
function closeAddMarkerForm() {
    closeModal('add-marker-modal');
}

// Закрытие модального окна с информацией о владельце
function closeOwnerInfoForm() {
    closeModal('owner-info-modal');
}

// Открытие формы регистрации
function showRegistrationForm() {
    closeModal('login-modal');
    openModal('registration-modal');
}

// Открытие модального окна с информацией о владельце после добавления локации
function showOwnerInfoForm() {
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
            document.getElementById('location_id').value = result.location_id;
            openModal('owner-info-modal');
        } else {
            showNotification(`Ошибка добавления локации: ${result.message}`);
        }
    }).catch(error => {
        console.error('Ошибка:', error);
        showNotification('Произошла ошибка при добавлении локации. Пожалуйста, попробуйте снова.');
    });

    closeModal('add-marker-modal');
}

// Открытие модального окна для добавления отзыва
window.openReviewModal = function(locationId) {
    if (isUserAuthenticated()) {
        const reviewModal = document.getElementById('review-modal');
        reviewModal.style.display = 'block';

        // Убедимся, что location_id правильно передается
        console.log("Selected location ID:", locationId);

        // Заполняем скрытое поле location_id
        document.getElementById('review-location-id').value = locationId;
    } else {
        showLoginRequiredModal();
    }
}

// Показывает модальное окно с требованием авторизации, если пользователь не авторизован
function showLoginRequiredModal() {
    openModal('login-required-modal');
    setTimeout(() => {
        closeModal('login-required-modal');
    }, 2000);
}
