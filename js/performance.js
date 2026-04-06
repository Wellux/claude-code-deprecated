/**
 * WelluxAI Performance Optimierung
 * Implementiert Best Practices für schnellere Ladezeiten und verbesserte Core Web Vitals
 */

document.addEventListener('DOMContentLoaded', function() {
    // Performance-Messung initialisieren
    initPerformanceMonitoring();
    
    // Lazy Loading für Bilder aktivieren
    initLazyLoading();
    
    // Präfetching für häufig besuchte Seiten
    initPrefetching();
    
    // Font-Loading optimieren
    optimizeFontLoading();
});

/**
 * Performance-Monitoring mit Web Vitals API
 * Misst LCP, FID und CLS
 */
function initPerformanceMonitoring() {
    // Nur ausführen, wenn die Web Vitals API unterstützt wird
    if ('performance' in window && 'PerformanceObserver' in window) {
        try {
            // LCP (Largest Contentful Paint) messen
            const lcpObserver = new PerformanceObserver((entryList) => {
                const entries = entryList.getEntries();
                const lastEntry = entries[entries.length - 1];
                console.log('LCP:', lastEntry.startTime / 1000, 'seconds');
                
                // In Analytics senden, wenn verfügbar
                if (window.WelluxAnalytics) {
                    window.WelluxAnalytics.trackMetric('LCP', lastEntry.startTime);
                }
            });
            lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true });
            
            // FID (First Input Delay) messen
            const fidObserver = new PerformanceObserver((entryList) => {
                const entries = entryList.getEntries();
                entries.forEach(entry => {
                    console.log('FID:', entry.processingStart - entry.startTime, 'ms');
                    
                    // In Analytics senden, wenn verfügbar
                    if (window.WelluxAnalytics) {
                        window.WelluxAnalytics.trackMetric('FID', entry.processingStart - entry.startTime);
                    }
                });
            });
            fidObserver.observe({ type: 'first-input', buffered: true });
            
            // CLS (Cumulative Layout Shift) messen
            let cumulativeLayoutShift = 0;
            const clsObserver = new PerformanceObserver((entryList) => {
                for (const entry of entryList.getEntries()) {
                    // Nur wenn der Benutzer nicht gezoomt hat
                    if (!entry.hadRecentInput) {
                        cumulativeLayoutShift += entry.value;
                        console.log('CLS updated:', cumulativeLayoutShift);
                        
                        // In Analytics senden, wenn verfügbar
                        if (window.WelluxAnalytics) {
                            window.WelluxAnalytics.trackMetric('CLS', cumulativeLayoutShift);
                        }
                    }
                }
            });
            clsObserver.observe({ type: 'layout-shift', buffered: true });
        } catch (e) {
            console.error('Performance monitoring error:', e);
        }
    }
}

/**
 * Lazy Loading für Bilder aktivieren
 * Lädt Bilder erst, wenn sie im Viewport sichtbar werden
 */
function initLazyLoading() {
    // Native lazy loading verwenden, falls unterstützt
    if ('loading' in HTMLImageElement.prototype) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.loading = 'lazy';
            img.classList.add('lazy-loaded');
        });
    } else {
        // Fallback mit Intersection Observer
        if ('IntersectionObserver' in window) {
            const lazyImageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const lazyImage = entry.target;
                        if (lazyImage.dataset.src) {
                            lazyImage.src = lazyImage.dataset.src;
                            lazyImage.classList.add('lazy-loaded');
                            lazyImageObserver.unobserve(lazyImage);
                        }
                    }
                });
            });
            
            const lazyImages = document.querySelectorAll('img[data-src]');
            lazyImages.forEach(lazyImage => {
                lazyImageObserver.observe(lazyImage);
            });
        } else {
            // Fallback für ältere Browser ohne IntersectionObserver
            // Alle Bilder sofort laden
            const lazyImages = document.querySelectorAll('img[data-src]');
            lazyImages.forEach(img => {
                img.src = img.dataset.src;
                img.classList.add('lazy-loaded');
            });
        }
    }
    
    // Auch für Hintergrundbilder anwenden
    if ('IntersectionObserver' in window) {
        const lazyBackgrounds = document.querySelectorAll('[data-background]');
        const lazyBackgroundObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const lazyBackground = entry.target;
                    if (lazyBackground.dataset.background) {
                        lazyBackground.style.backgroundImage = `url(${lazyBackground.dataset.background})`;
                        lazyBackground.classList.add('lazy-loaded');
                        lazyBackgroundObserver.unobserve(lazyBackground);
                    }
                }
            });
        });
        
        lazyBackgrounds.forEach(lazyBackground => {
            lazyBackgroundObserver.observe(lazyBackground);
        });
    }
}

/**
 * Prefetching für häufig besuchte Seiten
 * Lädt Seiten vorab, die wahrscheinlich als nächstes besucht werden
 */
function initPrefetching() {
    // Nur auf schnellen Verbindungen prefetchen
    if (navigator.connection && (navigator.connection.saveData || 
        (navigator.connection.effectiveType && navigator.connection.effectiveType !== '4g'))) {
        return;
    }
    
    // Hauptseiten nach einer kurzen Verzögerung prefetchen
    setTimeout(() => {
        const prefetchUrls = [
            'index.html',
            'loesungen.html',
            'erfolgsgeschichten.html',
            'kontakt.html'
        ];
        
        // Bereits besuchte oder aktuelle Seite nicht erneut prefetchen
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        const filteredUrls = prefetchUrls.filter(url => url !== currentPath);
        
        // Nicht mehr als 3 Seiten prefetchen
        const limitedUrls = filteredUrls.slice(0, 3);
        
        // Links erstellen und einfügen
        limitedUrls.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = url;
            document.head.appendChild(link);
        });
    }, 3000); // 3 Sekunden nach Seitenladung starten
    
    // Bei Hover über Navigationslinks die Zielseite prefetchen
    const navLinks = document.querySelectorAll('nav a, .main-menu a');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            const href = link.getAttribute('href');
            if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;
            
            // Prüfen, ob der Link bereits prefetched wurde
            if (!document.querySelector(`link[rel="prefetch"][href="${href}"]`)) {
                const prefetchLink = document.createElement('link');
                prefetchLink.rel = 'prefetch';
                prefetchLink.href = href;
                document.head.appendChild(prefetchLink);
            }
        });
    });
}

/**
 * Font-Loading optimieren
 * Verhindert FOUT (Flash of Unstyled Text) und verbessert CLS
 */
function optimizeFontLoading() {
    // Font-Display Swap über CSS aktivieren
    const fontDisplayStyle = document.createElement('style');
    fontDisplayStyle.textContent = `
        @font-face {
            font-display: swap;
        }
    `;
    document.head.appendChild(fontDisplayStyle);
    
    // Optionales Font-Loading-API verwenden, falls verfügbar
    if ('fonts' in document) {
        // Fonts vorladen und erst anzeigen, wenn sie bereit sind
        Promise.all([
            document.fonts.load('1em Inter'),
            document.fonts.load('1em Montserrat')
        ]).then(() => {
            document.documentElement.classList.add('fonts-loaded');
        }).catch(err => {
            console.warn('Font loading failed, using fallbacks:', err);
            // Bei Fehler trotzdem die Klasse setzen, damit die Seite nicht blockiert wird
            document.documentElement.classList.add('fonts-loaded');
        });
    } else {
        // Fallback: Zeitbasiert die Klasse setzen
        setTimeout(() => {
            document.documentElement.classList.add('fonts-loaded');
        }, 1000); // 1 Sekunde warten
    }
}

/**
 * Script-Loading optimieren
 * Diese Funktion kann von der Hauptseite aufgerufen werden,
 * um zusätzliche Skripte zu laden, ohne den Seitenaufbau zu blockieren
 * 
 * @param {string} src - Pfad zum Skript
 * @param {boolean} defer - Ob das Skript verzögert geladen werden soll
 * @param {function} callback - Funktion, die nach dem Laden ausgeführt wird
 */
function loadScript(src, defer = true, callback) {
    const script = document.createElement('script');
    script.src = src;
    
    if (defer) {
        script.defer = true;
    }
    
    if (callback && typeof callback === 'function') {
        script.onload = callback;
    }
    
    document.body.appendChild(script);
    
    return script;
}

/**
 * CSS-Loading optimieren
 * Diese Funktion kann von der Hauptseite aufgerufen werden,
 * um zusätzliche CSS-Dateien zu laden, ohne den Seitenaufbau zu blockieren
 * 
 * @param {string} href - Pfad zum CSS
 * @param {boolean} critical - Ob das CSS kritisch für die erste Darstellung ist
 */
function loadCSS(href, critical = false) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    
    if (!critical) {
        link.media = 'print';
        link.onload = function() {
            this.media = 'all';
        };
    }
    
    document.head.appendChild(link);
    
    return link;
}
