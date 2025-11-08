import type { FormEvent } from 'react'
import { useState } from 'react'
import { ReservationList } from '../components/ReservationList'
import { useAuthToken } from '../hooks/useAuthToken'
import { useProfessorPanel } from '../hooks/useProfessorPanel'

export function ReservationsPage() {
  const [formState, setFormState] = useState({
    room: '',
    date: '',
    start: '',
    end: '',
  })
  const [feedback, setFeedback] = useState<string | null>(null)
  const { token } = useAuthToken()
  const { reservations, availability, fetchAvailability, cancelReservation, loading, error } = useProfessorPanel(token)

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    const date = formState.date || new Date().toISOString().slice(0, 10)
    const start = formState.start || '08:00'
    const end = formState.end || '10:00'
    setFeedback('Consultando disponibilidade...')
    await fetchAvailability(date, start, end)
    setFeedback('Salas atualizadas!')
  }

  return (
    <div className="space-y-8">
      <div className="grid gap-6 lg:grid-cols-2">
      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-800">Criar reserva</h2>
        <p className="text-sm text-slate-500">
          Informe data e horário para consultar /api/reservations/available/. Com token salvo, o botão envia a requisição real.
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
        {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
      </section>
      <section>
        <h2 className="text-xl font-semibold text-slate-800">Salas disponíveis</h2>
        <p className="text-sm text-slate-500">Os dados abaixo refletem a última consulta realizada.</p>
        <div className="mt-4 space-y-3">
          {availability.map((room) => (
            <div
              key={room.room_id}
              className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm flex items-center justify-between"
            >
              <div>
                <p className="text-sm font-semibold text-slate-700">{room.room_name}</p>
                <p className="text-xs text-slate-500">Código: {room.room_code}</p>
              </div>
              <span className={`text-xs font-semibold ${room.available ? 'text-green-600' : 'text-red-500'}`}>
                {room.available ? 'Disponível' : 'Ocupada'}
              </span>
            </div>
          ))}
        </div>
      </section>
    </div>
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-slate-800">Minhas reservas</h2>
          <p className="text-sm text-slate-500">Ações de cancelamento exigem autenticação (token salvo no login).</p>
        </div>
        <button
          disabled={loading}
          onClick={() => fetchAvailability(formState.date || new Date().toISOString().slice(0, 10), formState.start || '08:00', formState.end || '10:00')}
          className="rounded bg-slate-100 px-3 py-2 text-sm font-medium text-slate-700"
        >
          Atualizar
        </button>
      </div>
      <div className="mt-4">
        <ReservationList
          reservations={reservations}
          onCancel={(id) => cancelReservation(id).then(() => undefined)}
          canCancel={Boolean(token)}
        />
      </div>
    </section>
  </div>
  )
}
