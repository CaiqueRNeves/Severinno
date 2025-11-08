import type { Reservation } from '../hooks/useProfessorPanel'

interface Props {
  reservations: Reservation[]
  onCancel: (id: number) => Promise<void> | void
  canCancel: boolean
}

export function ReservationList({ reservations, onCancel, canCancel }: Props) {
  if (reservations.length === 0) {
    return <p className="text-sm text-slate-500">Nenhuma reserva encontrada.</p>
  }

  return (
    <ul className="space-y-3">
      {reservations.map((reservation) => (
        <li key={reservation.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <div className="flex items-center justify-between font-medium text-slate-700">
            <span>{reservation.room_name ?? reservation.room}</span>
            <span className="text-xs rounded bg-slate-100 px-2 py-1 uppercase tracking-wide">
              {reservation.status}
            </span>
          </div>
          <p className="text-sm text-slate-500">
            {reservation.date} • {reservation.start_time} - {reservation.end_time}
          </p>
          {canCancel && reservation.status === 'SCHEDULED' && (
            <button
              className="mt-3 text-sm font-medium text-brand-600 hover:underline"
              onClick={() => onCancel(reservation.id)}
            >
              Cancelar reserva
            </button>
          )}
        </li>
      ))}
    </ul>
  )
}
