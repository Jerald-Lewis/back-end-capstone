import React, { Component } from 'react';
import axios from 'axios';

export default class Login extends Component {
    constructor(props) {
        super(props);

        this.state = {
            email: "",
            password: "",
            errorText: ""
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value,
            errorText: ""
        })
    }

    handleSubmit(event) {
        axios.post('http://127.0.0.1:5000/user/verify',
        {
            body: {
                email: this.state.email,
                password: this.state.password
            }
        },
        { withCredentials: true }
        ).then(response => {
            if (response.data === 'User has been verified!'){
                console.log("You can log in")
                this.props.handleSuccessfulAuth();
            } else {
                this.setState({
                    errorText: "Email or password is wrong!"
                })
            }
        }).catch(error => {
            this.setState({
                errorText: "An error occurred!"
            })
        });
        
        event.preventDefault();
    }
    render() {
    return (
        <div>
            <h1>Login to access the knowledge base and your inventory.</h1>

            <div>{this.state.errorText}</div>

            <form onSubmit={this.handleSubmit}>
                <input 
                    type='email'
                    name="email"
                    placeholder='Type your email'
                    value={this.state.email}
                    onChange={this.handleChange}
                />
                <input 
                    type='password'
                    name="password"
                    placeholder='Type your password'
                    value={this.state.password}
                    onChange={this.handleChange}
                />

                <div>
                    <button type='submit'>Login</button>
                </div>
            </form>
        </div>
        )
    }
}