const grid = document.getElementById("movie-grid");
const statusEl = document.getElementById("status-message");

function itemCardHTML(item) {
  const poster = item.poster_url || PLACEHOLDER_POSTER;
  return `
    <li class="movie-card">
      <a class="movie-card__poster-link" href="movie.html?id=${item.tmdb_id}">
        <img src="${poster}" alt="Pôster de ${item.title}" loading="lazy" onerror="handlePosterError(this)" />
      </a>
      <div class="movie-card__body">
        <h3><a href="movie.html?id=${item.tmdb_id}">${item.title}</a></h3>
        <p class="movie-card__meta">
          ${item.release_year || "ano desconhecido"}${item.is_favorite ? " · ★ favorito" : ""}
        </p>
        <p class="movie-card__meta">Sua nota: ${item.user_rating ?? "sem nota"}</p>
        ${item.review_text ? `<p class="movie-card__review">"${item.review_text}"</p>` : ""}
        <button class="movie-card__delete" data-id="${item.id}" type="button">Remover</button>
      </div>
    </li>
  `;
}

async function loadMyMovies() {
  if (!isLoggedIn()) {
    window.location.href = "login.html";
    return;
  }

  statusEl.textContent = "Carregando seus filmes...";
  try {
    const items = await apiFetch("/my-movies");
    if (!items.length) {
      statusEl.textContent = "Você ainda não salvou nenhum filme. Explore a busca e favorite alguns westerns!";
      grid.innerHTML = "";
      return;
    }
    statusEl.textContent = "";
    grid.innerHTML = items.map(itemCardHTML).join("");

    grid.querySelectorAll(".movie-card__delete").forEach((button) => {
      button.addEventListener("click", async () => {
        if (!confirm("Remover este filme da sua lista?")) return;
        try {
          await apiFetch(`/my-movies/${button.dataset.id}`, { method: "DELETE" });
          loadMyMovies();
        } catch (err) {
          alert(err.message);
        }
      });
    });
  } catch (err) {
    statusEl.textContent = err.message;
  }
}

loadMyMovies();
