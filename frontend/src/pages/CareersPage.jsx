import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, errorMessage } from '../api'
import { useAuth } from '../auth'
import { Readiness } from '../components/ui'

export default function CareersPage() {
  const { user } = useAuth()
  const [careers, setCareers] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    api('/careers/')
      .then(setCareers)
      .catch((err) => setError(errorMessage(err)))
  }, [user])

  return (
    <section className="page">
      <div className="section-head">
        <div>
          <p className="eyebrow">Career catalog</p>
          <h1>Pick a role worth preparing for.</h1>
          <p className="lede">
            {user
              ? 'The percentage is how close your current ratings are to that role. Core skills count more.'
              : 'Sign in to compare these roles with your own skill ratings.'}
          </p>
        </div>
      </div>
      {error && <p className="banner-error">{error}</p>}
      <div className="career-grid">
        {careers.map((career) => (
          <Link key={career.slug} to={`/careers/${career.slug}`} className="career-card tall">
            <i style={{ background: career.accent }} />
            <div className="career-top">
              <h2>{career.title}</h2>
              {user && <Readiness value={career.readiness} accent={career.accent} />}
            </div>
            <p>{career.summary}</p>
            <div className="meta">
              <span>{career.outlook}</span>
              <span>{career.salary_range}</span>
              <span>{career.core_skill_count} core skills</span>
            </div>
            {career.is_target && <em className="pill">Your path</em>}
          </Link>
        ))}
      </div>
    </section>
  )
}
