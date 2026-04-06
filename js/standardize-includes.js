/**
 * Standardisierter Header- und Footer-Loader für WelluxAI
 * Diese Datei muss auf ALLEN HTML-Seiten eingebunden werden
 */

document.addEventListener('DOMContentLoaded', function() {
    // Header sofort laden
    const headerPlaceholder = document.getElementById('header-placeholder');
    if (headerPlaceholder) {
        loadInclude('includes/header.html', headerPlaceholder, function() {
            // Nach dem Laden des Headers:
            initHeaderFunctions();
        });
    }
    
    // Footer sofort laden
    const footerPlaceholder = document.getElementById('footer-placeholder');
    if (footerPlaceholder) {
        loadInclude('includes/footer.html', footerPlaceholder);
    }
    
    // Theme aus localStorage wiederherstellen
    restoreTheme();
});

// Hilfsfunktion zum Laden von Includes
function loadInclude(url, targetElement, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                targetElement.innerHTML = xhr.responseText;
                if (typeof callback === 'function') callback();
            } else {
                console.error('Fehler beim Laden von ' + url + ': ' + xhr.status);
            }
        }
    };
    xhr.onerror = function() {
        console.error('Fehler beim Laden von ' + url);
    };
    xhr.send();
}

// Header-Funktionen initialisieren
function initHeaderFunctions() {
    // Theme-Toggle aktivieren
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Mobiles Menü aktivieren
    window.toggleMobileMenu = function() {
        const menuToggle = document.getElementById('mobile-menu-toggle');
        const mobileSidebar = document.getElementById('mobile-sidebar');
        const mobileOverlay = document.getElementById('mobile-menu-overlay');
        const body = document.body;
        
        if (menuToggle && mobileSidebar && mobileOverlay) {
            menuToggle.classList.toggle('menu-open');
            mobileSidebar.classList.toggle('show');
            mobileOverlay.classList.toggle('show');
            body.classList.toggle('no-scroll');
        }
    }
    
    // Mobile Dropdown-Menüs
    window.toggleMobileSubmenu = function(submenuId) {
        const submenu = document.getElementById(submenuId);
        if (submenu) {
            if (submenu.style.display === 'block') {
                submenu.style.display = 'none';
            } else {
                // Alle anderen Untermenüs schließen
                const allSubmenus = document.querySelectorAll('.mobile-submenu');
                allSubmenus.forEach(menu => {
                    if (menu.id !== submenuId) {
                        menu.style.display = 'none';
                    }
                });
                submenu.style.display = 'block';
            }
        }
    }
    
    // Aktive Navigation markieren
    highlightActiveNavLink();
    
    // Sprachauswahl-Dropdown
    window.toggleLanguageDropdown = function() {
        const dropdown = document.getElementById('language-dropdown');
        if (dropdown) {
            dropdown.classList.toggle('show');
        }
    }
    
    // Mobile Sprachauswahl-Dropdown
    window.toggleMobileLanguageDropdown = function() {
        const dropdown = document.getElementById('mobile-language-dropdown');
        if (dropdown) {
            dropdown.classList.toggle('show');
        }
    }
    
    // Login-Navigation aktualisieren
    updateLoginNavLinks();
}

// Aktive Links in der Navigation markieren
function highlightActiveNavLink() {
    const currentPath = window.location.pathname;
    const currentPage = currentPath.split('/').pop() || 'index.html';
    
    // Hauptmenü-Links
    const mainMenuLinks = document.querySelectorAll('.main-menu a');
    mainMenuLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (!href) return;
        
        if (href === currentPage) {
            link.classList.add('active');
            
            // Dropdown-Eltern aktivieren
            const parentDropdown = link.closest('.dropdown');
            if (parentDropdown) {
                const dropdownToggle = parentDropdown.querySelector('.dropdown-toggle');
                if (dropdownToggle) dropdownToggle.classList.add('active');
            }
        }
    });
    
    // Mobile-Menü-Links
    const mobileLinks = document.querySelectorAll('.mobile-nav a');
    mobileLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (!href || href === 'javascript:void(0)') return;
        
        if (href === currentPage) {
            link.classList.add('active');
            
            // Mobile Dropdown-Eltern aktivieren
            const parentSubmenu = link.closest('.mobile-submenu');
            if (parentSubmenu) {
                const parentDropdown = parentSubmenu.closest('.mobile-dropdown');
                if (parentDropdown) {
                    const dropdownLink = parentDropdown.querySelector('a');
                    if (dropdownLink) dropdownLink.classList.add('active');
                }
            }
        }
    });
}

// Login-Navigation aktualisieren
function updateLoginNavLinks() {
    // Verzögerung hinzufügen, um sicherzustellen, dass user-system.js geladen ist
    setTimeout(function() {
        if (typeof WelluxUsers !== 'undefined') {
            const isLoggedIn = WelluxUsers.isLoggedIn();
            const loginNavLink = document.getElementById('loginNavLink');
            const mobileLoginNavLink = document.getElementById('mobileLoginNavLink');
            
            if (isLoggedIn) {
                if (loginNavLink) {
                    loginNavLink.textContent = 'Dashboard';
                    loginNavLink.href = 'dashboard.html';
                }
                if (mobileLoginNavLink) {
                    mobileLoginNavLink.textContent = 'Dashboard';
                    mobileLoginNavLink.setAttribute('onclick', "window.location.href='dashboard.html'; toggleMobileMenu();");
                }
            } else {
                if (loginNavLink) {
                    loginNavLink.textContent = 'Konto';
                    loginNavLink.href = 'login.html';
                }
                if (mobileLoginNavLink) {
                    mobileLoginNavLink.textContent = 'Konto';
                    mobileLoginNavLink.setAttribute('onclick', "window.location.href='login.html'; toggleMobileMenu();");
                }
            }
        }
    }, 300);
}

// Theme wechseln
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Theme-Toggle-Icon aktualisieren
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        const darkIcon = themeToggle.querySelector('.dark-icon');
        const lightIcon = themeToggle.querySelector('.light-icon');
        
        if (darkIcon && lightIcon) {
            if (newTheme === 'light') {
                darkIcon.style.display = 'inline-block';
                lightIcon.style.display = 'none';
            } else {
                darkIcon.style.display = 'none';
                lightIcon.style.display = 'inline-block';
            }
        }
    }
}

// Gespeichertes Theme wiederherstellen
function restoreTheme() {
    const storedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', storedTheme);
    
    // Icons aktualisieren
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        const darkIcon = themeToggle.querySelector('.dark-icon');
        const lightIcon = themeToggle.querySelector('.light-icon');
        
        if (darkIcon && lightIcon) {
            if (storedTheme === 'light') {
                darkIcon.style.display = 'inline-block';
                lightIcon.style.display = 'none';
            } else {
                darkIcon.style.display = 'none';
                lightIcon.style.display = 'inline-block';
            }
        }
    }
}
