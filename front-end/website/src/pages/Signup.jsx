import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/Signup.css'
import api from '../api.js'

export default function Signup() {

    //Necessary for messages relating to sign up, i.e. account already created
    const [signUpErrorMsg, setSignUpErrorMsg] = useState("")

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");

    const submit = async (event) => {
        event.preventDefault()
        if (username === "" || password === "") {
            return
        }

        const data = {
            username: username,
            password: password,
            password2: password2,
        }

        try {
            await fetch(api.post('/signup'), { // url of the Fast API
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
                Sign up
            </h1>
            <form name="login" action="" onsubmit="" method="post" class="">
                <div>
                    <input type="username" id="username" placeholder="Username" onChange={(event) => {
                        setUsername(event.target.value)
                    }} required class=""/>
                </div>
                <div>
                    <input type="password" id="password" placeholder="Password" onChange={(event) => {
                        setPassword(event.target.value)
                    }} required class=""/>
                </div>
                <div>
                    <input type="password2" id="password2" placeholder="Confirm Password" onChange={(event) => {
                        setPassword2(event.target.value)
                    }} required class=""/>
                </div>
                <div class="mb-2 text-danger">
                    {signUpErrorMsg}
                </div>
                <div>
                    <button class="submit w-full" onClick={submit}>
                        Sign up
                    </button>
                </div>
            </form>
        </div>
    );
    } 