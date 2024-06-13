function toggleForms(formId) {
    document.querySelectorAll('form').forEach(form => {
        form.classList.remove('active-form');
    });
    document.getElementById(formId).classList.add('active-form');
}
