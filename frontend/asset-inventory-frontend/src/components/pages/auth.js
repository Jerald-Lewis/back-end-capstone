import React, { Component } from 'react';
import Login from '../auth/login.js';
import loginImage from '../../../images/login.png';

export default class Auth extends Component {
    render() {
    return (
        <div className='auth-page-wrapper'>
            <div
             className='left-column'
             style={{
                 backgroundImage: `url(${loginImage})`
             }}   
            />

            <div className='right-column'>
                <Login />
            </div>
        </div>
        )
    }
}