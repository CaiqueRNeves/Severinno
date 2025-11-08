import type { Room } from '../../hooks/useAdminData'

interface Props {
  data: Room[]
}

export function AdminRoomsPage({ data }: Props) {
  return (
    <section>
      <header className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-slate-800">Salas</h2>
          <p className="text-sm text-slate-500">Permite editar capacidade, status e detalhes técnicos.</p>
        </div>
        <button className="rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white">Adicionar sala</button>
      </header>
      <div className="grid gap-4">
        {data.map((room) => (
          <article key={room.id} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-slate-800">{room.name}</h3>
                <p className="text-sm text-slate-500">Código {room.code} • Capacidade {room.capacity ?? '—'}</p>
              </div>
              <span className={`text-xs font-semibold ${room.is_active ? 'text-green-600' : 'text-red-500'}`}>
                {room.is_active ? 'Ativa' : 'Inativa'}
              </span>
            </div>
            <div className="mt-3 flex gap-3">
              <button className="text-sm font-medium text-brand-600 hover:underline">Editar</button>
              <button className="text-sm font-medium text-red-500 hover:underline">Excluir</button>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
