/**
 * Modern Header JavaScript für WelluxAI
 * Verbesserte Interaktionen und Effekte
 */

document.addEventListener('DOMContentLoaded', function() {
    // Header-Scroll-Effekt
    const header = document.getElementById('site-header');
    const scrollThreshold = 50;
    
    function handleHeaderScroll() {
        if (window.scrollY > scrollThreshold) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
    
    window.addEventListener('scroll', handleHeaderScroll);
    
    // Initial Check
    handleHeaderScroll();
    
    // Sprachauswahl-Dropdown
    function toggleLanguageDropdown() {
        const dropdown = document.getElementById('language-dropdown');
        dropdown.classList.toggle('show');
    }
    
    // Mobile-Sprachauswahl
    function toggleMobileLanguageDropdown() {
        const dropdown = document.getElementById('mobile-language-dropdown');
        dropdown.classList.toggle('show');
    }
    
    // Click-Handler für Sprachauswahl
    const langSelector = document.querySelector('.current-language');
    if (langSelector) {
        langSelector.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleLanguageDropdown();
        });
    }
    
    const mobileLangSelector = document.querySelector('.mobile-sidebar .current-language');
    if (mobileLangSelector) {
        mobileLangSelector.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleMobileLanguageDropdown();
        });
    }
    
    // Schließen der Dropdowns beim Klick außerhalb
    document.addEventListener('click', function() {
        const dropdown = document.getElementById('language-dropdown');
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
        
        const mobileDropdown = document.getElementById('mobile-language-dropdown');
        if (mobileDropdown && mobileDropdown.classList.contains('show')) {
            mobileDropdown.classList.remove('show');
        }
    });
    
    // Mobile-Menü-Handling
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const mobileOverlay = document.getElementById('mobile-menu-overlay');
    const mobileSidebar = document.getElementById('mobile-sidebar');
    const mobileClose = document.querySelector('.mobile-close');
    const body = document.body;
    
    function toggleMobileMenu() {
        menuToggle.classList.toggle('menu-open');
        mobileSidebar.classList.toggle('show');
        mobileOverlay.classList.toggle('show');
        body.classList.toggle('no-scroll');
    }
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            toggleMobileMenu();
        });
    }
    
    if (mobileClose) {
        mobileClose.addEventListener('click', function() {
            toggleMobileMenu();
        });
    }
    
    if (mobileOverlay) {
        mobileOverlay.addEventListener('click', function() {
            toggleMobileMenu();
        });
    }
    
    // Theme Toggle Funktionalität
    const themeToggle = document.querySelector('.theme-toggle');
    
    function toggleTheme() {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }
    
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Aktiver Link in der Navigation
    function setActiveNavLink() {
        const currentPath = window.location.pathname;
        // Korrekte Selektoren für die Hauptnavigation und mobile Navigation
        const navLinks = document.querySelectorAll('.main-menu a');
        const mobileNavLinks = document.querySelectorAll('.mobile-nav a');
        
        function markActiveLinks(links) {
            links.forEach(link => {
                const linkPath = link.getAttribute('href');
                if (!linkPath) return;
                
                // Entferne bestehende aktive Klasse
                link.classList.remove('active');
                
                // Setze aktive Klasse wenn der Pfad passt
                if (
                    (linkPath !== '#' && currentPath.endsWith(linkPath)) ||
                    (currentPath === '/' && linkPath === 'index.html')
                ) {
                    link.classList.add('active');
                    
                    // Wenn der Link in einem Dropdown-Menü ist, aktiviere auch das übergeordnete Element
                    const parentDropdown = link.closest('.dropdown');
                    if (parentDropdown) {
                        const dropdownToggle = parentDropdown.querySelector('.dropdown-toggle');
                        if (dropdownToggle) {
                            dropdownToggle.classList.add('active');
                        }
                    }
                    
                    // Wenn der Link in einem mobilen Submenu ist
                    const parentMobileDropdown = link.closest('.mobile-submenu');
                    if (parentMobileDropdown) {
                        const parentMobileItem = parentMobileDropdown.closest('.mobile-dropdown');
                        if (parentMobileItem) {
                            const mobileToggle = parentMobileItem.querySelector('a');
                            if (mobileToggle) {
                                mobileToggle.classList.add('active');
                            }
                        }
                    }
                }
            });
        }
        
        markActiveLinks(navLinks);
        markActiveLinks(mobileNavLinks);
    }
    
    setActiveNavLink();
    
    // Lokalisierung aktualisieren wenn Sprache geändert wird
    document.addEventListener('language-changed', function(e) {
        const lang = e.detail.language;
        
        // Sprachauswahl-Display aktualisieren
        const currentLangDisplay = document.querySelector('.current-language span');
        const mobileLangDisplay = document.getElementById('mobile-current-lang-display');
        
        if (currentLangDisplay) {
            currentLangDisplay.textContent = lang === 'de' ? 'Deutsch' : 'English';
        }
        
        if (mobileLangDisplay) {
            mobileLangDisplay.textContent = lang === 'de' ? 'Deutsch' : 'English';
        }
        
        // Aktive Klasse für Sprachoptionen aktualisieren
        const langOptions = document.querySelectorAll('.language-option');
        langOptions.forEach(option => {
            option.classList.remove('active');
            const optionLang = option.getAttribute('data-lang') || 
                               (option.textContent.trim() === 'Deutsch' ? 'de' : 'en');
            
            if (optionLang === lang) {
                option.classList.add('active');
            }
        });
    });
});

// Öffentliche Funktionen
window.toggleLanguageDropdown = function() {
    const dropdown = document.getElementById('language-dropdown');
    dropdown.classList.toggle('show');
};

window.toggleMobileLanguageDropdown = function() {
    const dropdown = document.getElementById('mobile-language-dropdown');
    dropdown.classList.toggle('show');
};

window.toggleMobileMenu = function() {
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const mobileSidebar = document.getElementById('mobile-sidebar');
    const mobileOverlay = document.getElementById('mobile-menu-overlay');
    const body = document.body;
    
    menuToggle.classList.toggle('menu-open');
    mobileSidebar.classList.toggle('show');
    mobileOverlay.classList.toggle('show');
    body.classList.toggle('no-scroll');
};

// Funktion zum Umschalten der mobilen Untermenüs
window.toggleMobileSubmenu = function(submenuId) {
    const submenu = document.getElementById(submenuId);
    if (!submenu) return;
    
    // Toggle für das aktuelle Untermenü
    const isVisible = submenu.style.display === 'block';
    submenu.style.display = isVisible ? 'none' : 'block';
    
    // Finde den übergeordneten Listeneintrag und rotiere das Icon
    const parentItem = submenu.closest('li');
    if (parentItem) {
        const icon = parentItem.querySelector('i');
        if (icon) {
            icon.style.transform = isVisible ? '' : 'rotate(180deg)';
        }
    }
    
    // Schließe andere offene Untermenüs, wenn ein neues geöffnet wird
    if (!isVisible) {
        const allSubmenus = document.querySelectorAll('.mobile-submenu');
        allSubmenus.forEach(menu => {
            if (menu.id !== submenuId && menu.style.display === 'block') {
                menu.style.display = 'none';
                const menuParent = menu.closest('li');
                if (menuParent) {
                    const menuIcon = menuParent.querySelector('i');
                    if (menuIcon) {
                        menuIcon.style.transform = '';
                    }
                }
            }
        });
    }
};

window.toggleTheme = function() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
};
