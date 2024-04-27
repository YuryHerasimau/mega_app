document.addEventListener('DOMContentLoaded', function() {
    // form1
    const form1 = document.getElementById('form1');
    const credentialsInputField1 = document.getElementById('username_base');
    const credentialsInputField2 = document.getElementById('qty');
    const credentialsInputField3 = document.getElementById('length');
    const submitButton1 = document.getElementById('submitButton1');
    form1.addEventListener('input', function() {
        submitButton1.disabled = !credentialsInputField1.value || !credentialsInputField2.value || !credentialsInputField3.value;
    });
    // form2
    const form2 = document.getElementById('form2');
    const inputField2 = document.getElementById('csv_data');
    const dropDown2 = document.getElementById('actions');
    const submitButton2 = document.getElementById('submitButton2');
    form2.addEventListener('input', function() {
        submitButton2.disabled = !inputField2.value || !dropDown2.value;
    });
    // form3
    const form3 = document.getElementById('form3');
    const radios3 = document.getElementsByName('locale');
    const dropDown3 = document.getElementById('data_type');
    const submitButton3 = document.getElementById('submitButton3');
    form3.addEventListener('input', function() {
        const isFormFilled = [...radios3].some(radio =>
            radio.checked) && dropDown3.value !== '';
        submitButton3.disabled = !isFormFilled; 
    });
    form3.addEventListener('change', function() {
        const isFormFilled = [...radios3].some(radio =>
            radio.checked) && dropDown3.value !== '';
        submitButton3.disabled = !isFormFilled;
    });
});