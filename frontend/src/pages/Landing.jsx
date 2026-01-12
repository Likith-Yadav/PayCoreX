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
    <div className="min-h-screen bg-white relative overflow-hidden">
      {/* Background gradient and grid */}
      <div className="absolute inset-0 gradient-bg grid-pattern opacity-50"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-primary-100 rounded-full blur-3xl opacity-30 -translate-x-1/2 translate-y-1/2"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-primary-100 rounded-full blur-3xl opacity-30 translate-x-1/2 translate-y-1/2"></div>
      
      <div className="relative z-10">
        {/* Navigation */}
        <nav className="bg-white/80 backdrop-blur-sm border-b border-gray-100 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <span className="text-2xl font-bold text-black">PayCoreX</span>
              </div>
              <div className="flex items-center space-x-3 sm:space-x-6">
                {loading ? (
                  <div className="w-6 h-6 sm:w-8 sm:h-8 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
                ) : user ? (
                  <Link
                    to="/dashboard"
                    className="btn-primary text-sm sm:text-base px-4 sm:px-6 py-2"
                  >
                    Dashboard
                  </Link>
                ) : (
                  <>
                    <Link
                      to="/login"
                      className="text-black hover:text-gray-700 px-2 sm:px-4 py-2 font-medium transition-colors text-sm sm:text-base"
                    >
                      Log in
                    </Link>
                    <Link
                      to="/signup"
                      className="btn-primary text-sm sm:text-base px-4 sm:px-6 py-2"
                    >
                      Sign Up Free
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="relative pt-12 sm:pt-16 md:pt-20 pb-20 sm:pb-24 md:pb-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-black mb-6 leading-tight px-4">
                <span className="inline-block bg-primary-300 text-white px-3 py-2 sm:px-4 sm:py-2 rounded-lg mr-2 sm:mr-3 mb-2 sm:mb-0">Payments</span>
                <span className="block sm:inline">Made for Developers, Not Just APIs</span>
              </h1>
              <p className="text-lg sm:text-xl text-gray-700 mb-8 sm:mb-10 max-w-3xl mx-auto leading-relaxed px-4">
                Transform the way you accept payments—integrate seamlessly, process securely, and scale effortlessly with our modern payment gateway.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
                {user ? (
                  <Link
                    to="/dashboard"
                    className="btn-primary text-lg px-8 py-4 inline-flex items-center"
                  >
                    Go to Dashboard
                    <ArrowRightIcon className="ml-2 h-5 w-5" />
                  </Link>
                ) : (
                  <Link
                    to="/signup"
                    className="btn-primary text-lg px-8 py-4 inline-flex items-center"
                  >
                    Start With 15 Days Trial
                    <ArrowRightIcon className="ml-2 h-5 w-5" />
                  </Link>
                )}
              </div>
              
              {/* Demo Request Section */}
              {!user && (
                <div className="max-w-md mx-auto">
                  <div className="flex flex-col sm:flex-row gap-3 mb-3">
                    <input
                      type="email"
                      placeholder="Enter your E-mail"
                      className="input-field flex-1"
                    />
                    <button className="btn-secondary whitespace-nowrap">
                      Request a demo
                    </button>
                  </div>
                  <p className="text-sm text-gray-600">
                    Test your free demo without any payment form
                  </p>
                </div>
              )}
            </div>
          </div>
        </section>

      {/* Features Section */}
      <section className="py-12 sm:py-16 md:py-20 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-black mb-4">Everything You Need</h2>
            <p className="text-lg sm:text-xl text-gray-700">Powerful features to grow your business</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <div
                  key={index}
                  className="card hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                >
                  <div className="bg-primary-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
                    <Icon className="h-7 w-7 text-primary-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-black mb-3">{feature.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-12 sm:py-16 md:py-20 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 sm:gap-12 items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
                Why Choose PayCoreX?
              </h2>
              <p className="text-lg text-gray-700 mb-8 leading-relaxed">
                We've built a payment gateway that's not just powerful, but also intuitive
                and developer-friendly. Join thousands of businesses already using PayCoreX.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center">
                    <CheckIcon className="h-5 w-5 text-primary-500 mr-3 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="card shadow-xl">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-5 bg-primary-50 rounded-xl">
                  <span className="text-gray-700 font-medium">Total Volume Processed</span>
                  <span className="text-2xl font-bold text-primary-600">₹10M+</span>
                </div>
                <div className="flex items-center justify-between p-5 bg-green-50 rounded-xl">
                  <span className="text-gray-700 font-medium">Active Merchants</span>
                  <span className="text-2xl font-bold text-green-600">5,000+</span>
                </div>
                <div className="flex items-center justify-between p-5 bg-purple-50 rounded-xl">
                  <span className="text-gray-700 font-medium">Success Rate</span>
                  <span className="text-2xl font-bold text-purple-600">99.9%</span>
                </div>
                <div className="flex items-center justify-between p-5 bg-blue-50 rounded-xl">
                  <span className="text-gray-700 font-medium">Uptime</span>
                  <span className="text-2xl font-bold text-blue-600">99.99%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 sm:py-16 md:py-20 relative z-10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-black mb-4">Ready to Get Started?</h2>
          <p className="text-lg sm:text-xl text-gray-700 mb-6 sm:mb-8">
            Join thousands of businesses already using PayCoreX to accept payments
          </p>
          {user ? (
            <Link
              to="/dashboard"
              className="btn-primary text-lg px-8 py-4 inline-flex items-center"
            >
              Go to Dashboard
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
          ) : (
            <Link
              to="/signup"
              className="btn-primary text-lg px-8 py-4 inline-flex items-center"
            >
              Create Your Account
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-12 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="sm:col-span-2 lg:col-span-1">
              <span className="text-2xl font-bold text-black mb-4 block">PayCoreX</span>
              <p className="text-sm text-gray-600 leading-relaxed">
                The modern payment gateway for growing businesses.
              </p>
            </div>
            <div>
              <h4 className="text-black font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link to="/docs" className="text-gray-600 hover:text-black transition-colors">
                    Documentation
                  </Link>
                </li>
                <li>
                  <Link to="/docs" className="text-gray-600 hover:text-black transition-colors">
                    API Reference
                  </Link>
                </li>
                <li>
                  <a href="#" className="text-gray-600 hover:text-black transition-colors">
                    Pricing
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-black font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="text-gray-600 hover:text-black transition-colors">
                    About
                  </a>
                </li>
                <li>
                  <a href="#" className="text-gray-600 hover:text-black transition-colors">
                    Blog
                  </a>
                </li>
                <li>
                  <a href="#" className="text-gray-600 hover:text-black transition-colors">
                    Careers
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-black font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="text-gray-600 hover:text-black transition-colors">
                    Help Center
                  </a>
                </li>
                <li>
                  <a href="#" className="text-gray-600 hover:text-black transition-colors">
                    Contact Us
                  </a>
                </li>
                <li>
                  <a href="#" className="text-gray-600 hover:text-black transition-colors">
                    Status
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-200 mt-8 pt-8 text-center text-sm text-gray-600">
            <p>&copy; 2026 PayCoreX. All rights reserved.</p>
          </div>
        </div>
      </footer>
      </div>
    </div>
  )
}

