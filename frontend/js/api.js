// Cliente simples para conversar com o backend Flask.
// Guarda o token JWT e os dados do usuário no localStorage do navegador,
// o que mantém a sessão ativa entre recarregamentos de página.

const TOKEN_KEY = "wr_token";
const USER_KEY = "wr_user";

// Pôster reserva: usado quando o filme não tem poster_url, e também como
// rede de segurança se a imagem real falhar ao carregar (bloqueio de rede,
// extensão do navegador, etc.) — assim nunca aparece um ícone quebrado.
const PLACEHOLDER_POSTER =
  "data:image/svg+xml;utf8," +
  encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="450"><rect width="100%" height="100%" fill="%232b2018"/><text x="50%" y="50%" fill="%23b8a88f" font-family="sans-serif" font-size="16" text-anchor="middle">Sem pôster</text></svg>'
  );

function handlePosterError(imgEl) {
  imgEl.onerror = null;
  imgEl.src = PLACEHOLDER_POSTER;
}

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setSession(token, user) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

function getUser() {
  const raw = localStorage.getItem(USER_KEY);
  return raw ? JSON.parse(raw) : null;
}

function isLoggedIn() {
  return Boolean(getToken());
}

/**
 * Faz uma chamada à API, anexando o token JWT quando disponível.
 * Lança um Error com uma mensagem amigável quando a resposta não é OK.
 */
async function apiFetch(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(`${window.API_BASE_URL}${path}`, { ...options, headers });
  } catch (networkError) {
    throw new Error(
      "Não foi possível falar com o servidor. Verifique se o backend está rodando " +
        "e se o endereço em js/config.js está correto."
    );
  }

  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json") ? await response.json() : null;

  if (!response.ok) {
    throw new Error((body && body.error) || `Erro inesperado (${response.status}).`);
  }
  return body;
}
