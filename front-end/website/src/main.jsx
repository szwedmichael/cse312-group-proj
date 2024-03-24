// react stuff
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

// pages
import Homepage from './pages/Homepage.jsx'
import Login from './pages/Login.jsx'
import Signup from './pages/Signup.jsx'
import Mediapage from './pages/Mediapage.jsx'
import HomepageLogged from './pages/HomepageLogged.jsx'
// styles
import './styles/index.css'


// homepage logged in is located at /home for TESTING
// should be eveutually located at /
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route exact path="/" Component={Homepage} />
        <Route exact path="/login" Component={Login} />
        <Route exact path="/signup" Component={Signup} />
        <Route exact path="/mediapage" Component={Mediapage} />
        <Route exact path="/home" Component={HomepageLogged} /> 
      </Routes>
    </Router>
  </React.StrictMode>,
)
