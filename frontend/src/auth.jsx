import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { api } from './api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    if (!localStorage.getItem('access')) {
      setReady(true)
      return
    }
    api('/auth/me/')
      .then(setUser)
      .catch(() => {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        setUser(null)
      })
      .finally(() => setReady(true))
  }, [])

  const value = useMemo(
    () => ({
      user,
      ready,
      setUser,
      async login(username, password) {
        const tokens = await api('/auth/token/', {
          method: 'POST',
          auth: false,
          body: { username, password },
        })
        localStorage.setItem('access', tokens.access)
        localStorage.setItem('refresh', tokens.refresh)
        const me = await api('/auth/me/')
        setUser(me)
        return me
      },
      async register(payload) {
        const data = await api('/auth/register/', {
          method: 'POST',
          auth: false,
          body: payload,
        })
        localStorage.setItem('access', data.access)
        localStorage.setItem('refresh', data.refresh)
        setUser(data.user)
        return data.user
      },
      logout() {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        setUser(null)
      },
      async refreshUser() {
        const me = await api('/auth/me/')
        setUser(me)
        return me
      },
    }),
    [user, ready],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}

export function Protected({ children }) {
  const { user, ready } = useAuth()
  const location = useLocation()
  if (!ready) return <p className="page-loading">Loading your workspace…</p>
  if (!user) return <Navigate to="/login" replace state={{ from: location.pathname }} />
  return children
}
