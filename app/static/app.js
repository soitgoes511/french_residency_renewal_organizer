/**
 * French Residence Permit Tracker - Frontend Application
 * Enhanced with profile selection, notes, and due dates.
 */

// API base URL
const API_BASE = '/api';

// State
let currentPermitType = null;
let documents = [];
let categories = {};
let profiles = {};
let selectedProfiles = ['common'];
let currentEditingDocId = null;

// DOM Elements
const permitTypeSelect = document.getElementById('permitTypeSelect');
const permitDescription = document.getElementById('permitDescription');
const profileSection = document.getElementById('profileSection');
const profileList = document.getElementById('profileList');
const progressSection = document.getElementById('progressSection');
const progressBar = document.getElementById('progressBar');
const progressPercentage = document.getElementById('progressPercentage');
const progressStats = document.getElementById('progressStats');
const resetButton = document.getElementById('resetButton');
const documentsSection = document.getElementById('documentsSection');
const documentsList = document.getElementById('documentsList');
const linksSection = document.getElementById('linksSection');
const importantLinks = document.getElementById('importantLinks');
const lastVerified = document.getElementById('lastVerified');
const notesModal = document.getElementById('notesModal');
const notesInput = document.getElementById('notesInput');
const notesDocName = document.getElementById('notesDocName');
const dueDateInput = document.getElementById('dueDateInput');
const clearDueDateBtn = document.getElementById('clearDueDate');

// Initialize the application
async function init() {
    try {
        // Load categories and profiles
        await Promise.all([
            loadCategories(),
            loadProfiles(),
            loadMetadata()
        ]);

        // Load permit types
        await loadPermitTypes();

        // Load important links
        await loadImportantLinks();

        // Load user settings
        await loadUserSettings();

        // Set up event listeners
        setupEventListeners();
    } catch (error) {
        console.error('Failed to initialize application:', error);
        showError('Failed to load application. Please refresh the page.');
    }
}

// Load categories
async function loadCategories() {
    const response = await fetch(`${API_BASE}/categories`);
    const data = await response.json();
    if (data.success) {
        categories = data.data;
    }
}

// Load profiles
async function loadProfiles() {
    const response = await fetch(`${API_BASE}/profiles`);
    const data = await response.json();
    if (data.success) {
        profiles = data.data;
    }
}

// Load metadata (last verified date)
async function loadMetadata() {
    try {
        const response = await fetch(`${API_BASE}/metadata`);
        const data = await response.json();
        if (data.success && data.data.last_verified) {
            lastVerified.textContent = `Requirements last verified: ${data.data.last_verified}`;
            lastVerified.style.display = 'block';
        }
    } catch (e) {
        // Metadata is optional
    }
}

// Load user settings
async function loadUserSettings() {
    try {
        const response = await fetch(`${API_BASE}/user-settings`);
        const data = await response.json();
        if (data.success) {
            selectedProfiles = data.data.selected_profiles || ['common'];
        }
    } catch (e) {
        selectedProfiles = ['common'];
    }
}

// Load permit types into dropdown
async function loadPermitTypes() {
    const response = await fetch(`${API_BASE}/permit-types`);
    const data = await response.json();

    if (data.success) {
        data.data.forEach(permit => {
            const option = document.createElement('option');
            option.value = permit.id;
            option.textContent = `${permit.name_en} (${permit.name_fr})`;
            option.dataset.description = permit.description;
            option.dataset.url = permit.official_url;
            option.dataset.lastVerified = permit.last_verified || '';
            permitTypeSelect.appendChild(option);
        });
    }
}

// Load important links
async function loadImportantLinks() {
    const response = await fetch(`${API_BASE}/important-links`);
    const data = await response.json();

    if (data.success) {
        importantLinks.innerHTML = data.data.map(link => `
            <a href="${link.url}" target="_blank" rel="noopener" class="link-item">
                <div class="link-title">
                    <span class="link-name-fr">${link.name_fr}</span>
                    <span class="link-name-en">${link.name_en}</span>
                </div>
                <p class="link-description">${link.description}</p>
            </a>
        `).join('');
    }
}

// Render profile selector
function renderProfiles() {
    const profileEntries = Object.entries(profiles).filter(([key]) => key !== 'common');

    profileList.innerHTML = profileEntries.map(([key, profile]) => {
        const isSelected = selectedProfiles.includes(key);
        return `
            <label class="profile-chip ${isSelected ? 'selected' : ''}" data-profile="${key}">
                <input type="checkbox" ${isSelected ? 'checked' : ''}>
                <span class="profile-icon">${profile.icon || '📋'}</span>
                <span class="profile-name">${profile.name_en}</span>
            </label>
        `;
    }).join('');

    // Add click handlers
    document.querySelectorAll('.profile-chip').forEach(chip => {
        chip.addEventListener('click', handleProfileToggle);
    });
}

// Handle profile toggle
async function handleProfileToggle(event) {
    const chip = event.currentTarget;
    const profileId = chip.dataset.profile;
    const checkbox = chip.querySelector('input[type="checkbox"]');

    // Toggle selection
    if (selectedProfiles.includes(profileId)) {
        selectedProfiles = selectedProfiles.filter(p => p !== profileId);
        chip.classList.remove('selected');
        checkbox.checked = false;
    } else {
        selectedProfiles.push(profileId);
        chip.classList.add('selected');
        checkbox.checked = true;
    }

    // Always include 'common'
    if (!selectedProfiles.includes('common')) {
        selectedProfiles.push('common');
    }

    // Save to server
    try {
        await fetch(`${API_BASE}/user-settings/profiles`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ profiles: selectedProfiles })
        });
    } catch (e) {
        console.error('Failed to save profiles:', e);
    }

    // Reload documents with new profile filter
    if (currentPermitType) {
        await loadDocuments(currentPermitType);
        await updateProgress();
    }
}

// Set up event listeners
function setupEventListeners() {
    permitTypeSelect.addEventListener('change', handlePermitTypeChange);
    resetButton.addEventListener('click', handleResetProgress);
    clearDueDateBtn.addEventListener('click', () => {
        dueDateInput.value = '';
    });

    // Close modal on outside click
    notesModal.addEventListener('click', (e) => {
        if (e.target === notesModal) {
            closeNotesModal();
        }
    });

    // Close modal on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !notesModal.classList.contains('hidden')) {
            closeNotesModal();
        }
    });
}

// Handle permit type selection change
async function handlePermitTypeChange(event) {
    const permitType = event.target.value;

    if (!permitType) {
        hideApplication();
        return;
    }

    currentPermitType = permitType;

    // Show description
    const selectedOption = event.target.selectedOptions[0];
    const description = selectedOption.dataset.description;
    const url = selectedOption.dataset.url;

    permitDescription.innerHTML = `
        ${description}
        <br><br>
        <a href="${url}" target="_blank" rel="noopener">📖 View official requirements on service-public.fr</a>
    `;
    permitDescription.classList.remove('hidden');

    // Show and render profile selector
    renderProfiles();
    profileSection.classList.remove('hidden');

    // Load documents and show sections
    await loadDocuments(permitType);
    await updateProgress();

    progressSection.classList.remove('hidden');
    documentsSection.classList.remove('hidden');
    linksSection.classList.remove('hidden');
}

// Load documents for a permit type
async function loadDocuments(permitType) {
    const profilesParam = selectedProfiles.join(',');
    const response = await fetch(`${API_BASE}/documents/${permitType}?profiles=${profilesParam}`);
    const data = await response.json();

    if (data.success) {
        documents = data.data;
        renderDocuments();
    }
}

// Render documents grouped by category
function renderDocuments() {
    // Group documents by category
    const grouped = {};
    documents.forEach(doc => {
        const cat = doc.category || 'other';
        if (!grouped[cat]) {
            grouped[cat] = [];
        }
        grouped[cat].push(doc);
    });

    // Render each category
    const categoryOrder = ['identity', 'family', 'residence', 'financial', 'administrative', 'integration', 'payment'];

    documentsList.innerHTML = categoryOrder
        .filter(cat => grouped[cat])
        .map(cat => {
            const categoryInfo = categories[cat] || { name_en: cat, icon: '📄' };
            const docs = grouped[cat];
            const completedCount = docs.filter(d => d.is_complete).length;

            return `
                <div class="document-category">
                    <div class="category-header">
                        <span class="category-icon">${categoryInfo.icon}</span>
                        <span class="category-title">${categoryInfo.name_en}</span>
                        <span class="category-subtitle">${completedCount}/${docs.length}</span>
                    </div>
                    <div class="category-documents">
                        ${docs.map(doc => renderDocumentItem(doc)).join('')}
                    </div>
                </div>
            `;
        }).join('');

    // Add click handlers for checkboxes
    document.querySelectorAll('.document-checkbox-area').forEach(item => {
        item.addEventListener('click', handleDocumentClick);
    });

    // Add click handlers for notes button
    document.querySelectorAll('.notes-btn').forEach(btn => {
        btn.addEventListener('click', handleNotesClick);
    });

    // Prevent link click from triggering checkbox
    document.querySelectorAll('.document-link').forEach(link => {
        link.addEventListener('click', (e) => e.stopPropagation());
    });
}

// Render a single document item
function renderDocumentItem(doc) {
    const completedClass = doc.is_complete ? 'completed' : '';
    const hasNotes = doc.notes && doc.notes.trim().length > 0;
    const hasDueDate = doc.due_date;
    const isOverdue = hasDueDate && new Date(doc.due_date) < new Date();
    const isDueSoon = hasDueDate && !isOverdue &&
        (new Date(doc.due_date) - new Date()) / (1000 * 60 * 60 * 24) <= 7;

    const dueDateClass = isOverdue ? 'overdue' : (isDueSoon ? 'due-soon' : '');

    const linkHtml = doc.link
        ? `<a href="${doc.link}" target="_blank" rel="noopener" class="document-link">
               <span class="document-link-icon">🔗</span>
               ${doc.link_text}
           </a>`
        : `<span class="document-link no-link">
               <span class="document-link-icon">ℹ️</span>
               ${doc.link_text}
           </span>`;

    const dueDateHtml = hasDueDate
        ? `<span class="due-date-badge ${dueDateClass}">📅 ${formatDate(doc.due_date)}</span>`
        : '';

    const validityHint = doc.validity_days
        ? `<span class="validity-hint">Valid for ${doc.validity_days} days</span>`
        : '';

    return `
        <div class="document-item ${completedClass}" data-id="${doc.id}">
            <div class="document-header">
                <div class="document-checkbox-area" data-id="${doc.id}">
                    <div class="document-checkbox"></div>
                </div>
                <div class="document-content">
                    <div class="document-title">
                        <span class="document-name-fr">${doc.name_fr}</span>
                        <span class="document-name-en">${doc.name_en}</span>
                    </div>
                    <p class="document-description">${doc.description}</p>
                    <div class="document-meta">
                        ${linkHtml}
                        ${validityHint}
                        ${dueDateHtml}
                    </div>
                    ${hasNotes ? `<div class="document-notes-preview">📝 ${truncate(doc.notes, 50)}</div>` : ''}
                </div>
                <button class="notes-btn ${hasNotes ? 'has-notes' : ''}" data-id="${doc.id}" title="Add notes">
                    📝
                </button>
            </div>
        </div>
    `;
}

// Handle document checkbox click
async function handleDocumentClick(event) {
    event.stopPropagation();
    const area = event.currentTarget;
    const docId = area.dataset.id;
    const item = area.closest('.document-item');
    const isCompleted = item.classList.contains('completed');

    // Optimistic update
    item.classList.toggle('completed');

    try {
        const endpoint = isCompleted ? 'incomplete' : 'complete';
        const response = await fetch(`${API_BASE}/documents/${docId}/${endpoint}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (!data.success) {
            item.classList.toggle('completed');
            showError('Failed to update document status');
        } else {
            // Update local state
            const doc = documents.find(d => d.id === docId);
            if (doc) {
                doc.is_complete = !isCompleted;
            }
            // Update progress and re-render
            await updateProgress();
            renderDocuments();
        }
    } catch (error) {
        item.classList.toggle('completed');
        console.error('Failed to update document:', error);
        showError('Failed to update document status');
    }
}

// Handle notes button click
function handleNotesClick(event) {
    event.stopPropagation();
    const docId = event.currentTarget.dataset.id;
    const doc = documents.find(d => d.id === docId);

    if (!doc) return;

    currentEditingDocId = docId;
    notesDocName.textContent = `${doc.name_en} (${doc.name_fr})`;
    notesInput.value = doc.notes || '';
    dueDateInput.value = doc.due_date || '';

    notesModal.classList.remove('hidden');
    notesInput.focus();
}

// Close notes modal
function closeNotesModal() {
    notesModal.classList.add('hidden');
    currentEditingDocId = null;
}

// Save notes
async function saveNotes() {
    if (!currentEditingDocId) return;

    const notes = notesInput.value.trim();
    const dueDate = dueDateInput.value || null;

    try {
        // Save notes
        await fetch(`${API_BASE}/documents/${currentEditingDocId}/notes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ notes })
        });

        // Save due date
        await fetch(`${API_BASE}/documents/${currentEditingDocId}/due-date`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ due_date: dueDate })
        });

        // Update local state
        const doc = documents.find(d => d.id === currentEditingDocId);
        if (doc) {
            doc.notes = notes;
            doc.due_date = dueDate;
        }

        closeNotesModal();
        renderDocuments();

    } catch (error) {
        console.error('Failed to save notes:', error);
        showError('Failed to save notes');
    }
}

// Update progress display
async function updateProgress() {
    if (!currentPermitType) return;

    const profilesParam = selectedProfiles.join(',');
    const response = await fetch(`${API_BASE}/progress/${currentPermitType}?profiles=${profilesParam}`);
    const data = await response.json();

    if (data.success) {
        const { completed, total, percentage } = data.data;

        progressBar.style.width = `${percentage}%`;
        progressPercentage.textContent = `${percentage}%`;
        progressStats.textContent = `${completed} of ${total} documents completed`;

        // Change color based on progress
        if (percentage === 100) {
            progressPercentage.style.color = '#3fb950';
        } else if (percentage >= 50) {
            progressPercentage.style.color = '#58a6ff';
        } else {
            progressPercentage.style.color = '#d29922';
        }
    }
}

// Handle reset progress
async function handleResetProgress() {
    if (!currentPermitType) return;

    const confirmed = confirm(
        'Are you sure you want to reset all progress? This will clear all checkmarks, notes, and due dates. This cannot be undone.'
    );

    if (!confirmed) return;

    try {
        const response = await fetch(`${API_BASE}/reset/${currentPermitType}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            await loadDocuments(currentPermitType);
            await updateProgress();
        } else {
            showError('Failed to reset progress');
        }
    } catch (error) {
        console.error('Failed to reset progress:', error);
        showError('Failed to reset progress');
    }
}

// Hide application sections
function hideApplication() {
    currentPermitType = null;
    documents = [];
    permitDescription.classList.add('hidden');
    profileSection.classList.add('hidden');
    progressSection.classList.add('hidden');
    documentsSection.classList.add('hidden');
    linksSection.classList.add('hidden');
}

// Utility functions
function showError(message) {
    alert(message);
}

function truncate(str, length) {
    if (!str) return '';
    return str.length > length ? str.substring(0, length) + '...' : str;
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
}

// Make functions available globally for onclick handlers
window.closeNotesModal = closeNotesModal;
window.saveNotes = saveNotes;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);
