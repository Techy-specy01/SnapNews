/* ═══════════════════════════════════════════
   script.js — SnapNews
   Simple JS for loading states + UX polish
═══════════════════════════════════════════ */

// ── Show loading overlay when navigating ─────────────────
function showLoading(message = "Fetching & summarizing news...") {
  // Don't add if already exists
  if (document.querySelector(".loading-overlay")) return;

  const overlay = document.createElement("div");
  overlay.className = "loading-overlay";
  overlay.innerHTML = `
    <div class="spinner"></div>
    <p class="loading-text">⚡ ${message}</p>
  `;
  document.body.appendChild(overlay);
}

// ── Attach loading to nav category links ─────────────────
document.addEventListener("DOMContentLoaded", function () {

  // Show loading when clicking category links
  const catLinks = document.querySelectorAll(".nav-cat-pill, .see-all-link, .other-cat-pill");
  catLinks.forEach(function (link) {
    link.addEventListener("click", function () {
      showLoading("Loading " + (link.textContent.trim()) + " news...");
    });
  });

  // Show loading on logo click
  const logo = document.querySelector(".nav-logo");
  if (logo) {
    logo.addEventListener("click", function () {
      showLoading("Loading SnapNews...");
    });
  }

  // Show loading on search submit
  const searchForm = document.querySelector(".search-form");
  if (searchForm) {
    searchForm.addEventListener("submit", function () {
      const q = document.querySelector(".search-input").value.trim();
      if (q) {
        showLoading("Searching for \"" + q + "\"...");
      }
    });
  }

  // ── Animate cards on page load ──────────────────────────
  const cards = document.querySelectorAll(".news-card");
  cards.forEach(function (card, index) {
    card.style.opacity = "0";
    card.style.transform = "translateY(16px)";
    card.style.transition = "opacity 0.4s ease, transform 0.4s ease";

    setTimeout(function () {
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, 60 + index * 40); // stagger: each card appears 40ms after previous
  });

  // ── Keyboard shortcut: press "/" to focus search ────────
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement.tagName !== "INPUT") {
      e.preventDefault();
      const searchInput = document.querySelector(".search-input");
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
    }
  });

  // ── Highlight active category in nav ───────────────────
  const currentPath = window.location.pathname;
  const navPills = document.querySelectorAll(".nav-cat-pill");
  navPills.forEach(function (pill) {
    const href = pill.getAttribute("href");
    if (href && currentPath.startsWith(href)) {
      pill.classList.add("active");
    }
  });

});

// ── Remove loading overlay when page finishes loading ────
window.addEventListener("load", function () {
  const overlay = document.querySelector(".loading-overlay");
  if (overlay) {
    overlay.style.opacity = "0";
    overlay.style.transition = "opacity 0.3s";
    setTimeout(function () { overlay.remove(); }, 300);
  }
});
