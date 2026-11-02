import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth'

export default function Shell() {
  const { user, ready, logout } = useAuth()
  const navigate = useNavigate()
  const roadmap = user?.profile?.target_career

  return (
    <div className="app">
      <header className="nav">
        <NavLink to="/" end className="brand" aria-label="Pathwise home">
          <span className="mark" aria-hidden="true" />
          Pathwise
        </NavLink>
        <nav className="nav-links">
          {ready && user && (
            <>
              <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'nav-link on' : 'nav-link')}>
                Dashboard
              </NavLink>
              <NavLink to="/skills" className={({ isActive }) => (isActive ? 'nav-link on' : 'nav-link')}>
                Skills
              </NavLink>
            </>
          )}
          <NavLink to="/careers" end className={({ isActive }) => (isActive ? 'nav-link on' : 'nav-link')}>
            Careers
          </NavLink>
          {ready && roadmap && (
            <NavLink
              to={`/careers/${roadmap.slug}`}
              className={({ isActive }) => (isActive ? 'nav-link on' : 'nav-link')}
            >
              My roadmap
            </NavLink>
          )}
        </nav>
        <div className="nav-end">
          {!ready ? (
            <span className="who">Loading…</span>
          ) : user ? (
            <>
              <span className="who">{user.profile.full_name}</span>
              <button
                className="btn btn-ghost"
                type="button"
                onClick={() => {
                  logout()
                  navigate('/')
                }}
              >
                Sign out
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className="btn btn-ghost">
                Sign in
              </NavLink>
              <NavLink to="/register" className="btn btn-primary">
                Create account
              </NavLink>
            </>
          )}
        </div>
      </header>
      <Outlet />
      <footer className="footer">
        Pathwise keeps a student skill inventory, a career comparison, and a roadmap you can mark off.
        Salary figures are illustrative US ranges.
      </footer>
    </div>
  )
}
