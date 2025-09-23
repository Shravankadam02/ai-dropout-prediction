/**
 * Main JavaScript for SIH Dropout Prediction System
 * Contains shared utilities and helper functions
 */

// Global variables
let currentToast = null;

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Set up global event listeners
    setupGlobalEventListeners();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Check for URL parameters (e.g., student modal)
    checkUrlParameters();
    
    // Set up periodic updates (every 5 minutes)
    setInterval(updateNotificationCount, 300000);
    
    console.log('SIH Dropout Prediction System initialized');
}

/**
 * Set up global event listeners
 */
function setupGlobalEventListeners() {
    // Handle ESC key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                bootstrap.Modal.getInstance(modal)?.hide();
            });
        }
    });
    
    // Handle clicks outside dropdowns
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
    
    // Auto-hide alerts after 5 seconds
    document.addEventListener('DOMNodeInserted', function(e) {
        if (e.target.classList && e.target.classList.contains('alert')) {
            setTimeout(() => {
                if (e.target && e.target.parentNode) {
                    e.target.remove();
                }
            }, 5000);
        }
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Check URL parameters for actions
 */
function checkUrlParameters() {
    const urlParams = new URLSearchParams(window.location.search);
    const studentId = urlParams.get('student');
    
    if (studentId && typeof showStudentProfile === 'function') {
        // Delay to ensure page is loaded
        setTimeout(() => {
            showStudentProfile(studentId);
        }, 500);
    }
}

/**
 * Show enhanced alert with animations
 */
function showAlert(type, message, duration = 5000) {
    // Create alert element
    const alertId = 'alert-' + Date.now();
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show alert-floating" role="alert">
            <i class="bi bi-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    // Add to page
    document.body.insertAdjacentHTML('beforeend', alertHTML);
    
    // Auto-remove after duration
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }
    }, duration);
}

/**
 * Get appropriate icon for alert type
 */
function getAlertIcon(type) {
    const icons = {
        success: 'check-circle-fill',
        danger: 'exclamation-triangle-fill',
        warning: 'exclamation-circle-fill',
        info: 'info-circle-fill',
        primary: 'info-circle-fill'
    };
    return icons[type] || 'info-circle-fill';
}

/**
 * Enhanced loading functions
 */
function showLoading(target = null) {
    const selectors = target ? [target] : ['.loading-spinner', '.spinner-border'];
    
    selectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.style.display = 'inline-block';
            el.classList.add('fade-in');
        });
    });
}

function hideLoading(target = null) {
    const selectors = target ? [target] : ['.loading-spinner', '.spinner-border'];
    
    selectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.style.display = 'none';
            el.classList.remove('fade-in');
        });
    });
}

/**
 * Create loading overlay for containers
 */
function showLoadingOverlay(container) {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="text-muted">Processing...</div>
        </div>
    `;
    
    const targetContainer = typeof container === 'string' 
        ? document.querySelector(container) 
        : container;
    
    if (targetContainer) {
        targetContainer.style.position = 'relative';
        targetContainer.appendChild(overlay);
    }
    
    return overlay;
}

function hideLoadingOverlay(overlay) {
    if (overlay && overlay.parentNode) {
        overlay.remove();
    }
}

/**
 * Format numbers with appropriate suffixes
 */
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
        return 'Today';
    } else if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else {
        return date.toLocaleDateString();
    }
}

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Update notification count (simulated)
 */
function updateNotificationCount() {
    // In production, this would fetch from an API
    // For demo, simulate random notifications
    const count = Math.floor(Math.random() * 5) + 1;
    const notificationElement = document.getElementById('notificationCount');
    
    if (notificationElement) {
        notificationElement.textContent = count;
        notificationElement.classList.add('pulse-slow');
    }
}

/**
 * Copy text to clipboard with feedback
 */
function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('success', successMessage, 2000);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            showAlert('success', successMessage, 2000);
        } catch (err) {
            showAlert('danger', 'Failed to copy text');
        }
        document.body.removeChild(textArea);
    }
}

/**
 * Export table data to CSV
 */
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) {
        showAlert('danger', 'Table not found');
        return;
    }
    
    const rows = Array.from(table.querySelectorAll('tr'));
    const csv = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        return cells.map(cell => {
            const text = cell.textContent.trim();
            return `"${text.replace(/"/g, '""')}"`;
        }).join(',');
    }).join('\n');
    
    downloadCSV(csv, filename);
}

/**
 * Download CSV content
 */
function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showAlert('success', 'File downloaded successfully');
    }
}

/**
 * Validate form inputs
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const requiredInputs = form.querySelectorAll('[required]');
    
    requiredInputs.forEach(input => {
        const errorElement = document.querySelector(`#${input.id}-error`);
        
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            if (errorElement) {
                errorElement.textContent = 'This field is required';
            }
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            if (errorElement) {
                errorElement.textContent = '';
            }
        }
    });
    
    return isValid;
}

/**
 * Format risk score for display
 */
function formatRiskScore(score) {
    const numScore = parseFloat(score);
    if (isNaN(numScore)) return '0.000';
    return numScore.toFixed(3);
}

/**
 * Get risk level from score
 */
function getRiskLevel(score) {
    const numScore = parseFloat(score);
    if (numScore >= 0.7) return 'High';
    if (numScore >= 0.4) return 'Medium';
    return 'Low';
}

/**
 * Get risk color class
 */
function getRiskColor(level) {
    const colors = {
        'High': 'danger',
        'Medium': 'warning',
        'Low': 'success'
    };
    return colors[level] || 'secondary';
}

/**
 * Animate counting numbers
 */
function animateCounter(element, target, duration = 1000) {
    const start = parseInt(element.textContent) || 0;
    const increment = (target - start) / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

/**
 * Smooth scroll to element
 */
function scrollToElement(elementId, offset = 0) {
    const element = document.getElementById(elementId);
    if (element) {
        const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
        const offsetPosition = elementPosition - offset;
        
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

/**
 * Toggle sidebar on mobile
 */
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}

/**
 * Print current page
 */
function printPage() {
    window.print();
}

/**
 * Check if device is mobile
 */
function isMobile() {
    return window.innerWidth <= 768;
}

/**
 * Check if device has touch capability
 */
function isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

/**
 * Get browser information
 */
function getBrowserInfo() {
    const ua = navigator.userAgent;
    let browserName = 'Unknown';
    
    if (ua.indexOf('Chrome') > -1) browserName = 'Chrome';
    else if (ua.indexOf('Firefox') > -1) browserName = 'Firefox';
    else if (ua.indexOf('Safari') > -1) browserName = 'Safari';
    else if (ua.indexOf('Edge') > -1) browserName = 'Edge';
    
    return {
        name: browserName,
        userAgent: ua,
        isMobile: isMobile(),
        isTouch: isTouchDevice()
    };
}

/**
 * Log system information (for debugging)
 */
function logSystemInfo() {
    const info = getBrowserInfo();
    console.log('System Information:', {
        browser: info.name,
        mobile: info.isMobile,
        touch: info.isTouch,
        viewport: {
            width: window.innerWidth,
            height: window.innerHeight
        },
        timestamp: new Date().toISOString()
    });
}

// Expose functions globally
window.SIHApp = {
    showAlert,
    showLoading,
    hideLoading,
    showLoadingOverlay,
    hideLoadingOverlay,
    formatNumber,
    formatDate,
    debounce,
    copyToClipboard,
    exportTableToCSV,
    validateForm,
    formatRiskScore,
    getRiskLevel,
    getRiskColor,
    animateCounter,
    scrollToElement,
    toggleSidebar,
    printPage,
    isMobile,
    isTouchDevice,
    getBrowserInfo,
    logSystemInfo
};

// Log system info on load (for debugging)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    logSystemInfo();
}