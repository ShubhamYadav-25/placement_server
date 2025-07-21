import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { auth } from "../firebase-config";
// Remove firebase imports completely
import axios from 'axios'; // optional, you can also use fetch
import "../custom.css";

// Add keyframe animation for spinner
const spinnerStyle = document.createElement('style');
spinnerStyle.innerHTML = `
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
`;
document.head.appendChild(spinnerStyle);

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userType, setUserType] = useState("student");
  const [isSignUp, setIsSignUp] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // handleSubmit function is defined below


  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");
  setIsLoading(true);

  try {
    if (isSignUp) {
      const res = await fetch("http://localhost:5000/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: email.split('@')[0], email, password, role: userType }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.message || "Signup failed");
      alert("Signup successful! Please log in.");
      setIsSignUp(false);
    } else {
      const res = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, role: userType }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.message || "Login failed");
      localStorage.setItem("token", data.token || "dummy_token");
      alert("Login successful");

      // Redirect
      navigate("/student-dashboard");
    }
  } catch (error) {
    setError(error.message);
  } finally {
    setIsLoading(false);
  }
};


  useEffect(() => {
    // Add a class to the body to ensure full-page styling
    document.body.classList.add('login-page');
    return () => {
      document.body.classList.remove('login-page');
    };
  }, []);