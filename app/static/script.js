let isAddingMarker = false;
let selectedLatLng = null;
let map;

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
            location.reload();
        } else {
            alert(`Ошибка входа: ${result.message}`);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при входе. Пожалуйста, попробуйте снова.');
    }
}

function showLoginModal() {
    document.getElementById('login-modal').style.display = 'block';
    document.getElementById('login-required-modal').style.display = 'none';
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

function closeOwnerInfoForm() {
    document.getElementById('owner-info-modal').style.display = 'none';
}

function showRegistrationForm() {
    document.getElementById('login-modal').style.display = 'none';
    document.getElementById('registration-modal').style.display = 'block';
}

function showOwnerInfoForm() {
    document.getElementById('owner-info-modal').style.display = 'block';
    document.getElementById('add-marker-modal').style.display = 'none';
    document.getElementById('location_id').value = selectedLatLng ? selectedLatLng.latLng : null;
}

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
            document.getElementById('add-marker-modal').style.display = 'block';
            document.getElementById('latitude').value = selectedLatLng.lat();
            document.getElementById('longitude').value = selectedLatLng.lng();
            isAddingMarker = false;
        }
    });
}

function promptLocationSelection() {
    isAddingMarker = true;
    notifyMarkerModeActivated();
}

function openReviewModal(locationId) {
    if (isUserAuthenticated()) {
        const reviewModal = document.getElementById('review-modal');
        reviewModal.style.display = 'block';
        document.getElementById('review-location-id').value = locationId;
    } else {
        showLoginRequiredModal();
    }
}

function isUserAuthenticated() {
    return !!document.getElementById('profileDropdown');
}

function showLoginRequiredModal() {
    const loginModal = document.getElementById('login-required-modal');
    loginModal.style.display = 'block';

    setTimeout(() => {
        loginModal.style.display = 'none';
    }, 2000);
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
            alert('Ваша оценка успешно сохранена!');
        } else {
            alert(`Ошибка сохранения оценки: ${result.message}`);
        }
    } catch (error) {
        alert('Произошла ошибка при сохранении оценки. Пожалуйста, попробуйте снова.');
    }
}

async function handleReviewSubmit(event) {
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
            alert('Ваш отзыв успешно отправлен!');
            document.getElementById('review-modal').style.display = 'none';
            location.reload(); // Перезагрузка страницы для обновления данных
        } else {
            alert(`Ошибка отправки отзыва: ${result.message}`);
        }
    } catch (error) {
        alert('Произошла ошибка при отправке отзыва. Пожалуйста, попробуйте снова.');
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
            alert('Ошибка при определении местоположения.');
        });
    } else {
        alert('Геолокация не поддерживается вашим браузером.');
    }
}

function zoomIn() {
    map.setZoom(map.getZoom() + 1);
}

function zoomOut() {
    map.setZoom(map.getZoom() - 1);
}

window.onclick = function(event) {
    const modals = ['login-modal', 'registration-modal', 'add-marker-modal', 'owner-info-modal', 'review-modal', 'success-modal'];
    modals.forEach(function(modal) {
        if (event.target == document.getElementById(modal)) {
            document.getElementById(modal).style.display = "none";
        }
    });
}
