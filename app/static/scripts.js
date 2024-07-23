document.getElementById('add-location-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    formData.append('latitude', document.getElementById('latitude').value);
    formData.append('longitude', document.getElementById('longitude').value);

    fetch('/add_location', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Location added successfully!');
            location.reload();
        } else {
            alert('Error adding location: ' + data.message);
        }
    })
    .catch(error => {
        alert('An error occurred: ' + error.message);
    });
});

let addMarkerMode = false;

document.getElementById('add-marker-button').addEventListener('click', function() {
    addMarkerMode = !addMarkerMode;
    this.classList.toggle('active');
    if (addMarkerMode) {
        document.getElementById('map').style.cursor = 'pointer';
    } else {
        document.getElementById('map').style.cursor = 'default';
    }
});

document.getElementById('cancel-button').addEventListener('click', function() {
    document.getElementById('marker-form').style.display = 'none';
    addMarkerMode = false;
    document.getElementById('add-marker-button').classList.remove('active');
    document.getElementById('map').style.cursor = 'default';
});

ymaps.ready(init);

function init() {
    var map = new ymaps.Map("map", {
        center: [55.76, 37.64], // Координаты центра карты
        zoom: 8,
        controls: [] // Убираем все элементы управления
    });

    // Загрузка меток с сервера
    fetch('/markers')
        .then(response => response.json())
        .then(data => {
            data.forEach(marker => {
                var placemark = new ymaps.Placemark([marker.latitude, marker.longitude], {
                    balloonContent: `<div><strong>${marker.name}</strong><br>${marker.description}</div>`,
                    iconLayout: 'default#image',
                    iconImageHref: '{{ url_for('static', filename='marker.png') }}', // Путь к вашему PNG файлу
                    iconImageSize: [30, 42],
                    iconImageOffset: [-15, -42]
                });
                map.geoObjects.add(placemark);
            });
        });

    // Добавление метки по клику
    map.events.add('click', function (e) {
        if (addMarkerMode) {
            var coords = e.get('coords');
            document.getElementById('latitude').value = coords[0];
            document.getElementById('longitude').value = coords[1];
            document.getElementById('marker-form').style.display = 'block';
        }
    });
}
