export const LEVELS = ['Unrated', 'Aware', 'Beginner', 'Intermediate', 'Advanced', 'Expert']

export function Readiness({ value, accent = '#c45c26' }) {
  return (
    <div
      className="ring"
      style={{ '--p': value, '--accent': accent }}
      role="img"
      aria-label={`${value} percent ready`}
    >
      <span>
        {value}
        <small>%</small>
      </span>
    </div>
  )
}

export function LevelPicker({ value, onChange, disabled }) {
  return (
    <div className="levels" role="group" aria-label="Skill level">
      {LEVELS.map((label, index) => (
        <button
          key={label}
          type="button"
          className={index === value ? 'level on' : 'level'}
          aria-pressed={index === value}
          disabled={disabled}
          onClick={() => onChange(index)}
        >
          <b>{index}</b>
          {label}
        </button>
      ))}
    </div>
  )
}

export function Meter({ current, required }) {
  return (
    <div className="meter" aria-hidden="true">
      <span style={{ width: `${(current / 5) * 100}%` }} />
      <i style={{ left: `${(required / 5) * 100}%` }} />
    </div>
  )
}
