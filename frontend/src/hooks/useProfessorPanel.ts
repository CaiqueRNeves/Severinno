import { useCallback, useEffect, useMemo, useState } from 'react'
import { apiFetch } from '../lib/api'

export type Reservation = {
  id: number
  room_name?: string
  room?: number
  date: string
  start_time: string
  end_time: string
  status: string
}

export type Availability = {
  room_id: number
  room_name: string
  room_code: string
  available: boolean
}

const mockReservations: Reservation[] = [
  {
    id: 1,
    room_name: 'LAB REDES',
    date: '2025-01-10',
    start_time: '10:00',
    end_time: '12:00',
    status: 'SCHEDULED',
  },
]

const mockAvailability: Availability[] = [
  { room_id: 1, room_name: 'LAB 101', room_code: 'LAB101', available: true },
  { room_id: 2, room_name: 'LAB 102', room_code: 'LAB102', available: false },
]

export function useProfessorPanel(token: string | null) {
  const [reservations, setReservations] = useState<Reservation[]>(mockReservations)
  const [availability, setAvailability] = useState<Availability[]>(mockAvailability)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const authHeaders = useMemo(() => (token ? { auth: token } : undefined), [token])

  const fetchReservations = useCallback(async () => {
    if (!token) return
    setLoading(true)
    try {
      const data = await apiFetch('/api/reservations/', { method: 'GET', ...authHeaders })
      setReservations(data as Reservation[])
      setError(null)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }, [token, authHeaders])

  useEffect(() => {
    fetchReservations()
  }, [fetchReservations])

  const fetchAvailability = useCallback(
    async (date: string, start: string, end: string) => {
      if (!token) {
        setAvailability(mockAvailability)
        return
      }
      setLoading(true)
      try {
        const query = new URLSearchParams({ date, start_time: start, end_time: end })
        const data = await apiFetch(`/api/reservations/available/?${query.toString()}`, {
          method: 'GET',
          ...authHeaders,
        })
        setAvailability(data as Availability[])
        setError(null)
      } catch (err) {
        setError((err as Error).message)
      } finally {
        setLoading(false)
      }
    },
    [token, authHeaders],
  )

  const cancelReservation = useCallback(
    async (id: number) => {
      if (!token) {
        setError('É necessário estar logado para cancelar reservas.')
        return false
      }
      try {
        await apiFetch(`/api/reservations/${id}/cancel/`, { method: 'POST', ...authHeaders })
        await fetchReservations()
        return true
      } catch (err) {
        setError((err as Error).message)
        return false
      }
    },
    [token, authHeaders, fetchReservations],
  )

  return { reservations, availability, fetchAvailability, cancelReservation, loading, error }
}
