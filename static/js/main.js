// Main JavaScript for VSK Gujarat Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the site
    initSite();

    // Handle form submissions
    handleForms();

    // Initialize animations
    initAnimations();
});

// Initialize the site
function initSite() {
    console.log('VSK Gujarat Website Initialized');

    // Set current year in copyright
    const yearElement = document.querySelector('.copyright p');
    if (yearElement) {
        const currentYear = new Date().getFullYear();
        yearElement.innerHTML = yearElement.innerHTML.replace('2023', currentYear);
    }

    // Add active class to current page in navigation
    highlightCurrentPage();

    // Close alert messages
    setupAlertClose();
}

// Highlight current page in navigation
function highlightCurrentPage() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath || (currentPath === '/' && linkPath === '/')) {
            link.classList.add('active');
        }
    });
}

// Setup alert close functionality
function setupAlertClose() {
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
}

// Handle form submissions
function handleForms() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Basic validation
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;

            if (!name || !email || !message) {
                showNotification('Please fill in all required fields.', 'error');
                return;
            }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showNotification('Please enter a valid email address.', 'error');
                return;
            }

            // If validation passes, show success message
            showNotification('Thank you for your message! We will get back to you soon.', 'success');
            contactForm.reset();
        });
    }
}

// Initialize animations
function initAnimations() {
    // Animate elements on scroll
    const animatedElements = document.querySelectorAll('.feature-card, .news-card, .article-card, .gallery-item');

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = 1;
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    animatedElements.forEach(element => {
        element.style.opacity = 0;
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(element);
    });
}

// Show notification
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

// Mobile menu toggle (if needed)
function toggleMobileMenu() {
    const nav = document.querySelector('nav ul');
    nav.classList.toggle('show');
}