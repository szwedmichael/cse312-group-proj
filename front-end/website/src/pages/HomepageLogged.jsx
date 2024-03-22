import { useState, useEffect } from 'react';
import api from '../api.js';

function HomepageLogged() {

    const [userName, setUserName] = useState('');
    const [posts, setPosts] = useState([]);

    useEffect(() => {

        // get request for username
        const fetchUserDetails = async () => {
          try {
            const response = await api.get('/user-details', { withCredentials: true });
            if (response.data.username) {
              setUserName(response.data.username);
            }
          } catch (error) {
            console.error('Error fetching user details:', error);
          }
        };

        // get request for posts
        const fetchPosts = async () => {
          try {
            const response = await api.get('/all-posts', { withCredentials: true });
            if (response.data.posts) {
              setPosts(response.data.posts);
            }
          } catch (error) {
            console.error('Error fetching posts:', error);
          }
        };

        fetchUserDetails();
        fetchPosts();
        }, []);

    // posts {"location": "Buffalo, NY", "description": "I went to Niagara Falls and it was awesome", "date": MM/YYYY, "xsrf":xsrf}
    return (
        <>
        <div className='homepage-welcome'>
            <h1>Welcome, {userName}!</h1>
        </div>
        <div className='homepage-posts'>
            <h2>Posts</h2>
            <ul>
                {posts.map((post) => (
                    <li key={post.id}>
                        <h3>{post.location}</h3>
                        <p>{post.description0}</p>
                    </li>
                ))}
            </ul>
        </div>
        </>

    );
}

export default HomepageLogged;