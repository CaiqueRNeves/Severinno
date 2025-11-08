import type { FormEvent } from 'react'
import { useState } from 'react'
import { API_URL } from '../lib/api'

export function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState<string | null>(null)

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setMessage('Realizando login (mock). Configure integração quando a API estiver pronta.')
    try {
      const response = await fetch(`${API_URL}/api/accounts/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      if (!response.ok) {
        throw new Error('Falha no login')
      }
      setMessage('Login realizado! Salve o token no armazenamento seguro.')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  return (
    <div className="max-w-md mx-auto bg-white shadow-sm rounded-lg p-8">
      <h1 className="text-2xl font-semibold text-slate-800 mb-6">Entrar no Severinno</h1>
      <form className="space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block mb-1 text-sm font-medium text-slate-700" htmlFor="email">
            Email institucional
          </label>
          <input
            id="email"
            type="email"
            className="w-full rounded border border-slate-200 px-3 py-2 focus:outline-none focus:ring focus:ring-brand-200"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>
        <div>
          <label className="block mb-1 text-sm font-medium text-slate-700" htmlFor="password">
            Senha
          </label>
          <input
            id="password"
            type="password"
            className="w-full rounded border border-slate-200 px-3 py-2 focus:outline-none focus:ring focus:ring-brand-200"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="w-full rounded bg-brand-600 py-2 text-white font-medium hover:bg-brand-700 transition"
        >
          Entrar
        </button>
      </form>
      {message && <p className="mt-4 text-sm text-slate-600">{message}</p>}
    </div>
  )
}
