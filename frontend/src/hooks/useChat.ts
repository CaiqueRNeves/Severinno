import { useCallback, useEffect, useRef, useState } from 'react'
import { API_URL, apiFetch } from '../lib/api'

export type Conversation = {
  id: number
  title: string
}

export type ChatMessage = {
  id: number
  sender: string
  content: string
  created_at: string
}

const mockConversations: Conversation[] = [
  { id: 1, title: 'Suporte geral (mock)' },
]

const mockMessages: ChatMessage[] = [
  { id: 1, sender: 'admin@example.com', content: 'Bem-vindo ao Severinno!', created_at: new Date().toISOString() },
]

const WS_BASE = API_URL.replace('http', 'ws')

export function useChat(token: string | null) {
  const [conversations, setConversations] = useState<Conversation[]>(mockConversations)
  const [messages, setMessages] = useState<ChatMessage[]>(mockMessages)
  const [activeConversation, setActiveConversation] = useState<number | null>(null)
  const [error, setError] = useState<string | null>(null)
  const wsRef = useRef<WebSocket | null>(null)

  const fetchConversations = useCallback(async () => {
    if (!token) return
    try {
      const data = await apiFetch('/api/chat/conversations/', { method: 'GET', auth: token })
      setConversations(data as Conversation[])
      setError(null)
    } catch (err) {
      setError((err as Error).message)
    }
  }, [token])

  const fetchMessages = useCallback(
    async (conversationId: number) => {
      if (!token) return
      try {
        const data = await apiFetch(`/api/chat/conversations/${conversationId}/messages/`, { method: 'GET', auth: token })
        setMessages(data as ChatMessage[])
      } catch (err) {
        setError((err as Error).message)
      }
    },
    [token],
  )

  const connectWebSocket = useCallback(
    (conversationId: number) => {
      if (!token) return
      wsRef.current?.close()
      const socket = new WebSocket(`${WS_BASE}/ws/chat/${conversationId}/?token=${token}`)
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        setMessages((prev) => [...prev, data as ChatMessage])
      }
      socket.onerror = () => {
        setError('Falha no WebSocket, verifique o worker/Redis.')
      }
      wsRef.current = socket
    },
    [token],
  )

  const openConversation = useCallback(
    async (conversationId: number) => {
      setActiveConversation(conversationId)
      if (!token) {
        setMessages(mockMessages)
        return
      }
      await fetchMessages(conversationId)
      connectWebSocket(conversationId)
    },
    [token, fetchMessages, connectWebSocket],
  )

  const sendMessage = useCallback(
    (text: string) => {
      if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
        setMessages((prev) => [...prev, { id: Date.now(), sender: 'Você', content: text, created_at: new Date().toISOString() }])
        return
      }
      wsRef.current.send(JSON.stringify({ message: text }))
    },
    [],
  )

  useEffect(() => {
    if (token) {
      fetchConversations()
    }
    return () => wsRef.current?.close()
  }, [token, fetchConversations])

  return { conversations, messages, activeConversation, openConversation, sendMessage, error }
}
