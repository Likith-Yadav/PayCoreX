import { useState, useEffect } from 'react'
import { dashboardAPI } from '../services/api'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function Analytics() {
  const [stats, setStats] = useState(null)
  const [payments, setPayments] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [statsRes, paymentsRes] = await Promise.all([
        dashboardAPI.getStats(),
        dashboardAPI.getPayments({ limit: 100 }),
      ])
      setStats(statsRes.data)
      setPayments(paymentsRes.data.results)
    } catch (error) {
      console.error('Failed to load analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  // Process data for charts
  const processChartData = () => {
    const methodData = {}
    const statusData = {}

    payments.forEach((payment) => {
      methodData[payment.method] = (methodData[payment.method] || 0) + 1
      statusData[payment.status] = (statusData[payment.status] || 0) + 1
    })

    return {
      methods: Object.entries(methodData).map(([name, value]) => ({ name, value })),
      statuses: Object.entries(statusData).map(([name, value]) => ({ name, value })),
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const chartData = processChartData()

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        <p className="text-gray-600 mt-1">Insights into your payment performance</p>
      </div>

      {stats && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Payment Methods</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData.methods}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#0ea5e9" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Transaction Status</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData.statuses}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-sm font-medium text-gray-600 mb-2">Total Volume</h3>
          <p className="text-3xl font-bold text-gray-900">
            ₹{stats?.overview.total_volume.toLocaleString('en-IN')}
          </p>
        </div>
        <div className="card">
          <h3 className="text-sm font-medium text-gray-600 mb-2">Success Rate</h3>
          <p className="text-3xl font-bold text-gray-900">{stats?.overview.success_rate}%</p>
        </div>
        <div className="card">
          <h3 className="text-sm font-medium text-gray-600 mb-2">Total Transactions</h3>
          <p className="text-3xl font-bold text-gray-900">
            {stats?.overview.total_transactions.toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  )
}

