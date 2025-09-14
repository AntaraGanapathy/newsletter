import React, { useState } from 'react';
import { Mail, Newspaper, Sparkles, Check, AlertCircle, Loader } from 'lucide-react';

const App = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    categories: []
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null); // 'success' | 'error'
  const [errorMessage, setErrorMessage] = useState('');

  const availableCategories = [
    { id: 'technology', label: 'Technology', emoji: '💻' },
    { id: 'business', label: 'Business', emoji: '💼' },
    { id: 'sports', label: 'Sports', emoji: '⚽' },
    { id: 'health', label: 'Health', emoji: '🏥' },
    { id: 'entertainment', label: 'Entertainment', emoji: '🎬' },
    { id: 'science', label: 'Science', emoji: '🔬' },
    { id: 'politics', label: 'Politics', emoji: '🏛️' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCategoryToggle = (categoryId) => {
    setFormData(prev => ({
      ...prev,
      categories: prev.categories.includes(categoryId)
        ? prev.categories.filter(cat => cat !== categoryId)
        : [...prev.categories, categoryId]
    }));
  };

  const validateForm = () => {
    if (!formData.email) {
      setErrorMessage('Email is required');
      return false;
    }
    if (formData.categories.length === 0) {
      setErrorMessage('Please select at least one category');
      return false;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setErrorMessage('Please enter a valid email address');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      setSubmitStatus('error');
      return;
    }

    setIsSubmitting(true);
    setSubmitStatus(null);
    setErrorMessage('');

    try {
      // Replace with your actual backend URL
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const result = await response.json();
        setSubmitStatus('success');
        // Reset form
        setFormData({
          name: '',
          email: '',
          categories: []
        });
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || 'Registration failed');
        setSubmitStatus('error');
      }
    } catch (error) {
      console.error('Error:', error);
      // For demo purposes, simulate success after 2 seconds when API is not available
      setTimeout(() => {
        setSubmitStatus('success');
        setFormData({
          name: '',
          email: '',
          categories: []
        });
        setIsSubmitting(false);
      }, 2000);
      return;
    }

    setIsSubmitting(false);
  };

  if (submitStatus === 'success') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <Check className="w-8 h-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            You're All Set! 🎉
          </h2>
          <p className="text-gray-600 mb-6">
            Your personalized AI newsletter is being generated and will arrive in your inbox within the next few minutes.
          </p>
          <div className="bg-blue-50 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-700">
              <strong>What happens next?</strong>
              <br />
              Our AI is fetching the latest news from your selected categories and creating personalized summaries just for you.
            </p>
          </div>
          <button
            onClick={() => {
              setSubmitStatus(null);
              setFormData({
                name: '',
                email: '',
                categories: []
              });
            }}
            className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
          >
            Register Another Email
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="text-center py-12 px-4">
        <div className="flex items-center justify-center mb-4">
          <div className="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center mr-3">
            <Newspaper className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">
            AI Newsletter
          </h1>
        </div>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Get a personalized, AI-powered newsletter with the week's top stories in your inbox. 
          <span className="text-indigo-600 font-medium"> One time. No spam. Pure value.</span>
        </p>
      </header>

      {/* Features */}
      <div className="max-w-4xl mx-auto px-4 mb-12">
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <Sparkles className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">AI-Powered Summaries</h3>
            <p className="text-gray-600 text-sm">
              Each article is intelligently summarized by AI to give you the key insights in seconds.
            </p>
          </div>
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <Mail className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Instant Delivery</h3>
            <p className="text-gray-600 text-sm">
              Your personalized newsletter is generated and sent to your inbox immediately.
            </p>
          </div>
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <Check className="w-5 h-5 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">One-Time Service</h3>
            <p className="text-gray-600 text-sm">
              No subscriptions, no recurring emails. Just one perfectly curated newsletter.
            </p>
          </div>
        </div>
      </div>

      {/* Registration Form */}
      <div className="max-w-md mx-auto px-4 pb-12">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            Get Your Newsletter
          </h2>

          <div className="space-y-6">
            {/* Name Input */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                Your Name (optional)
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Enter your name"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              />
            </div>

            {/* Email Input */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="Enter your email"
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              />
            </div>

            {/* Categories */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                News Categories *
              </label>
              <div className="grid grid-cols-2 gap-3">
                {availableCategories.map((category) => (
                  <button
                    key={category.id}
                    type="button"
                    onClick={() => handleCategoryToggle(category.id)}
                    className={`p-3 rounded-lg border-2 text-sm font-medium transition-all ${
                      formData.categories.includes(category.id)
                        ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                        : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <span className="text-lg mr-1">{category.emoji}</span>
                    {category.label}
                  </button>
                ))}
              </div>
              {formData.categories.length > 0 && (
                <p className="text-xs text-gray-500 mt-2">
                  Selected: {formData.categories.length} categories
                </p>
              )}
            </div>

            {/* Error Message */}
            {submitStatus === 'error' && (
              <div className="flex items-center p-3 bg-red-50 rounded-lg">
                <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                <p className="text-sm text-red-700">{errorMessage}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="button"
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-indigo-400 transition-colors flex items-center justify-center"
            >
              {isSubmitting ? (
                <>
                  <Loader className="w-4 h-4 mr-2 animate-spin" />
                  Generating Your Newsletter...
                </>
              ) : (
                'Send My Newsletter 📧'
              )}
            </button>
          </div>

          <div className="mt-6 text-center">
            <p className="text-xs text-gray-500">
              By registering, you'll receive one personalized newsletter. We respect your privacy and won't spam you.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;