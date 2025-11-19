import React, { useState, useEffect } from 'react';
import { Upload, FileText, AlertCircle, CheckCircle, XCircle, Clock, Filter, Search, Home, Info } from 'lucide-react';
import VerifyForm from './components/VerifyForm';
import ResultCard from './components/ResultCard';
import { fetchHistory, checkAPIStatus } from './api';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// Helper: localStorage wrapper (fallback)
const STORAGE_PREFIX = 'verification:';

const saveToStorage = (key, value) => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (err) {
    console.error('localStorage set error', err);
  }
};

const loadFromStorage = () => {
  try {
    const keys = Object.keys(localStorage).filter(k => k.startsWith(STORAGE_PREFIX));
    const history = keys.map(k => {
      try { return JSON.parse(localStorage.getItem(k)); } catch { return null; }
    }).filter(Boolean);
    return history.sort((a,b) => new Date(b.timestamp) - new Date(a.timestamp));
  } catch (err) {
    console.error('localStorage read error', err);
    return [];
  }
};

const App = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [verificationHistory, setVerificationHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');


  useEffect(() => {
    // Load history from API first, fallback to localStorage
    const loadHistory = async () => {
      const apiHistory = await fetchHistory();
      if (apiHistory.length > 0) {
        setVerificationHistory(apiHistory);
      } else {
        setVerificationHistory(loadFromStorage());
      }
    };
    loadHistory();
    
    // Check API status
    checkAPIStatus()
      .then((isOnline) => setApiStatus(isOnline ? 'online' : 'offline'))
      .catch(() => setApiStatus('offline'));
  }, []);


  const handleVerificationComplete = (result) => {
    // Save to localStorage as backup
    saveToStorage(`${STORAGE_PREFIX}${result.id}`, result);
    
    // Update history
    const updatedHistory = [result, ...verificationHistory];
    setVerificationHistory(updatedHistory);
    
    // Navigate to results page
    setCurrentPage('result');
    setApiStatus('online');
  };

  const handleBatchComplete = (results) => {
    // Add batch results to history without navigation
    results.forEach(result => {
      saveToStorage(`${STORAGE_PREFIX}${result.id}`, result);
    });
    
    // Update history with all batch results
    const updatedHistory = [...results, ...verificationHistory];
    setVerificationHistory(updatedHistory);
    setApiStatus('online');
  };

  const getRiskColor = (risk) => {
    switch(risk) {
      case 'Low': return 'text-green-600 bg-green-50';
      case 'Medium': return 'text-yellow-600 bg-yellow-50';
      case 'High': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getStatusIcon = (status) => {
    return status === 'Verified' ? 
      <CheckCircle className="w-5 h-5 text-green-600" /> : 
      <AlertCircle className="w-5 h-5 text-red-600" />;
  };

  const filteredHistory = verificationHistory.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.aadharNumber.includes(searchTerm);
    const matchesFilter = filterStatus === 'all' || item.riskLevel === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const latestResult = verificationHistory[0];

  // Dashboard Page
  const DashboardPage = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total Verifications</p>
              <p className="text-3xl font-bold text-gray-800">{verificationHistory.length}</p>
            </div>
            <FileText className="w-10 h-10 text-blue-500" />
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Verified</p>
              <p className="text-3xl font-bold text-gray-800">{verificationHistory.filter(v => v.status === 'Verified').length}</p>
            </div>
            <CheckCircle className="w-10 h-10 text-green-500" />
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-red-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Flagged</p>
              <p className="text-3xl font-bold text-gray-800">{verificationHistory.filter(v => v.status === 'Flagged').length}</p>
            </div>
            <AlertCircle className="w-10 h-10 text-red-500" />
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">System Overview</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
            <span className="text-gray-700">Backend API Status</span>
            <span className={`font-semibold ${apiStatus === 'online' ? 'text-green-600' : apiStatus === 'offline' ? 'text-red-600' : 'text-yellow-600'}`}>
              {apiStatus === 'online' ? '✓ Online' : apiStatus === 'offline' ? '✗ Offline' : '⏳ Checking...'}
            </span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
            <span className="text-gray-700">AI Models Active</span>
            <span className={`font-semibold ${apiStatus === 'online' ? 'text-green-600' : 'text-gray-400'}`}>
              {apiStatus === 'online' ? '✓ Online' : '—'}
            </span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
            <span className="text-gray-700">Compliance Status</span>
            <span className="text-green-600 font-semibold">✓ Compliant</span>
          </div>
          {apiStatus === 'offline' && (
            <div className="p-3 bg-yellow-50 border border-yellow-200 rounded">
              <p className="text-sm text-yellow-800">
                ⚠️ Backend API is offline. Please ensure the backend server is running at {API_BASE_URL}
              </p>
            </div>
          )}
        </div>
      </div>

      {verificationHistory.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Recent Verifications</h2>
          <div className="space-y-3">
            {verificationHistory.slice(0, 5).map((item) => (
              <div key={item.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                <div className="flex items-center gap-3">
                  {getStatusIcon(item.status)}
                  <div>
                    <p className="font-semibold text-gray-800">{item.name}</p>
                    <p className="text-sm text-gray-500">{item.aadharNumber}</p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(item.riskLevel)}`}>
                  {item.riskLevel} Risk
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  // Upload/Verify Page
  const UploadPage = () => (
    <VerifyForm
      onVerificationComplete={handleVerificationComplete}
      onBatchComplete={handleBatchComplete}
      isLoading={isLoading}
      setIsLoading={setIsLoading}
      setError={setError}
      apiStatus={apiStatus}
    />
  );

  // Result Page
  const ResultPage = () => (
    <ResultCard
      result={latestResult}
      onNewVerification={() => setCurrentPage('upload')}
    />
  );

  // History Page
  const HistoryPage = () => {
    const [refreshing, setRefreshing] = useState(false);
    
    const refreshHistory = async () => {
      setRefreshing(true);
      const apiHistory = await fetchHistory();
      if (apiHistory.length > 0) {
        setVerificationHistory(apiHistory);
      }
      setRefreshing(false);
    };

    return (
    <div>
      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <div className="flex flex-col md:flex-row gap-4 mb-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by name or AADHAR number..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-500" />
            <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="all">All Risk Levels</option>
              <option value="Low">Low Risk</option>
              <option value="Medium">Medium Risk</option>
              <option value="High">High Risk</option>
            </select>
            <button
              onClick={refreshHistory}
              disabled={refreshing}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
            >
              {refreshing ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">AADHAR</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Timestamp</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Level</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredHistory.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-gray-500">No verification records found</td>
                </tr>
              ) : (
                filteredHistory.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-800">{item.id}</td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-800">{item.name}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{item.aadharNumber}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{new Date(item.timestamp).toLocaleDateString()}</td>
                    <td className="px-6 py-4"><span className={`px-3 py-1 rounded-full text-xs font-semibold ${getRiskColor(item.riskLevel)}`}>{item.riskLevel}</span></td>
                    <td className="px-6 py-4"><div className="flex items-center gap-2">{getStatusIcon(item.status)}<span className="text-sm font-medium text-gray-800">{item.status}</span></div></td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    );
  };

  // About Page
  const AboutPage = () => {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white p-8 rounded-lg shadow-md">
          <h2 className="text-3xl font-bold mb-6 text-gray-800">AI-Powered Identity Verification System</h2>
          
          <div className="space-y-6">
            <section>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Project Overview</h3>
              <p className="text-gray-700 leading-relaxed">This advanced AI-driven identity verification system is tailored for BFSI (Banking, Financial Services, and Insurance) KYC and AML (Anti-Money Laundering) compliance. Leveraging cutting-edge technologies such as Graph Neural Networks (GNNs), Natural Language Processing (NLP), and Computer Vision, the solution validates customer identities and verifies the legitimacy of documents like AADHAR cards.</p>
            </section>

            <section>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Key Features</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-blue-50 rounded-lg"><h4 className="font-semibold text-blue-900 mb-2">Enhanced Identity Verification</h4><p className="text-sm text-gray-700">AI and deep learning automate and improve identity checks for KYC/AML compliance.</p></div>
                <div className="p-4 bg-green-50 rounded-lg"><h4 className="font-semibold text-green-900 mb-2">Fraudulent Address Detection</h4><p className="text-sm text-gray-700">Robust mechanisms verify the authenticity of AADHAR addresses.</p></div>
                <div className="p-4 bg-purple-50 rounded-lg"><h4 className="font-semibold text-purple-900 mb-2">Improved Compliance</h4><p className="text-sm text-gray-700">Automatic checks aligned with regulatory frameworks prevent fraud.</p></div>
                <div className="p-4 bg-yellow-50 rounded-lg"><h4 className="font-semibold text-yellow-900 mb-2">Cost Reduction</h4><p className="text-sm text-gray-700">Minimization of manual effort through intelligent automation.</p></div>
              </div>
            </section>

            <section>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Technology Stack</h3>
              <div className="flex flex-wrap gap-2">{['Azure OpenAI', 'Graph Neural Networks', 'NLP', 'Computer Vision', 'React', 'Python'].map(tech => (<span key={tech} className="px-4 py-2 bg-gray-100 rounded-full text-sm font-medium text-gray-700">{tech}</span>))}</div>
            </section>

            <section>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Implementation Modules</h3>
              <div className="space-y-3">
                <div className="border-l-4 border-blue-500 pl-4 py-2"><h4 className="font-semibold text-gray-800">Module 1: Data Collection & Preprocessing</h4><p className="text-sm text-gray-600">Collect and prepare identity documents for model development.</p></div>
                <div className="border-l-4 border-green-500 pl-4 py-2"><h4 className="font-semibold text-gray-800">Module 2: Model Development</h4><p className="text-sm text-gray-600">Build AI models to verify identities and detect fraudulent addresses.</p></div>
                <div className="border-l-4 border-purple-500 pl-4 py-2"><h4 className="font-semibold text-gray-800">Module 3: AML & KYC Integration</h4><p className="text-sm text-gray-600">Enable real-time validation workflows integrated with compliance systems.</p></div>
                <div className="border-l-4 border-yellow-500 pl-4 py-2"><h4 className="font-semibold text-gray-800">Module 4: Deployment & Verification</h4><p className="text-sm text-gray-600">Deploy end-to-end system and validate performance with real data.</p></div>
              </div>
            </section>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center"><FileText className="w-6 h-6 text-white" /></div>
              <div><h1 className="text-2xl font-bold text-gray-800">KYC Verification System</h1><p className="text-sm text-gray-500">AI-Powered Identity & Fraud Detection</p></div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[{ id: 'dashboard', label: 'Dashboard', icon: Home },{ id: 'upload', label: 'Verify Identity', icon: Upload },{ id: 'result', label: 'Results', icon: FileText },{ id: 'history', label: 'History', icon: Clock },{ id: 'about', label: 'About', icon: Info }].map(({ id, label, icon: Icon }) => (
              <button key={id} onClick={() => setCurrentPage(id)} className={`flex items-center gap-2 py-4 px-2 border-b-2 font-medium text-sm transition ${currentPage === id ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}>
                <Icon className="w-4 h-4" />
                {label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentPage === 'dashboard' && <DashboardPage />}
        {currentPage === 'upload' && <UploadPage />}
        {currentPage === 'result' && <ResultPage />}
        {currentPage === 'history' && <HistoryPage />}
        {currentPage === 'about' && <AboutPage />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6"><p className="text-center text-gray-500 text-sm">© 2025 KYC Verification System | BFSI Compliance & AML Detection</p></div>
      </footer>
    </div>
  );
};

export default App;
