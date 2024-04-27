document.getElementById('showNewsButton').addEventListener('click', function() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_news', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            var newsList = document.getElementById('newsList');
            newsList.innerHTML = xhr.responseText;
        } else {
            console.error('Error loading news');
        }
    };
    xhr.send();
});