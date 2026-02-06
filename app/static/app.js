/**
 * French Residence Permit Tracker - Frontend Application
 */

// API base URL
const API_BASE = '/api';

// State
let currentPermitType = null;
let documents = [];
let categories = {};

// DOM Elements
const permitTypeSelect = document.getElementById('permitTypeSelect');
const permitDescription = document.getElementById('permitDescription');
const progressSection = document.getElementById('progressSection');
const progressBar = document.getElementById('progressBar');
const progressPercentage = document.getElementById('progressPercentage');
const progressStats = document.getElementById('progressStats');
const resetButton = document.getElementById('resetButton');
const documentsSection = document.getElementById('documentsSection');
const documentsList = document.getElementById('documentsList');
const linksSection = document.getElementById('linksSection');
const importantLinks = document.getElementById('importantLinks');

// Initialize the application
async function init() {
    try {
        // Load categories
        await loadCategories();

        // Load permit types
        await loadPermitTypes();

        // Load important links
        await loadImportantLinks();

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

// Set up event listeners
function setupEventListeners() {
    permitTypeSelect.addEventListener('change', handlePermitTypeChange);
    resetButton.addEventListener('click', handleResetProgress);
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

    // Load documents and show sections
    await loadDocuments(permitType);
    await updateProgress();

    progressSection.classList.remove('hidden');
    documentsSection.classList.remove('hidden');
    linksSection.classList.remove('hidden');
}

// Load documents for a permit type
async function loadDocuments(permitType) {
    const response = await fetch(`${API_BASE}/documents/${permitType}`);
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
        if (!grouped[doc.category]) {
            grouped[doc.category] = [];
        }
        grouped[doc.category].push(doc);
    });

    // Render each category
    const categoryOrder = ['identity', 'residence', 'financial', 'administrative', 'integration', 'payment'];

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

    // Add click handlers
    document.querySelectorAll('.document-item').forEach(item => {
        item.addEventListener('click', handleDocumentClick);
    });

    // Prevent link click from triggering checkbox
    document.querySelectorAll('.document-link').forEach(link => {
        link.addEventListener('click', (e) => e.stopPropagation());
    });
}

// Render a single document item
function renderDocumentItem(doc) {
    const completedClass = doc.is_complete ? 'completed' : '';
    const linkHtml = doc.link
        ? `<a href="${doc.link}" target="_blank" rel="noopener" class="document-link">
               <span class="document-link-icon">🔗</span>
               ${doc.link_text}
           </a>`
        : `<span class="document-link" style="opacity: 0.6; cursor: default;">
               <span class="document-link-icon">ℹ️</span>
               ${doc.link_text}
           </span>`;

    return `
        <div class="document-item ${completedClass}" data-id="${doc.id}">
            <div class="document-header">
                <div class="document-checkbox"></div>
                <div class="document-content">
                    <div class="document-title">
                        <span class="document-name-fr">${doc.name_fr}</span>
                        <span class="document-name-en">${doc.name_en}</span>
                    </div>
                    <p class="document-description">${doc.description}</p>
                    ${linkHtml}
                </div>
            </div>
        </div>
    `;
}

// Handle document click (toggle completion)
async function handleDocumentClick(event) {
    const item = event.currentTarget;
    const docId = item.dataset.id;
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
            // Revert on failure
            item.classList.toggle('completed');
            showError('Failed to update document status');
        } else {
            // Update progress
            await updateProgress();
            // Update local state
            const doc = documents.find(d => d.id === docId);
            if (doc) {
                doc.is_complete = !isCompleted;
            }
            // Re-render to update category counts
            renderDocuments();
        }
    } catch (error) {
        // Revert on error
        item.classList.toggle('completed');
        console.error('Failed to update document:', error);
        showError('Failed to update document status');
    }
}

// Update progress display
async function updateProgress() {
    if (!currentPermitType) return;

    const response = await fetch(`${API_BASE}/progress/${currentPermitType}`);
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
        'Are you sure you want to reset all progress? This cannot be undone.'
    );

    if (!confirmed) return;

    try {
        const response = await fetch(`${API_BASE}/reset/${currentPermitType}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            // Reload documents and progress
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
    progressSection.classList.add('hidden');
    documentsSection.classList.add('hidden');
    linksSection.classList.add('hidden');
}

// Show error message
function showError(message) {
    // Simple alert for now - could be enhanced with a toast notification
    alert(message);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);
