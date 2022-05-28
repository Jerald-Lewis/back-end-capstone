import React, { Component } from 'react';
import { withRouter } from "react-router";
import { NavLink } from 'react-router-dom';
import moment from 'moment';
import logo from '../../../images/Altice-horz-logo.png';


export default class NavigationComponent extends Component {
    constructor() {
        super();
    }
    render() {
    return (
        <div className='nav-wrapper'>
            <div className='left-side'>
                <div className='logo-wrapper'>
                <a href='https://www.alticeusa.com/' target='blank'>
                    <img className="logo" src={logo} alt="logo"/>
                </a>
                <div className='date'>
                {moment().format('MMMM Do YYYY')}
                </div>
                </div>
                <div className='nav-link-container'>
                <div className='nav-link-wrapper'>
                    <NavLink exact to="/" activeClassName='nav-link-active' className={'nav-link'}>
                        Home
                    </NavLink>
                </div>

                <div className='nav-link-wrapper'>
                    <NavLink to="/about" activeClassName='nav-link-active' className={'nav-link'}>
                        About
                    </NavLink>
                </div>

                <div className='nav-link-wrapper'>
                    <NavLink to="/knowledge" activeClassName='nav-link-active' className={'nav-link'}>
                        Knowledge Base
                    </NavLink>
                </div>

                <div className='nav-link-wrapper'>
                    <NavLink to='/inventory' activeClassName='nav-link-active' className={'nav-link'}>
                        Inventory
                    </NavLink>
                </div>
                </div>
            </div>

            <div className='right-side'>
                <div className='welcome-message'>
                Welcome user's firName lasName
                </div>
            </div>
        </div>
    )
}
}