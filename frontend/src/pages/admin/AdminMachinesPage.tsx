import type { Machine } from '../../hooks/useAdminData'

interface Props {
  data: Machine[]
}

export function AdminMachinesPage({ data }: Props) {
  return (
    <section>
      <header className="mb-4">
        <h2 className="text-2xl font-semibold text-slate-800">Máquinas</h2>
        <p className="text-sm text-slate-500">Gerencie hardware de cada sala e atualize status de disponibilidade.</p>
      </header>
      <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3">Hostname</th>
              <th className="px-4 py-3">Processador</th>
              <th className="px-4 py-3">Número de série</th>
              <th className="px-4 py-3">Sala</th>
              <th className="px-4 py-3">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {data.map((machine) => (
              <tr key={machine.id}>
                <td className="px-4 py-3 font-medium text-slate-800">{machine.hostname ?? '—'}</td>
                <td className="px-4 py-3 text-slate-600">{machine.processador}</td>
                <td className="px-4 py-3 text-slate-600">{machine.numero_serie}</td>
                <td className="px-4 py-3 text-slate-600">{machine.room_name ?? '—'}</td>
                <td className="px-4 py-3 text-slate-600">
                  <button className="text-xs font-semibold text-brand-600 hover:underline">Editar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
