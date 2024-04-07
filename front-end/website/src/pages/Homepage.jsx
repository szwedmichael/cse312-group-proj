import { useState, useEffect } from "react";
import "../styles/Homepage.css";
import vacationImage from "../images/red-m&m.png";
import api from "../api";
import HomepageLogged from './HomepageLogged.jsx'

/*
checks if user is logged in
renders login or signup if not
renders homepage where posts are if they are
*/
function Homepage() {
  // sends get request to verify-auth to check if user is logged in
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true); // Add a loading state

  useEffect(() => {
    const checkAuth = async () => {
      setIsLoading(true); // Set loading to true before making the request
      try {
        const response = await api.get("/verify-auth", {
          withCredentials: true,
        });
        if (response.data.isAuthenticated) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error("Error verifying authentication:", error);
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false); // Set loading to false after the request is complete
      }
    };

    checkAuth();
  }, []);

  if (isLoading) {

    return (<div class="loader-container">
              <span className="loading loading-spinner loading-lg"></span>
            </div>)

  }

  // renders based on requests reponse bool (yes or no)
  return (
    <div className="home-entirepage">
      {isAuthenticated ? (
        <HomepageLogged />
      ) : (
        <>
          <div className="home-title">
            <h1 className="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-7xl lg:text-6xl dark:text-white">Vacation Hub</h1>
          </div>
          <div className="home-image">
            <img
              src={vacationImage}
              alt="Vacation Scene"
              className="home-image"
            />
          </div>
          <div className="home-login">
            <form>
              <a href={`${api.defaults.baseURL}/login`} className="login-button">
                Login
              </a>
            </form>
          </div>
          <div className="home-signup">
            <form>
              <a href={`${api.defaults.baseURL}/signup`} className="signup-button">
                Sign up
              </a>
            </form>
          </div>
        </>
      )}
    </div>
  );
}

export default Homepage;
