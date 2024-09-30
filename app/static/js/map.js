// map.js

// Объявляем глобальные переменные
window.isAddingMarker = false;
window.selectedLatLng = null;
window.map = null;

// Инициализация карты Google Maps
window.initMap = function() {
    window.map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -34.6037, lng: -58.3816 },
        zoom: 8,
        disableDefaultUI: true
    });

    fetchMarkers(window.map);

    window.map.addListener('click', function(event) {
        if (window.isAddingMarker) {
            window.selectedLatLng = event.latLng;
            openModal('add-marker-modal');
            document.getElementById('latitude').value = window.selectedLatLng.lat();
            document.getElementById('longitude').value = window.selectedLatLng.lng();
            document.getElementById('location_id').value = window.selectedLatLng.lat() + ',' + window.selectedLatLng.lng();
            window.isAddingMarker = false;
        }
    });

    document.getElementById('add-marker-form').addEventListener('submit', handleAddMarker);
}

// Функция для активации режима добавления метки
window.promptLocationSelection = function() {
    window.isAddingMarker = true;
    notifyMarkerModeActivated(); // уведомление о включении режима
};

window.fetchMarkers = async function(map) {
    try {
        const response = await fetch('/markers');
        const markers = await response.json();

        for (const marker of markers) {
            if (!marker.id) continue;

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
                        // Проверяем, есть ли текст отзыва
                        if (review.comment) {
                            reviewsContent += `
                                <div>
                                    <p><strong>${review.user_name}:</strong> ${review.comment}</p>
                                    <p>Оценка: ${review.rating}</p>
                                </div>
                            `;
                        }
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

// Возвращает иконку маркера в зависимости от средней оценки
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

// Генерирует HTML-код для отображения рейтинга в виде звезд
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

// Отправляет рейтинг локации на сервер и отображает уведомление о результате
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

// Определяет текущее местоположение пользователя и центрирует карту на этом месте
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

// Увеличивает масштаб карты
function zoomIn() {
    map.setZoom(map.getZoom() + 1);
}

// Уменьшает масштаб карты
function zoomOut() {
    map.setZoom(map.getZoom() - 1);
}
