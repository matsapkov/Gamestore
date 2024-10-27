document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('profile-form');
    const saveButton = document.getElementById('save-btn');

    const checkForChanges = () => {
        // Проверка, есть ли изменения
        const isFormChanged = Array.from(form.elements).some(element => {
            return element.tagName === 'INPUT' && element.value !== element.defaultValue;
        });

        saveButton.style.display = isFormChanged ? 'block' : 'none';
    };

    Array.from(form.elements).forEach(element => {
        if (element.tagName === 'INPUT') {
            element.addEventListener('input', checkForChanges);
        }
    });
});
