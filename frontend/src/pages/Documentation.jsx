import { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  BookOpenIcon, 
  KeyIcon, 
  CreditCardIcon, 
  CodeBracketIcon,
  ServerIcon,
  DevicePhoneMobileIcon,
  ArrowPathIcon,
  WalletIcon,
  BellIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline'
import PublicLayout from '../components/PublicLayout'
import { useAuth } from '../context/AuthContext'

export default function Documentation() {
  const { user, loading } = useAuth()
  const [activeSection, setActiveSection] = useState('overview')
  const [activeSubSection, setActiveSubSection] = useState(null)

  const sections = [
    {
      id: 'overview',
      label: 'Overview',
      icon: BookOpenIcon,
      subsections: []
    },
    {
      id: 'api-integration',
      label: 'API Integration',
      icon: CodeBracketIcon,
      subsections: ['introduction', 'integration-steps', 'api-reference']
    },
    {
      id: 'backend-sdk',
      label: 'Backend SDK',
      icon: ServerIcon,
      subsections: ['python', 'nodejs', 'java', 'php']
    },
    {
      id: 'authentication',
      label: 'Authentication',
      icon: KeyIcon,
      subsections: ['hmac-signature', 'headers', 'examples']
    },
    {
      id: 'payments',
      label: 'Payments',
      icon: CreditCardIcon,
      subsections: ['create-payment', 'payment-methods', 'check-status', 'refunds']
    },
    {
      id: 'wallet',
      label: 'Wallet System',
      icon: WalletIcon,
      subsections: ['create-wallet', 'topup', 'balance', 'payments']
    },
    {
      id: 'webhooks',
      label: 'Webhooks',
      icon: BellIcon,
      subsections: ['setup', 'events', 'verification', 'handling']
    },
    {
      id: 'dashboard',
      label: 'Dashboard & Analytics',
      icon: ChartBarIcon,
      subsections: ['statistics', 'payments-list', 'ledger']
    },
    {
      id: 'security',
      label: 'Security',
      icon: ShieldCheckIcon,
      subsections: ['best-practices', 'pci-compliance', 'encryption']
    }
  ]

  const renderContent = () => {
    switch (activeSection) {
      case 'overview':
        return (
          <div className="space-y-8">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-4">PayCoreX Payment Gateway</h1>
              <p className="text-xl text-gray-600 mb-6">
                A secure, scalable, and high-performance payment gateway designed for modern businesses. 
                Accept payments via Wallet, Tokenized Cards, UPI, and Cryptocurrency.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl">
                <ShieldCheckIcon className="h-10 w-10 text-blue-600 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure & Compliant</h3>
                <p className="text-gray-700">PCI DSS compliant with end-to-end encrypted transactions and HMAC authentication.</p>
              </div>
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl">
                <CreditCardIcon className="h-10 w-10 text-green-600 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Multiple Payment Methods</h3>
                <p className="text-gray-700">Support for Wallet, Tokenized Cards, UPI Intent, and Cryptocurrency payments.</p>
              </div>
              <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl">
                <ChartBarIcon className="h-10 w-10 text-purple-600 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">High Performance</h3>
                <p className="text-gray-700">Built for high-volume transactions with fast processing and high success rates.</p>
              </div>
            </div>

            <div className="bg-gray-50 p-6 rounded-xl">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Base URL</h2>
              <code className="block p-4 bg-white rounded-lg text-lg font-mono text-gray-800 border-2 border-gray-200">
                https://api.buildforu.pw
              </code>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Start</h2>
              <ol className="list-decimal list-inside space-y-3 text-gray-700">
                <li>Register as a merchant to get your API credentials</li>
                <li>Choose your integration method (API or Backend SDK)</li>
                <li>Implement HMAC signature authentication</li>
                <li>Create your first payment</li>
                <li>Set up webhooks to receive payment notifications</li>
              </ol>
            </div>
          </div>
        )

      case 'api-integration':
        if (activeSubSection === 'introduction' || !activeSubSection) {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">API Integration</h2>
              <p className="text-lg text-gray-700">
                Integrate PayCoreX directly using REST APIs. Perfect for custom integrations and full control over the payment flow.
              </p>
              
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                <p className="text-blue-800">
                  <strong>Recommended for:</strong> Custom applications, full control over payment flow, server-side integrations
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Features</h3>
                <ul className="list-disc list-inside space-y-2 text-gray-700">
                  <li>RESTful API design</li>
                  <li>HMAC-SHA256 authentication</li>
                  <li>JSON request/response format</li>
                  <li>Comprehensive error handling</li>
                  <li>Webhook support for real-time notifications</li>
                </ul>
              </div>
            </div>
          )
        }
        if (activeSubSection === 'integration-steps') {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">Integration Steps</h2>
              
              <div className="space-y-6">
                <div className="border-l-4 border-blue-500 pl-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Step 1: Register as Merchant</h3>
                  <p className="text-gray-700 mb-3">Get your API credentials by registering your business.</p>
                  <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                    <pre className="text-sm text-gray-100">
{`POST /v1/merchants/register
Content-Type: application/json

{
  "name": "Your Business Name",
  "email": "merchant@example.com"
}

Response:
{
  "api_key": "your-api-key",
  "secret": "your-secret-key",
  ...
}`}
                    </pre>
                  </div>
                </div>

                <div className="border-l-4 border-green-500 pl-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Step 2: Implement Authentication</h3>
                  <p className="text-gray-700 mb-3">Generate HMAC signature for each API request.</p>
                  <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                    <pre className="text-sm text-gray-100">
{`Signature = HMAC-SHA256(secret, timestamp + request_body)

Required Headers:
- X-API-Key: your-api-key
- X-Signature: hmac-signature
- X-Timestamp: unix-timestamp`}
                    </pre>
                  </div>
                </div>

                <div className="border-l-4 border-purple-500 pl-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Step 3: Create Payment</h3>
                  <p className="text-gray-700 mb-3">Process your first payment transaction.</p>
                  <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                    <pre className="text-sm text-gray-100">
{`POST /v1/payments/create
Headers: X-API-Key, X-Signature, X-Timestamp
Body: {
  "amount": 1000.00,
  "method": "wallet",
  "user_id": "user-123",
  "reference_id": "order-456"
}`}
                    </pre>
                  </div>
                </div>

                <div className="border-l-4 border-orange-500 pl-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Step 4: Set Up Webhooks</h3>
                  <p className="text-gray-700 mb-3">Receive real-time payment status updates.</p>
                  <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                    <pre className="text-sm text-gray-100">
{`POST /v1/webhooks/provider
Body: {
  "url": "https://your-domain.com/webhook",
  "events": ["payment.success", "payment.failed"]
}`}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          )
        }
        if (activeSubSection === 'api-reference') {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">API Reference</h2>
              
              <div className="space-y-8">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Merchant Registration</h3>
                  <div className="bg-gray-50 p-4 rounded-lg mb-2">
                    <code className="text-sm font-mono">POST /v1/merchants/register</code>
                  </div>
                  <p className="text-gray-700 mb-3">Register a new merchant account. No authentication required.</p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Create Payment</h3>
                  <div className="bg-gray-50 p-4 rounded-lg mb-2">
                    <code className="text-sm font-mono">POST /v1/payments/create</code>
                  </div>
                  <p className="text-gray-700 mb-3">Create a new payment transaction. Requires HMAC authentication.</p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Get Payment Status</h3>
                  <div className="bg-gray-50 p-4 rounded-lg mb-2">
                    <code className="text-sm font-mono">GET /v1/payments/{'{payment_id}'}</code>
                  </div>
                  <p className="text-gray-700 mb-3">Retrieve payment details and status.</p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Initiate Refund</h3>
                  <div className="bg-gray-50 p-4 rounded-lg mb-2">
                    <code className="text-sm font-mono">POST /v1/payments/refund</code>
                  </div>
                  <p className="text-gray-700 mb-3">Process full or partial refunds for successful payments.</p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Wallet Operations</h3>
                  <div className="space-y-2">
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <code className="text-sm font-mono">POST /v1/wallet/create</code>
                    </div>
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <code className="text-sm font-mono">POST /v1/wallet/topup</code>
                    </div>
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <code className="text-sm font-mono">GET /v1/wallet/balance</code>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Webhooks</h3>
                  <div className="bg-gray-50 p-4 rounded-lg mb-2">
                    <code className="text-sm font-mono">POST /v1/webhooks/provider</code>
                  </div>
                  <p className="text-gray-700 mb-3">Configure webhook endpoints for payment notifications.</p>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Dashboard</h3>
                  <div className="space-y-2">
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <code className="text-sm font-mono">GET /v1/dashboard/stats</code>
                    </div>
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <code className="text-sm font-mono">GET /v1/dashboard/payments</code>
                    </div>
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <code className="text-sm font-mono">GET /v1/dashboard/ledgers</code>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )
        }
        break

      case 'backend-sdk':
        if (activeSubSection === 'python' || !activeSubSection) {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">Python Backend SDK</h2>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Installation</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`pip install requests`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Class Initialization</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`import hmac
import hashlib
import time
import json
import requests

class PayCoreXClient:
    def __init__(self, api_key, secret, base_url="https://api.buildforu.pw"):
        self.api_key = api_key
        self.secret = secret
        self.base_url = base_url
    
    def _generate_signature(self, timestamp, body):
        payload = f"{timestamp}{body}"
        return hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _get_headers(self, body):
        timestamp = str(int(time.time()))
        signature = self._generate_signature(timestamp, body)
        return {
            "X-API-Key": self.api_key,
            "X-Signature": signature,
            "X-Timestamp": timestamp,
            "Content-Type": "application/json"
        }`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Create Payment</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`def create_payment(self, amount, method, user_id=None, reference_id=None):
    url = f"{self.base_url}/v1/payments/create"
    body = json.dumps({
        "amount": amount,
        "method": method,
        "user_id": user_id,
        "reference_id": reference_id
    })
    
    response = requests.post(
        url,
        data=body,
        headers=self._get_headers(body)
    )
    return response.json()

# Usage
client = PayCoreXClient(api_key="your-key", secret="your-secret")
payment = client.create_payment(
    amount=1000.00,
    method="wallet",
    user_id="user-123"
)`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Check Order Status</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`def get_payment(self, payment_id):
    url = f"{self.base_url}/v1/payments/{payment_id}"
    body = ""
    
    response = requests.get(
        url,
        headers=self._get_headers(body)
    )
    return response.json()`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Initiate Refund</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`def create_refund(self, payment_id, amount=None, reason=None):
    url = f"{self.base_url}/v1/payments/refund"
    body = json.dumps({
        "payment_id": payment_id,
        "amount": amount,  # Omit for full refund
        "reason": reason
    })
    
    response = requests.post(
        url,
        data=body,
        headers=self._get_headers(body)
    )
    return response.json()`}
                  </pre>
                </div>
              </div>
            </div>
          )
        }
        if (activeSubSection === 'nodejs') {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">Node.js Backend SDK</h2>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Installation</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`npm install axios
# or
yarn add axios`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Class Initialization</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`const crypto = require('crypto');
const axios = require('axios');

class PayCoreXClient {
    constructor(apiKey, secret, baseUrl = 'https://api.buildforu.pw') {
        this.apiKey = apiKey;
        this.secret = secret;
        this.baseUrl = baseUrl;
    }
    
    _generateSignature(timestamp, body) {
        const payload = \`\${timestamp}\${body}\`;
        return crypto
            .createHmac('sha256', this.secret)
            .update(payload)
            .digest('hex');
    }
    
    _getHeaders(body) {
        const timestamp = Math.floor(Date.now() / 1000).toString();
        const signature = this._generateSignature(timestamp, body);
        return {
            'X-API-Key': this.apiKey,
            'X-Signature': signature,
            'X-Timestamp': timestamp,
            'Content-Type': 'application/json'
        };
    }
}`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Create Payment</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`async createPayment(amount, method, userId = null, referenceId = null) {
    const url = \`\${this.baseUrl}/v1/payments/create\`;
    const body = JSON.stringify({
        amount,
        method,
        user_id: userId,
        reference_id: referenceId
    });
    
    const response = await axios.post(url, body, {
        headers: this._getHeaders(body)
    });
    
    return response.data;
}

// Usage
const client = new PayCoreXClient('your-key', 'your-secret');
const payment = await client.createPayment(
    1000.00,
    'wallet',
    'user-123'
);`}
                  </pre>
                </div>
              </div>
            </div>
          )
        }
        if (activeSubSection === 'java') {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">Java Backend SDK</h2>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Installation</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`// Add to pom.xml (Maven)
<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp</artifactId>
    <version>4.11.0</version>
</dependency>`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Class Initialization</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class PayCoreXClient {
    private String apiKey;
    private String secret;
    private String baseUrl;
    
    public PayCoreXClient(String apiKey, String secret) {
        this.apiKey = apiKey;
        this.secret = secret;
        this.baseUrl = "https://api.buildforu.pw";
    }
    
    private String generateSignature(long timestamp, String body) {
        try {
            String payload = timestamp + body;
            Mac mac = Mac.getInstance("HmacSHA256");
            SecretKeySpec secretKey = new SecretKeySpec(
                secret.getBytes(StandardCharsets.UTF_8),
                "HmacSHA256"
            );
            mac.init(secretKey);
            byte[] hash = mac.doFinal(payload.getBytes(StandardCharsets.UTF_8));
            return bytesToHex(hash);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}`}
                  </pre>
                </div>
              </div>
            </div>
          )
        }
        if (activeSubSection === 'php') {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">PHP Backend SDK</h2>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Installation</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`composer require guzzlehttp/guzzle`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Class Initialization</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`<?php
require 'vendor/autoload.php';

use GuzzleHttp\Client;

class PayCoreXClient {
    private $apiKey;
    private $secret;
    private $baseUrl;
    private $client;
    
    public function __construct($apiKey, $secret) {
        $this->apiKey = $apiKey;
        $this->secret = $secret;
        $this->baseUrl = 'https://api.buildforu.pw';
        $this->client = new Client();
    }
    
    private function generateSignature($timestamp, $body) {
        $payload = $timestamp . $body;
        return hash_hmac('sha256', $payload, $this->secret);
    }
    
    private function getHeaders($body) {
        $timestamp = time();
        $signature = $this->generateSignature($timestamp, $body);
        return [
            'X-API-Key' => $this->apiKey,
            'X-Signature' => $signature,
            'X-Timestamp' => $timestamp,
            'Content-Type' => 'application/json'
        ];
    }
}`}
                  </pre>
                </div>
              </div>
            </div>
          )
        }
        break

      case 'authentication':
        if (activeSubSection === 'hmac-signature' || !activeSubSection) {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">HMAC Signature Authentication</h2>
              
              <p className="text-lg text-gray-700">
                All API requests (except merchant registration) require HMAC-SHA256 signature authentication 
                to ensure secure communication between your server and PayCoreX.
              </p>

              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                <p className="text-blue-800">
                  <strong>Formula:</strong> <code>HMAC-SHA256(secret, timestamp + request_body)</code>
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Required Headers</h3>
                <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                  <div>
                    <code className="text-sm font-mono font-semibold">X-API-Key</code>
                    <p className="text-gray-600 text-sm">Your merchant API key</p>
                  </div>
                  <div>
                    <code className="text-sm font-mono font-semibold">X-Signature</code>
                    <p className="text-gray-600 text-sm">HMAC-SHA256 signature</p>
                  </div>
                  <div>
                    <code className="text-sm font-mono font-semibold">X-Timestamp</code>
                    <p className="text-gray-600 text-sm">Unix timestamp in seconds</p>
                  </div>
                </div>
              </div>
            </div>
          )
        }
        if (activeSubSection === 'examples') {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">Code Examples</h2>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Python</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`import hmac
import hashlib
import time
import json

def generate_signature(secret, timestamp, body):
    payload = f"{timestamp}{body}"
    return hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

# Usage
timestamp = str(int(time.time()))
body = json.dumps({"amount": 1000, "method": "wallet"})
signature = generate_signature("your-secret", timestamp, body)

headers = {
    "X-API-Key": "your-api-key",
    "X-Signature": signature,
    "X-Timestamp": timestamp
}`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Node.js</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`const crypto = require('crypto');

function generateSignature(secret, timestamp, body) {
    const payload = \`\${timestamp}\${body}\`;
    return crypto
        .createHmac('sha256', secret)
        .update(payload)
        .digest('hex');
}

// Usage
const timestamp = Math.floor(Date.now() / 1000).toString();
const body = JSON.stringify({amount: 1000, method: 'wallet'});
const signature = generateSignature('your-secret', timestamp, body);

const headers = {
    'X-API-Key': 'your-api-key',
    'X-Signature': signature,
    'X-Timestamp': timestamp
};`}
                  </pre>
                </div>
              </div>
            </div>
          )
        }
        break

      case 'payments':
        if (activeSubSection === 'create-payment' || !activeSubSection) {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">Create Payment</h2>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Endpoint</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <code className="text-lg font-mono">POST /v1/payments/create</code>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Request Body</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`{
  "amount": 1000.00,
  "currency": "INR",
  "method": "wallet",
  "user_id": "user-123",
  "reference_id": "order-456",
  "metadata": {
    "order_id": "ORD-12345",
    "description": "Product purchase"
  }
}`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Response (Success)</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`{
  "id": "payment-uuid",
  "status": "success",
  "amount": "1000.00",
  "currency": "INR",
  "method": "wallet",
  "provider_reference": "provider-txn-id",
  "created_at": "2026-01-12T05:30:00Z"
}`}
                  </pre>
                </div>
              </div>
            </div>
          )
        }
        if (activeSubSection === 'payment-methods') {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">Payment Methods</h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="border border-gray-200 p-6 rounded-xl">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Wallet</h3>
                  <p className="text-gray-700 mb-3">Process payments from user wallet balance.</p>
                  <code className="text-sm bg-gray-100 px-2 py-1 rounded">method: "wallet"</code>
                </div>

                <div className="border border-gray-200 p-6 rounded-xl">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Tokenized Card</h3>
                  <p className="text-gray-700 mb-3">Secure card payments using stored payment tokens.</p>
                  <code className="text-sm bg-gray-100 px-2 py-1 rounded">method: "tokenized"</code>
                </div>

                <div className="border border-gray-200 p-6 rounded-xl">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">UPI Intent</h3>
                  <p className="text-gray-700 mb-3">UPI payment intent for seamless transactions.</p>
                  <code className="text-sm bg-gray-100 px-2 py-1 rounded">method: "upi_intent"</code>
                </div>

                <div className="border border-gray-200 p-6 rounded-xl">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Cryptocurrency</h3>
                  <p className="text-gray-700 mb-3">Accept payments in Ethereum, Polygon, or BSC.</p>
                  <code className="text-sm bg-gray-100 px-2 py-1 rounded">method: "crypto"</code>
                </div>
              </div>
            </div>
          )
        }
        if (activeSubSection === 'check-status') {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">Check Payment Status</h2>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Endpoint</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <code className="text-lg font-mono">GET /v1/payments/{'{payment_id}'}</code>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Payment Statuses</h3>
                <div className="space-y-2">
                  <div className="flex items-center space-x-3">
                    <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">pending</span>
                    <span className="text-gray-700">Payment initiated, awaiting processing</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">processing</span>
                    <span className="text-gray-700">Payment is being processed</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">success</span>
                    <span className="text-gray-700">Payment completed successfully</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">failed</span>
                    <span className="text-gray-700">Payment failed</span>
                  </div>
                </div>
              </div>
            </div>
          )
        }
        if (activeSubSection === 'refunds') {
          return (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">Refunds</h2>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Endpoint</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <code className="text-lg font-mono">POST /v1/payments/refund</code>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Request Body</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`{
  "payment_id": "payment-uuid",
  "amount": 500.00,  // Optional - omit for full refund
  "reason": "Customer requested refund"
}`}
                  </pre>
                </div>
              </div>

              <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                <p className="text-yellow-800">
                  <strong>Note:</strong> Only successful payments can be refunded. Omit the <code>amount</code> field for a full refund.
                </p>
              </div>
            </div>
          )
        }
        break

      case 'wallet':
        return (
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-gray-900">Wallet System</h2>
            <p className="text-lg text-gray-700">
              Manage user wallets for seamless payment processing and balance management.
            </p>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Create Wallet</h3>
                <div className="bg-gray-50 p-4 rounded-lg mb-2">
                  <code className="text-sm font-mono">POST /v1/wallet/create</code>
                </div>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`Body: {
  "user_id": "user-123"
}`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Top Up Wallet</h3>
                <div className="bg-gray-50 p-4 rounded-lg mb-2">
                  <code className="text-sm font-mono">POST /v1/wallet/topup</code>
                </div>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`Body: {
  "user_id": "user-123",
  "amount": 5000.00,
  "currency": "INR"
}`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Get Balance</h3>
                <div className="bg-gray-50 p-4 rounded-lg mb-2">
                  <code className="text-sm font-mono">GET /v1/wallet/balance?user_id=user-123</code>
                </div>
              </div>
            </div>
          </div>
        )

      case 'webhooks':
        return (
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-gray-900">Webhooks</h2>
            <p className="text-lg text-gray-700">
              Receive real-time notifications about payment events and status changes.
            </p>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Setup Webhook Endpoint</h3>
                <div className="bg-gray-50 p-4 rounded-lg mb-2">
                  <code className="text-sm font-mono">POST /v1/webhooks/provider</code>
                </div>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`Body: {
  "url": "https://your-domain.com/webhook",
  "events": ["payment.success", "payment.failed", "refund.success"]
}`}
                  </pre>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Webhook Events</h3>
                <ul className="list-disc list-inside space-y-2 text-gray-700">
                  <li><code>payment.success</code> - Payment completed successfully</li>
                  <li><code>payment.failed</code> - Payment failed</li>
                  <li><code>payment.processing</code> - Payment is being processed</li>
                  <li><code>refund.success</code> - Refund processed successfully</li>
                </ul>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Webhook Payload</h3>
                <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-100">
{`{
  "event": "payment.success",
  "timestamp": "2026-01-12T05:30:00Z",
  "data": {
    "payment_id": "payment-uuid",
    "amount": "1000.00",
    "status": "success",
    "method": "wallet"
  }
}`}
                  </pre>
                </div>
              </div>

              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                <p className="text-blue-800">
                  <strong>Security:</strong> Always verify the <code>X-Webhook-Signature</code> header to ensure the webhook is from PayCoreX.
                </p>
              </div>
            </div>
          </div>
        )

      case 'dashboard':
        return (
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-gray-900">Dashboard & Analytics</h2>
            <p className="text-lg text-gray-700">
              Access comprehensive analytics and transaction data through our dashboard APIs.
            </p>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Get Statistics</h3>
                <div className="bg-gray-50 p-4 rounded-lg mb-2">
                  <code className="text-sm font-mono">GET /v1/dashboard/stats</code>
                </div>
                <p className="text-gray-700">Returns total volume, success rate, refund statistics, and more.</p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Get Payments List</h3>
                <div className="bg-gray-50 p-4 rounded-lg mb-2">
                  <code className="text-sm font-mono">GET /v1/dashboard/payments?status=success&limit=50</code>
                </div>
                <p className="text-gray-700">Retrieve filtered list of payments with pagination support.</p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Get Ledger Entries</h3>
                <div className="bg-gray-50 p-4 rounded-lg mb-2">
                  <code className="text-sm font-mono">GET /v1/dashboard/ledgers</code>
                </div>
                <p className="text-gray-700">View complete transaction ledger with credits and debits.</p>
              </div>
            </div>
          </div>
        )

      case 'security':
        return (
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-gray-900">Security</h2>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Best Practices</h3>
                <ul className="list-disc list-inside space-y-2 text-gray-700">
                  <li>Never expose your secret key in client-side code</li>
                  <li>Always use HTTPS for API calls</li>
                  <li>Verify webhook signatures before processing</li>
                  <li>Implement proper error handling and logging</li>
                  <li>Use environment variables for sensitive data</li>
                  <li>Monitor API usage and set up alerts</li>
                </ul>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">PCI Compliance</h3>
                <p className="text-gray-700 mb-3">
                  PayCoreX is PCI DSS compliant and handles all sensitive payment data securely. 
                  We never store full card numbers or CVV codes.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Encryption</h3>
                <p className="text-gray-700 mb-3">
                  All API communications are encrypted using TLS 1.2+. HMAC signatures ensure 
                  request authenticity and integrity.
                </p>
              </div>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  // Show loading state
  if (loading) {
    return (
      <PublicLayout>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="w-8 h-8 border-2 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
        </div>
      </PublicLayout>
    )
  }

  return (
    <PublicLayout>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation Bar */}
        <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <Link to="/" className="text-2xl font-bold text-primary-600">PayCoreX</Link>
              </div>
              <div className="flex items-center space-x-4">
                {loading ? (
                  <div className="w-8 h-8 border-2 border-primary-600 border-t-transparent rounded-full animate-spin"></div>
                ) : user ? (
                  <Link
                    to="/dashboard"
                    className="bg-primary-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-primary-700 transition-colors"
                  >
                    Dashboard
                  </Link>
                ) : (
                  <>
                    <Link
                      to="/login"
                      className="text-gray-700 hover:text-gray-900 px-4 py-2 font-medium transition-colors"
                    >
                      Sign In
                    </Link>
                    <Link
                      to="/signup"
                      className="bg-primary-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-primary-700 transition-colors"
                    >
                      Get Started
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col lg:flex-row gap-8">
            {/* Sidebar Navigation */}
            <div className="lg:w-64 flex-shrink-0">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sticky top-8">
                <nav className="space-y-1">
                  {sections.map((section) => {
                    const Icon = section.icon
                    const isActive = activeSection === section.id
                    return (
                      <div key={section.id}>
                        <button
                          onClick={() => {
                            setActiveSection(section.id)
                            setActiveSubSection(section.subsections.length > 0 ? section.subsections[0] : null)
                          }}
                          className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                            isActive
                              ? 'bg-primary-600 text-white font-medium'
                              : 'text-gray-700 hover:bg-gray-100'
                          }`}
                        >
                          <Icon className="h-5 w-5" />
                          <span>{section.label}</span>
                        </button>
                        
                        {isActive && section.subsections.length > 0 && (
                          <div className="mt-2 ml-4 space-y-1">
                            {section.subsections.map((sub) => (
                              <button
                                key={sub}
                                onClick={() => setActiveSubSection(sub)}
                                className={`w-full text-left px-4 py-2 rounded-lg text-sm transition-colors ${
                                  activeSubSection === sub
                                    ? 'bg-primary-100 text-primary-700 font-medium'
                                    : 'text-gray-600 hover:bg-gray-50'
                                }`}
                              >
                                {sub.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                              </button>
                            ))}
                          </div>
                        )}
                      </div>
                    )
                  })}
                </nav>
              </div>
            </div>

            {/* Main Content */}
            <div className="flex-1">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
                {renderContent()}
              </div>
            </div>
          </div>
        </div>
      </div>
    </PublicLayout>
  )
}
