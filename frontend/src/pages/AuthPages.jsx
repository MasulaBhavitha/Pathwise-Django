import { useState } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { errorMessage } from '../api'
import { useAuth } from '../auth'

export function Login() {
  const { login, user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)
  const destination = location.state?.from || '/dashboard'

  if (user) return <Navigate to={destination} replace />

  async function submit(event) {
    event.preventDefault()
    setPending(true)
    setError('')
    try {
      await login(username.trim(), password)
      navigate(destination, { replace: true })
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setPending(false)
    }
  }

  return (
    <section className="auth">
      <div>
        <p className="eyebrow">Welcome back</p>
        <h1>Sign in to your roadmap.</h1>
        <p className="lede">The demo student is Maya Chen. Username <b>demo</b>, password <b>pathwise123</b>.</p>
      </div>
      <form className="card form" onSubmit={submit}>
        {error && <p className="banner-error">{error}</p>}
        <label>
          Username
          <input value={username} onChange={(event) => setUsername(event.target.value)} autoComplete="username" required />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            required
          />
        </label>
        <button className="btn btn-primary" type="submit" disabled={pending}>
          {pending ? 'Signing in…' : 'Sign in'}
        </button>
        <button
          className="btn btn-ghost"
          type="button"
          onClick={() => {
            setUsername('demo')
            setPassword('pathwise123')
          }}
        >
          Fill demo account
        </button>
        <p className="fine">
          New here? <Link to="/register">Create an account</Link>
        </p>
      </form>
    </section>
  )
}

export function Register() {
  const { register, user } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    full_name: '',
    username: '',
    email: '',
    college: '',
    password: '',
  })
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)

  if (user) return <Navigate to="/dashboard" replace />

  function update(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }))
  }

  async function submit(event) {
    event.preventDefault()
    setPending(true)
    setError('')
    try {
      await register({ ...form, username: form.username.trim(), email: form.email.trim() })
      navigate('/skills', { replace: true })
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setPending(false)
    }
  }

  return (
    <section className="auth">
      <div>
        <p className="eyebrow">New student</p>
        <h1>Create the map, then rate what you already know.</h1>
        <p className="lede">
          You will land on the skill inventory. A few honest ratings are enough to compare careers.
        </p>
      </div>
      <form className="card form" onSubmit={submit}>
        {error && <p className="banner-error">{error}</p>}
        <label>
          Full name
          <input name="full_name" value={form.full_name} onChange={update} required />
        </label>
        <label>
          Username
          <input name="username" value={form.username} onChange={update} autoComplete="username" required />
        </label>
        <label>
          Email
          <input name="email" type="email" value={form.email} onChange={update} autoComplete="email" required />
        </label>
        <label>
          College
          <input name="college" value={form.college} onChange={update} />
        </label>
        <label>
          Password
          <input
            name="password"
            type="password"
            value={form.password}
            onChange={update}
            autoComplete="new-password"
            minLength={8}
            required
          />
        </label>
        <button className="btn btn-primary" type="submit" disabled={pending}>
          {pending ? 'Creating…' : 'Create account'}
        </button>
        <p className="fine">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </form>
    </section>
  )
}
