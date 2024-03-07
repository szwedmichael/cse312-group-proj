import React from 'react'
import ReactDOM from 'react-dom/client'
import Homepage from './pages/Homepage.jsx'
import Login from './pages/Login.jsx'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './styles/index.css'




ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route exact path="/" Component={Homepage} />
        <Route exact path="/login" Component={Login} />
      </Routes>
    </Router>
  </React.StrictMode>,
)
