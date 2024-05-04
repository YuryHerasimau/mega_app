document.getElementById('image-link').addEventListener('click', function(event) {
    event.preventDefault(); // Отмена действия по умолчанию
    $('#myModal').modal(); // Открываем модальное окно
});