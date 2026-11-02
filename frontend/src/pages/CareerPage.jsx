import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, errorMessage } from '../api'
import { useAuth } from '../auth'
import { LEVELS, Meter, Readiness } from '../components/ui'

const STATUSES = [
  ['not_started', 'To do'],
  ['in_progress', 'Doing'],
  ['completed', 'Done'],
]

export default function CareerPage() {
  const { slug } = useParams()
  const { user, refreshUser } = useAuth()
  const [career, setCareer] = useState(null)
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)

  useEffect(() => {
    setCareer(null)
    api(`/careers/${slug}/`)
      .then(setCareer)
      .catch((err) => setError(errorMessage(err)))
  }, [slug, user])

  async function choosePath() {
    setPending(true)
    setError('')
    try {
      await api('/me/target/', {
        method: 'PUT',
        body: { career_slug: career.is_target ? null : career.slug },
      })
      await refreshUser()
      const fresh = await api(`/careers/${slug}/`)
      setCareer(fresh)
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setPending(false)
    }
  }

  async function setStatus(stepId, status) {
    const previous = career
    setCareer({
      ...career,
      stages: career.stages.map((stage) => ({
        ...stage,
        steps: stage.steps.map((step) => (step.id === stepId ? { ...step, status } : step)),
      })),
    })
    try {
      await api(`/me/steps/${stepId}/`, { method: 'PATCH', body: { status } })
    } catch (err) {
      setCareer(previous)
      setError(errorMessage(err))
    }
  }

  if (!career) {
    return <p className="page-loading">{error || 'Loading roadmap…'}</p>
  }

  const steps = career.stages.flatMap((stage) => stage.steps)
  const done = steps.filter((step) => step.status === 'completed').length
  const percent = steps.length ? Math.round((100 * done) / steps.length) : 0

  return (
    <section className="page">
      <div className="career-hero">
        <div>
          <p className="eyebrow">{career.outlook} · typical US range {career.salary_range}</p>
          <h1>{career.title}</h1>
          <p className="lede">{career.description}</p>
          <div className="hero-actions">
            {user ? (
              <button className="btn btn-primary" type="button" onClick={choosePath} disabled={pending}>
                {career.is_target ? 'Remove as my path' : 'Set as my path'}
              </button>
            ) : (
              <Link className="btn btn-primary" to="/login" state={{ from: `/careers/${career.slug}` }}>
                Sign in to track this path
              </Link>
            )}
            <Link className="btn btn-ghost" to="/skills">
              Rate skills
            </Link>
          </div>
        </div>
        <div className="card score-card">
          <Readiness value={career.readiness} accent={career.accent} />
          <div>
            <strong>Skill readiness</strong>
            <p>{user ? 'Based on your ratings. Core skills count double.' : 'Sign in and rate skills to personalize this.'}</p>
            <p className="fine">
              Roadmap {done}/{steps.length} · {percent}%
            </p>
          </div>
        </div>
      </div>
      {error && <p className="banner-error">{error}</p>}

      <section className="card">
        <h2>Skills this role expects</h2>
        <ul className="reqs">
          {career.requirements.map((item) => (
            <li key={item.skill_id}>
              <div>
                <strong>{item.skill_name}</strong>
                <span>
                  {item.category} · {item.importance} · you {LEVELS[item.current_level]} · need {LEVELS[item.required_level]}
                </span>
              </div>
              <Meter current={item.current_level} required={item.required_level} />
              {item.gap > 0 && <em className="gap">+{item.gap}</em>}
            </li>
          ))}
        </ul>
      </section>

      <section className="timeline">
        {career.stages.map((stage, index) => (
          <article key={stage.id} className="card stage">
            <header>
              <span>Stage {index + 1}</span>
              <h2>{stage.title}</h2>
              <p>
                {stage.summary} · about {stage.weeks} weeks
              </p>
            </header>
            <ol>
              {stage.steps.map((step) => (
                <li key={step.id} className={`step ${step.status}`}>
                  <div>
                    <h3>{step.title}</h3>
                    <p>{step.detail}</p>
                    <p className="fine">
                      {step.skill_name && <span>Practice: {step.skill_name}</span>}
                      {step.resource_url && (
                        <a href={step.resource_url} target="_blank" rel="noreferrer">
                          {step.resource_label || 'Resource'}
                        </a>
                      )}
                    </p>
                  </div>
                  {user ? (
                    <div className="status">
                      {STATUSES.map(([value, label]) => (
                        <button
                          key={value}
                          type="button"
                          className={step.status === value ? 'on' : ''}
                          onClick={() => setStatus(step.id, value)}
                        >
                          {label}
                        </button>
                      ))}
                    </div>
                  ) : (
                    <span className="pill">Sign in to track</span>
                  )}
                </li>
              ))}
            </ol>
          </article>
        ))}
      </section>
    </section>
  )
}
