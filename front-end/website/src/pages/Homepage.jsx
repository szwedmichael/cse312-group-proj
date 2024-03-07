import { useState } from 'react'
import '../styles/Homepage.css'

// change hrefs to correct url

function Homepage() {

  return (
    <>
      <div className="home-entirepage">
        <div className="home-header">
          <h1>Vacation Hub</h1>
        </div>
        <div className= "home-login">
          <form >
            <a href="http://localhost:5173/login" className="login-button">Login</a>  
          </form>
        </div>
        <div className= "home-signup">
          <form>
            <a href="http://localhost:5173/signup" className="signup-button">Sign up</a>
          </form>
        </div>
      </div>
    </>
  )
}

export default Homepage
