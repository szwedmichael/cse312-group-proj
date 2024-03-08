import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/Login.css'
import '../api.js'
import api from '../api.js'

export default function Login() {

    //Necessary for messages relating to sign up, i.e. account already created
    const [signUpErrorMsg, setSignUpErrorMsg] = useState("")

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [rememberMe, setRememberMe] = useState(false);

    const submit = async (event) => {
        event.preventDefault()
        if (username === "" || password === "") {
            return
        }

        const data = {
            username: username,
            password: password,
            rememberMe: rememberMe
        }

        try {
            await fetch(api.post('/login'), { // url of the Fast API
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            }).then((response) => {
                if (response.status === 200) { //ok
                    window.location.href = response.url
    
                } else { //not ok whatsoever :(
                    setSignUpErrorMsg(response.statusText)
                }
            })
        } catch(e) {
            console.error(e)
        }
    }

    return(
        <div class="text-center">
            <h1>
                Login
            </h1>
            <form name="login" action="" onsubmit="" method="post" class="">
                <div>
                    <input type="username" id="username" placeholder="Email" onChange={(event) => {
                        setUsername(event.target.value)
                    }} required class=""/>
                </div>
                <div>
                    <input type="password" id="password" placeholder="Password" onChange={(event) => {
                        setPassword(event.target.value)
                    }} required class=""/>
                </div>
                <div>
                    <input type="checkbox" id="rememberMe" name="rememberMe" onClick={() => {
                        setRememberMe(!rememberMe)
                    }}/>
                    <label for="rememberMe">
                        Remember Me
                    </label>
                </div>
                <div class="mb-2 text-danger">
                    {signUpErrorMsg}
                </div>
                <div>
                    <button class="submit w-full" onClick={submit}>
                        Login
                    </button>
                </div>
            </form>
        </div>
    );
    } 