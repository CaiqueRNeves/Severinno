import { useAuthToken } from '../../hooks/useAuthToken'
import { useAdminData } from '../../hooks/useAdminData'
import { AdminDashboardPage } from './AdminDashboardPage'
import { AdminProfessorsPage } from './AdminProfessorsPage'
import { AdminRoomsPage } from './AdminRoomsPage'
import { AdminMachinesPage } from './AdminMachinesPage'

export function AdminPanelPage() {
  const { token } = useAuthToken()
  const { stats, professors, rooms, machines, fetchAll, loading, error } = useAdminData(token)

  return (
    <div className="space-y-10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-widest text-slate-500">Área administrativa</p>
          <h1 className="text-3xl font-semibold text-slate-800">Controle geral</h1>
          <p className="text-sm text-slate-500">
            Use o login de administrador para que os cards sejam preenchidos dinamicamente a partir dos endpoints REST.
          </p>
        </div>
        <button
          onClick={fetchAll}
          className="rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
          disabled={loading}
        >
          Atualizar dados
        </button>
      </div>
      {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-600">{error}</p>}
      <AdminDashboardPage stats={stats} loading={loading} />
      <AdminProfessorsPage data={professors} />
      <AdminRoomsPage data={rooms} />
      <AdminMachinesPage data={machines} />
    </div>
  )
}
