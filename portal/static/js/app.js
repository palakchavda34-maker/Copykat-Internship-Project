/**
 * Internship Portal - Frontend Application JavaScript
 */

// Toast notification helper
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let icon = 'ℹ️';
  if (type === 'success') icon = '✅';
  if (type === 'error') icon = '⚠️';

  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Authentication Storage Helpers
const Auth = {
  getUser: function() {
    try {
      const data = localStorage.getItem('portal_user');
      if (!data || data === 'undefined' || data === 'null') return null;
      return JSON.parse(data);
    } catch (e) {
      return null;
    }
  },
  getRole: function() {
    return localStorage.getItem('portal_role'); // 'student' or 'company'
  },
  getTokens: function() {
    try {
      const data = localStorage.getItem('portal_tokens');
      if (!data || data === 'undefined' || data === 'null') return null;
      const parsed = JSON.parse(data);
      if (parsed && parsed.access && parsed.access !== 'undefined' && parsed.access !== 'null') {
        return parsed;
      }
      return null;
    } catch (e) {
      return null;
    }
  },
  setUser: function(user, role, tokens) {
    localStorage.setItem('portal_user', JSON.stringify(user));
    localStorage.setItem('portal_role', role);
    if (tokens) {
      localStorage.setItem('portal_tokens', JSON.stringify(tokens));
    }
  },
  logout: function() {
    localStorage.removeItem('portal_user');
    localStorage.removeItem('portal_role');
    localStorage.removeItem('portal_tokens');
    window.location.href = '/';
  }
};

// Global Navbar Updater
function renderNavbar() {
  const navButtons = document.getElementById('nav-buttons');
  if (!navButtons) return;

  const user = Auth.getUser();
  const role = Auth.getRole();

  if (user && role) {
    const name = role === 'student' ? user.name : user.company_name;
    const initial = name ? name.charAt(0).toUpperCase() : 'U';
    const dashboardUrl = role === 'student' ? '/student/dashboard/' : '/company/dashboard/';

    navButtons.innerHTML = `
      <a href="${dashboardUrl}" class="user-menu-badge">
        <div class="user-avatar">${initial}</div>
        <div class="user-name-role">
          <span class="user-name">${name}</span>
          <span class="user-role">${role}</span>
        </div>
      </a>
      <button onclick="Auth.logout()" class="btn btn-outline btn-sm">Logout</button>
    `;
  } else {
    navButtons.innerHTML = `
      <a href="/student/login/" class="btn btn-outline btn-sm">Student Login</a>
      <a href="/company/login/" class="btn btn-primary btn-sm">Company Portal</a>
    `;
  }
}

// Robust API Request Wrapper
async function apiRequest(url, options = {}) {
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  const method = (options.method || 'GET').toUpperCase();
  const tokens = Auth.getTokens();

  if (tokens && tokens.access) {
    defaultHeaders['Authorization'] = `Bearer ${tokens.access}`;
  }

  options.headers = { ...defaultHeaders, ...options.headers };

  try {
    let response = await fetch(url, options);
    
    // If GET request fails with 401 or 403 while sending Authorization header, retry without Authorization header
    if (!response.ok && (response.status === 401 || response.status === 403) && method === 'GET' && options.headers['Authorization']) {
      delete options.headers['Authorization'];
      response = await fetch(url, options);
    }

    const data = await response.json();
    return { ok: response.ok, status: response.status, data };
  } catch (err) {
    console.error('API Request Error:', err);
    return { ok: false, status: 500, data: { error: 'Network error or server unavailable.' } };
  }
}

// Global modal helpers
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add('active');
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', () => {
  renderNavbar();
});
