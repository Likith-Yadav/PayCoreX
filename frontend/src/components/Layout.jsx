import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import {
  HomeIcon,
  KeyIcon,
  DocumentTextIcon,
  ChartBarIcon,
  ArrowRightOnRectangleIcon,
  BookOpenIcon,
  CreditCardIcon,
  CheckCircleIcon,
  Bars3Icon,
  XMarkIcon,
} from '@heroicons/react/24/outline'

export default function Layout({ children }) {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: HomeIcon },
    { path: '/api-keys', label: 'API Keys', icon: KeyIcon },
    { path: '/payment-settings', label: 'Payment Settings', icon: CreditCardIcon },
    { path: '/transactions', label: 'Transactions', icon: DocumentTextIcon },
    { path: '/verifications', label: 'Verifications', icon: CheckCircleIcon },
    { path: '/analytics', label: 'Analytics', icon: ChartBarIcon },
    { path: '/docs', label: 'Documentation', icon: BookOpenIcon },
  ]

  return (
    <div className="min-h-screen bg-white relative">
      {/* Background gradient and grid */}
      <div className="fixed inset-0 gradient-bg grid-pattern opacity-30 pointer-events-none"></div>
      
      <div className="relative z-10">
        {/* Header */}
        <header className="bg-white/90 backdrop-blur-sm border-b border-gray-100 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <Link to="/dashboard" className="text-xl sm:text-2xl font-bold text-black">
                  PayCoreX
                </Link>
              </div>
              <div className="flex items-center space-x-2 sm:space-x-4">
                <div className="hidden sm:block text-sm text-gray-700 font-medium">
                  {user?.first_name} {user?.last_name}
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 text-gray-700 hover:text-black transition-colors px-2 sm:px-0"
                >
                  <ArrowRightOnRectangleIcon className="h-5 w-5" />
                  <span className="hidden sm:inline">Logout</span>
                </button>
                {/* Mobile menu button */}
                <button
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="lg:hidden p-2 text-gray-700 hover:text-black transition-colors"
                >
                  {mobileMenuOpen ? (
                    <XMarkIcon className="h-6 w-6" />
                  ) : (
                    <Bars3Icon className="h-6 w-6" />
                  )}
                </button>
              </div>
            </div>
          </div>
        </header>

        <div className="flex flex-col lg:flex-row">
          {/* Mobile Sidebar */}
          {mobileMenuOpen && (
            <div className="lg:hidden fixed inset-0 z-40 bg-black/50" onClick={() => setMobileMenuOpen(false)}>
              <aside 
                className="w-64 bg-white border-r border-gray-100 h-full shadow-xl"
                onClick={(e) => e.stopPropagation()}
              >
                <nav className="p-4 space-y-1">
                  {navItems.map((item) => {
                    const Icon = item.icon
                    const isActive = location.pathname === item.path
                    return (
                      <Link
                        key={item.path}
                        to={item.path}
                        onClick={() => setMobileMenuOpen(false)}
                        className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                          isActive
                            ? 'bg-primary-100 text-black font-semibold shadow-sm'
                            : 'text-gray-700 hover:bg-gray-50 hover:text-black'
                        }`}
                      >
                        <Icon className="h-5 w-5" />
                        <span>{item.label}</span>
                      </Link>
                    )
                  })}
                </nav>
              </aside>
            </div>
          )}

          {/* Desktop Sidebar */}
          <aside className="hidden lg:block w-64 bg-white/80 backdrop-blur-sm border-r border-gray-100 min-h-[calc(100vh-4rem)] sticky top-16">
            <nav className="p-4 space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                      isActive
                        ? 'bg-primary-100 text-black font-semibold shadow-sm'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-black'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
            </nav>
          </aside>

          {/* Main Content */}
          <main className="flex-1 p-4 sm:p-6 lg:p-8">
            {children}
          </main>
        </div>
      </div>
    </div>
  )
}

