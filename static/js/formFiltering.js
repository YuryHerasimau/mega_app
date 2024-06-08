function filterForms() {
    var selectedCategory = document.getElementById('category').value;
    var forms = document.querySelectorAll('.card-deck .card');

    forms.forEach(function(form) {
        if (selectedCategory === 'all' || form.textContent.toLowerCase().includes(selectedCategory.toLowerCase())) {
            console.log(selectedCategory);
            console.log(form.textContent);
            console.log(form.textContent.toLowerCase().includes(selectedCategory.toLowerCase()));
            form.style.display = 'block'; // Display the form
        } else {
            form.style.display = 'none'; // Hide the form
        }
    });
};