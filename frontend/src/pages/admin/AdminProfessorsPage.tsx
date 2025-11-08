import type { Professor } from '../../hooks/useAdminData'

interface Props {
  data: Professor[]
}

export function AdminProfessorsPage({ data }: Props) {
  return (
    <section>
      <header className="mb-4">
        <h2 className="text-2xl font-semibold text-slate-800">Professores cadastrados</h2>
        <p className="text-sm text-slate-500">Integre com /api/accounts/ ou endpoints específicos de administração.</p>
      </header>
      <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3">Nome</th>
              <th className="px-4 py-3">Email</th>
              <th className="px-4 py-3">Matrícula</th>
              <th className="px-4 py-3 text-right">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {data.map((professor) => (
              <tr key={professor.id}>
                <td className="px-4 py-3 font-medium text-slate-800">{professor.full_name ?? '—'}</td>
                <td className="px-4 py-3 text-slate-600">{professor.email}</td>
                <td className="px-4 py-3 text-slate-600">{professor.matricula}</td>
                <td className="px-4 py-3 text-right">
                  <button className="text-xs font-semibold text-brand-600 hover:underline">Editar</button>
                  <button className="ml-3 text-xs font-semibold text-red-500 hover:underline">Remover</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
