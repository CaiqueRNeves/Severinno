import { useEffect, useState } from 'react'

const ACCESS_KEY = 'severinno.accessToken'

export function useAuthToken() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(ACCESS_KEY))

  const saveToken = (value: string | null) => {
    if (value) {
      localStorage.setItem(ACCESS_KEY, value)
    } else {
      localStorage.removeItem(ACCESS_KEY)
    }
    setToken(value)
  }

  useEffect(() => {
    const handler = (event: StorageEvent) => {
      if (event.key === ACCESS_KEY) {
        setToken(event.newValue)
      }
    }

    window.addEventListener('storage', handler)
    return () => window.removeEventListener('storage', handler)
  }, [])

  return { token, saveToken }
}
