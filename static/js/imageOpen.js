document.getElementById('image-link').addEventListener('click', function(event) {
    event.preventDefault(); // Отмена действия по умолчанию
    window.open(this.href, '_blank'); // Открывает ссылку в новом окне
});