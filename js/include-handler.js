/**
 * WelluxAI Include-Handler
 * Einheitliche Einbindung von Header und Footer auf allen Seiten
 * Version 2.0 - Vereinfachte robuste Implementation
 */

document.addEventListener('DOMContentLoaded', function() {
    // Header laden
    loadHeader();
    
    // Footer laden
    loadFooter();
    
    // Theme aus localStorage wiederherstellen
    restoreTheme();
});

function loadHeader() {
    const headerPlaceholder = document.getElementById('header-placeholder');
    if (headerPlaceholder) {
        const request = new XMLHttpRequest();
        request.open('GET', 'includes/header.html', false); // Synchroner Aufruf für zuverlässigeres Laden
        
        try {
            request.send();
            if (request.status === 200) {
                headerPlaceholder.innerHTML = request.responseText;
                
                // Nach dem Einfügen des Headers:
                // 1. Theme-Toggle-Button initialisieren
                initThemeToggle();
                
                // 2. Aktive Navigation markieren
                highlightActiveNavLink();
            }
        } catch (error) {
            console.error('Fehler beim Laden des Headers:', error);
        }
    }
}

function loadFooter() {
    const footerPlaceholder = document.getElementById('footer-placeholder');
    if (footerPlaceholder) {
        const request = new XMLHttpRequest();
        request.open('GET', 'includes/footer.html', false); // Synchroner Aufruf für zuverlässigeres Laden
        
        try {
            request.send();
            if (request.status === 200) {
                footerPlaceholder.innerHTML = request.responseText;
            }
        } catch (error) {
            console.error('Fehler beim Laden des Footers:', error);
        }
    }
}

function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

function highlightActiveNavLink() {
    // Aktuellen Pfad ermitteln (z.B. /index.html oder /unterseiten/seite.html)
    const currentPath = window.location.pathname;
    const currentPage = currentPath.split('/').pop() || 'index.html';
    
    // Alle Navigations-Links im Hauptmenü
    const mainMenuLinks = document.querySelectorAll('.main-menu a');
    
    // Alle Navigations-Links im mobilen Menü
    const mobileNavLinks = document.querySelectorAll('.mobile-nav a');
    
    // Funktion zum Markieren aktiver Links
    function markActive(links) {
        links.forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;
            
            // Setze aktive Klasse wenn der Pfad passt
            if (href === currentPage) {
                link.classList.add('active');
                
                // Wenn Link in Dropdown, aktiviere auch den Dropdown-Toggle
                const parentDropdown = link.closest('.dropdown');
                if (parentDropdown) {
                    const dropdownToggle = parentDropdown.querySelector('.dropdown-toggle');
                    if (dropdownToggle) dropdownToggle.classList.add('active');
                }
                
                // Wenn Link in Mobile-Submenu, aktiviere auch den Mobile-Dropdown
                const parentMobileSubmenu = link.closest('.mobile-submenu');
                if (parentMobileSubmenu) {
                    const parentDropdown = parentMobileSubmenu.closest('.mobile-dropdown');
                    if (parentDropdown) {
                        const dropdownToggle = parentDropdown.querySelector('a');
                        if (dropdownToggle) dropdownToggle.classList.add('active');
                    }
                }
            }
        });
    }
    
    // Aktive Links markieren
    markActive(mainMenuLinks);
    markActive(mobileNavLinks);
}

function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    // Theme ändern
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Icon aktualisieren
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.innerHTML = newTheme === 'light' 
            ? '<i class="fas fa-moon"></i>' 
            : '<i class="fas fa-sun"></i>';
    }
}

function restoreTheme() {
    const storedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', storedTheme);
}
