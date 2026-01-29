/**
 * GitHub Webhook Monitor - Frontend JavaScript
 * 
 * This script polls the backend API every 15 seconds to fetch webhook events
 * and displays them in a user-friendly format.
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';
const POLL_INTERVAL = 15000; // 15 seconds in milliseconds

// State
let pollTimer = null;

/**
 * Format timestamp to human-readable format
 * Example: "1st April 2021 - 9:30 PM UTC"
 * 
 * @param {string} isoTimestamp - ISO 8601 timestamp string
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(isoTimestamp) {
    const date = new Date(isoTimestamp);
    
    // Get day with suffix (1st, 2nd, 3rd, 4th, etc.)
    const day = date.getUTCDate();
    const daySuffix = getDaySuffix(day);
    
    // Get month name
    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    const month = monthNames[date.getUTCMonth()];
    
    // Get year
    const year = date.getUTCFullYear();
    
    // Get time in 12-hour format
    let hours = date.getUTCHours();
    const minutes = date.getUTCMinutes().toString().padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12 || 12; // Convert to 12-hour format
    
    return `${day}${daySuffix} ${month} ${year} - ${hours}:${minutes} ${ampm} UTC`;
}

/**
 * Get day suffix (st, nd, rd, th)
 * 
 * @param {number} day - Day of the month
 * @returns {string} Suffix
 */
function getDaySuffix(day) {
    if (day >= 11 && day <= 13) {
        return 'th';
    }
    switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
    }
}

/**
 * Format event message based on action type
 * 
 * @param {object} event - Event object from API
 * @returns {string} Formatted message
 */
function formatEventMessage(event) {
    const timestamp = formatTimestamp(event.timestamp);
    
    switch (event.action) {
        case 'PUSH':
            return `${event.author} pushed to ${event.to_branch} on ${timestamp}`;
        
        case 'PULL_REQUEST':
            return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${timestamp}`;
        
        case 'MERGE':
            return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${timestamp}`;
        
        default:
            return `${event.author} performed ${event.action} on ${timestamp}`;
    }
}

/**
 * Create HTML element for a single event
 * 
 * @param {object} event - Event object from API
 * @returns {string} HTML string
 */
function createEventElement(event) {
    const actionClass = event.action.toLowerCase().replace('_', '-');
    const message = formatEventMessage(event);
    
    return `
        <div class="event-item ${actionClass}">
            <div class="event-message">${message}</div>
            <div class="event-meta">
                <span class="event-badge ${actionClass}">${event.action}</span>
                <span>Request ID: ${event.request_id}</span>
            </div>
        </div>
    `;
}

/**
 * Update connection status indicator
 * 
 * @param {boolean} isConnected - Connection status
 */
function updateConnectionStatus(isConnected) {
    const statusElement = document.getElementById('connection-status');
    if (isConnected) {
        statusElement.textContent = 'Connected';
        statusElement.className = 'status-value connected';
    } else {
        statusElement.textContent = 'Disconnected';
        statusElement.className = 'status-value disconnected';
    }
}

/**
 * Update last updated timestamp
 */
function updateLastUpdated() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('last-updated').textContent = timeString;
}

/**
 * Fetch events from the API and update the UI
 */
async function fetchAndDisplayEvents() {
    try {
        const response = await fetch(`${API_BASE_URL}/events`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update connection status
        updateConnectionStatus(true);
        
        // Update event count
        document.getElementById('event-count').textContent = data.count;
        
        // Update last updated time
        updateLastUpdated();
        
        // Display events
        const eventsList = document.getElementById('events-list');
        
        if (data.events.length === 0) {
            eventsList.innerHTML = '<div class="no-events">No events yet. Waiting for GitHub webhooks...</div>';
        } else {
            // Events are already sorted by timestamp (newest first) from the backend
            const eventsHTML = data.events.map(event => createEventElement(event)).join('');
            eventsList.innerHTML = eventsHTML;
        }
        
    } catch (error) {
        console.error('Error fetching events:', error);
        updateConnectionStatus(false);
        
        const eventsList = document.getElementById('events-list');
        eventsList.innerHTML = `
            <div class="loading">
                Failed to connect to backend. Please ensure the Flask server is running.
                <br><br>
                Error: ${error.message}
            </div>
        `;
    }
}

/**
 * Start polling for events
 */
function startPolling() {
    // Fetch immediately on load
    fetchAndDisplayEvents();
    
    // Then poll every 15 seconds
    pollTimer = setInterval(fetchAndDisplayEvents, POLL_INTERVAL);
    
    console.log(`Started polling backend every ${POLL_INTERVAL / 1000} seconds`);
}

/**
 * Stop polling (useful for cleanup)
 */
function stopPolling() {
    if (pollTimer) {
        clearInterval(pollTimer);
        pollTimer = null;
        console.log('Stopped polling');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('GitHub Webhook Monitor initialized');
    startPolling();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    stopPolling();
});