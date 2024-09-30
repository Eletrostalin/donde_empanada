// user.js

// Проверяет, авторизован ли пользователь
window.isUserAuthenticated = function() {
    return !!document.getElementById('profileDropdown');
}

// Переключает отображение выпадающего меню пользователя
window.toggleDropdown = function() {
    const dropdown = document.getElementById('user-dropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}
