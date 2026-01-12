import { useState } from 'react'
import { CodeBracketIcon, BookOpenIcon, KeyIcon, CreditCardIcon } from '@heroicons/react/24/outline'
import PublicLayout from '../components/PublicLayout'

export default function Documentation() {
  const [activeTab, setActiveTab] = useState('getting-started')

  const tabs = [
    { id: 'getting-started', label: 'Getting Started', icon: BookOpenIcon },
    { id: 'authentication', label: 'Authentication', icon: KeyIcon },
    { id: 'payments', label: 'Payments', icon: CreditCardIcon },
    { id: 'code-examples', label: 'Code Examples', icon: CodeBracketIcon },
  ]

  return (
    <PublicLayout>
      <div>
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Documentation</h1>
          <p className="text-gray-600 mt-1">Complete guide to integrating PayCoreX API</p>
        </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar */}
        <div className="lg:w-64 flex-shrink-0">
          <div className="card">
            <nav className="space-y-2">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-primary-50 text-primary-700 font-medium'
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1">
          <div className="card">
            {activeTab === 'getting-started' && (
              <div className="prose max-w-none">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Getting Started</h2>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Base URL</h3>
                    <code className="block p-3 bg-gray-100 rounded-lg text-sm">
                      https://api.buildforu.pw
                    </code>
                  </div>

                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Quick Start</h3>
                    <ol className="list-decimal list-inside space-y-2 text-gray-700">
                      <li>Sign up for a PayCoreX account</li>
                      <li>Get your API key and secret from the dashboard</li>
                      <li>Generate HMAC signature for each request</li>
                      <li>Start processing payments!</li>
                    </ol>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'authentication' && (
              <div className="prose max-w-none">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Authentication</h2>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">HMAC Signature</h3>
                    <p className="text-gray-700 mb-4">
                      All API requests require HMAC-SHA256 signature authentication.
                    </p>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <p className="text-sm font-mono text-gray-800">
                        Signature = HMAC-SHA256(secret, timestamp + request_body)
                      </p>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Required Headers</h3>
                    <ul className="list-disc list-inside space-y-2 text-gray-700">
                      <li><code>X-API-Key</code>: Your API key</li>
                      <li><code>X-Signature</code>: HMAC signature</li>
                      <li><code>X-Timestamp</code>: Unix timestamp (seconds)</li>
                    </ul>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'payments' && (
              <div className="prose max-w-none">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Payments API</h2>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Create Payment</h3>
                    <p className="text-gray-700 mb-2">Endpoint: <code>POST /v1/payments/create</code></p>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <pre className="text-sm text-gray-800 overflow-x-auto">
{`{
  "amount": 1000.00,
  "method": "wallet",
  "user_id": "user-123",
  "reference_id": "order-456"
}`}
                      </pre>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Payment Methods</h3>
                    <ul className="list-disc list-inside space-y-2 text-gray-700">
                      <li><code>wallet</code> - Wallet payment</li>
                      <li><code>tokenized</code> - Tokenized card</li>
                      <li><code>upi_intent</code> - UPI payment</li>
                      <li><code>crypto</code> - Cryptocurrency</li>
                    </ul>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'code-examples' && (
              <div className="prose max-w-none">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Code Examples</h2>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Python</h3>
                    <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                      <pre className="text-sm text-gray-100">
{`import hmac
import hashlib
import time
import requests

api_key = "your-api-key"
secret = "your-secret"
timestamp = str(int(time.time()))
body = '{"amount":1000,"method":"wallet"}'
payload = f"{timestamp}{body}"

signature = hmac.new(
    secret.encode(),
    payload.encode(),
    hashlib.sha256
).hexdigest()

headers = {
    "X-API-Key": api_key,
    "X-Signature": signature,
    "X-Timestamp": timestamp
}

response = requests.post(
    "https://api.buildforu.pw/v1/payments/create",
    data=body,
    headers=headers
)`}
                      </pre>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">JavaScript</h3>
                    <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                      <pre className="text-sm text-gray-100">
{`const crypto = require('crypto');

const apiKey = 'your-api-key';
const secret = 'your-secret';
const timestamp = Math.floor(Date.now() / 1000).toString();
const body = JSON.stringify({amount: 1000, method: 'wallet'});
const payload = \`\${timestamp}\${body}\`;

const signature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

fetch('https://api.buildforu.pw/v1/payments/create', {
    method: 'POST',
    headers: {
        'X-API-Key': apiKey,
        'X-Signature': signature,
        'X-Timestamp': timestamp,
        'Content-Type': 'application/json'
    },
    body: body
})`}
                      </pre>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      </div>
    </PublicLayout>
  )
}

