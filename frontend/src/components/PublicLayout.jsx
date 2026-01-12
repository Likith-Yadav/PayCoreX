import { Link, useLocation } from 'react-router-dom'
import { BookOpenIcon, ArrowLeftIcon } from '@heroicons/react/24/outline'

export default function PublicLayout({ children }) {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Link to="/" className="text-2xl font-bold text-primary-600">
                PayCoreX
              </Link>
              <div className="flex items-center text-sm text-gray-500">
                <BookOpenIcon className="h-4 w-4 mr-1" />
                <span>Documentation</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/"
                className="inline-flex items-center text-gray-700 hover:text-gray-900 px-4 py-2 font-medium transition-colors"
              >
                <ArrowLeftIcon className="h-4 w-4 mr-2" />
                Back to Home
              </Link>
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
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  )
}

