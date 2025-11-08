import { useCallback, useEffect, useState } from 'react'
import { apiFetch } from '../lib/api'

export type AdminStats = {
  reservationsToday: number
  pendingSoftware: number
  availableRooms: number
}

export type Professor = {
  id: number
  full_name?: string
  email: string
  matricula: string
  user_type: string
}

export type Room = {
  id: number
  name: string
  code: string
  capacity?: number
  is_active?: boolean
}

export type Machine = {
  id: number
  hostname?: string
  processador: string
  numero_serie: string
  room_name?: string
}

const mockStats: AdminStats = {
  reservationsToday: 8,
  pendingSoftware: 3,
  availableRooms: 5,
}

const mockProfessors: Professor[] = [
  { id: 1, full_name: 'Ana Lima', email: 'ana@example.com', matricula: 'PRF001', user_type: 'PROFESSOR' },
  { id: 2, full_name: 'Carlos Souza', email: 'carlos@example.com', matricula: 'PRF002', user_type: 'PROFESSOR' },
]

const mockRooms: Room[] = [
  { id: 1, name: 'Lab Redes', code: 'LABRED', capacity: 25, is_active: true },
  { id: 2, name: 'Lab IoT', code: 'LABIOT', capacity: 20, is_active: true },
]

const mockMachines: Machine[] = [
  { id: 1, hostname: 'PC-01', processador: 'Intel i5', numero_serie: 'SN-001', room_name: 'Lab Redes' },
  { id: 2, hostname: 'PC-02', processador: 'Ryzen 5', numero_serie: 'SN-002', room_name: 'Lab IoT' },
]

export function useAdminData(token: string | null) {
  const [stats, setStats] = useState<AdminStats>(mockStats)
  const [professors, setProfessors] = useState<Professor[]>(mockProfessors)
  const [rooms, setRooms] = useState<Room[]>(mockRooms)
  const [machines, setMachines] = useState<Machine[]>(mockMachines)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const headers = token ? { auth: token } : undefined

  const fetchAll = useCallback(async () => {
    if (!token) {
      setStats(mockStats)
      setProfessors(mockProfessors)
      setRooms(mockRooms)
      setMachines(mockMachines)
      return
    }
    try {
      setLoading(true)
      const [reservations, software, roomsData, machinesData, users] = await Promise.all([
        apiFetch('/api/reservations/', { method: 'GET', ...headers }) as Promise<any[]>,
        apiFetch('/api/software-requests/', { method: 'GET', ...headers }) as Promise<any[]>,
        apiFetch('/api/rooms/', { method: 'GET', ...headers }) as Promise<any[]>,
        apiFetch('/api/machines/', { method: 'GET', ...headers }) as Promise<any[]>,
        apiFetch('/api/accounts/me/', { method: 'GET', ...headers }).then(() => mockProfessors),
      ])
      setStats({
        reservationsToday: reservations.length,
        pendingSoftware: software.filter((item) => item.status !== 'INSTALLED').length,
        availableRooms: roomsData.filter((room) => room.is_active).length,
      })
      setProfessors(users as Professor[])
      setRooms(roomsData as Room[])
      setMachines(machinesData as Machine[])
      setError(null)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }, [token, headers])

  useEffect(() => {
    fetchAll()
  }, [fetchAll])

  return { stats, professors, rooms, machines, fetchAll, loading, error }
}
