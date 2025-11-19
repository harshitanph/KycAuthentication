// /**
//  * API Service for KYC Verification
//  * Handles all communication with FastAPI backend
//  */

// // Normalize API URL (remove trailing slash if exists)
// const BASE = import.meta.env.VITE_API_URL?.replace(/\/+$/, '') || "http://127.0.0.1:8000";
// const API_BASE_URL = BASE;

// /**
//  * Verify KYC data with fraud detection model
//  */
// export const verifyKYC = async (data) => {
//   try {
//     const response = await fetch(`${API_BASE_URL}/api/verify-kyc`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({
//         name: data.name,
//         documentNumber: data.documentNumber,
//         address: data.address || "",
//         documentType: data.documentType,
//       }),
//     });

//     if (!response.ok) {
//       const errorData = await response.json().catch(() => ({
//         message: `HTTP error! status: ${response.status}`,
//       }));
//       throw new Error(errorData.message || errorData.detail || "Verification failed");
//     }

//     const result = await response.json();
//     return { success: true, data: result };
//   } catch (error) {
//     console.error("KYC Verification Error:", error);
//     return {
//       success: false,
//       error: error.message || "Backend not reachable.",
//     };
//   }
// };

// /**
//  * Fetch verification history from backend
//  */
// export const fetchHistory = async () => {
//   try {
//     const response = await fetch(`${API_BASE_URL}/api/history`);

//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }

//     const data = await response.json();

//     return data
//       .map((item) => ({
//         id: `VER${Date.parse(item.Timestamp)}`,
//         timestamp: item.Timestamp,
//         name: item.Name,
//         documentNumber: item.Document_Number,
//         aadharNumber: item.Document_Number,
//         documentType: item.ID_Type,
//         fraudProbability: item.Fraud_Probability,
//         riskLevel: item.Fraud_Risk_Level,
//         status: item.Fraud_Risk_Level === "High" ? "Flagged" : "Verified",
//         confidence: item.Confidence,
//         details: {
//           documentAuthenticity: item.Fraud_Risk_Level === "High" ? "Suspicious" : "Valid",
//           addressVerification: "Verified",
//           anomalyScore: item.Fraud_Probability.toFixed(2),
//         },
//       }))
//       .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
//   } catch (error) {
//     console.error("History Fetch Error:", error);
//     return [];
//   }
// };

// /**
//  * CSV Batch KYC processing
//  */
// export const verifyKYCBatch = async (file) => {
//   try {
//     const formData = new FormData();
//     formData.append("file", file);

//     const response = await fetch(`${API_BASE_URL}/api/verify-kyc-batch`, {
//       method: "POST",
//       body: formData,
//     });

//     if (!response.ok) {
//       const errorData = await response.json().catch(() => ({
//         message: `HTTP error! status: ${response.status}`,
//       }));
//       throw new Error(errorData.detail || errorData.message || "Batch verification failed");
//     }

//     const result = await response.json();
//     return { success: true, data: result };
//   } catch (error) {
//     console.error("CSV Batch Error:", error);
//     return { success: false, error: error.message || "Backend not reachable." };
//   }
// };

// /**
//  * API health check
//  */
// export const checkAPIStatus = async () => {
//   try {
//     const response = await fetch(`${API_BASE_URL}/`, {
//       method: "GET",
//       headers: { "Content-Type": "application/json" },
//     });
//     return response.ok;
//   } catch (error) {
//     console.log("API Status Error → Backend Offline:", error);
//     return false;
//   }
// };

// /**
//  * Test API connection with a sample request
//  */
// export const testAPI = async () => {
//   console.log("Testing API connection...");

//   try {
//     const testData = {
//       name: "Test User",
//       documentNumber: "123456789012",
//       address: "123 Test Road",
//       documentType: "AADHAR",
//     };

//     const result = await verifyKYC(testData);
//     if (result.success) {
//       console.log("✅ API Test Successful:", result.data);
//       return result.data;
//     } else {
//       console.error("❌ API Test Failed:", result.error);
//       return null;
//     }
//   } catch (error) {
//     console.error("❌ API Test Error:", error);
//     return null;
//   }
// };

// export default {
//   verifyKYC,
//   verifyKYCBatch,
//   fetchHistory,
//   checkAPIStatus,
//   testAPI,
//   API_BASE_URL,
// };

/**
 * API Service for KYC Verification
 * Handles all communication with FastAPI backend
 */

// Normalize API URL (remove trailing slash if exists)
const BASE = import.meta.env.VITE_API_URL?.replace(/\/+$/, '') || "https://kyc-backend1-c6ba.onrender.com";
const API_BASE_URL = BASE;

/**
 * Verify KYC data with fraud detection model
 */
export const verifyKYC = async (data) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/verify-kyc`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: data.name,
        documentNumber: data.documentNumber,
        address: data.address || "",
        documentType: data.documentType,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        message: `HTTP error! status: ${response.status}`,
      }));
      throw new Error(errorData.message || errorData.detail || "Verification failed");
    }

    const result = await response.json();
    return { success: true, data: result };
  } catch (error) {
    console.error("KYC Verification Error:", error);
    return {
      success: false,
      error: error.message || "Backend not reachable.",
    };
  }
};

/**
 * Fetch verification history from backend
 */
export const fetchHistory = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/history`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    return data
      .map((item) => ({
        id: `VER${Date.parse(item.Timestamp)}`,
        timestamp: item.Timestamp,
        name: item.Name,
        documentNumber: item.Document_Number,
        aadharNumber: item.Document_Number,
        documentType: item.ID_Type,
        fraudProbability: item.Fraud_Probability,
        riskLevel: item.Fraud_Risk_Level,
        status: item.Fraud_Risk_Level === "High" ? "Flagged" : "Verified",
        confidence: item.Confidence,
        details: {
          documentAuthenticity: item.Fraud_Risk_Level === "High" ? "Suspicious" : "Valid",
          addressVerification: "Verified",
          anomalyScore: item.Fraud_Probability.toFixed(2),
        },
      }))
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  } catch (error) {
    console.error("History Fetch Error:", error);
    return [];
  }
};

/**
 * CSV Batch KYC processing - FIXED ENDPOINT
 */
export const verifyKYCBatch = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    // FIXED: Changed from /api/verify-kyc-batch to /api/batch-verify
    const response = await fetch(`${API_BASE_URL}/api/batch-verify`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        message: `HTTP error! status: ${response.status}`,
      }));
      throw new Error(errorData.detail || errorData.message || "Batch verification failed");
    }

    const result = await response.json();
    return { success: true, data: result };
  } catch (error) {
    console.error("CSV Batch Error:", error);
    return { success: false, error: error.message || "Backend not reachable." };
  }
};

/**
 * API health check
 */
export const checkAPIStatus = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    return response.ok;
  } catch (error) {
    console.log("API Status Error → Backend Offline:", error);
    return false;
  }
};

/**
 * Test API connection with a sample request
 */
export const testAPI = async () => {
  console.log("Testing API connection...");

  try {
    const testData = {
      name: "Test User",
      documentNumber: "123456789012",
      address: "123 Test Road",
      documentType: "AADHAR",
    };

    const result = await verifyKYC(testData);
    if (result.success) {
      console.log("✅ API Test Successful:", result.data);
      return result.data;
    } else {
      console.error("❌ API Test Failed:", result.error);
      return null;
    }
  } catch (error) {
    console.error("❌ API Test Error:", error);
    return null;
  }
};

export default {
  verifyKYC,
  verifyKYCBatch,
  fetchHistory,
  checkAPIStatus,
  testAPI,
  API_BASE_URL,
};