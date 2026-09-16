const params = new URLSearchParams(window.location.search);
const tmdbId = params.get("id");

const detailEl = document.getElementById("movie-detail");
const reviewSectionEl = document.getElementById("review-section");

function renderMovie(movie) {
  document.title = `${movie.title} — Western Reels`;
  const castItems = (movie.cast || [])
    .map((c) => `<li>${c.name}${c.character ? ` <span class="movie-card__meta">como ${c.character}</span>` : ""}</li>`)
    .join("");

  detailEl.innerHTML = `
    <div class="detail__poster">
      <img src="${movie.poster_url || PLACEHOLDER_POSTER}" alt="Pôster de ${movie.title}" onerror="handlePosterError(this)" />
    </div>
    <div class="detail__info">
      <h1>${movie.title}</h1>
      <p class="detail__meta">
        ${movie.release_year || "ano desconhecido"}
        ${movie.genres && movie.genres.length ? " · " + movie.genres.join(", ") : ""}
        ${movie.runtime_minutes ? ` · ${movie.runtime_minutes} min` : ""}
      </p>
      <p class="detail__rating">Nota externa (TMDB): ${movie.external_rating ? movie.external_rating.toFixed(1) : "—"} / 10</p>
      <p>${movie.synopsis || "Sinopse não disponível."}</p>
      <h2>Elenco</h2>
      <ul class="detail__cast">${castItems || "<li>Elenco não disponível.</li>"}</ul>
    </div>
  `;
}

async function loadUserEntry(movie) {
  if (!isLoggedIn()) {
    reviewSectionEl.innerHTML = `<p><a href="login.html">Entre na sua conta</a> para favoritar, dar nota e escrever uma avaliação sobre este filme.</p>`;
    return;
  }

  try {
    const mine = await apiFetch("/my-movies");
    const entry = mine.find((item) => String(item.tmdb_id) === String(movie.tmdb_id));
    renderReviewForm(movie, entry);
  } catch (err) {
    reviewSectionEl.innerHTML = `<p class="error">${err.message}</p>`;
  }
}

function renderReviewForm(movie, entry) {
  reviewSectionEl.innerHTML = `
    <h2>Sua avaliação</h2>
    <form id="review-form" class="review-form">
      <label>
        <input type="checkbox" id="fav-checkbox" ${entry?.is_favorite ? "checked" : ""} />
        Favoritar este filme
      </label>
      <label>
        Sua nota (0 a 10)
        <input type="number" id="rating-input" min="0" max="10" step="0.5" value="${entry?.user_rating ?? ""}" />
      </label>
      <label>
        Sua avaliação
        <textarea id="review-textarea" rows="4" placeholder="O que você achou deste western?">${entry?.review_text ?? ""}</textarea>
      </label>
      <div class="review-form__actions">
        <button type="submit">${entry ? "Atualizar avaliação" : "Salvar"}</button>
        ${entry ? '<button type="button" id="delete-review-btn" class="btn--danger">Excluir</button>' : ""}
      </div>
      <p class="form-error" id="review-status"></p>
    </form>
  `;

  document.getElementById("review-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const statusEl = document.getElementById("review-status");
    statusEl.textContent = "";

    const ratingValue = document.getElementById("rating-input").value;
    const payload = {
      tmdb_id: movie.tmdb_id,
      title: movie.title,
      poster_path: movie.poster_path,
      release_year: movie.release_year,
      external_rating: movie.external_rating,
      is_favorite: document.getElementById("fav-checkbox").checked,
      user_rating: ratingValue === "" ? null : parseFloat(ratingValue),
      review_text: document.getElementById("review-textarea").value,
    };

    try {
      if (entry) {
        await apiFetch(`/my-movies/${entry.id}`, { method: "PUT", body: JSON.stringify(payload) });
      } else {
        await apiFetch("/my-movies", { method: "POST", body: JSON.stringify(payload) });
      }
      statusEl.style.color = "var(--accent-teal)";
      statusEl.textContent = "Avaliação salva!";
      loadUserEntry(movie);
    } catch (err) {
      statusEl.style.color = "";
      statusEl.textContent = err.message;
    }
  });

  document.getElementById("delete-review-btn")?.addEventListener("click", async () => {
    if (!entry || !confirm("Remover este filme e sua avaliação da sua lista?")) return;
    try {
      await apiFetch(`/my-movies/${entry.id}`, { method: "DELETE" });
      loadUserEntry(movie);
    } catch (err) {
      alert(err.message);
    }
  });
}

async function loadMovie() {
  if (!tmdbId) {
    detailEl.innerHTML = `<p class="error">Filme não especificado.</p>`;
    return;
  }
  try {
    const movie = await apiFetch(`/movies/${tmdbId}`);
    renderMovie(movie);
    await loadUserEntry(movie);
  } catch (err) {
    detailEl.innerHTML = `<p class="error">${err.message}</p>`;
  }
}

loadMovie();
