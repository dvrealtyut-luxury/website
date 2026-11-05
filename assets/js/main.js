(function () {
  "use strict";

  var doc = document.documentElement;
  var body = document.body;

  // Page-load entrance
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { body.classList.add("is-loaded"); });
  });

  // Header: solid on scroll, hide on scroll-down, show on scroll-up
  var header = document.querySelector(".site-header");
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    if (!header) return;
    header.classList.toggle("is-scrolled", y > 40);
    if (!body.classList.contains("menu-open")) {
      header.classList.toggle("is-hidden", y > 600 && y > lastY + 4);
      if (y < lastY - 4) header.classList.remove("is-hidden");
    }
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var menu = document.getElementById("mobile-menu");
  function setMenu(open) {
    body.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    menu.setAttribute("aria-hidden", String(!open));
    if (open) { header.classList.remove("is-hidden"); }
  }
  if (toggle && menu) {
    toggle.addEventListener("click", function () { setMenu(!body.classList.contains("menu-open")); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
  }

  // Scroll reveals
  var targets = document.querySelectorAll(".reveal, .mask");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  } else {
    targets.forEach(function (el) { el.classList.add("is-in"); });
  }

  // Footer year
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Contact form — opens the visitor's email app with a pre-filled message.
  // To receive submissions directly instead, set data-endpoint on the <form>
  // to a form service URL (e.g. Formspree) and it will POST there.
  var form = document.querySelector("form[data-contact]");
  if (form) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      var endpoint = form.getAttribute("data-endpoint");

      if (endpoint) {
        status.textContent = "Sending…";
        fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } })
          .then(function (r) {
            if (!r.ok) throw new Error();
            form.reset();
            status.textContent = "Thank you — Danielle will be in touch within one business day.";
          })
          .catch(function () {
            status.textContent = "Something went wrong. Please call or email Danielle directly.";
          });
        return;
      }

      var interests = data.getAll("interest").join(", ") || "—";
      var lines = [
        "Name: " + data.get("name"),
        "Email: " + data.get("email"),
        "Phone: " + (data.get("phone") || "—"),
        "Moving from: " + (data.get("from") || "—"),
        "Timeline: " + (data.get("timeline") || "—"),
        "Interested in: " + interests,
        "",
        data.get("message") || ""
      ];
      var to = form.getAttribute("data-email");
      var subject = "Consultation request — " + data.get("name");
      window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
      status.textContent = "Opening your email app… If nothing happens, email " + to + " directly.";
    });
  }
})();
