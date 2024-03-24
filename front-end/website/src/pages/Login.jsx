import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";
import "../api.js";
import api from "../api.js";

export default function Login() {
  //Necessary for messages relating to sign up, i.e. account already created
  const [signUpErrorMsg, setSignUpErrorMsg] = useState("");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    if (username === "" || password === "") {
      return;
    }

    const data = {
      username: username,
      password: password,
    };

    try {
      await api.post("/login", data).then((response) => {
        // TODO: This doesnt work on response but I got the post working
        if (response.status === 200) {
          //ok
          window.location.href = response.url;
        } else {
          //not ok whatsoever :(
          setSignUpErrorMsg(response.statusText);
        }
      });
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div class="text-center">
      <h1>Login</h1>
      <form name="login" action="" onsubmit="" method="post" class="">
        <div>
          <input
            type="username"
            id="username"
            placeholder="Username"
            onChange={(event) => {
              setUsername(event.target.value);
            }}
            required
            class=""
          />
        </div>
        <div>
          <input
            type="password"
            id="password"
            placeholder="Password"
            onChange={(event) => {
              setPassword(event.target.value);
            }}
            required
            class=""
          />
        </div>
        <div class="mb-2 text-danger">{signUpErrorMsg}</div>
        <div>
          <button class="submit w-full" onClick={submit}>
            Login
          </button>
        </div>
      </form>
    </div>
  );
}
