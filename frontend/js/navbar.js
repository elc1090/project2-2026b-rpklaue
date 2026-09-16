function renderNavbar() {
  const nav = document.getElementById("nav-links");
  if (!nav) return;

  const user = getUser();

  nav.innerHTML = user
    ? `
      <a href="index.html">Buscar filmes</a>
      <a href="my-movies.html">Meus filmes</a>
      <span class="nav-user">${user.username}</span>
      <button id="logout-btn" type="button">Sair</button>
    `
    : `
      <a href="index.html">Buscar filmes</a>
      <a href="login.html">Entrar</a>
      <a href="register.html">Criar conta</a>
    `;

  document.getElementById("logout-btn")?.addEventListener("click", () => {
    clearSession();
    window.location.href = "index.html";
  });
}

renderNavbar();
