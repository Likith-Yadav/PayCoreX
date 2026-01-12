import { useState, useEffect } from 'react'
import { authAPI } from '../services/api'
import { useAuth } from '../context/AuthContext'
import { KeyIcon, DocumentDuplicateIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline'

export default function APIKeys() {
  const { user, loadUser } = useAuth()
  const [secret, setSecret] = useState(null)
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  const handleRegenerate = async () => {
    if (!confirm('Are you sure you want to regenerate your API key? This will invalidate your current key.')) {
      return
    }

    setLoading(true)
    try {
      const response = await authAPI.regenerateKey()
      setSecret(response.data.secret)
      await loadUser()
      alert('API key regenerated! Please save your new secret key.')
    } catch (error) {
      alert('Failed to regenerate API key')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const downloadCredentials = () => {
    const content = `PayCoreX API Credentials

API Key: ${user?.api_key}
Secret Key: ${secret || 'Please regenerate to get secret'}

IMPORTANT: Keep these credentials secure and never share them publicly.

Generated: ${new Date().toLocaleString()}
`
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'paycorex-credentials.txt'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">API Keys</h1>
        <p className="text-gray-600 mt-1">Manage your API credentials for integration</p>
      </div>

      <div className="card mb-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <KeyIcon className="h-8 w-8 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">Your API Credentials</h2>
          </div>
          <button
            onClick={handleRegenerate}
            disabled={loading}
            className="btn-secondary disabled:opacity-50"
          >
            {loading ? 'Regenerating...' : 'Regenerate Keys'}
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              API Key
            </label>
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={user?.api_key || ''}
                readOnly
                className="input-field bg-gray-50 font-mono text-sm"
              />
              <button
                onClick={() => copyToClipboard(user?.api_key)}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                title="Copy to clipboard"
              >
                <DocumentDuplicateIcon className="h-5 w-5" />
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Secret Key {secret && <span className="text-red-600">(New - Save this!)</span>}
            </label>
            <div className="flex items-center space-x-2">
              <input
                type="password"
                value={secret || '••••••••••••••••'}
                readOnly
                className="input-field bg-gray-50 font-mono text-sm"
              />
              {secret && (
                <button
                  onClick={() => copyToClipboard(secret)}
                  className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                  title="Copy to clipboard"
                >
                  <DocumentDuplicateIcon className="h-5 w-5" />
                </button>
              )}
            </div>
            {!secret && (
              <p className="mt-2 text-sm text-gray-500">
                Secret key is only shown once when generated. Regenerate to get a new one.
              </p>
            )}
          </div>

          {copied && (
            <div className="p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
              Copied to clipboard!
            </div>
          )}
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <button
            onClick={downloadCredentials}
            className="flex items-center space-x-2 btn-secondary"
          >
            <ArrowDownTrayIcon className="h-5 w-5" />
            <span>Download Credentials</span>
          </button>
        </div>
      </div>

      <div className="card bg-yellow-50 border-yellow-200">
        <h3 className="font-semibold text-yellow-900 mb-2">⚠️ Security Reminders</h3>
        <ul className="text-sm text-yellow-800 space-y-1 list-disc list-inside">
          <li>Never share your API credentials publicly</li>
          <li>Keep your secret key secure and never commit it to version control</li>
          <li>Regenerate keys immediately if you suspect they've been compromised</li>
          <li>Use environment variables to store credentials in your applications</li>
        </ul>
      </div>
    </div>
  )
}

