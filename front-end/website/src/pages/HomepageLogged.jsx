import { useState, useEffect } from 'react';
import api from '../api.js';
import '../styles/HomepageLogged.css'
import likeButton from '../images/like-button.png';

/*
This is the homepage for a logged in user
It is located at /home

DONE:
- get request for username
- get request for posts
- logout
- like or unlike post

NOT DONE:
- post request for posts (creating posts)
*/
function HomepageLogged() {

    const [userName, setUserName] = useState('');
    // some mock posts
    const [posts, setPosts] = useState([
        { id: 1, username: "yolo12", location: 'Buffalo, NY', description: 'i love it here !!!!', date: '03/2024', likes: 12},
        { id: 2, username: "ohboy", location: 'New York, NY', description: 'Boston is better ;)', date: '03/2024', likes: 20 },
        { id: 3, username: "sofun", location: 'Los Angeles, CA', description: 'What happend to this place', date: '03/2024', likes: 5 },
    ]);

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

    // logout 
    const logout = async (event) => {
        event.preventDefault();
        try {
            await api.post('/logout', { withCredentials: true });
            window.location.href = '/';
        } catch (error) {
            console.error('Error logging out:', error);
        }
    }

    // like or unlike post
    const likePost = async (postId) => {
        const data = {
            post_id: postId,
        }
        const updatedPosts = posts.map(post => {
            if (post.id === postId) {
                // updates on frontend
                const likedByUser = !post.likedByUser;
                const likes = likedByUser ? post.likes + 1 : post.likes - 1;
                return { ...post, likedByUser, likes };
            }
            return post;
        });
        setPosts(updatedPosts);

        // change request whether like or unlike
        const endpoint = updatedPosts.find(post => post.id === postId).likedByUser ? '/like-post' : '/unlike-post';

        // send that post request (like-post or unlike-post)
        try {
            await api.post(endpoint, data);
        } catch (error) {
            console.error('Error updating like:', error);
        }
    };

    // posts {"location": "Buffalo, NY", "description": "I went to Niagara Falls and it was awesome", "date": MM/YYYY, "xsrf":xsrf}
    return (
        <>
        <div className='homepage-welcome'>
            <h1>Welcome, {userName}!</h1>
        </div>
        <div className='homepage-logout'>
            <button onClick={logout}>Logout</button>
        </div>
        <div className='homepage-all-posts'>
            <h1>Posts</h1>
            <ul>
                {posts.map((post) => (
                    <li key={post.id} className='post'>
                        <h2>{post.username}</h2>
                        <h4>{post.location}</h4>
                        <p>{post.description}</p>
                        <div className='post-date'>{post.date}</div>
                        <div className='like-section'>
                            <img src={likeButton} alt="Like" onClick={(event) => likePost(post.id, event)}/>
                            <span className='like-count'>{post.likes}</span>
                        </div>
                    </li>

                ))}
            </ul>
        </div>
        </>

    );
}

export default HomepageLogged;