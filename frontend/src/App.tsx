import { useEffect, useState } from 'react'

const apiBaseUrl = (
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
).replace(/\/+$/, '')

const statusMessages = {
  checking: 'Checking backend...',
  connected: 'Backend connected.',
  unavailable: 'Backend unavailable. Start the FastAPI server.',
}

type BackendStatus = keyof typeof statusMessages

export default function App() {
  const [backendStatus, setBackendStatus] = useState<BackendStatus>('checking')

  useEffect(() => {
    const controller = new AbortController()

    fetch(`${apiBaseUrl}/health`, { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error('Health check failed')
        }

        const data: { status?: unknown } = await response.json()
        if (data.status !== 'ok') {
          throw new Error('Unexpected health-check response')
        }

        setBackendStatus('connected')
      })
      .catch(() => {
        if (!controller.signal.aborted) {
          setBackendStatus('unavailable')
        }
      })

    return () => controller.abort()
  }, [])

  return (
    <main>
      <h1>BUYorBYE is running.</h1>
      <p role="status">{statusMessages[backendStatus]}</p>
    </main>
  )
}
