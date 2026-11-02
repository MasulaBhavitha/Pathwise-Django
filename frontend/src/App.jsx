import { Route, Routes } from 'react-router-dom'
import { Protected } from './auth'
import Shell from './components/Shell'
import CareerPage from './pages/CareerPage'
import CareersPage from './pages/CareersPage'
import Dashboard from './pages/Dashboard'
import Home from './pages/Home'
import { Login, Register } from './pages/AuthPages'
import SkillsPage from './pages/SkillsPage'

export default function App() {
  return (
    <Routes>
      <Route element={<Shell />}>
        <Route index element={<Home />} />
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route path="careers" element={<CareersPage />} />
        <Route path="careers/:slug" element={<CareerPage />} />
        <Route path="skills" element={<Protected><SkillsPage /></Protected>} />
        <Route path="dashboard" element={<Protected><Dashboard /></Protected>} />
        <Route path="*" element={<section className="page"><h1>That page is not on the map.</h1></section>} />
      </Route>
    </Routes>
  )
}
