import { useState, useEffect } from 'react'
import api from '../services/api'
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  CheckCircleIcon,
  XCircleIcon,
  BuildingLibraryIcon,
  DevicePhoneMobileIcon,
  CreditCardIcon,
} from '@heroicons/react/24/outline'

export default function PaymentSettings() {
  const [configs, setConfigs] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingConfig, setEditingConfig] = useState(null)
  const [formData, setFormData] = useState({
    config_type: 'bank_account',
    is_primary: false,
    is_active: true,
    // Bank Account
    account_holder_name: '',
    account_number: '',
    ifsc_code: '',
    bank_name: '',
    branch_name: '',
    // UPI
    upi_id: '',
    // Payment Provider
    provider_key: '',
    provider_secret: '',
    provider_merchant_id: '',
    provider_webhook_secret: '',
  })

  useEffect(() => {
    loadConfigs()
  }, [])

  const loadConfigs = async () => {
    try {
      setLoading(true)
      const response = await api.get('/api/dashboard/payment-configs')
      setConfigs(response.data)
    } catch (error) {
      console.error('Failed to load payment configs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      // Clean up form data - remove empty strings for optional fields
      const cleanedData = { ...formData }
      
      // Remove empty strings for fields that aren't relevant to the selected type
      if (cleanedData.config_type !== 'bank_account') {
        cleanedData.account_holder_name = cleanedData.account_holder_name || null
        cleanedData.account_number = cleanedData.account_number || null
        cleanedData.ifsc_code = cleanedData.ifsc_code || null
        cleanedData.bank_name = cleanedData.bank_name || null
        cleanedData.branch_name = cleanedData.branch_name || null
      }
      
      if (cleanedData.config_type !== 'upi') {
        cleanedData.upi_id = cleanedData.upi_id || null
      }
      
      if (!['razorpay', 'stripe', 'phonepe', 'paytm', 'other'].includes(cleanedData.config_type)) {
        cleanedData.provider_key = cleanedData.provider_key || null
        cleanedData.provider_secret = cleanedData.provider_secret || null
        cleanedData.provider_merchant_id = cleanedData.provider_merchant_id || null
        cleanedData.provider_webhook_secret = cleanedData.provider_webhook_secret || null
      }
      
      if (editingConfig) {
        await api.put(`/api/dashboard/payment-configs/${editingConfig.id}`, cleanedData)
      } else {
        await api.post('/api/dashboard/payment-configs', cleanedData)
      }
      setShowForm(false)
      setEditingConfig(null)
      resetForm()
      loadConfigs()
    } catch (error) {
      console.error('Failed to save payment config:', error)
      console.error('Error response:', error.response?.data)
      
      // Handle validation errors
      const errorData = error.response?.data
      let errorMessage = 'Failed to save payment configuration'
      
      if (errorData) {
        // If it's a dictionary of errors (Django serializer errors)
        if (typeof errorData === 'object' && !errorData.error) {
          const errorMessages = []
          for (const [field, messages] of Object.entries(errorData)) {
            if (Array.isArray(messages)) {
              errorMessages.push(`${field}: ${messages.join(', ')}`)
            } else if (typeof messages === 'string') {
              errorMessages.push(`${field}: ${messages}`)
            } else {
              errorMessages.push(`${field}: ${JSON.stringify(messages)}`)
            }
          }
          errorMessage = errorMessages.length > 0 
            ? errorMessages.join('\n') 
            : 'Validation failed. Please check all required fields.'
        } else if (errorData.error) {
          errorMessage = errorData.error
        } else if (typeof errorData === 'string') {
          errorMessage = errorData
        } else if (Array.isArray(errorData)) {
          errorMessage = errorData.join('\n')
        }
      } else if (error.message) {
        errorMessage = error.message
      }
      
      alert(errorMessage)
    }
  }

  const handleEdit = (config) => {
    setEditingConfig(config)
    setFormData({
      config_type: config.config_type,
      is_primary: config.is_primary,
      is_active: config.is_active,
      account_holder_name: config.account_holder_name || '',
      account_number: config.account_number || '',
      ifsc_code: config.ifsc_code || '',
      bank_name: config.bank_name || '',
      branch_name: config.branch_name || '',
      upi_id: config.upi_id || '',
      provider_key: config.provider_key || '',
      provider_secret: config.provider_secret || '',
      provider_merchant_id: config.provider_merchant_id || '',
      provider_webhook_secret: config.provider_webhook_secret || '',
    })
    setShowForm(true)
  }

  const handleDelete = async (configId) => {
    if (!window.confirm('Are you sure you want to delete this payment configuration?')) {
      return
    }
    try {
      await api.delete(`/api/dashboard/payment-configs/${configId}`)
      loadConfigs()
    } catch (error) {
      console.error('Failed to delete payment config:', error)
      alert('Failed to delete payment configuration')
    }
  }

  const resetForm = () => {
    setFormData({
      config_type: 'bank_account',
      is_primary: false,
      is_active: true,
      account_holder_name: '',
      account_number: '',
      ifsc_code: '',
      bank_name: '',
      branch_name: '',
      upi_id: '',
      provider_key: '',
      provider_secret: '',
      provider_merchant_id: '',
      provider_webhook_secret: '',
    })
  }

  const getConfigIcon = (type) => {
    switch (type) {
      case 'bank_account':
        return BuildingLibraryIcon
      case 'upi':
        return DevicePhoneMobileIcon
      default:
        return CreditCardIcon
    }
  }

  const getConfigLabel = (type) => {
    const labels = {
      bank_account: 'Bank Account',
      upi: 'UPI',
      razorpay: 'Razorpay',
      stripe: 'Stripe',
      phonepe: 'PhonePe',
      paytm: 'Paytm',
      other: 'Other',
    }
    return labels[type] || type
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Payment Settings</h1>
          <p className="text-gray-600 mt-1">
            Manage how you receive payments - bank accounts, UPI, and payment providers
          </p>
        </div>
        <button
          onClick={() => {
            resetForm()
            setEditingConfig(null)
            setShowForm(true)
          }}
          className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          <PlusIcon className="h-5 w-5" />
          <span>Add Payment Method</span>
        </button>
      </div>

      {/* Payment Configs List */}
      {configs.length === 0 && !showForm ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
          <BuildingLibraryIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Payment Methods</h3>
          <p className="text-gray-600 mb-4">
            Add a payment method to start receiving payments from your customers.
          </p>
          <button
            onClick={() => {
              resetForm()
              setShowForm(true)
            }}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Add Payment Method
          </button>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-6">
          {configs.map((config) => {
            const Icon = getConfigIcon(config.config_type)
            return (
              <div
                key={config.id}
                className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <Icon className="h-8 w-8 text-primary-600" />
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {getConfigLabel(config.config_type)}
                      </h3>
                      <div className="flex items-center space-x-2 mt-1">
                        {config.is_primary && (
                          <span className="px-2 py-1 bg-primary-100 text-primary-700 text-xs font-medium rounded">
                            Primary
                          </span>
                        )}
                        {config.is_verified ? (
                          <span className="flex items-center space-x-1 text-green-600 text-xs" title={config.verified_by_username ? `Verified by ${config.verified_by_username}` : 'Verified'}>
                            <CheckCircleIcon className="h-4 w-4" />
                            <span>Verified{config.verified_by_username ? ` by ${config.verified_by_username}` : ''}</span>
                          </span>
                        ) : (
                          <span className="flex items-center space-x-1 text-yellow-600 text-xs" title="Awaiting admin verification">
                            <XCircleIcon className="h-4 w-4" />
                            <span>Pending Admin Verification</span>
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleEdit(config)}
                      className="p-2 text-gray-600 hover:text-primary-600 hover:bg-gray-50 rounded-lg"
                    >
                      <PencilIcon className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(config.id)}
                      className="p-2 text-gray-600 hover:text-red-600 hover:bg-gray-50 rounded-lg"
                    >
                      <TrashIcon className="h-5 w-5" />
                    </button>
                  </div>
                </div>

                <div className="space-y-2 text-sm text-gray-600">
                  {config.config_type === 'bank_account' && (
                    <>
                      <div>
                        <span className="font-medium">Account:</span> {config.account_number ? `****${config.account_number.slice(-4)}` : 'N/A'}
                      </div>
                      <div>
                        <span className="font-medium">Bank:</span> {config.bank_name || 'N/A'}
                      </div>
                      <div>
                        <span className="font-medium">IFSC:</span> {config.ifsc_code || 'N/A'}
                      </div>
                      <div>
                        <span className="font-medium">Holder:</span> {config.account_holder_name || 'N/A'}
                      </div>
                    </>
                  )}
                  {config.config_type === 'upi' && (
                    <div>
                      <span className="font-medium">UPI ID:</span> {config.upi_id || 'N/A'}
                    </div>
                  )}
                  {['razorpay', 'stripe', 'phonepe', 'paytm', 'other'].includes(config.config_type) && (
                    <>
                      <div>
                        <span className="font-medium">Merchant ID:</span> {config.provider_merchant_id || 'N/A'}
                      </div>
                      <div>
                        <span className="font-medium">Status:</span> {config.is_active ? 'Active' : 'Inactive'}
                      </div>
                    </>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Add/Edit Form */}
      {showForm && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">
            {editingConfig ? 'Edit Payment Method' : 'Add Payment Method'}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Method Type
              </label>
              <select
                value={formData.config_type}
                onChange={(e) => {
                  setFormData({ ...formData, config_type: e.target.value })
                }}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                disabled={!!editingConfig}
              >
                <option value="bank_account">Bank Account</option>
                <option value="upi">UPI</option>
                <option value="razorpay">Razorpay</option>
                <option value="stripe">Stripe</option>
                <option value="phonepe">PhonePe</option>
                <option value="paytm">Paytm</option>
                <option value="other">Other</option>
              </select>
            </div>

            {/* Bank Account Fields */}
            {formData.config_type === 'bank_account' && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Account Holder Name *
                  </label>
                  <input
                    type="text"
                    value={formData.account_holder_name}
                    onChange={(e) => setFormData({ ...formData, account_holder_name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Account Number *
                  </label>
                  <input
                    type="text"
                    value={formData.account_number}
                    onChange={(e) => setFormData({ ...formData, account_number: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    required
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      IFSC Code *
                    </label>
                    <input
                      type="text"
                      value={formData.ifsc_code}
                      onChange={(e) => setFormData({ ...formData, ifsc_code: e.target.value.toUpperCase() })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Bank Name *
                    </label>
                    <input
                      type="text"
                      value={formData.bank_name}
                      onChange={(e) => setFormData({ ...formData, bank_name: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Branch Name
                  </label>
                  <input
                    type="text"
                    value={formData.branch_name}
                    onChange={(e) => setFormData({ ...formData, branch_name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </>
            )}

            {/* UPI Fields */}
            {formData.config_type === 'upi' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  UPI ID *
                </label>
                <input
                  type="text"
                  value={formData.upi_id}
                  onChange={(e) => setFormData({ ...formData, upi_id: e.target.value })}
                  placeholder="yourname@paytm"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  required
                />
              </div>
            )}

            {/* Payment Provider Fields */}
            {['razorpay', 'stripe', 'phonepe', 'paytm', 'other'].includes(formData.config_type) && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Key *
                  </label>
                  <input
                    type="text"
                    value={formData.provider_key}
                    onChange={(e) => setFormData({ ...formData, provider_key: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Secret Key *
                  </label>
                  <input
                    type="password"
                    value={formData.provider_secret}
                    onChange={(e) => setFormData({ ...formData, provider_secret: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Merchant ID
                  </label>
                  <input
                    type="text"
                    value={formData.provider_merchant_id}
                    onChange={(e) => setFormData({ ...formData, provider_merchant_id: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Webhook Secret
                  </label>
                  <input
                    type="password"
                    value={formData.provider_webhook_secret}
                    onChange={(e) => setFormData({ ...formData, provider_webhook_secret: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  />
                </div>
              </>
            )}

            <div className="flex items-center space-x-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.is_primary}
                  onChange={(e) => setFormData({ ...formData, is_primary: e.target.checked })}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">Set as primary payment method</span>
              </label>
            </div>

            <div className="flex items-center justify-end space-x-4">
              <button
                type="button"
                onClick={() => {
                  setShowForm(false)
                  setEditingConfig(null)
                  resetForm()
                }}
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                {editingConfig ? 'Update' : 'Add'} Payment Method
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}

