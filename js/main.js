// Theme Toggle Functionality
function toggleTheme() {
    const html = document.documentElement;
    const theme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

// Check for saved theme preference
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
});

// Mobile Menu Functionality
function toggleMobileMenu() {
    const hamburger = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('mobile-sidebar');
    const overlay = document.getElementById('mobile-menu-overlay');
    
    hamburger.classList.toggle('active');
    sidebar.classList.toggle('show');
    overlay.classList.toggle('show');
    
    // Toggle body scroll when menu is open
    document.body.style.overflow = sidebar.classList.contains('show') ? 'hidden' : '';
    
    // Add overlay click event to close menu
    if (overlay.classList.contains('show')) {
        overlay.addEventListener('click', toggleMobileMenu);
    } else {
        overlay.removeEventListener('click', toggleMobileMenu);
    }
}

function toggleMobileLanguageDropdown() {
    const dropdown = document.getElementById('mobile-language-dropdown');
    dropdown.classList.toggle('show');
}

function toggleLanguageDropdown() {
    const dropdown = document.getElementById('language-dropdown');
    dropdown.classList.toggle('show');
}

// Language Dropdown Management (actual translation is handled by translations.js)
function updateLanguageUI(lang) {
    // Close language dropdowns
    const desktopDropdown = document.getElementById('language-dropdown');
    const mobileDropdown = document.getElementById('mobile-language-dropdown');
    
    if (desktopDropdown) {
        desktopDropdown.classList.remove('show');
    }
    
    if (mobileDropdown) {
        mobileDropdown.classList.remove('show');
    }
    
    // Update current language display
    const currentLangDisplay = document.getElementById('current-lang-display');
    const mobileLangDisplay = document.getElementById('mobile-current-lang-display');
    
    if (currentLangDisplay) {
        currentLangDisplay.textContent = lang === 'de' ? 'Deutsch' : 'English';
    }
    
    if (mobileLangDisplay) {
        mobileLangDisplay.textContent = lang === 'de' ? 'Deutsch' : 'English';
    }
    
    // Update active state
    const langOptions = document.querySelectorAll('.language-option');
    langOptions.forEach(option => {
        if (option.querySelector('span').textContent === (lang === 'de' ? 'Deutsch' : 'English')) {
            option.classList.add('active');
        } else {
            option.classList.remove('active');
        }
    });
}

// Listen for language changes from the translation system
document.addEventListener('languageChanged', function(e) {
    updateLanguageUI(e.detail.language);
});

// Smooth Scroll
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    for (const link of links) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href === '#') return;
            
            e.preventDefault();
            
            const target = document.querySelector(href);
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    }
});

// Toast Notification System
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    // Set icon based on type
    let icon = 'info-circle';
    if (type === 'success') icon = 'check-circle';
    if (type === 'error') icon = 'exclamation-circle';
    if (type === 'warning') icon = 'exclamation-triangle';
    
    toast.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
    `;
    
    // Add to container
    toastContainer.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast && toast.parentElement) {
            toast.classList.add('toast-hide');
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
}
