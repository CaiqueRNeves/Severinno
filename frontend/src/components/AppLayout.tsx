import { Link, NavLink, Outlet } from 'react-router-dom'

const navLinks = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/reservas', label: 'Reservas' },
  { to: '/chat', label: 'Chat' },
  { to: '/admin', label: 'Admin' },
]

export function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/dashboard" className="text-xl font-semibold text-brand-700">
            Severinno
          </Link>
          <nav className="space-x-4">
            {navLinks.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `text-sm font-medium ${isActive ? 'text-brand-700' : 'text-slate-500 hover:text-slate-700'}`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}
