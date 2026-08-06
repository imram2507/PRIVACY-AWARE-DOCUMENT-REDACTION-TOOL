/* ==========================================================================
   PRIVACY-AWARE DOCUMENT REDACTION TOOL - JAVASCRIPT
   Handles: Dark Mode, Drag & Drop Upload, Progress Stepper, Copy & Results
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initDarkMode();
  initUploadDropzone();
  initCopyButtons();
  initSearchFilter();
  initFormSubmission();
});

/* --------------------------------------------------------------------------
   1. DARK MODE TOGGLE & PERSISTENCE
   -------------------------------------------------------------------------- */
function initDarkMode() {
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');
  
  // Preferred or stored theme
  const storedTheme = localStorage.getItem('theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initialTheme = storedTheme || (systemPrefersDark ? 'dark' : 'light');

  setTheme(initialTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-bs-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      setTheme(newTheme);
    });
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('theme', theme);
    if (themeIcon) {
      themeIcon.className = theme === 'dark' ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-stars-fill';
    }
  }
}

/* --------------------------------------------------------------------------
   2. DRAG AND DROP UPLOAD ZONE
   -------------------------------------------------------------------------- */
function initUploadDropzone() {
  const dropzone = document.getElementById('uploadDropzone');
  const fileInput = document.getElementById('fileInput');
  const selectedFileCard = document.getElementById('selectedFileCard');
  const fileNameDisplay = document.getElementById('fileNameDisplay');
  const fileSizeDisplay = document.getElementById('fileSizeDisplay');
  const fileIconDisplay = document.getElementById('fileIconDisplay');
  const removeFileBtn = document.getElementById('removeFileBtn');
  const submitBtn = document.getElementById('submitBtn');

  if (!dropzone || !fileInput) return;

  // Clicking dropzone triggers file dialog
  dropzone.addEventListener('click', (e) => {
    if (e.target.closest('#removeFileBtn') || e.target.closest('#selectedFileCard')) return;
    fileInput.click();
  });

  // Drag over / leave effects
  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add('drag-over');
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove('drag-over');
    }, false);
  });

  // File Drop
  dropzone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files && files.length > 0) {
      fileInput.files = files;
      handleFileSelected(files[0]);
    }
  });

  // File Input Change
  fileInput.addEventListener('change', () => {
    if (fileInput.files && fileInput.files.length > 0) {
      handleFileSelected(fileInput.files[0]);
    }
  });

  // Remove Selected File
  if (removeFileBtn) {
    removeFileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.value = '';
      if (selectedFileCard) selectedFileCard.classList.remove('show');
      if (submitBtn) submitBtn.disabled = true;
    });
  }

  function handleFileSelected(file) {
    if (!file) return;

    if (fileNameDisplay) fileNameDisplay.textContent = file.name;
    if (fileSizeDisplay) fileSizeDisplay.textContent = formatBytes(file.size);

    if (fileIconDisplay) {
      if (file.name.toLowerCase().endsWith('.pdf')) {
        fileIconDisplay.className = 'bi bi-file-earmark-pdf-fill text-danger fs-3';
      } else {
        fileIconDisplay.className = 'bi bi-file-earmark-image-fill text-primary fs-3';
      }
    }

    if (selectedFileCard) selectedFileCard.classList.add('show');
    if (submitBtn) submitBtn.disabled = false;
  }
}

function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/* --------------------------------------------------------------------------
   3. ANIMATED PROCESS STEPPER & ASYNCHRONOUS FORM SUBMISSION
   -------------------------------------------------------------------------- */
function initFormSubmission() {
  const uploadForm = document.getElementById('uploadForm');
  const submitBtn = document.getElementById('submitBtn');
  const progressStepper = document.getElementById('progressStepper');
  const stepProgressBar = document.getElementById('stepProgressBar');
  const resultsContainer = document.getElementById('resultsContainer');

  if (!uploadForm) return;

  uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
      showToast('Please select a file to upload first.', 'warning');
      return;
    }

    // Show Progress Stepper UI
    if (progressStepper) progressStepper.classList.add('show');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span> Processing Document...';
    }

    // Animate Pipeline Steps
    await runPipelineAnimations(stepProgressBar);

    // Send Form Data via Fetch API
    const formData = new FormData(uploadForm);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error(`Server returned HTTP ${response.status}`);

      const htmlText = await response.text();
      
      // Parse HTML returned by FastAPI endpoint
      parseAndInjectResults(htmlText);

      showToast('Document processed & redacted successfully!', 'success');

      // Scroll to Results Section smoothly
      if (resultsContainer) {
        resultsContainer.style.display = 'block';
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }

    } catch (err) {
      console.error('Error uploading file:', err);
      showToast('Error processing file. Please try again.', 'danger');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-shield-lock-fill"></i> Redact Document Now';
      }
    }
  });
}

// Pipeline Steps Simulation Animation
async function runPipelineAnimations(progressBar) {
  const steps = [
    { stepId: 'step1', progress: '20%' },
    { stepId: 'step2', progress: '45%' },
    { stepId: 'step3', progress: '70%' },
    { stepId: 'step4', progress: '90%' },
    { stepId: 'step5', progress: '100%' }
  ];

  for (let i = 0; i < steps.length; i++) {
    const stepEl = document.getElementById(steps[i].stepId);
    
    // Set previous step to completed
    if (i > 0) {
      const prevStepEl = document.getElementById(steps[i-1].stepId);
      if (prevStepEl) {
        prevStepEl.classList.remove('active');
        prevStepEl.classList.add('completed');
        const node = prevStepEl.querySelector('.step-node');
        if (node) node.innerHTML = '<i class="bi bi-check-lg"></i>';
      }
    }

    if (stepEl) stepEl.classList.add('active');
    if (progressBar) progressBar.style.width = steps[i].progress;

    // Delay between steps for visual delight
    await new Promise(res => setTimeout(res, 400));
  }
}

/* --------------------------------------------------------------------------
   4. PARSE & INJECT FASTAPI HTML RESPONSE INTO REDESIGNED DASHBOARD CARDS
   -------------------------------------------------------------------------- */
function parseAndInjectResults(htmlString) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlString, 'text/html');

  // Extract components from doc
  const pres = doc.querySelectorAll('pre');
  const originalText = pres.length > 0 ? pres[0].textContent : '';
  const redactedText = pres.length > 1 ? pres[1].textContent : '';

  // Extract PII Detection text
  const piiContainer = doc.querySelector('.card-header.bg-warning')?.parentElement?.querySelector('.card-body');
  const piiText = piiContainer ? piiContainer.textContent.trim() : '';

  // Extract Summary Table
  const summaryRows = doc.querySelectorAll('table tr');
  const summaryData = {};
  summaryRows.forEach(row => {
    const cols = row.querySelectorAll('td');
    if (cols.length === 2) {
      summaryData[cols[0].textContent.trim()] = cols[1].textContent.trim();
    }
  });

  // Extract Download Section
  const downloadAnchor = doc.querySelector('a[href^="/outputs/"]');
  const downloadHref = downloadAnchor ? downloadAnchor.getAttribute('href') : '';
  const isPdf = downloadHref.endsWith('.pdf');

  // 1. Inject Original Text
  const originalTextEl = document.getElementById('originalTextDisplay');
  if (originalTextEl) originalTextEl.textContent = originalText || 'No text extracted.';

  // 2. Inject Redacted Text
  const redactedTextEl = document.getElementById('redactedTextDisplay');
  if (redactedTextEl) {
    if (redactedText) {
      // Highlight [REDACTED...] tags visually
      const formattedRedacted = redactedText.replace(/\[REDACTED[^\]]*\]/g, (match) => {
        return `<span class="redacted-tag">${match}</span>`;
      });
      redactedTextEl.innerHTML = formattedRedacted;
    } else {
      redactedTextEl.textContent = 'No redacted output available.';
    }
  }

  // 3. Inject PII Badges
  const piiBadgesContainer = document.getElementById('piiBadgesContainer');
  if (piiBadgesContainer) {
    piiBadgesContainer.innerHTML = '';
    if (piiText && piiText !== 'No PII Found') {
      const items = piiText.split(/\n|<br>|\s{2,}/).map(s => s.trim()).filter(Boolean);
      items.forEach(item => {
        const badge = createPiiBadge(item);
        piiBadgesContainer.appendChild(badge);
      });
    } else {
      piiBadgesContainer.innerHTML = '<span class="text-muted"><i class="bi bi-shield-check text-success me-1"></i> No PII entities were detected in this document.</span>';
    }
  }

  // 4. Inject Summary Cards
  const namesCount = summaryData['Names'] || '0';
  const emailsCount = summaryData['Emails'] || '0';
  const phonesCount = summaryData['Phone Numbers'] || '0';
  const aadhaarCount = summaryData['Aadhaar'] || '0';
  const panCount = summaryData['PAN'] || '0';
  const othersCount = summaryData['Others'] || '0';

  setMetric('metricNames', namesCount);
  setMetric('metricEmails', emailsCount);
  setMetric('metricPhones', phonesCount);
  setMetric('metricAadhaar', aadhaarCount);
  setMetric('metricPan', panCount);
  setMetric('metricOthers', othersCount);

  // 5. Inject Download Links
  const downloadArea = document.getElementById('downloadArea');
  if (downloadArea && downloadHref) {
    downloadArea.innerHTML = `
      <div class="download-section-card">
        <h3 class="mb-2 font-heading"><i class="bi bi-file-earmark-check-fill text-success me-2"></i> Redacted Document Ready</h3>
        <p class="text-muted mb-4">Your sensitive data has been permanently redacted. Download your sanitized file below.</p>
        <div class="download-btn-group">
          <a href="${downloadHref}" target="_blank" class="btn-download-action">
            <i class="bi bi-download fs-5"></i> Download Redacted ${isPdf ? 'PDF' : 'Image'}
          </a>
        </div>
      </div>
    `;
  }
}

function createPiiBadge(text) {
  const span = document.createElement('span');
  let tagClass = 'pii-tag-other';
  let iconClass = 'bi-shield-exclamation';

  const lower = text.toLowerCase();
  if (lower.includes('email') || lower.includes('@')) {
    tagClass = 'pii-tag-email';
    iconClass = 'bi-envelope-fill';
  } else if (lower.includes('phone') || /^\+?\d[\d\s-]{8,}/.test(text)) {
    tagClass = 'pii-tag-phone';
    iconClass = 'bi-telephone-fill';
  } else if (lower.includes('aadhaar') || /^\d{4}\s\d{4}\s\d{4}/.test(text)) {
    tagClass = 'pii-tag-aadhaar';
    iconClass = 'bi-card-heading';
  } else if (lower.includes('pan') || /[a-z]{5}\d{4}[a-z]{1}/i.test(text)) {
    tagClass = 'pii-tag-pan';
    iconClass = 'bi-person-vcard-fill';
  } else if (lower.includes('name')) {
    tagClass = 'pii-tag-name';
    iconClass = 'bi-person-fill';
  }

  span.className = `pii-tag ${tagClass}`;
  span.innerHTML = `<i class="bi ${iconClass}"></i> ${escapeHtml(text)}`;
  return span;
}

function setMetric(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/* --------------------------------------------------------------------------
   5. UTILITIES: COPY TO CLIPBOARD & SEARCH FILTERING
   -------------------------------------------------------------------------- */
function initCopyButtons() {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-copy-target]');
    if (!btn) return;

    const targetId = btn.getAttribute('data-copy-target');
    const targetEl = document.getElementById(targetId);
    if (!targetEl) return;

    const textToCopy = targetEl.innerText || targetEl.textContent;
    navigator.clipboard.writeText(textToCopy).then(() => {
      const originalInner = btn.innerHTML;
      btn.innerHTML = '<i class="bi bi-check2 text-success me-1"></i> Copied!';
      showToast('Copied to clipboard!', 'success');
      setTimeout(() => {
        btn.innerHTML = originalInner;
      }, 2000);
    }).catch(err => {
      console.error('Copy failed:', err);
      showToast('Failed to copy text.', 'danger');
    });
  });
}

function initSearchFilter() {
  const searchInput = document.getElementById('textSearchInput');
  const targetText = document.getElementById('originalTextDisplay');

  if (!searchInput || !targetText) return;

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase().trim();
    if (!query) {
      targetText.innerHTML = escapeHtml(targetText.textContent);
      return;
    }

    const raw = targetText.textContent;
    const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
    const highlighted = escapeHtml(raw).replace(regex, '<mark class="bg-warning text-dark px-1 rounded">$1</mark>');
    targetText.innerHTML = highlighted;
  });
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function showToast(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `alert alert-${type} alert-dismissible fade show shadow-lg border-0 rounded-3 d-flex align-items-center gap-2 mb-2`;
  toast.style.minWidth = '280px';
  toast.innerHTML = `
    <i class="bi ${type === 'success' ? 'bi-check-circle-fill' : type === 'warning' ? 'bi-exclamation-triangle-fill' : 'bi-info-circle-fill'} fs-5"></i>
    <div>${message}</div>
    <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert" aria-label="Close"></button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
