import type { FormEvent } from 'react'
import { useState } from 'react'
import { useAuthToken } from '../hooks/useAuthToken'
import { useChat } from '../hooks/useChat'

export function ChatPage() {
  const { token } = useAuthToken()
  const { conversations, messages, activeConversation, openConversation, sendMessage, error } = useChat(token)
  const [input, setInput] = useState('')

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (!input.trim()) return
    sendMessage(input.trim())
    setInput('')
  }

  return (
    <div className="grid gap-6 lg:grid-cols-4">
      <aside className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm lg:col-span-1">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-800">Conversas</h2>
          {!token && <span className="text-xs text-slate-400">Modo offline</span>}
        </div>
        <p className="text-sm text-slate-500">Selecione uma conversa para continuar o atendimento em tempo real.</p>
        <ul className="mt-4 space-y-2">
          {conversations.map((conversation) => (
            <li key={conversation.id}>
              <button
                onClick={() => openConversation(conversation.id)}
                className={`w-full rounded-lg border px-3 py-2 text-left text-sm transition ${
                  activeConversation === conversation.id
                    ? 'border-brand-500 bg-brand-50 text-brand-700'
                    : 'border-slate-200 text-slate-700 hover:border-brand-200'
                }`}
              >
                {conversation.title}
              </button>
            </li>
          ))}
        </ul>
      </aside>
      <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm lg:col-span-3 flex flex-col">
        <header className="border-b border-slate-100 pb-3 mb-3">
          <h2 className="text-lg font-semibold text-slate-800">Chat</h2>
          <p className="text-sm text-slate-500">
            O WebSocket é iniciado automaticamente para a conversa selecionada. Tokens JWT são passados via querystring.
          </p>
        </header>
        <div className="flex-1 overflow-y-auto space-y-3">
          {messages.map((message) => (
            <div key={message.id} className="rounded-lg border border-slate-100 bg-slate-50 p-3">
              <div className="text-xs text-slate-400">{message.sender}</div>
              <p className="text-sm text-slate-800">{message.content}</p>
              <span className="text-[10px] text-slate-400">{new Date(message.created_at).toLocaleString()}</span>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
          <input
            type="text"
            className="flex-1 rounded border border-slate-200 px-3 py-2"
            placeholder={token ? 'Digite sua mensagem' : 'Entre como administrador para enviar mensagens reais'}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={!token}
          />
          <button className="rounded bg-brand-600 px-4 py-2 text-white" disabled={!token}>
            Enviar
          </button>
        </form>
        {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
      </section>
    </div>
  )
}
