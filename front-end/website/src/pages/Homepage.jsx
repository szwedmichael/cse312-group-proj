import { useState } from 'react'
import '../styles/Homepage.css'

function Homepage() {

  return (
    <>
      <div className="home-entirepage">
        <div className="home-header">
          <h1>Trips</h1>
        </div>
        <div className= "home-login">
          <form>
            <button type="submit">Login</button>
          </form>
        </div>
        <div className= "home-signup">
          <form>
            <button type="submit">Signup</button>
          </form>
        </div>
      </div>
    </>
  )
}

export default Homepage
