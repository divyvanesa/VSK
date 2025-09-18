// Admin Panel JavaScript for VSK Gujarat

document.addEventListener('DOMContentLoaded', function() {
    // Initialize admin panel
    initAdmin();

    // Handle admin functionality
    handleAdminFeatures();
});

function initAdmin() {
    console.log('Admin Panel Initialized');

    // Setup alert close functionality
    setupAlertClose();

    // Initialize form validation
    initFormValidation();
}

function setupAlertClose() {
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
}

function initFormValidation() {
    // Add validation to forms in admin panel
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '#ddd';
                }
            });

            if (!valid) {
                e.preventDefault();
                showNotification('Please fill in all required fields.', 'error');
            }
        });
    });
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="alert-close">&times;</button>
    `;

    // Add styles
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '10000';
    notification.style.maxWidth = '350px';

    // Add close functionality
    const closeButton = notification.querySelector('.alert-close');
    closeButton.addEventListener('click', function() {
        notification.remove();
    });

    // Add to document
    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function handleAdminFeatures() {
    // Handle delete buttons
    const deleteButtons = document.querySelectorAll('.btn-icon.delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // Handle image preview for file inputs
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Create or update preview image
                    let preview = input.parentNode.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'image-preview';
                        input.parentNode.appendChild(preview);
                    }

                    preview.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 200px; margin-top: 10px;">`;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
}