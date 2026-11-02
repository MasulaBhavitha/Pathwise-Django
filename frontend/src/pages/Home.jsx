import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../auth'

const STEPS = [
  ['01', 'Rate your skills', 'Be honest about six areas, from programming to how you write and present.'],
  ['02', 'Pick a career', 'Each role has a skill bar. Pathwise shows the gap, not a generic percentage.'],
  ['03', 'Walk the roadmap', 'Stages and steps tell you what to practice next, with a place to mark progress.'],
]

export default function Home() {
  const { user } = useAuth()
  const [careers, setCareers] = useState([])

  useEffect(() => {
    api('/careers/', { auth: false })
      .then(setCareers)
      .catch(() => setCareers([]))
  }, [])

  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Student skill and career roadmap</p>
          <h1>See the distance between what you know and the work you want.</h1>
          <p className="lede">
            Pathwise is a personal map for students. Rate real skills, compare them with a role,
            and follow a staged roadmap instead of collecting random tutorials.
          </p>
          <div className="hero-actions">
            {user ? (
              <Link className="btn btn-primary" to="/dashboard">
                Open your dashboard
              </Link>
            ) : (
              <Link className="btn btn-primary" to="/register">
                Start your map
              </Link>
            )}
            <Link className="btn btn-ghost" to="/careers">
              Browse careers
            </Link>
          </div>
        </div>
        <ol className="hero-map">
          <li>
            <span>Now</span>
            <strong>HTML, a little JavaScript</strong>
            <em>Class projects</em>
          </li>
          <li>
            <span>Next</span>
            <strong>React, APIs, accessibility</strong>
            <em>The gap that matters</em>
          </li>
          <li>
            <span>Role</span>
            <strong>Frontend engineer</strong>
            <em>A roadmap you can finish</em>
          </li>
        </ol>
      </section>

      <section className="band">
        {STEPS.map(([index, title, copy]) => (
          <article key={index}>
            <span>{index}</span>
            <h2>{title}</h2>
            <p>{copy}</p>
          </article>
        ))}
      </section>

      <section className="page">
        <div className="section-head">
          <h2>Six directions, already mapped</h2>
          <Link to="/careers">See all careers</Link>
        </div>
        <div className="career-grid">
          {careers.map((career) => (
            <Link key={career.slug} to={`/careers/${career.slug}`} className="career-card">
              <i style={{ background: career.accent }} />
              <h3>{career.title}</h3>
              <p>{career.summary}</p>
              <div className="meta">
                <span>{career.outlook}</span>
                <span>{career.salary_range}</span>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </>
  )
}
