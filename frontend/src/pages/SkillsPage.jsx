import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api'
import { LEVELS, LevelPicker } from '../components/ui'

export default function SkillsPage() {
  const [categories, setCategories] = useState([])
  const [active, setActive] = useState('')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(null)

  useEffect(() => {
    api('/skills/')
      .then((data) => {
        setCategories(data)
        setActive((current) => current || data[0]?.slug || '')
      })
      .catch((err) => setError(errorMessage(err)))
  }, [])

  const category = categories.find((item) => item.slug === active)

  async function rate(skill, level) {
    const previous = skill.level
    setCategories((current) =>
      current.map((group) => ({
        ...group,
        skills: group.skills.map((item) => (item.id === skill.id ? { ...item, level } : item)),
      })),
    )
    setSaving(skill.id)
    setError('')
    try {
      await api('/me/skills/', { method: 'PUT', body: { skill_id: skill.id, level } })
    } catch (err) {
      setCategories((current) =>
        current.map((group) => ({
          ...group,
          skills: group.skills.map((item) => (item.id === skill.id ? { ...item, level: previous } : item)),
        })),
      )
      setError(errorMessage(err))
    } finally {
      setSaving(null)
    }
  }

  return (
    <section className="page">
      <div className="section-head">
        <div>
          <p className="eyebrow">Skill inventory</p>
          <h1>Rate what you can do today.</h1>
          <p className="lede">
            {LEVELS[1]} means you have seen it. {LEVELS[3]} means you can use it without a tutorial open.
            {` ${LEVELS[5]} means you could teach it.`}
          </p>
        </div>
      </div>
      {error && <p className="banner-error">{error}</p>}
      <div className="chips">
        {categories.map((item) => (
          <button
            key={item.slug}
            type="button"
            className={item.slug === active ? 'chip on' : 'chip'}
            onClick={() => setActive(item.slug)}
          >
            {item.name}
          </button>
        ))}
      </div>
      {category && (
        <div className="card skill-card">
          <p className="muted">{category.description}</p>
          <ul className="skills">
            {category.skills.map((skill) => (
              <li key={skill.id}>
                <div>
                  <h2>{skill.name}</h2>
                  <p>{skill.description}</p>
                </div>
                <LevelPicker value={skill.level} disabled={saving === skill.id} onChange={(level) => rate(skill, level)} />
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  )
}
