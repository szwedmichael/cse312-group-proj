import { useState, useEffect } from "react";
import api from "../api.js";
import "../styles/HomepageLogged.css";
import likeButton from "../images/like-button.png";
import unlikeButton from "../images/unlike-button.png";

/*
This is the homepage for a logged in user
It is located at /home

DONE:
- get request for username
- get request for posts
- logout
- like or unlike post
- post request for posts
- images for posts
*/
function CountdownTimer({ initialTimeRemaining }) {
  // State to keep track of the current time remaining
  const [timeRemaining, setTimeRemaining] = useState(initialTimeRemaining);

  useEffect(() => {
    // Set up a timer that decrements the time remaining every second
    const timer = setInterval(() => {
      setTimeRemaining((prevTime) => prevTime > 0 ? prevTime - 1 : 0);
    }, 1000);

    // Clean up the interval on component unmount
    return () => clearInterval(timer);
  }, []);

  // Convert seconds into a readable format
  const formatTime = (seconds) => {
    return seconds;
  };

  return (
    <div>
      <h1>Latest Scheduled Post Timer</h1>
      <p>Seconds Remaining: {formatTime(timeRemaining)}</p>
    </div>
  );
}

function HomepageLogged() {
  const [userName, setUserName] = useState("");

  // some mock posts
  const [posts, setPosts] = useState([
    // { id: 1, username: "yolo12", content: { location: 'Buffalo, NY', description: 'I love it here!!!!', date: '03/2024' }, likes: 12 },
    // { id: 2, username: "ohboy", content: { location: 'New York, NY', description: 'Boston is better ;)', date: '03/2024' }, likes: 20 },
    // { id: 3, username: "sofun", content: { location: 'Los Angeles, Califona', description: 'YOYOYOYOYOYOYOYOYOYOYOYOYOYO\nYOYOYOYOYOYOYOYOYOYOYOYOYOYO\nYOYOYOYOYOYOYOYOYOYOYOYOYOYO\nYOYOYOYOYOYOYOYOYOYOYOYOYOYO\nYOYOYOYOYOYOYOYOYOYOYOYOYOYO\n', date: '03/2024' }, likes: 5 },
  ]);
  
  // new post
  const [newPost, setNewPost] = useState({
    location: "",
    description: "",
    date: "",
    day: '',      // New field for day
    month: '',    // New field for month
    year: '',     // New field for year
    hour: '',     // Existing field for hour
    minute: '',   // Existing field for minute
    file: null
  });

  // get request for posts
  const fetchPosts = async () => {
    try {
      const response = await api.get("/all-posts", { withCredentials: true });
      if (response.status === 200) {
        setPosts(response.data);
      }
    } catch (error) {
      console.error("Error fetching posts:", error);
    }
  };
  // get random posts
  const fetchRandomPosts = async () => {
    try {
      const response = await api.get("/random-posts", { withCredentials: true });
      if (response.status === 200) {
        setPosts(response.data);
      }
    } catch (error) {
      console.error("Error fetching random posts:", error);
    }
  };
  // get request for username
  const fetchUserDetails = async () => {
    try {
      const response = await api.get("/user-details", {
        withCredentials: true,
      });
      if (response.data.username) {
        setUserName(response.data.username);
      }
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  };

  useEffect(() => {
    fetchUserDetails();
    fetchPosts();
  }, []);

  // state for websockets
  const [ws, setWs] = useState(null); 
  // useEffect to connect to websocket
  useEffect(() => {
    let websocket;
    // start a websocket and handle incoming messages
    const connectWebSocket = () => {
      // main
      websocket = new WebSocket(`wss://vacationhub.live/ws-posts`);
      // testing
      // websocket = new WebSocket(`ws://localhost:8080/ws-posts`);
      websocket.onopen = () => {
        console.log("WebSocket Connected");
        setWs(websocket); // Update the WebSocket reference
      };
      // handle incoming messages
      websocket.onmessage = (event) => {
        console.log('Received message:', event.data);
        const message = JSON.parse(event.data);
        // if the server sends the complete post object
        if (message.post_id && (message.likes !== undefined) && (message.like_status !== undefined)) {
          // ipdate the likes for the post
          updatePostLikes(message.post_id, message.likes, message.like_status);
        } else {
          console.error('Invalid message format', message);
        }
      };
      websocket.onerror = (error) => {
        console.log("WebSocket Error:", error);
      };
      // handle disconnecting, reconnets after 3 seconds (can get rid of)
      websocket.onclose = (event) => {
        console.log("WebSocket Disconnected", event);
        if (!event.wasClean) {
          console.log(`WebSocket reconnecting...`);
          setTimeout(connectWebSocket, 3000); // Reconnect after 3 seconds
        }
      };
    };
    // init connection
    connectWebSocket();
    return () => {
      if (websocket) {
        websocket.close(1000, 'Component unmounting');
      }
    };
  }, []);
  
  // updates likes for a post 
  const updatePostLikes = (postId, likes, likeStatus) => {
    console.log(`Updating likes for post ${postId}: likes = ${likes}, likedByUser = ${likeStatus}`);
    // update the post state
    setPosts(currentPosts => 
      currentPosts.map(post => {
        if (post.id === postId) {
          console.log(`Found post ${postId}, updating...`);
          return { ...post, likes, likedByUser: likeStatus };
        }
        return post;
      })
    );
  };

  // Like or unlike post using WebSocket
  const likePost = (postId) => {
    // find if post exists
    const post = posts.find(p => p.id === postId);
    if (!post) return;
    console.log('Post likedByUser:', post.likedByUser);
    // change action depending on likedByUser
    const action = "like";
    // send message to server
    const message = { action, post_id: postId };
    console.log('Sending message:', message);
    ws.send(JSON.stringify(message));
  };

  // Like or unlike post using WebSocket
  const unlikePost = (postId) => {
    // find if post exists
    const post = posts.find(p => p.id === postId);
    if (!post) return;
    console.log('Post likedByUser:', post.likedByUser);
    // change action depending on likedByUser
    const action = "unlike";
    // send message to server
    const message = { action, post_id: postId };
    console.log('Sending message:', message);
    ws.send(JSON.stringify(message));
  };
  
  // logout
  const logout = async (event) => {
    event.preventDefault();
    try {
      await api.post("/logout", { withCredentials: true });
      window.location.href = "/";
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  const [showForm, setShowForm] = useState(false); // State to toggle form visibility

  // resets values after pressing post button
  const postReset = (event) => {
    const { name, value, files } = event.target;
    if (name === "file") {
      setNewPost({ ...newPost, file: files[0] });
    } else {
      setNewPost({ ...newPost, [name]: value });
    }
  };
  let timeRemaining = "0";
  // post request for posts
  const handlePost = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("location", newPost.location);
    formData.append("description", newPost.description);
    formData.append("date", newPost.date);
    formData.append("day", newPost.day);
    formData.append("month", newPost.month);
    formData.append("year", newPost.year);
    formData.append("hour", newPost.hour);
    formData.append("minute", newPost.minute);
    if (newPost.file) {
      formData.append("file", newPost.file);
    }
    // send post request
    try {
      const response = await api.post("/add-post", formData, {
        withCredentials: true,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      const createdPost = response.data;
      setPosts([createdPost, ...posts]);
      setNewPost({ location: "", description: "", date: "", file: null });
      setShowForm(false);
      fetchPosts();
      timeRemaining = createdPost.content.time_remaining;
    } catch (error) {
      console.error("Error creating post:", error);
    }
  };

  // parse timer
  const parseTimeRemaining = (timeStr) => {
    const seconds = Number(timeStr);
    return seconds;
  };

  const timeFromBackend = timeRemaining;
  // const timeFromBackend = "10000"; // Example time received from the backend
  const initialTimeRemaining = parseTimeRemaining(timeFromBackend);

  // posts format { id: 1, username: "yolo12", content: { location: 'Buffalo, NY', description: 'I love it here!!!!', date: '03/2024' }, likes: 12 },
  return (
    <>
    <div>
      {timeFromBackend !== "0" && <CountdownTimer initialTimeRemaining={initialTimeRemaining}  />}
    </div>
    <div className="home-entirepage">
      <h1 className="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">Welcome, {userName}!</h1>
      <div className="homepage-logout">
        <button className='btn mb-2' onClick={logout}>Logout</button>
      </div>
      <div className="homepage-new-post">
        <button className="btn mb-4" onClick={() => setShowForm(!showForm)}>Create New Post</button>
        {showForm && (
          <div className="max-w-lg lg:ms-auto mx-auto text-center ">
            <div className="py-16 px-7 rounded-md bg-white">           
              <form onSubmit={handlePost}>
                  <div className="grid md:grid-cols-2 grid-cols-1 gap-6">
                    <div>
                      <label htmlFor="subject" className="float-left block  font-normal text-gray-400 text-lg">Location</label>
                      <input type="text" maxLength="20" name="location" placeholder="Location" value={newPost.location} onChange={postReset} className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700 "></input>  
                    </div>
                    <div>
                      <label htmlFor="subject" className="float-left block  font-normal text-gray-400 text-lg">Date</label>
                      <input type="text" maxLength="7" name="date" placeholder="MM/YYYY"  value={newPost.date} onChange={postReset} className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700"></input>                                                                          
                    </div>
                    <div className="md:col-span-2">
                      <label htmlFor="subject" className="float-left block  font-normal text-gray-400 text-lg">Upload an image &#128513;</label>
                      <input type="file" id="file" name="file" placeholder="Upload an image" accept=".jpg, .png" onChange={postReset} className="peer block w-full appearance-none border-none   bg-transparent py-2.5 px-0 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0"></input>
                    </div>
                    <div className="md:col-span-2">
                      <textarea name="description" maxLength="150" value={newPost.description} onChange={postReset} placeholder="Post description" className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700" rows="5" cols="" ></textarea>
                    </div>
                    <div>
                      <label htmlFor="day" className="float-left block font-normal text-gray-400 text-lg">Day</label>
                      <input type="number" name="day" placeholder="Day (1-31)" min="1" max="31" value={newPost.day} onChange={postReset} className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700" />
                    </div>
                    <div>
                      <label htmlFor="month" className="float-left block font-normal text-gray-400 text-lg">Month</label>
                      <input type="number" name="month" placeholder="Month (1-12)" min="1" max="12" value={newPost.month} onChange={postReset} className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700" />
                    </div>
                    <div>
                      <label htmlFor="year" className="float-left block font-normal text-gray-400 text-lg">Year</label>
                      <input type="number" name="year" placeholder="Year (e.g., 2024)" value={newPost.year} onChange={postReset} className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700" />
                    </div>
                    <div>
                      <label htmlFor="hour" className="float-left block font-normal text-gray-400 text-lg">Hour</label>
                      <input type="number" name="hour" placeholder="Hour (0-23)" min="0" max="23" value={newPost.hour} onChange={postReset} className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700" />
                    </div>
                    <div>
                      <label htmlFor="minute" className="float-left block font-normal text-gray-400 text-lg">Minute</label>
                      <input type="number" name="minute" placeholder="Minute (0-59)" min="0" max="59" value={newPost.minute} onChange={postReset} className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700" />
                    </div>
                    <div className="md:col-span-2">
                      <button className="py-3 text-base font-medium rounded text-white bg-blue-800 w-full hover:bg-blue-700 transition duration-300">Post</button>
                    </div>
                  </div>
              </form>
            </div>
          </div>
        )}
      </div>
      <div className="homepage-random-posts">
        <button className="btn mb-4" onClick={fetchRandomPosts}>Randomize Posts</button>
      </div>
      <h1 className="mb-4 text-4xl leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">Posts</h1>
      <div className="homepage-all-posts">
        <ul>
          {posts.map((post) => (
            <li key={post.id} className="mb-10">
              <div className="card w-96 bg-base-100 shadow-xl">
                {post.file && (
                 <figure>
                  <img src={post.file} alt="Shoes" />
                 </figure> 
                )}
                <div className="card-body">
                  <h2 className="card-title">
                    {post.username}
                  </h2>
                  <p>{post.content.description}</p>
                  <div className="card-actions justify-end">
                    <div className="like-section">
                      <img
                        src={unlikeButton}
                        alt="Unlike"
                        onClick={() => unlikePost(post.id)}
                      />
                      <img
                        src={likeButton}
                        alt="Like"
                        onClick={() => likePost(post.id)}
                      />
                      <span className="like-count">{post.likes}</span>
                    </div>
                    <div className="badge badge-outline">{post.content.location}</div> 
                    <div className="badge badge-outline">{post.content.date}</div>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
    </>
  );
  }

export default HomepageLogged;





