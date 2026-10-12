const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '') + '/api'

export async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`, { method: 'GET' })
    if (!res.ok) return { online: false, status: res.status }
    const data = await res.json()
    return { online: true, ...data }
  } catch (err) {
    return { online: false, error: err.message }
  }
}

export async function runResearchQuery(query) {
  const res = await fetch(`${API_BASE_URL}/research`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  })

  if (!res.ok) {
    let errorDetail = 'Research request failed'
    try {
      const errorJson = await res.json()
      errorDetail = errorJson.detail || errorDetail
    } catch {
      errorDetail = `Server returned status ${res.status}`
    }
    throw new Error(errorDetail)
  }

  return await res.json()
}

export async function fetchResearchHistory() {
  try {
    const res = await fetch(`${API_BASE_URL}/history`, { method: 'GET' })
    if (!res.ok) return []
    return await res.json()
  } catch (err) {
    console.error('Failed to fetch research history:', err)
    return []
  }
}

export async function fetchResearchById(id) {
  const res = await fetch(`${API_BASE_URL}/history/${id}`, { method: 'GET' })
  if (!res.ok) {
    throw new Error('Failed to load past research dossier')
  }
  return await res.json()
}

export async function deleteResearchById(id) {
  const res = await fetch(`${API_BASE_URL}/history/${id}`, { method: 'DELETE' })
  if (!res.ok) {
    throw new Error('Failed to delete research session')
  }
  return await res.json()
}
