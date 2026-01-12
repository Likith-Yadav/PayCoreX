import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import {
  ArrowRightIcon,
  CheckIcon,
  CreditCardIcon,
  ShieldCheckIcon,
  ChartBarIcon,
  BoltIcon,
  GlobeAltIcon,
} from '@heroicons/react/24/outline'

export default function Landing() {
  const { user, loading } = useAuth()
  const features = [
    {
      icon: CreditCardIcon,
      title: 'Multiple Payment Methods',
      description: 'Accept payments via UPI, Wallet, Cards, and Cryptocurrency',
    },
    {
      icon: ShieldCheckIcon,
      title: 'Secure & Compliant',
      description: 'Bank-level security with HMAC authentication and encryption',
    },
    {
      icon: ChartBarIcon,
      title: 'Real-time Analytics',
      description: 'Track transactions, revenue, and performance metrics in real-time',
    },
    {
      icon: BoltIcon,
      title: 'Lightning Fast',
      description: 'Process payments instantly with our optimized infrastructure',
    },
    {
      icon: GlobeAltIcon,
      title: 'Global Reach',
      description: 'Accept payments from anywhere in the world',
    },
    {
      icon: CheckIcon,
      title: 'Easy Integration',
      description: 'Simple API with comprehensive documentation and SDKs',
    },
  ]

  const benefits = [
    'Zero setup fees',
    'Competitive transaction rates',
    '24/7 customer support',
    'Instant settlements',
    'Webhook notifications',
    'Comprehensive dashboard',
  ]

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-primary-600">PayCoreX</span>
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

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 via-white to-primary-50 pt-20 pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Payment Gateway
              <span className="text-primary-600"> Made Simple</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Accept payments seamlessly with our powerful, secure, and easy-to-integrate
              payment gateway. Built for modern businesses.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              {user ? (
                <Link
                  to="/dashboard"
                  className="inline-flex items-center justify-center bg-primary-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-primary-700 transition-all transform hover:scale-105 shadow-lg"
                >
                  Go to Dashboard
                  <ArrowRightIcon className="ml-2 h-5 w-5" />
                </Link>
              ) : (
                <Link
                  to="/signup"
                  className="inline-flex items-center justify-center bg-primary-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-primary-700 transition-all transform hover:scale-105 shadow-lg"
                >
                  Start Free Trial
                  <ArrowRightIcon className="ml-2 h-5 w-5" />
                </Link>
              )}
              <a
                href="/docs"
                className="inline-flex items-center justify-center bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg border-2 border-primary-600 hover:bg-primary-50 transition-all"
              >
                View Documentation
              </a>
            </div>
            {!user && (
              <p className="text-sm text-gray-500 mt-4">No credit card required • Free to get started</p>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Everything You Need</h2>
            <p className="text-xl text-gray-600">Powerful features to grow your business</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <div
                  key={index}
                  className="p-6 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-lg transition-all bg-white"
                >
                  <div className="bg-primary-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                    <Icon className="h-6 w-6 text-primary-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Why Choose PayCoreX?
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                We've built a payment gateway that's not just powerful, but also intuitive
                and developer-friendly. Join thousands of businesses already using PayCoreX.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center">
                    <CheckIcon className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-200">
              <div className="space-y-6">
                <div className="flex items-center justify-between p-4 bg-primary-50 rounded-lg">
                  <span className="text-gray-700 font-medium">Total Volume Processed</span>
                  <span className="text-2xl font-bold text-primary-600">₹10M+</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                  <span className="text-gray-700 font-medium">Active Merchants</span>
                  <span className="text-2xl font-bold text-green-600">5,000+</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
                  <span className="text-gray-700 font-medium">Success Rate</span>
                  <span className="text-2xl font-bold text-purple-600">99.9%</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                  <span className="text-gray-700 font-medium">Uptime</span>
                  <span className="text-2xl font-bold text-blue-600">99.99%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">Ready to Get Started?</h2>
          <p className="text-xl text-primary-100 mb-8">
            Join thousands of businesses already using PayCoreX to accept payments
          </p>
          {user ? (
            <Link
              to="/dashboard"
              className="inline-flex items-center justify-center bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-50 transition-all transform hover:scale-105 shadow-lg"
            >
              Go to Dashboard
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
          ) : (
            <Link
              to="/signup"
              className="inline-flex items-center justify-center bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-50 transition-all transform hover:scale-105 shadow-lg"
            >
              Create Your Account
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <span className="text-2xl font-bold text-white mb-4 block">PayCoreX</span>
              <p className="text-sm">
                The modern payment gateway for growing businesses.
              </p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link to="/docs" className="hover:text-white transition-colors">
                    Documentation
                  </Link>
                </li>
                <li>
                  <Link to="/docs" className="hover:text-white transition-colors">
                    API Reference
                  </Link>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Pricing
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    About
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Blog
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Careers
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Help Center
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Contact Us
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Status
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
            <p>&copy; 2026 PayCoreX. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

