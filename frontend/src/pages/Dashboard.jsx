import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, errorMessage } from '../api'
import { useAuth } from '../auth'
import { Readiness } from '../components/ui'

export default function Dashboard() {
  const { user, setUser } = useAuth()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [profile, setProfile] = useState(null)
  const [notice, setNotice] = useState('')

  useEffect(() => {
    if (!user) return
    setProfile({
      full_name: user.profile.full_name,
      headline: user.profile.headline,
      college: user.profile.college,
      graduation_year: user.profile.graduation_year || '',
      bio: user.profile.bio,
    })
  }, [user])

  function load() {
    return api('/dashboard/')
      .then(setData)
      .catch((err) => setError(errorMessage(err)))
  }

  useEffect(() => {
    load()
  }, [])

  async function saveProfile(event) {
    event.preventDefault()
    setNotice('')
    setError('')
    try {
      const updated = await api('/auth/me/', {
        method: 'PATCH',
        body: {
          ...profile,
          graduation_year: profile.graduation_year ? Number(profile.graduation_year) : null,
        },
      })
      setUser(updated)
      setNotice('Profile saved.')
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  async function setStep(step, status) {
    setError('')
    try {
      await api(`/me/steps/${step.id}/`, { method: 'PATCH', body: { status } })
      await load()
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  if (!data || !profile) {
    return <p className="page-loading">{error || 'Loading your dashboard…'}</p>
  }

  return (
    <section className="page">
      <div className="section-head">
        <div>
          <p className="eyebrow">{profile.college || 'Student workspace'}</p>
          <h1>Hello, {profile.full_name.split(' ')[0]}.</h1>
        </div>
      </div>
      {error && <p className="banner-error">{error}</p>}
      {notice && <p className="banner-ok">{notice}</p>}

      <div className="dash-grid">
        <article className="card target-card">
          {data.target ? (
            <>
              <Readiness value={data.target.readiness} accent={data.target.accent} />
              <div>
                <p className="eyebrow">Target role</p>
                <h2>{data.target.title}</h2>
                <p>{data.target.summary}</p>
                <p className="fine">
                  Roadmap {data.roadmap.completed} of {data.roadmap.total} steps · {data.roadmap.percent}%
                </p>
                <Link className="btn btn-primary" to={`/careers/${data.target.slug}`}>
                  Continue roadmap
                </Link>
              </div>
            </>
          ) : (
            <div>
              <h2>Choose a direction</h2>
              <p>Rate a few skills, then set one career as your path. The dashboard will track the gap.</p>
              <Link className="btn btn-primary" to="/careers">
                Browse careers
              </Link>
            </div>
          )}
        </article>

        <article className="card stat">
          <strong>{data.skills_rated}</strong>
          <span>of {data.skills_total} skills rated</span>
          <Link to="/skills">Update skills</Link>
        </article>
        <article className="card stat">
          <strong>{data.roadmap.percent}%</strong>
          <span>roadmap complete</span>
          <div className="track">
            <span style={{ width: `${data.roadmap.percent}%` }} />
          </div>
        </article>
      </div>

      <div className="split">
        <section className="card">
          <h2>Next steps</h2>
          {data.next_steps.length === 0 ? (
            <p className="muted">
              {data.target
                ? 'Every step on this roadmap is done. Pick another career or raise a skill that is still short.'
                : 'Set a target career to get a short list of what to practice.'}
            </p>
          ) : (
            <ul className="step-list">
              {data.next_steps.map((step) => (
                <li key={step.id}>
                  <div>
                    <span className="pill">{step.stage}</span>
                    <h3>{step.title}</h3>
                    <p>{step.detail}</p>
                  </div>
                  <div className="row-actions">
                    {step.status !== 'in_progress' && (
                      <button className="btn btn-ghost" type="button" onClick={() => setStep(step, 'in_progress')}>
                        Start
                      </button>
                    )}
                    <button className="btn btn-primary" type="button" onClick={() => setStep(step, 'completed')}>
                      Done
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="card">
          <h2>Biggest skill gaps</h2>
          {data.top_gaps.length === 0 ? (
            <p className="muted">
              {data.target
                ? 'You meet the published skill bar for this role.'
                : 'Gaps appear after you choose a target career.'}
            </p>
          ) : (
            <ul className="gap-list">
              {data.top_gaps.map((gap) => (
                <li key={gap.skill_slug}>
                  <div>
                    <strong>{gap.skill_name}</strong>
                    <span>
                      You {gap.current_level} · role {gap.required_level}
                    </span>
                  </div>
                  <em>{gap.importance}</em>
                </li>
              ))}
            </ul>
          )}
          <h2 className="spaced">Close careers</h2>
          <ul className="suggest">
            {data.suggestions.map((career) => (
              <li key={career.slug}>
                <Link to={`/careers/${career.slug}`}>{career.title}</Link>
                <span>{career.readiness}%</span>
              </li>
            ))}
          </ul>
        </section>
      </div>

      <form className="card form profile-form" onSubmit={saveProfile}>
        <h2>Profile</h2>
        <div className="form-grid">
          <label>
            Full name
            <input
              value={profile.full_name}
              onChange={(event) => setProfile({ ...profile, full_name: event.target.value })}
              required
            />
          </label>
          <label>
            Headline
            <input
              value={profile.headline}
              onChange={(event) => setProfile({ ...profile, headline: event.target.value })}
            />
          </label>
          <label>
            College
            <input
              value={profile.college}
              onChange={(event) => setProfile({ ...profile, college: event.target.value })}
            />
          </label>
          <label>
            Graduation year
            <input
              type="number"
              min="2000"
              max="2045"
              value={profile.graduation_year}
              onChange={(event) => setProfile({ ...profile, graduation_year: event.target.value })}
            />
          </label>
        </div>
        <label>
          Bio
          <textarea
            rows="3"
            value={profile.bio}
            onChange={(event) => setProfile({ ...profile, bio: event.target.value })}
          />
        </label>
        <button className="btn btn-primary" type="submit">
          Save profile
        </button>
      </form>
    </section>
  )
}
