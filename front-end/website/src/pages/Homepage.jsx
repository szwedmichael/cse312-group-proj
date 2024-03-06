import { useState } from 'react'
import '../styles/Homepage.css'

function Homepage() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="home-header">
        <h1>Trips</h1>
      </div>
    </>
  )
}

export default Homepage
