import type { AdminStats } from '../../hooks/useAdminData'

interface Props {
  stats: AdminStats
  loading: boolean
}

export function AdminDashboardPage({ stats, loading }: Props) {
  const cards = [
    { label: 'Reservas Hoje', value: stats.reservationsToday, description: 'Contabiliza reservas retornadas pela API.' },
    { label: 'Solicitações pendentes', value: stats.pendingSoftware, description: 'Baseado no status de software requests.' },
    { label: 'Salas disponíveis', value: stats.availableRooms, description: 'Salas ativas no endpoint /api/rooms/.' },
  ]

  return (
    <section>
      <header className="mb-6">
        <p className="text-sm uppercase text-slate-500">Painel Administrativo</p>
        <h1 className="text-3xl font-semibold text-slate-800">Visão geral</h1>
        <p className="text-slate-500">
          Todos os cartões consomem os endpoints do backend assim que o token de administrador for utilizado.
        </p>
      </header>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {cards.map((card) => (
          <article key={card.label} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm text-slate-500">{card.label}</p>
            <p className="mt-2 text-4xl font-bold text-slate-900">{loading ? '...' : card.value}</p>
            <p className="mt-2 text-sm text-slate-500">{card.description}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
