import { useState, useEffect } from 'react'
import { dashboardAPI } from '../services/api'
import { CheckCircleIcon, XCircleIcon, ClockIcon } from '@heroicons/react/24/outline'

export default function PaymentVerifications() {
  const [payments, setPayments] = useState([])
  const [loading, setLoading] = useState(true)
  const [verifying, setVerifying] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchPendingVerifications()
  }, [])

  const fetchPendingVerifications = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await dashboardAPI.getPendingVerifications()
      setPayments(response.data.results || [])
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to fetch pending verifications')
    } finally {
      setLoading(false)
    }
  }

  const handleVerify = async (paymentId, utrNumber) => {
    if (!window.confirm(`Are you sure you want to verify this payment?\n\nUTR: ${utrNumber}\n\nPlease ensure this UTR matches the payment in your bank account.`)) {
      return
    }

    try {
      setVerifying(paymentId)
      setError(null)

      await dashboardAPI.verifyPayment(paymentId, {
        utr_number: utrNumber,
      })

      // Remove verified payment from list
      setPayments(payments.filter(p => p.id !== paymentId))
      alert('Payment verified successfully!')
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to verify payment')
    } finally {
      setVerifying(null)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const formatAmount = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Payment Verifications</h1>
        <p className="text-gray-600 mt-1">
          Verify payments by checking UTR numbers against your bank account
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {payments.length === 0 ? (
        <div className="card text-center py-12">
          <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">All Clear!</h3>
          <p className="text-gray-600">
            No pending payments require verification at the moment.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="card p-4 bg-yellow-50 border border-yellow-200">
            <p className="text-yellow-800 text-sm">
              <strong>Note:</strong> Please verify each UTR number against your bank account 
              before marking payments as verified. Once verified, the payment will be marked as 
              successful and funds will be credited to your account.
            </p>
          </div>

          {payments.map((payment) => (
            <div key={payment.id} className="card">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <ClockIcon className="h-6 w-6 text-yellow-500" />
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {formatAmount(payment.amount)}
                      </h3>
                      <p className="text-sm text-gray-500">
                        Payment ID: {payment.id.slice(0, 8)}...
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-600 mb-1">UTR Number</p>
                      <p className="text-base font-mono font-semibold text-gray-900 bg-gray-50 p-2 rounded">
                        {payment.utr_number}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Payment Method</p>
                      <p className="text-base text-gray-900 capitalize">
                        {payment.method.replace('_', ' ')}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Reference ID</p>
                      <p className="text-base text-gray-900 font-mono text-sm">
                        {payment.reference_id || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Submitted At</p>
                      <p className="text-base text-gray-900">
                        {payment.utr_submitted_at 
                          ? formatDate(payment.utr_submitted_at)
                          : formatDate(payment.created_at)}
                      </p>
                    </div>
                  </div>

                  {payment.user_id && (
                    <div className="mb-4">
                      <p className="text-sm text-gray-600 mb-1">User ID</p>
                      <p className="text-base text-gray-900 font-mono text-sm">
                        {payment.user_id}
                      </p>
                    </div>
                  )}
                </div>

                <div className="ml-4">
                  <button
                    onClick={() => handleVerify(payment.id, payment.utr_number)}
                    disabled={verifying === payment.id}
                    className="btn bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                  >
                    {verifying === payment.id ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        Verifying...
                      </>
                    ) : (
                      <>
                        <CheckCircleIcon className="h-5 w-5" />
                        Verify Payment
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {payments.length > 0 && (
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>Total Pending Verifications: <strong>{payments.length}</strong></p>
        </div>
      )}
    </div>
  )
}


