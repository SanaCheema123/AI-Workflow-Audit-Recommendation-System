const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  const type = response.headers.get('content-type') || '';
  const payload = type.includes('application/json') ? await response.json() : await response.text();
  if (!response.ok) {
    const message = payload?.detail || payload?.message || payload || `Request failed (${response.status})`;
    throw new Error(typeof message === 'string' ? message : JSON.stringify(message));
  }
  return payload;
}

export const api = {
  health: () => request('/health'),
  listAudits: () => request('/api/audits'),
  getAudit: (id) => request(`/api/audits/${id}`),
  createAudit: (body) => request('/api/audits', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }),
  uploadWorkflow: (id, file) => { const form = new FormData(); form.append('file', file); return request(`/api/audits/${id}/workflow`, { method: 'POST', body: form }); },
  startAudit: (id) => request(`/api/audits/${id}/start`, { method: 'POST' }),
  findings: (id) => request(`/api/audits/${id}/findings`),
  recommendations: (id) => request(`/api/audits/${id}/recommendations`),
  report: (id) => request(`/api/audits/${id}/report`),
  deleteAudit: (id) => request(`/api/audits/${id}`, { method: 'DELETE' }),
};

export { API_BASE_URL };
