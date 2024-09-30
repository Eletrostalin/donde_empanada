let isAddingMarker = false;
let selectedLatLng = null;
let map;

document.getElementById('add-marker-form').addEventListener('submit', handleAddMarker);
// Универсальная функция для открытия модального окна
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

// Универсальная функция для закрытия модального окна
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Универсальная функция для обработки отправки формы
async function handleFormSubmit(event, successCallback, errorCallback) {
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

        if (result.success && successCallback) {
            successCallback(result);
        } else if (errorCallback) {
            errorCallback(result);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова.');
    }
}

// Обработчик кликов по области вне модального окна
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
}

function notifyMarkerModeActivated() {
    const notification = document.createElement('div');
    notification.id = 'marker-mode-notification';
    notification.className = 'marker-mode-notification';
    notification.innerText = 'Режим добавления маркера активирован. Нажмите на карту, чтобы добавить маркер.';
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 2000);
}

// Универсальная функция для отображения уведомлений
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerText = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 2000); // Уведомление исчезает через 2 секунды
}

// Инициализация карты
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -34.6037, lng: -58.3816 },
        zoom: 8,
        disableDefaultUI: true
    });

    fetchMarkers(map);

    map.addListener('click', function(event) {
        if (isAddingMarker) {
            selectedLatLng = event.latLng;
            openModal('add-marker-modal');
            document.getElementById('latitude').value = selectedLatLng.lat();
            document.getElementById('longitude').value = selectedLatLng.lng();
            document.getElementById('location_id').value = selectedLatLng.lat() + ',' + selectedLatLng.lng();
            isAddingMarker = false;
        }
    });

    // Обработчик для формы добавления маркера
    document.getElementById('add-marker-form').addEventListener('submit', handleAddMarker);
}

// Функции для управления модальными окнами
function showLoginModal() {
    openModal('login-modal');
}

function closeLoginForm() {
    closeModal('login-modal');
}

function closeRegistrationForm() {
    closeModal('registration-modal');
}

function closeAddMarkerForm() {
    closeModal('add-marker-modal');
}

function closeOwnerInfoForm() {
    closeModal('owner-info-modal');
}

function showRegistrationForm() {
    closeModal('login-modal');
    openModal('registration-modal');
}

function showOwnerInfoForm() {
    const addMarkerForm = document.getElementById('add-marker-form');
    const formData = new FormData(addMarkerForm);

    // Сначала добавляем локацию
    fetch(addMarkerForm.action, {
        method: addMarkerForm.method,
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrf_token')
        }
    }).then(response => response.json())
    .then(result => {
        if (result.success) {
            // Если добавление локации успешно, открываем форму владельца
            document.getElementById('location_id').value = result.location_id; // сохраняем id локации
            openModal('owner-info-modal');
        } else {
            showNotification(`Ошибка добавления локации: ${result.message}`);
        }
    }).catch(error => {
        console.error('Ошибка:', error);
        showNotification('Произошла ошибка при добавлении локации. Пожалуйста, попробуйте снова.');
    });

    // Закрываем модалку с добавлением метки
    closeModal('add-marker-modal');
}

function openReviewModal(locationId) {
    if (isUserAuthenticated()) {
        const reviewModal = document.getElementById('review-modal');
        reviewModal.style.display = 'block';
        document.getElementById('location_id').value = selectedLatLng ? selectedLatLng.lat() + ',' + selectedLatLng.lng() : null;
    } else {
        showLoginRequiredModal();
    }
}

function showLoginRequiredModal() {
    openModal('login-required-modal');
    setTimeout(() => {
        closeModal('login-required-modal');
    }, 2000);
}

function toggleDropdown() {
    const dropdown = document.getElementById('user-dropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

function isUserAuthenticated() {
    return !!document.getElementById('profileDropdown');
}

// Функции для работы с картой и маркерами
function promptLocationSelection() {
    isAddingMarker = true;
    notifyMarkerModeActivated();
}

async function fetchMarkers(map) {
    try {
        const response = await fetch('/markers');
        const markers = await response.json();

        for (const marker of markers) {
            if (!marker.id) {
                continue;
            }

            const markerObj = new google.maps.Marker({
                position: { lat: marker.latitude, lng: marker.longitude },
                map: map,
                title: marker.name,
                icon: getMarkerIcon(marker.average_rating),
                animation: google.maps.Animation.DROP
            });

            let reviewsContent = '';
            try {
                const reviewsResponse = await fetch(`/reviews/${marker.id}`);
                const reviewsData = await reviewsResponse.json();

                if (reviewsData.length > 0) {
                    reviewsData.forEach(review => {
                        reviewsContent += `
                            <div>
                                <p><strong>${review.user_name}:</strong> ${review.comment}</p>
                                <p>Оценка: ${review.rating}</p>
                            </div>
                        `;
                    });
                } else {
                    reviewsContent = '<p>Отзывов пока нет.</p>';
                }
            } catch (error) {
                reviewsContent = '<p>Ошибка при загрузке отзывов.</p>';
            }

            const starsContent = getStarRatingHTML(marker.average_rating, marker.id);

            const infoWindowContent = `
                <div>
                    <h3>${marker.name}</h3>
                    <p>${marker.description}</p>
                    <p><strong>Адрес:</strong> ${marker.address}</p>
                    <p><strong>Часы работы:</strong> ${marker.working_hours}</p>
                    <p><strong>Средний чек:</strong> ${marker.average_check}</p>
                    <p><strong>Средняя оценка:</strong> ${marker.average_rating.toFixed(1)}</p>
                    <p><strong>Количество оценок:</strong> ${marker.rating_count}</p>
                    ${starsContent}
                    <h4>Отзывы:</h4>
                    ${reviewsContent}
                    <button class="btn btn-primary mt-2" onclick="openReviewModal(${marker.id})">Оставить отзыв</button>
                </div>
            `;

            const infoWindow = new google.maps.InfoWindow({
                content: infoWindowContent
            });

            markerObj.addListener('click', () => {
                infoWindow.open(map, markerObj);
            });

            initializeStars(marker.average_rating, marker.id);
        }
    } catch (error) {
        console.error('Ошибка при загрузке меток:', error);
    }
}

function getMarkerIcon(averageRating) {
    const size = new google.maps.Size(40, 40);
    if (averageRating < 1) {
        return { url: '/static/1.png', scaledSize: size };
    } else if (averageRating < 2) {
        return { url: '/static/2.png', scaledSize: size };
    } else if (averageRating < 3) {
        return { url: '/static/3.png', scaledSize: size };
    } else if (averageRating < 4) {
        return { url: '/static/4.png', scaledSize: size };
    } else {
        return { url: '/static/5.png', scaledSize: size };
    }
}

function getStarRatingHTML(averageRating, locationId) {
    let starsHTML = '<div class="star-rating">';
    for (let i = 1; i <= 5; i++) {
        starsHTML += `
            <span class="star" data-value="${i}" data-location-id="${locationId}" onclick="rateLocation(${locationId}, ${i})">
                ${i <= averageRating ? '★' : '☆'}
            </span>
        `;
    }
    starsHTML += '</div>';
    return starsHTML;
}

async function rateLocation(locationId, rating) {
    try {
        const response = await fetch('/rate_location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
            body: JSON.stringify({
                location_id: locationId,
                rating: rating
            })
        });

        const result = await response.json();

        if (result.success) {
            showNotification('Ваша оценка успешно сохранена!');
        } else {
            showNotification(`Ошибка сохранения оценки: ${result.message}`);
        }
    } catch (error) {
        showNotification('Произошла ошибка при сохранении оценки. Пожалуйста, попробуйте снова.');
    }
}

// Инициализация звездочек на основе среднего рейтинга
function initializeStars(averageRating, locationId) {
    document.querySelectorAll(`.star[data-location-id="${locationId}"]`).forEach(star => {
        let starValue = star.getAttribute('data-value');
        if (starValue <= averageRating) {
            star.classList.add('selected');
        } else {
            star.classList.remove('selected');
        }

        star.addEventListener('mouseover', function() {
            for (let i = 1; i <= starValue; i++) {
                document.querySelector(`.star[data-location-id="${locationId}"][data-value="${i}"]`).classList.add('hover');
            }
        });

        star.addEventListener('mouseout', function() {
            document.querySelectorAll(`.star[data-location-id="${locationId}"]`).forEach(s => {
                s.classList.remove('hover');
            });
        });
    });
}

function locateMe() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos);
            map.setZoom(14);
            new google.maps.Marker({
                position: pos,
                map: map,
                title: 'Вы здесь'
            });
        }, () => {
            showNotification('Ошибка при определении местоположения.');
        });
    } else {
        showNotification('Геолокация не поддерживается вашим браузером.');
    }
}

function zoomIn() {
    map.setZoom(map.getZoom() + 1);
}

function zoomOut() {
    map.setZoom(map.getZoom() - 1);
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
            showNotification(result.message);
            setTimeout(() => {
                location.reload(); // Перезагружаем страницу
                showLoginModal(); // Открываем форму авторизации
            }, 2000); // Задержка перед перезагрузкой (2 секунды)
        } else {
            showNotification(`Ошибка регистрации: ${result.message}`);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.');
    }
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
            showNotification(result.message);
            setTimeout(() => {
                location.reload(); // Перезагрузка страницы
            }, 2000); // Задержка в 2 секунды перед перезагрузкой
        } else {
            showNotification(`Ошибка входа: ${result.message}`);
            setTimeout(() => {
                closeLoginForm(); // Закрытие формы, если требуется
            }, 2000);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Произошла ошибка при входе. Пожалуйста, попробуйте снова.');
    }
}

async function handleAddMarker(event) {
    event.preventDefault();  // предотвращает стандартное поведение отправки формы
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
                location.reload();  // перезагружает страницу после уведомления
            }, 2000);
        } else {
            showNotification(`Ошибка добавления точки: ${result.message}`);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Произошла ошибка при добавлении точки. Пожалуйста, попробуйте снова.');
    }
}

async function handleOwnerInfoSubmit(event) {
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
                location.reload(); // Перезагрузка страницы через 2 секунды
            }, 2000);
        } else {
            showNotification(`Ошибка: ${result.message}`);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Произошла ошибка при добавлении информации. Пожалуйста, попробуйте снова.');
    }
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerText = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 2000); // Уведомление исчезает через 2 секунды
}