// Test script to debug API calls
// This script can help verify if the backend API is accessible and working correctly

async function testBackendAPI() {
  console.log('Testing backend API connectivity...');
  
  try {
    // Test the health endpoint first
    const healthResponse = await fetch('http://localhost:8000/health');
    console.log('Health check response:', await healthResponse.text());
    
    // Test the root endpoint
    const rootResponse = await fetch('http://localhost:8000/');
    console.log('Root endpoint response:', await rootResponse.text());
  } catch (error) {
    console.error('Error testing backend API:', error);
  }
}

// Run the test
testBackendAPI();