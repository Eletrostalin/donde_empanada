// notifications.js

// Функция для показа уведомлений
// Функция для показа уведомлений
window.showNotification = function(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerText = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 2000);
}

// Функция для показа модальных окон с ошибками
window.showModal = function(modalId, message) {
    const modal = document.getElementById(modalId);

    if (!modal) {
        console.error(`Modal with ID "${modalId}" not found`);
        return;
    }

    const messageContainer = modal.querySelector('.modal-content p');

    if (!messageContainer) {
        console.error(`Message container not found in modal with ID "${modalId}"`);
        return;
    }

    messageContainer.innerText = message;
    modal.style.display = 'block';

    // Закрытие модального окна через 2 секунды (если необходимо)
    setTimeout(() => {
        modal.style.display = 'none';
    }, 2000);
}
