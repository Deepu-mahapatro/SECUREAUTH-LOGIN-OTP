/* ============================================================
   SecureAuth — Vanilla JS logic
   Shared across index.html, verify.html, success.html
   Phase 5: wired to real Django backend (same-origin, no CORS).
   ============================================================ */

// Same-origin: Django serves this file, so relative paths just work.
// If you ever split frontend/backend onto different origins, set this
// to e.g. "http://127.0.0.1:8000" instead.
const API_BASE = "";
const RESEND_SECONDS = 60;

/* ---------------- Utilities ---------------- */

function showToast(message) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove("show"), 2500);
}

function isValidEmail(value) {
  return /^[^\s@]+@gmail\.com$/i.test(value.trim());
}

function setLoading(btn, isLoading, loadingLabel) {
  if (!btn) return;
  btn.disabled = isLoading;
  btn.classList.toggle("loading", isLoading);
  if (loadingLabel) {
    const labelEl = btn.querySelector(".btn-label");
    if (labelEl) {
      btn.dataset.originalLabel = btn.dataset.originalLabel || labelEl.textContent;
      labelEl.textContent = isLoading ? loadingLabel : btn.dataset.originalLabel;
      // Loading label is visually hidden by .btn.loading .btn-label { display:none } via spinner,
      // so also reflect it through aria-label for screen readers.
      btn.setAttribute("aria-label", isLoading ? loadingLabel : btn.dataset.originalLabel);
    }
  }
}

function getEmailFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("email");
}

/**
 * Shared POST helper for the OTP endpoints.
 * Returns { ok, status, data } — never throws for handled HTTP errors,
 * so callers can always read data.error for a user-facing message.
 */
async function postJSON(path, body) {
  try {
    const response = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    let data = {};
    try {
      data = await response.json();
    } catch {
      // Non-JSON response body — leave data as {}.
    }

    return { ok: response.ok, status: response.status, data };
  } catch (networkErr) {
    // fetch itself failed (server down, no connection, etc.)
    return {
      ok: false,
      status: 0,
      data: { error: "Could not reach the server. Check your connection and try again." },
    };
  }
}

/* ============================================================
   SCREEN 1 — index.html (email entry)
   ============================================================ */

function initEmailForm() {
  const form = document.getElementById("emailForm");
  if (!form) return;

  const emailInput = document.getElementById("email");
  const emailError = document.getElementById("emailError");
  const sendBtn = document.getElementById("sendBtn");

  emailInput.addEventListener("input", () => {
    emailInput.classList.remove("invalid");
    emailInput.setAttribute("aria-invalid", "false");
    emailError.classList.remove("show");
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    console.log("EMAIL FORM SUBMIT HANDLER IS RUNNING");

    const value = emailInput.value.trim();

    if (!value) {
      emailInput.classList.add("invalid");
      emailInput.setAttribute("aria-invalid", "true");
      document.getElementById("emailErrorText").textContent = "Please enter your email address.";
      emailError.classList.add("show");
      emailInput.focus();
      return;
    }

    if (!isValidEmail(value)) {
      emailInput.classList.add("invalid");
      emailInput.setAttribute("aria-invalid", "true");
      document.getElementById("emailErrorText").textContent ="Please enter a valid Gmail address.";
      emailError.classList.add("show");
      emailInput.focus();
      return;
    }

    setLoading(sendBtn, true, "Sending...");
    const result = await sendOTP(value);
    setLoading(sendBtn, false);

    if (!result.ok) {
      emailInput.classList.add("invalid");
      emailInput.setAttribute("aria-invalid", "true");
      document.getElementById("emailErrorText").textContent =
        result.error || "Something went wrong. Please try again.";
      emailError.classList.add("show");
      return;
    }

    window.location.href = `/verify/?email=${encodeURIComponent(value)}`;
  });
}

/**
 * Sends a one-time verification code to the given email.
 * POST /api/otp/send/  { "email": "..." }
 */
async function sendOTP(email) {
  const { ok, data } = await postJSON("/api/otp/send/", { email });
  return { ok, error: data.error };
}

/* ============================================================
   SCREEN 2 — verify.html (OTP entry)
   ============================================================ */

function initOtpForm() {
  const otpRow = document.getElementById("otpRow");
  if (!otpRow) return;

  const boxes = Array.from(otpRow.querySelectorAll(".otp-box"));
  const emailDisplay = document.getElementById("emailDisplay");
  const statusMsg = document.getElementById("statusMsg");
  const statusMsgText = document.getElementById("statusMsgText");
  const verifyBtn = document.getElementById("verifyBtn");
  const resendBtn = document.getElementById("resendBtn");
  const timerText = document.getElementById("timerText");
  const changeEmailBtn = document.getElementById("changeEmailBtn");
  const editEmailBtn = document.getElementById("editEmailBtn");

  const currentEmail = getEmailFromUrl();
  if (!currentEmail) {
    window.location.href = "/";
    return;
  }
  emailDisplay.textContent = currentEmail;

  boxes[0].focus();

  function clearStatus() {
    statusMsg.classList.remove("show", "error", "success", "info");
    boxes.forEach((b) => b.classList.remove("invalid"));
  }

  function setStatus(type, message) {
    statusMsg.classList.remove("error", "success", "info");
    statusMsg.classList.add("show", type);
    statusMsgText.textContent = message;
  }

  function getCode() {
    return boxes.map((b) => b.value).join("");
  }

  function updateVerifyState() {
    verifyBtn.disabled = getCode().length !== boxes.length;
  }

  boxes.forEach((box, i) => {
    box.addEventListener("input", () => {
      box.value = box.value.replace(/[^0-9]/g, "").slice(0, 1);
      clearStatus();

      if (box.value) {
        box.classList.add("filled");
        if (i < boxes.length - 1) boxes[i + 1].focus();
      } else {
        box.classList.remove("filled");
      }

      updateVerifyState();
    });

    box.addEventListener("keydown", (e) => {
      if (e.key === "Backspace") {
        if (!box.value && i > 0) {
          boxes[i - 1].focus();
          boxes[i - 1].value = "";
          boxes[i - 1].classList.remove("filled");
          updateVerifyState();
          e.preventDefault();
        }
      } else if (e.key === "ArrowLeft" && i > 0) {
        e.preventDefault();
        boxes[i - 1].focus();
      } else if (e.key === "ArrowRight" && i < boxes.length - 1) {
        e.preventDefault();
        boxes[i + 1].focus();
      } else if (e.key === "Enter") {
        e.preventDefault();
        if (!verifyBtn.disabled) handleVerify();
      }
    });

    box.addEventListener("paste", (e) => {
      e.preventDefault();
      const pasted = (e.clipboardData || window.clipboardData)
        .getData("text")
        .replace(/[^0-9]/g, "")
        .slice(0, boxes.length);

      if (!pasted) return;

      pasted.split("").forEach((digit, idx) => {
        if (boxes[idx]) {
          boxes[idx].value = digit;
          boxes[idx].classList.add("filled");
        }
      });

      const next = Math.min(pasted.length, boxes.length - 1);
      boxes[next].focus();
      clearStatus();
      updateVerifyState();
    });
  });

  async function handleVerify() {
    const code = getCode();

    if (code.length !== boxes.length) {
      boxes.forEach((b) => { if (!b.value) b.classList.add("invalid"); });
      setStatus("error", "Please enter all 6 digits.");
      return;
    }

    setLoading(verifyBtn, true, "Verifying...");
    const result = await verifyOTP(code);
    setLoading(verifyBtn, false);

    if (result.ok) {
      setStatus("success", "Verified! Redirecting...");
      window.location.href = "/success/";
    } else {
      boxes.forEach((b) => b.classList.add("invalid"));
      setStatus("error", result.error || "Invalid verification code. Please try again.");
      boxes[0].focus();
      boxes[0].select();
    }
  }

  verifyBtn.addEventListener("click", () => {
    if (!verifyBtn.disabled) handleVerify();
  });

  changeEmailBtn.addEventListener("click", () => { window.location.href = "/"; });
  editEmailBtn.addEventListener("click", () => { window.location.href = "/"; });

  /* ---- Resend countdown ---- */
  let remaining = RESEND_SECONDS;
  let timerId = null;

  function formatTime(s) {
    const mm = String(Math.floor(s / 60)).padStart(2, "0");
    const ss = String(s % 60).padStart(2, "0");
    return `${mm}:${ss}`;
  }

  function startCountdown() {
    remaining = RESEND_SECONDS;
    resendBtn.disabled = true;
    timerText.parentElement.classList.add("show");
    timerText.textContent = `Resend available in ${formatTime(remaining)}`;

    clearInterval(timerId);
    timerId = setInterval(() => {
      remaining -= 1;
      if (remaining <= 0) {
        clearInterval(timerId);
        resendBtn.disabled = false;
        timerText.parentElement.classList.remove("show");
      } else {
        timerText.textContent = `Resend available in ${formatTime(remaining)}`;
      }
    }, 1000);
  }

  resendBtn.addEventListener("click", async () => {
    if (resendBtn.disabled) return;
    resendBtn.disabled = true;
    resendBtn.textContent = "Sending...";

    const result = await resendOTP();

    resendBtn.textContent = "Resend code";

    if (!result.ok) {
      showToast(result.error || "Could not resend the code. Please try again.");
      resendBtn.disabled = false;
      return;
    }

    boxes.forEach((b) => { b.value = ""; b.classList.remove("filled", "invalid"); });
    clearStatus();
    updateVerifyState();
    boxes[0].focus();
    showToast("A new verification code has been sent.");
    startCountdown();
  });

  updateVerifyState();
  startCountdown();
}

/**
 * Verifies the entered code against the backend.
 * POST /api/otp/verify/  { "email": "...", "otp": "123456" }
 */
async function verifyOTP(otp) {
  const email = getEmailFromUrl();
  const { ok, data } = await postJSON("/api/otp/verify/", { email, otp });
  return { ok, error: data.error };
}

/**
 * Requests a new one-time verification code.
 * POST /api/otp/resend/  { "email": "..." }
 */
async function resendOTP() {
  const email = getEmailFromUrl();
  const { ok, data } = await postJSON("/api/otp/resend/", { email });
  return { ok, error: data.error };
}

/* ============================================================
   SCREEN 3 — success.html
   ============================================================ */

function initSuccessScreen() {
  const continueBtn = document.getElementById("continueBtn");
  const homeBtn = document.getElementById("homeBtn");
  if (!continueBtn) return;

  continueBtn.addEventListener("click", () => {
    // No backend/dashboard route yet — return to the start of the flow.
    // TODO: redirect to the authenticated dashboard route once it exists.
    window.location.href = "/";
  });

  homeBtn.addEventListener("click", () => {
    window.location.href = "/";
  });
}

/* ---------------- Init ---------------- */

document.addEventListener("DOMContentLoaded", () => {
  initEmailForm();
  initOtpForm();
  initSuccessScreen();
});