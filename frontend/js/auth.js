document.getElementById("login-form")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const errorEl = document.getElementById("form-error");
  errorEl.textContent = "";

  const identifier = document.getElementById("login-identifier").value.trim();
  const password = document.getElementById("login-password").value;

  try {
    const data = await apiFetch("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username: identifier, email: identifier, password }),
    });
    setSession(data.token, data.user);
    window.location.href = "index.html";
  } catch (err) {
    errorEl.textContent = err.message;
  }
});

document.getElementById("register-form")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const errorEl = document.getElementById("form-error");
  errorEl.textContent = "";

  const username = document.getElementById("reg-username").value.trim();
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value;

  try {
    const data = await apiFetch("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, email, password }),
    });
    setSession(data.token, data.user);
    window.location.href = "index.html";
  } catch (err) {
    errorEl.textContent = err.message;
  }
});
