const grid = document.getElementById("movie-grid");
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const statusEl = document.getElementById("status-message");

function movieCardHTML(movie) {
  const poster = movie.poster_url || PLACEHOLDER_POSTER;
  const rating = movie.external_rating ? movie.external_rating.toFixed(1) : "—";
  return `
    <li class="movie-card">
      <a class="movie-card__poster-link" href="movie.html?id=${movie.tmdb_id}">
        <img src="${poster}" alt="Pôster de ${movie.title}" loading="lazy" onerror="handlePosterError(this)" />
      </a>
      <div class="movie-card__body">
        <h3><a href="movie.html?id=${movie.tmdb_id}">${movie.title}</a></h3>
        <p class="movie-card__meta">${movie.release_year || "ano desconhecido"} · nota externa ${rating}</p>
      </div>
    </li>
  `;
}

async function loadMovies(query) {
  statusEl.textContent = "Procurando westerns...";
  grid.innerHTML = "";
  try {
    const data = await apiFetch(`/movies/search?q=${encodeURIComponent(query || "")}`);
    if (!data.results.length) {
      statusEl.textContent = "Nenhum filme western encontrado com esse termo.";
      return;
    }
    statusEl.textContent = "";
    grid.innerHTML = data.results.map(movieCardHTML).join("");
  } catch (err) {
    statusEl.textContent = err.message;
  }
}

searchForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  loadMovies(searchInput.value.trim());
});

loadMovies("");
