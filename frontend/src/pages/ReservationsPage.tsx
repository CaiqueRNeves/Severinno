import type { FormEvent } from 'react'
import { useState } from 'react'

export function ReservationsPage() {
  const [formState, setFormState] = useState({
    room: '',
    date: '',
    start: '',
    end: '',
  })
  const [feedback, setFeedback] = useState<string | null>(null)

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setFeedback('Envie os dados para /api/reservations/ quando a API estiver disponível.')
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-800">Criar reserva</h2>
        <p className="text-sm text-slate-500">
          Conecte este formulário ao endpoint /api/reservations/ para gravar reservas reais.
        </p>
        <form className="mt-4 space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium text-slate-600">Sala</label>
            <input
              className="mt-1 w-full rounded border border-slate-200 px-3 py-2"
              placeholder="Ex: LAB01"
              value={formState.room}
              onChange={(e) => setFormState({ ...formState, room: e.target.value })}
              required
            />
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-slate-600">Data</label>
              <input
                type="date"
                className="mt-1 w-full rounded border border-slate-200 px-3 py-2"
                value={formState.date}
                onChange={(e) => setFormState({ ...formState, date: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600">Hora inicial</label>
              <input
                type="time"
                className="mt-1 w-full rounded border border-slate-200 px-3 py-2"
                value={formState.start}
                onChange={(e) => setFormState({ ...formState, start: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600">Hora final</label>
              <input
                type="time"
                className="mt-1 w-full rounded border border-slate-200 px-3 py-2"
                value={formState.end}
                onChange={(e) => setFormState({ ...formState, end: e.target.value })}
                required
              />
            </div>
          </div>
          <button className="rounded bg-brand-600 px-4 py-2 text-white">Reservar</button>
        </form>
        {feedback && <p className="mt-4 text-sm text-slate-500">{feedback}</p>}
      </section>
      <section>
        <h2 className="text-xl font-semibold text-slate-800">Reservas recentes</h2>
        <p className="text-sm text-slate-500">
          Consuma /api/reservations/ para listar reservas reais. Abaixo um placeholder:
        </p>
        <div className="mt-4 space-y-3">
          {[1, 2, 3].map((item) => (
            <div key={item} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
              <p className="text-sm font-semibold text-slate-700">Laboratório placeholder {item}</p>
              <p className="text-sm text-slate-500">Data/hora serão preenchidas dinamicamente.</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
