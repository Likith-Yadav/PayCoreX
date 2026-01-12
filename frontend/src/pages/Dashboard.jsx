import { useState, useEffect } from 'react'
import { dashboardAPI } from '../services/api'
import {
  CurrencyDollarIcon,
  CreditCardIcon,
  CheckCircleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const response = await dashboardAPI.getStats()
      setStats(response.data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!stats) {
    return <div className="text-center text-gray-500">Failed to load dashboard</div>
  }

  const statCards = [
    {
      title: 'Total Volume',
      value: `₹${stats.overview.total_volume.toLocaleString('en-IN')}`,
      icon: CurrencyDollarIcon,
      color: 'bg-blue-500',
    },
    {
      title: 'Total Transactions',
      value: stats.overview.total_transactions.toLocaleString(),
      icon: CreditCardIcon,
      color: 'bg-green-500',
    },
    {
      title: 'Success Rate',
      value: `${stats.overview.success_rate}%`,
      icon: CheckCircleIcon,
      color: 'bg-purple-500',
    },
    {
      title: 'Net Volume',
      value: `₹${stats.overview.net_volume.toLocaleString('en-IN')}`,
      icon: CurrencyDollarIcon,
      color: 'bg-indigo-500',
    },
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-black mb-2">Dashboard</h1>
        <p className="text-gray-700 text-lg">Welcome back! Here's your payment overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <div key={index} className="card hover:shadow-lg transition-all duration-300">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-2 font-medium">{stat.title}</p>
                  <p className="text-3xl font-bold text-black">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-4 rounded-xl shadow-sm`}>
                  <Icon className="h-7 w-7 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* This Month Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">This Month</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Volume</span>
              <span className="font-semibold">₹{stats.this_month.volume.toLocaleString('en-IN')}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Transactions</span>
              <span className="font-semibold">{stats.this_month.transactions}</span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Payments</h3>
          <div className="space-y-3">
            {stats.recent_payments.slice(0, 5).map((payment) => (
              <div key={payment.id} className="flex justify-between items-center">
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    ₹{payment.amount.toLocaleString('en-IN')}
                  </p>
                  <p className="text-xs text-gray-500">{payment.method}</p>
                </div>
                <span
                  className={`px-2 py-1 rounded text-xs font-medium ${
                    payment.status === 'success'
                      ? 'bg-green-100 text-green-800'
                      : payment.status === 'failed'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}
                >
                  {payment.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

