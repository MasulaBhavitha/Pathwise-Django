const API = '/api'

export function errorMessage(error) {
  const data = error?.data
  if (!data) return error?.message || 'Something went wrong.'
  if (typeof data.detail === 'string') return data.detail
  if (typeof data === 'object') {
    return Object.entries(data)
      .map(([key, value]) => {
        const text = Array.isArray(value) ? value.join(' ') : String(value)
        return key === 'non_field_errors' ? text : `${key}: ${text}`
      })
      .join(' ')
  }
  return error.message
}

async function request(path, { method = 'GET', body, token } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers.Authorization = `Bearer ${token}`
  const response = await fetch(`${API}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  const text = await response.text()
  let data = null
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = { detail: text }
    }
  }
  return { response, data }
}

export async function api(path, options = {}) {
  const { auth = true, ...rest } = options
  let token = auth ? localStorage.getItem('access') : null
  let { response, data } = await request(path, { ...rest, token })

  if (response.status === 401 && auth && localStorage.getItem('refresh')) {
    const refreshed = await request('/auth/refresh/', {
      method: 'POST',
      body: { refresh: localStorage.getItem('refresh') },
    })
    if (refreshed.response.ok && refreshed.data?.access) {
      localStorage.setItem('access', refreshed.data.access)
      token = refreshed.data.access
      ;({ response, data } = await request(path, { ...rest, token }))
    } else {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    }
  }

  if (!response.ok) {
    const error = new Error(errorMessage({ data, message: 'Request failed' }))
    error.status = response.status
    error.data = data
    throw error
  }
  return data
}
