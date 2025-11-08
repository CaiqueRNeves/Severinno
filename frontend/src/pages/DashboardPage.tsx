const highlights = [
  {
    title: 'Reservas ativas',
    value: '—',
    description: 'Integre com /api/reservations/ para exibir dados reais.',
  },
  {
    title: 'Solicitações de software',
    value: '—',
    description: 'Conecte em /api/software-requests/ para acompanhar pendências.',
  },
  {
    title: 'Alertas não lidos',
    value: '—',
    description: 'Use /api/notifications/ para listar notificações.',
  },
]

export function DashboardPage() {
  return (
    <section>
      <header className="mb-6">
        <p className="text-sm uppercase text-slate-500">Visão geral</p>
        <h1 className="text-3xl font-semibold text-slate-800">Painel Severinno</h1>
        <p className="text-slate-500">Os cartões abaixo serão preenchidos automaticamente após integrar com a API.</p>
      </header>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {highlights.map((item) => (
          <div key={item.title} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm text-slate-500">{item.title}</p>
            <p className="mt-2 text-3xl font-semibold text-slate-900">{item.value}</p>
            <p className="mt-2 text-sm text-slate-500">{item.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
