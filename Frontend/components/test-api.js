/**
 * API Testing Utility
 * Use this file to test your FastAPI backend integration
 * 
 * Usage:
 * 1. Import in browser console or run in Node.js
 * 2. Or import in a React component for testing
 */

import { verifyKYC, fetchHistory, checkAPIStatus, testAPI } from './api';

/**
 * Example: Test API connection
 */
export const testConnection = async () => {
  console.log('🔍 Testing API Connection...');
  const isOnline = await checkAPIStatus();
  console.log(isOnline ? '✅ API is online' : '❌ API is offline');
  return isOnline;
};

/**
 * Example: Test KYC Verification
 */
export const testVerification = async () => {
  console.log('🧪 Testing KYC Verification...');
  
  const testData = {
    name: 'John Doe',
    documentNumber: '123456789012',
    address: '123 Main Street, City, State 12345',
    documentType: 'AADHAR'
  };

  console.log('📤 Sending data:', testData);
  
  const result = await verifyKYC(testData);
  
  if (result.success) {
    console.log('✅ Verification Successful!');
    console.log('📊 Results:', {
      status: result.data.status,
      fraudProbability: result.data.fraudProbability,
      riskLevel: result.data.riskLevel,
      confidence: result.data.confidence,
      details: result.data.details
    });
    return result.data;
  } else {
    console.error('❌ Verification Failed:', result.error);
    return null;
  }
};

/**
 * Example: Test History Fetch
 */
export const testHistory = async () => {
  console.log('📜 Testing History Fetch...');
  const history = await fetchHistory();
  console.log(`✅ Fetched ${history.length} records`);
  console.log('📋 History:', history);
  return history;
};

/**
 * Run all tests
 */
export const runAllTests = async () => {
  console.log('🚀 Running All API Tests...\n');
  
  // Test 1: Connection
  await testConnection();
  console.log('');
  
  // Test 2: Verification
  await testVerification();
  console.log('');
  
  // Test 3: History
  await testHistory();
  console.log('');
  
  console.log('✨ All tests completed!');
};

// Browser console usage:
// import { runAllTests } from './test-api';
// runAllTests();

export default {
  testConnection,
  testVerification,
  testHistory,
  runAllTests,
  testAPI, // From api.js
};

