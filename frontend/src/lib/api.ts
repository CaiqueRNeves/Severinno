const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export type FetchOptions = RequestInit & { auth?: string };

export async function apiFetch(path: string, options: FetchOptions = {}) {
  const headers = new Headers(options.headers);
  headers.set('Content-Type', 'application/json');

  if (options.auth) {
    headers.set('Authorization', `Bearer ${options.auth}`);
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || response.statusText);
  }

  return response.json();
}

export { API_URL };
