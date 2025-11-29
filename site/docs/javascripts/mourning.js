/**
 * Mourning Mode Toggle with Cookie Persistence
 * Handles grayscale filter toggle and remembers user preference across pages
 */

(function() {
    'use strict';
    
    // Cookie helper functions
    const CookieManager = {
        set: function(name, value, days) {
            let expires = '';
            if (days) {
                const date = new Date();
                date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                expires = '; expires=' + date.toUTCString();
            }
            document.cookie = name + '=' + (value || '') + expires + '; path=/';
        },
        
        get: function(name) {
            const nameEQ = name + '=';
            const ca = document.cookie.split(';');
            for (let i = 0; i < ca.length; i++) {
                let c = ca[i];
                while (c.charAt(0) === ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
            }
            return null;
        },
        
        remove: function(name) {
            document.cookie = name + '=; Max-Age=-99999999; path=/';
        }
    };
    
    // Mourning mode state management
    const MourningMode = {
        COOKIE_NAME: 'mourning_mode_disabled',
        COOKIE_DAYS: 30,
        
        isDisabled: function() {
            return CookieManager.get(this.COOKIE_NAME) === 'true';
        },
        
        setDisabled: function(disabled) {
            if (disabled) {
                CookieManager.set(this.COOKIE_NAME, 'true', this.COOKIE_DAYS);
            } else {
                CookieManager.remove(this.COOKIE_NAME);
            }
        },
        
        applyState: function() {
            const html = document.documentElement;
            if (this.isDisabled()) {
                html.classList.remove('mourning-mode');
            } else {
                html.classList.add('mourning-mode');
            }
            this.updateToggleButton();
        },
        
        toggle: function() {
            const newState = !this.isDisabled();
            this.setDisabled(newState);
            this.applyState();
        },
        
        updateToggleButton: function() {
            const button = document.getElementById('mourning-toggle-btn');
            if (button) {
                if (this.isDisabled()) {
                    button.textContent = 'Enable Grayscale';
                    button.setAttribute('aria-label', 'Enable mourning grayscale filter');
                } else {
                    button.textContent = 'Disable Grayscale';
                    button.setAttribute('aria-label', 'Disable mourning grayscale filter for better accessibility');
                }
            }
        }
    };
    
    // Apply state immediately to prevent flash
    MourningMode.applyState();
    
    // Initialize when DOM is ready
    function initialize() {
        // Apply state again after DOM loads
        MourningMode.applyState();
        
        // Attach event listener to toggle button
        const toggleButton = document.getElementById('mourning-toggle-btn');
        if (toggleButton) {
            toggleButton.addEventListener('click', function(e) {
                e.preventDefault();
                MourningMode.toggle();
            });
        }
    }
    
    // Run initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }
    
    // Also run on page navigation for SPA-like behavior
    document.addEventListener('DOMContentSwitch', initialize);
})();
