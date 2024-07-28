let map;
let selectedLatLng;
let isAddingMarker = false;

function toggleDropdown() {
    const dropdown = document.getElementById('user-dropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

async function handleLogin(event) {
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
            location.reload(); // Перезагрузка страницы для обновления состояния авторизации
        } else {
            alert(`Ошибка входа: ${result.message}`);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при входе. Пожалуйста, попробуйте снова.');
    }
}

async function handleRegistration(event) {
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
            showSuccessModal(result.message);  // Показать сообщение об успехе
            setTimeout(() => {
                document.getElementById('success-modal').style.display = 'none';
                location.reload();  // Перезагрузка страницы через 2 секунды
            }, 1500);
        } else {
            alert(`Ошибка регистрации: ${result.message}`);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.');
    }
}

function showSuccessModal(message) {
    const modal = document.getElementById('success-modal');
    const messageElement = document.getElementById('success-message');
    messageElement.textContent = message;
    modal.style.display = 'block';
}

function closeLoginForm() {
    document.getElementById('login-modal').style.display = 'none';
}

function closeRegistrationForm() {
    document.getElementById('registration-modal').style.display = 'none';
}

function closeAddMarkerForm() {
    document.getElementById('add-marker-modal').style.display = 'none';
}

function showRegistrationForm() {
    document.getElementById('login-modal').style.display = 'none';
    document.getElementById('registration-modal').style.display = 'block';
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 55.7558, lng: 37.6176 },
        zoom: 8,
        disableDefaultUI: true,  // Отключаем все кнопки
        zoomControl: true  // Включаем только управление зумом
    });

    fetchMarkers(map);

    map.addListener('click', function(event) {
        if (isAddingMarker) {
            selectedLatLng = event.latLng;
            document.getElementById('add-marker-modal').style.display = 'block';
            document.getElementById('latitude').value = selectedLatLng.lat();
            document.getElementById('longitude').value = selectedLatLng.lng();
            isAddingMarker = false;
        }
    });
}

function promptLocationSelection() {
    const alert = document.getElementById('custom-alert');
    alert.style.display = 'block';
    setTimeout(() => {
        alert.style.display = 'none';
    }, 3000);
    isAddingMarker = true;
}

async function fetchMarkers(map) {
    try {
        const response = await fetch('/markers');
        const markers = await response.json();

        markers.forEach(marker => {
            new google.maps.Marker({
                position: { lat: marker.latitude, lng: marker.longitude },
                map: map,
                title: marker.name
            });
        });
    } catch (error) {
        console.error('Ошибка при загрузке меток:', error);
    }
}

async function handleAddLocation(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    if (selectedLatLng) {
        formData.append('latitude', selectedLatLng.lat());
        formData.append('longitude', selectedLatLng.lng());
    } else {
        alert('Пожалуйста, выберите точку на карте');
        return;
    }

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
            showSuccessModal(result.message);  // Показать сообщение об успехе
            setTimeout(() => {
                document.getElementById('success-modal').style.display = 'none';
                location.reload();  // Перезагрузка страницы через 2 секунды
            }, 2000);
        } else {
            console.error(`Ошибка добавления локации: ${result.message}`);
            alert(`Ошибка добавления локации: ${result.message}`);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при добавлении локации. Пожалуйста, попробуйте снова.');
    }
}

window.onclick = function(event) {
    const modals = ['login-modal', 'registration-modal', 'add-marker-modal', 'success-modal'];
    modals.forEach(function(modal) {
        if (event.target == document.getElementById(modal)) {
            document.getElementById(modal).style.display = "none";
        }
    });
}
