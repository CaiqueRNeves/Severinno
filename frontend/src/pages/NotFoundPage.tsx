import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <div className="text-center space-y-4">
      <p className="text-sm uppercase tracking-widest text-slate-500">Erro 404</p>
      <h1 className="text-3xl font-semibold text-slate-800">Página não encontrada</h1>
      <p className="text-slate-500">Verifique o endereço ou retorne para o dashboard.</p>
      <Link to="/dashboard" className="inline-flex items-center rounded bg-brand-600 px-4 py-2 text-white">
        Voltar ao início
      </Link>
    </div>
  )
}
