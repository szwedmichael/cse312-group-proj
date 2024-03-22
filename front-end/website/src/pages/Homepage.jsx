import { useState } from 'react'
import '../styles/Homepage.css'
// import React from 'react';
import vacationImage from '../images/red-m&m.png';

function Homepage() {

  return (
    <div className="home-entirepage">
      <div className="home-header">
        <h1>Vacation Hub</h1>
        <img src={vacationImage} alt="Vacation Scene" className="home-image" />
      </div>
      <div className="home-login">
        <form>
          <a href="http://localhost:5173/login" className="login-button">Login</a>
        </form>
      </div>
      <div className="home-signup">
        <form>
          <a href="http://localhost:5173/signup" className="signup-button">Sign up</a>
        </form>
      </div>
    </div>
  );
}

export default Homepage;
