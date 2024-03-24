import { useState, useEffect } from 'react';
import '../styles/Homepage.css'
import vacationImage from '../images/red-m&m.png';
import api from '../api';

/*
checks if user is logged in
renders login or signup if not
renders homepage where posts are if they are
*/
function Homepage() {

  // sends get request to verify-auth to check if user is logged in
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await api.get('/verify-auth', { withCredentials: true });
        if (response.data.isAuthenticated) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Error verifying authentication:', error);
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  // renders based on requests reponse bool (yes or no)
  return (
    <div className="home-entirepage">
      {isAuthenticated ? (<HomepageLogged />) : (
      
      <>
        <div className="home-header">
          <h1>Vacation Hub</h1>
          <img src={vacationImage} alt="Vacation Scene" className="home-image" />
        </div>
        <div className="home-login">
          <form>
            <a href="http://127.0.0.1:8000/login" className="login-button">Login</a>
          </form>
        </div>
        <div className="home-signup">
          <form>
            <a href="http://127.0.0.1:8000/signup" className="signup-button">Sign up</a>
          </form>
        </div>
      </>

      )}

    </div>
  );
}

export default Homepage;
