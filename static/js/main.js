/* -------------------------------------------------------------
   Water Purity Tracker - Main JavaScript Controller (main.js)
   Sidebar, Theme Toggle, Toast System, Form Handlers, Modals
   ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
  // Remove loading overlay smoothly
  const loader = document.getElementById('app-loading-overlay');
  if (loader) {
    setTimeout(() => {
      loader.style.opacity = '0';
      setTimeout(() => loader.style.display = 'none', 500);
    }, 400);
  }

  // Sidebar Collapse Toggle
  const sidebar = document.getElementById('appSidebar');
  const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
  if (sidebar && sidebarToggleBtn) {
    sidebarToggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
      localStorage.setItem('sidebar_collapsed', sidebar.classList.contains('collapsed'));
    });

    if (localStorage.getItem('sidebar_collapsed') === 'true') {
      sidebar.classList.add('collapsed');
    }
  }

  // Dark / Light Theme Toggle
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('light-theme');
      const isLight = document.body.classList.contains('light-theme');
      localStorage.setItem('theme_preference', isLight ? 'light' : 'dark');
      themeToggleBtn.querySelector('i').className = isLight ? 'fas fa-sun' : 'fas fa-moon';
      showToast(isLight ? 'Switched to Light Theme' : 'Switched to Dark Theme', 'info');
    });

    if (localStorage.getItem('theme_preference') === 'light') {
      document.body.classList.add('light-theme');
      if (themeToggleBtn.querySelector('i')) {
        themeToggleBtn.querySelector('i').className = 'fas fa-sun';
      }
    }
  }

  // Scroll to Top Button Visibility
  const scrollTopBtn = document.getElementById('scrollTopBtn');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    });

    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Handle Login Form Submission
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const usernameInput = document.getElementById('usernameInput').value;
      const passwordInput = document.getElementById('passwordInput').value;

      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: usernameInput, password: passwordInput })
        });
        const result = await response.json();

        if (result.success) {
          showToast('Login successful! Redirecting to dashboard...', 'success');
          setTimeout(() => {
            window.location.href = result.redirect || '/dashboard';
          }, 800);
        } else {
          showToast(result.message || 'Invalid login credentials', 'error');
        }
      } catch (err) {
        showToast('Login connection error', 'error');
      }
    });
  }

  // Handle Water Test Form Submission
  const waterTestForm = document.getElementById('waterTestForm');
  if (waterTestForm) {
    waterTestForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(waterTestForm);
      const dataObj = Object.fromEntries(formData.entries());

      try {
        const response = await fetch('/api/water-test', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(dataObj)
        });
        const result = await response.json();

        if (result.success) {
          showToast(`Analysis Complete: Score ${result.score}/100 (${result.status})`, result.status === 'SAFE' ? 'success' : 'warning');
          // Show analysis modal if present or redirect
          if (document.getElementById('analysisResultModal')) {
            showAnalysisModal(result);
          } else {
            setTimeout(() => {
              window.location.href = '/analysis';
            }, 1200);
          }
        } else {
          showToast(result.message || 'Error processing water test', 'error');
        }
      } catch (err) {
        showToast('Network error saving water test', 'error');
      }
    });
  }
});

// Universal Toast Notification System
function showToast(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText = `
      position: fixed;
      top: 80px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    `;
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  const bgMap = {
    success: 'linear-gradient(135deg, #059669, #10b981)',
    error: 'linear-gradient(135deg, #dc2626, #ef4444)',
    warning: 'linear-gradient(135deg, #d97706, #f59e0b)',
    info: 'linear-gradient(135deg, #0284c7, #06b6d4)'
  };
  const iconMap = {
    success: 'fa-check-circle',
    error: 'fa-exclamation-circle',
    warning: 'fa-triangle-exclamation',
    info: 'fa-circle-info'
  };

  toast.style.cssText = `
    background: ${bgMap[type] || bgMap.info};
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    font-size: 0.88rem;
    font-weight: 500;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 280px;
    animation: toastIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  `;

  toast.innerHTML = `<i class="fas ${iconMap[type]}"></i> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(50px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Show Analysis Modal Helper
function showAnalysisModal(res) {
  const modalEl = document.getElementById('analysisResultModal');
  if (!modalEl) return;

  document.getElementById('modalScoreValue').innerText = res.score;
  document.getElementById('modalStatusText').innerText = res.status;
  document.getElementById('modalStatusText').className = res.status === 'SAFE' ? 'status-badge safe' : 'status-badge unsafe';
  document.getElementById('modalRecommendationText').innerText = res.recommendation;

  const bsModal = new bootstrap.Modal(modalEl);
  bsModal.show();
}

// Alert Status Toggle Action
async function toggleAlertResolved(alertId, btn) {
  try {
    const res = await fetch(`/api/alerts/toggle/${alertId}`, { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showToast('Alert status updated!', 'success');
      setTimeout(() => location.reload(), 600);
    }
  } catch (err) {
    showToast('Failed to update alert', 'error');
  }
}
