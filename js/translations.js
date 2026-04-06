/**
 * Übersetzungsverwaltung für die WelluxAI Website
 * Ermöglicht das dynamische Wechseln zwischen Deutsch und Englisch
 */

// Verfügbare Sprachen
const availableLanguages = ['de', 'en'];

// Übersetzungen
const translations = {
    // Deutsch (Standardsprache)
    'de': {
        // Navigation
        'nav_home': 'Startseite',
        'nav_tools': 'KI-Tools',
        'nav_prompts': 'Prompt-Bibliothek',
        'nav_roi': 'ROI-Rechner',
        'nav_assessment': 'KI-Readiness Check',
        'nav_blog': 'Blog',
        'nav_account': 'Konto',
        'nav_dashboard': 'Dashboard',
        'nav_contact': 'Kontakt',
        
        // Buttons
        'btn_learn_more': 'Mehr erfahren',
        'btn_contact_us': 'Kontakt aufnehmen',
        'btn_calculate': 'Berechnen',
        'btn_reset': 'Zurücksetzen',
        'btn_send': 'Senden',
        'btn_read_more': 'Weiterlesen',
        'btn_share': 'Teilen',
        
        // Homepage
        'hero_title': 'KI-Lösungen für kleine und mittelständische Unternehmen',
        'hero_subtitle': 'Wir helfen Ihnen, KI-Technologien effektiv zu nutzen und Ihre Geschäftsprozesse zu optimieren.',
        'services_title': 'Unsere Dienstleistungen',
        'services_subtitle': 'Entdecken Sie, wie KI Ihr Unternehmen voranbringen kann',
        'blog_title': 'Aktuelle Blogbeiträge',
        'blog_subtitle': 'Informieren Sie sich über die neuesten Trends und Entwicklungen im Bereich KI',
        
        // Formular-Labels
        'form_name': 'Name',
        'form_email': 'E-Mail',
        'form_subject': 'Betreff',
        'form_message': 'Nachricht',
        'form_privacy': 'Ich stimme der Datenschutzerklärung zu',
        'form_submit': 'Nachricht senden',
        
        // Toasts/Benachrichtigungen
        'toast_success': 'Erfolgreich!',
        'toast_error': 'Fehler!',
        'toast_contact_success': 'Ihre Nachricht wurde erfolgreich gesendet. Wir werden uns in Kürze bei Ihnen melden.',
        'toast_prompt_copied': 'Prompt in die Zwischenablage kopiert!',
        'toast_prompt_saved': 'Prompt wurde erfolgreich gespeichert!',
        'toast_login_required': 'Sie müssen angemeldet sein, um diese Funktion zu nutzen.',
        'toast_prompt_title_required': 'Bitte geben Sie einen Titel für den Prompt ein.',
        'toast_google_signin_error': 'Bei der Anmeldung mit Google ist ein Fehler aufgetreten.',
        'toast_google_login_success': 'Sie haben sich erfolgreich mit Google angemeldet.',
        'toast_google_register_success': 'Ihr Google-Konto wurde erfolgreich verknüpft.',
        'login_with_social': 'oder anmelden mit',
        'register_with_social': 'oder registrieren mit',
        'login_oauth_error': 'Dieses Konto verwendet Social Login. Bitte nutzen Sie die entsprechende Anmeldeoption.',
        'login_oauth_account_exists': 'Ein Konto mit dieser E-Mail-Adresse existiert bereits. Bitte melden Sie sich an.',
        'login_oauth_account_create': 'Kein Konto mit dieser E-Mail-Adresse gefunden. Ein neues Konto wird erstellt.',
        'auth_type_local': 'Lokales Konto',
        'auth_type_google': 'Google-Konto',
        'auth_type_oauth': 'Social Login',
        'password_oauth_disabled': 'Nicht verfügbar für Social-Login-Konten',
        'prompts_save': 'Speichern',
        'prompts_save_title': 'Prompt speichern',
        'prompts_save_name': 'Titel',
        'prompts_save_category': 'Kategorie',
        'btn_cancel': 'Abbrechen',
        
        // Footer
        'footer_about': 'Über uns',
        'footer_about_text': 'WelluxAI unterstützt kleine und mittelständische Unternehmen dabei, KI-Technologien effizient und gewinnbringend einzusetzen.',
        'footer_links': 'Quick Links',
        'footer_newsletter': 'Newsletter',
        'footer_newsletter_text': 'Abonnieren Sie unseren Newsletter für aktuelle Informationen zu KI-Trends und Veranstaltungen.',
        'footer_newsletter_placeholder': 'Ihre E-Mail-Adresse',
        'footer_newsletter_button': 'Abonnieren',
        'footer_copyright': 'Alle Rechte vorbehalten',
        
        // Tools
        'tools_title': 'KI-Tools Directory',
        'tools_subtitle': 'Entdecken Sie unsere kuratierte Sammlung von KI-Tools für verschiedene Geschäftsbereiche',
        'tools_filter_all': 'Alle Kategorien',
        'tools_search_placeholder': 'Tool suchen...',
        
        // Prompts
        'prompts_title': 'Prompt-Bibliothek',
        'prompts_subtitle': 'Durchsuchen Sie unsere Sammlung von bewährten Prompts für verschiedene KI-Anwendungen',
        'prompts_filter_all': 'Alle Kategorien',
        'prompts_search_placeholder': 'Prompt suchen...',
        'prompts_copy': 'Kopieren',
        'prompts_copied': 'Kopiert!',
        
        // ROI Calculator
        'roi_title': 'ROI-Rechner',
        'roi_subtitle': 'Berechnen Sie den Return on Investment Ihrer KI-Implementierung',
        'roi_cost_section': 'Kosten',
        'roi_savings_section': 'Einsparungen',
        'roi_results_section': 'Ergebnisse',
        
        // Assessment
        'assessment_title': 'KI-Readiness Assessment',
        'assessment_subtitle': 'Bewältigen Sie die Herausforderungen der KI-Integration mit unserem Assessment',
        'assessment_start': 'Assessment starten',
        
        // Blog
        'blog_category': 'Kategorie',
        'blog_search': 'Suchen...',
        'blog_no_results': 'Keine Blogbeiträge gefunden. Bitte versuchen Sie eine andere Suchanfrage.',
        'blog_prev': 'Vorherige',
        'blog_next': 'Nächste',
        'blog_page': 'Seite',
        'blog_of': 'von',
        
        // Login & Benutzerkonto
        'login_title': 'Anmelden oder Registrieren',
        'login_subtitle': 'Zugang zu Ihrem persönlichen Dashboard und gespeicherten Prompts',
        'login_tab': 'Anmelden',
        'register_tab': 'Registrieren',
        'form_name': 'Name',
        'form_email': 'E-Mail',
        'form_password': 'Passwort',
        'form_password_confirm': 'Passwort bestätigen',
        'form_privacy': 'Ich stimme der <a href="datenschutz.html">Datenschutzerklärung</a> zu und bin damit einverstanden, dass meine Daten gemäß dieser verarbeitet werden.',
        'btn_login': 'Anmelden',
        'btn_register': 'Registrieren',
        'btn_save': 'Speichern',
        'forgot_password': 'Passwort vergessen?',
        'login_footer': 'Durch die Anmeldung oder Registrierung stimmen Sie unseren Nutzungsbedingungen zu.',
        'form_password_change': 'Passwort ändern',
        
        // Dashboard
        'dashboard_saved_prompts': 'Gespeicherte Prompts',
        'dashboard_profile': 'Profil bearbeiten',
        'dashboard_preferences': 'Einstellungen',
        'dashboard_logout': 'Abmelden',
        'no_prompts_title': 'Keine gespeicherten Prompts',
        'no_prompts_text': 'Sie haben noch keine Prompts gespeichert. Besuchen Sie unsere Prompt-Bibliothek, um nützliche Prompts zu entdecken.',
        'browse_prompts': 'Prompt-Bibliothek entdecken',
        'form_theme': 'Theme',
        'form_language': 'Sprache',
        'theme_light': 'Hell',
        'theme_dark': 'Dunkel',
        'lang_deutsch': 'Deutsch',
        'lang_english': 'English'
    },
    
    // Englisch
    'en': {
        // Navigation
        'nav_home': 'Home',
        'nav_tools': 'AI Tools',
        'nav_prompts': 'Prompt Library',
        'nav_roi': 'ROI Calculator',
        'nav_assessment': 'AI Readiness Check',
        'nav_blog': 'Blog',
        'nav_account': 'Account',
        'nav_dashboard': 'Dashboard',
        'nav_contact': 'Contact',
        
        // Buttons
        'btn_learn_more': 'Learn more',
        'btn_contact_us': 'Contact us',
        'btn_calculate': 'Calculate',
        'btn_reset': 'Reset',
        'btn_send': 'Send',
        'btn_read_more': 'Read more',
        'btn_share': 'Share',
        
        // Homepage
        'hero_title': 'AI Solutions for Small and Medium-sized Businesses',
        'hero_subtitle': 'We help you effectively use AI technologies to optimize your business processes.',
        'services_title': 'Our Services',
        'services_subtitle': 'Discover how AI can advance your business',
        'blog_title': 'Latest Blog Posts',
        'blog_subtitle': 'Stay informed about the latest trends and developments in AI',
        
        // Formular-Labels
        'form_name': 'Name',
        'form_email': 'Email',
        'form_subject': 'Subject',
        'form_message': 'Message',
        'form_privacy': 'I agree to the privacy policy',
        'form_submit': 'Send message',
        
        // Toasts/Benachrichtigungen
        'toast_success': 'Success!',
        'toast_error': 'Error!',
        'toast_contact_success': 'Your message has been sent successfully. We will get back to you shortly.',
        'toast_prompt_copied': 'Prompt copied to clipboard!',
        'toast_prompt_saved': 'Prompt saved successfully!',
        'toast_login_required': 'You need to be logged in to use this feature.',
        'toast_prompt_title_required': 'Please enter a title for the prompt.',
        'toast_google_signin_error': 'An error occurred while signing in with Google.',
        'toast_google_login_success': 'You have successfully signed in with Google.',
        'toast_google_register_success': 'Your Google account has been successfully linked.',
        'login_with_social': 'or sign in with',
        'register_with_social': 'or register with',
        'login_oauth_error': 'This account uses social login. Please use the corresponding login option.',
        'login_oauth_account_exists': 'An account with this email already exists. Please sign in.',
        'login_oauth_account_create': 'No account found with this email. A new account will be created.',
        'auth_type_local': 'Local Account',
        'auth_type_google': 'Google Account',
        'auth_type_oauth': 'Social Login',
        'password_oauth_disabled': 'Not available for social login accounts',
        'prompts_save': 'Save',
        'prompts_save_title': 'Save Prompt',
        'prompts_save_name': 'Title',
        'prompts_save_category': 'Category',
        'btn_cancel': 'Cancel',
        
        // Footer
        'footer_about': 'About us',
        'footer_about_text': 'WelluxAI helps small and medium-sized businesses use AI technologies efficiently and profitably.',
        'footer_links': 'Quick Links',
        'footer_newsletter': 'Newsletter',
        'footer_newsletter_text': 'Subscribe to our newsletter for current information on AI trends and events.',
        'footer_newsletter_placeholder': 'Your email address',
        'footer_newsletter_button': 'Subscribe',
        'footer_copyright': 'All rights reserved',
        
        // Tools
        'tools_title': 'AI Tools Directory',
        'tools_subtitle': 'Explore our curated collection of AI tools for various business areas',
        'tools_filter_all': 'All categories',
        'tools_search_placeholder': 'Search tool...',
        
        // Prompts
        'prompts_title': 'Prompt Library',
        'prompts_subtitle': 'Browse our collection of proven prompts for various AI applications',
        'prompts_filter_all': 'All categories',
        'prompts_search_placeholder': 'Search prompt...',
        'prompts_copy': 'Copy',
        'prompts_copied': 'Copied!',
        
        // ROI Calculator
        'roi_title': 'ROI Calculator',
        'roi_subtitle': 'Calculate the return on investment of your AI implementation',
        'roi_cost_section': 'Costs',
        'roi_savings_section': 'Savings',
        'roi_results_section': 'Results',
        
        // Assessment
        'assessment_title': 'AI Readiness Assessment',
        'assessment_subtitle': 'Overcome the challenges of AI integration with our assessment',
        'assessment_start': 'Start assessment',
        
        // Blog
        'blog_category': 'Category',
        'blog_search': 'Search...',
        'blog_no_results': 'No blog posts found. Please try a different search query.',
        'blog_prev': 'Previous',
        'blog_next': 'Next',
        'blog_page': 'Page',
        'blog_of': 'of',
        
        // Login & User Account
        'login_title': 'Login or Register',
        'login_subtitle': 'Access your personal dashboard and saved prompts',
        'login_tab': 'Login',
        'register_tab': 'Register',
        'form_name': 'Name',
        'form_email': 'Email',
        'form_password': 'Password',
        'form_password_confirm': 'Confirm Password',
        'form_privacy': 'I agree to the <a href="privacy.html">Privacy Policy</a> and consent to the processing of my data in accordance with it.',
        'btn_login': 'Login',
        'btn_register': 'Register',
        'btn_save': 'Save',
        'forgot_password': 'Forgot password?',
        'login_footer': 'By logging in or registering, you agree to our Terms of Service.',
        'form_password_change': 'Change Password',
        
        // Dashboard
        'dashboard_saved_prompts': 'Saved Prompts',
        'dashboard_profile': 'Edit Profile',
        'dashboard_preferences': 'Preferences',
        'dashboard_logout': 'Logout',
        'no_prompts_title': 'No Saved Prompts',
        'no_prompts_text': 'You haven\'t saved any prompts yet. Visit our Prompt Library to discover useful prompts.',
        'browse_prompts': 'Browse Prompt Library',
        'form_theme': 'Theme',
        'form_language': 'Language',
        'theme_light': 'Light',
        'theme_dark': 'Dark',
        'lang_deutsch': 'Deutsch',
        'lang_english': 'English'
    }
};

/**
 * Aktuell ausgewählte Sprache (aus lokalem Speicher oder Standardsprache)
 */
let currentLanguage = localStorage.getItem('language') || 'de';

/**
 * Überprüft, ob die gewählte Sprache verfügbar ist und setzt ggf. die Standardsprache
 */
if (!availableLanguages.includes(currentLanguage)) {
    currentLanguage = 'de';
    localStorage.setItem('language', currentLanguage);
}

/**
 * Wechselt die Sprache der Website
 * @param {string} lang - Sprachcode ('de' oder 'en')
 */
function setLanguage(lang) {
    if (!availableLanguages.includes(lang)) {
        console.error(`Sprache ${lang} nicht verfügbar. Verfügbare Sprachen: ${availableLanguages.join(', ')}`);
        return;
    }
    
    // Sprache speichern
    currentLanguage = lang;
    localStorage.setItem('language', lang);
    
    // Alle Elemente mit dem data-i18n Attribut aktualisieren
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang][key]) {
            // Element-Typ bestimmen und entsprechend aktualisieren
            if (element.tagName === 'INPUT' && element.getAttribute('type') === 'placeholder') {
                element.setAttribute('placeholder', translations[lang][key]);
            } else {
                element.textContent = translations[lang][key];
            }
        }
    });
    
    // Sprach-Buttons aktualisieren
    document.querySelectorAll('.language-switcher button').forEach(button => {
        if (button.getAttribute('data-lang') === lang) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
    
    // Sprachumschaltung-Event auslösen
    document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
    
    console.log(`Sprache geändert auf: ${lang}`);
}

/**
 * Gibt die Übersetzung für einen bestimmten Schlüssel zurück
 * @param {string} key - Übersetzungsschlüssel
 * @returns {string} Übersetzter Text
 */
function translate(key) {
    if (!translations[currentLanguage][key]) {
        console.warn(`Übersetzung für Schlüssel "${key}" in Sprache "${currentLanguage}" nicht gefunden.`);
        return key;
    }
    return translations[currentLanguage][key];
}

/**
 * Initialisiert die Übersetzungsfunktionalität
 */
function initTranslations() {
    // Erste Übersetzung anwenden
    setLanguage(currentLanguage);
    
    // Event-Listener für Sprachumschaltung hinzufügen
    document.querySelectorAll('.language-switcher button').forEach(button => {
        button.addEventListener('click', () => {
            const lang = button.getAttribute('data-lang');
            setLanguage(lang);
        });
    });
    
    console.log('Übersetzungsmanager initialisiert');
}

// Beim Laden der Seite initialisieren
document.addEventListener('DOMContentLoaded', initTranslations);

// Funktionen für externe Nutzung exportieren
window.WelluxTranslations = {
    setLanguage,
    translate,
    getCurrentLanguage: () => currentLanguage
};
