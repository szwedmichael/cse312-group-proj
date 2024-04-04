import { useState, useEffect } from "react";
import api from "../api.js";
import "../styles/HomepageLogged.css";
import likeButton from "../images/like-button.png";

/*
This is the homepage for a logged in user
It is located at /home

DONE:
- get request for username
- get request for posts
- logout
- like or unlike post

IN PROGRESS:
- post request for posts (creating posts)
- authentication tokens ($$$)
*/
function HomepageLogged() {
  const [userName, setUserName] = useState("");

  // some mock posts
  const [posts, setPosts] = useState([
    // { id: 1, username: "yolo12", content: { location: 'Buffalo, NY', description: 'I love it here!!!!', date: '03/2024' }, likes: 12 },
    // { id: 2, username: "ohboy", content: { location: 'New York, NY', description: 'Boston is better ;)', date: '03/2024' }, likes: 20 },
    // { id: 3, username: "sofun", content: { location: 'Los Angeles, CA', description: 'What happened to this place', date: '03/2024' }, likes: 5 },
  ]);
  

  // new post
  const [newPost, setNewPost] = useState({
    location: "",
    description: "",
    date: "",
  });

  useEffect(() => {
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

    fetchUserDetails();
    fetchPosts();
  }, []);

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

  // like or unlike post
  const likePost = async (postId) => {
    const data = {
      post_id: postId,
    };
    const updatedPosts = posts.map((post) => {
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
    const endpoint = updatedPosts.find((post) => post.id === postId).likedByUser
      ? "/like-post"
      : "/unlike-post";

    // send that post request (like-post or unlike-post)
    try {
      await api.post(endpoint, data);
    } catch (error) {
      console.error("Error updating like:", error);
    }
  };

  const [showForm, setShowForm] = useState(false); // State to toggle form visibility

  // resets values after pressing post button
  const postReset = (event) => {
    const { name, value } = event.target;
    setNewPost({ ...newPost, [name]: value });
  };

  const handlePost = async (event) => {
    event.preventDefault();
    const postData = {
      post: newPost,
    };
    try {
      const response = await api.post("/add-post", newPost, {
        withCredentials: true,
      });
      const createdPost = response.data;
      setPosts([createdPost, ...posts]);
      setNewPost({ location: "", description: "", date: "" });
      setShowForm(false); // Hide form after posting
    } catch (error) {
      console.error("Error creating post:", error);
    }
  };

  // posts format { id: 1, username: "yolo12", content: { location: 'Buffalo, NY', description: 'I love it here!!!!', date: '03/2024' }, likes: 12 },
  return (
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
                      <label for="subject" className="float-left block  font-normal text-gray-400 text-lg">Location</label>
                      <input type="text" name="location" placeholder="Location" value={newPost.location} onChange={postReset} className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700 "></input>  
                    </div>
                    <div>
                      <label for="subject" className="float-left block  font-normal text-gray-400 text-lg">Date</label>
                      <input type="text" name="date" placeholder="MM/YYYY"  value={newPost.date} onChange={postReset} className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700"></input>                                                                          
                    </div>
                    <div className="md:col-span-2">
                      <label for="subject" className="float-left block  font-normal text-gray-400 text-lg">Upload an image &#128513;</label>
                      {/* FILE UPLOAD TODO */}
                      <input type="file" id="file" name="file" placeholder="Upload an image" accept=".jpg, .png" className="peer block w-full appearance-none border-none   bg-transparent py-2.5 px-0 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0"></input>
                    </div>
                    <div className="md:col-span-2">
                      <textarea name="description" value={newPost.description} onChange={postReset} placeholder="Post description" className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-700" rows="5" cols="" ></textarea>
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
      <h1 className="mb-4 text-4xl leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">Posts</h1>
      <div className="homepage-all-posts">
        <ul>
          {posts.map((post) => (
            <li key={post.id} className="mb-10">
              <div className="card w-full max-w-screen-xl bg-base-100 shadow-xl ">
                {/* DISPLAY IMAGE TODO */}
                <figure><img src={post.file} alt="Shoes" /></figure> {/* placeholder image */}
                <div className="card-body">
                  <h2 className="card-title">
                    {post.username}
                  </h2>
                  <p>{post.content.description}</p>
                  <div className="card-actions justify-end">
                    <div className="like-section">
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
  );
}
export default HomepageLogged;

// old post form
// <form onSubmit={handlePost}>
// <label>
//   Location:
//   <input
//     type="text"
//     name="location"
//     value={newPost.location}
//     onChange={postReset}
//     placeholder="Enter your location here..."
//   />
// </label>
// <label>
//   Description:
//   <textarea
//     type="text"
//     name="description"
//     value={newPost.description}
//     onChange={postReset}
//     placeholder="Enter your description here..."
//   />
// </label>
// <label>
//   Date:
//   <input
//     type="text"
//     name="date"
//     value={newPost.date}
//     onChange={postReset}
//     placeholder="MM/YYYY"
//   />
// </label>
// <button className='btn' type="submit">Post</button>
// </form>

