import React, { Component } from 'react';
import { 
  BrowserRouter as Router, 
  Switch, 
  Route } from "react-router-dom";
import axios from 'axios';
import NavigationContainer from './navigation/navigation-container';
import Home from './pages/home';
import About from './pages/about';
import Knowledge from './pages/knowledge';
import Inventory from './pages/inventory';
import Auth from './pages/auth';
import SignUp from './pages/signup';
import NoMatch from './pages/no-match';

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loggedInStatus: "NOT_LOGGED_IN"
    };

    this.handleSuccessfulLogin=this.handleSuccessfulLogin.bind(this);
    this.handleUnsuccessfulLogin=this.handleUnsuccessfulLogin.bind(this);

  }

  handleSuccessfulLogin() {
    this.setState({
      loggedInStatus: "LOGGED_IN"
    })
  }

  handleUnsuccessfulLogin() {
    this.setState({
      loggedInStatus: "NOT_LOGGED_IN"
    })
  }

  render() {
    return (
      <div className='app'>
        <Router>
          <div>
            <NavigationContainer />
            
            <h4>{this.state.loggedInStatus}</h4>
            <Switch>
              <Route exact path='/' component={Home} />
              <Route path='/auth'
                     render={props => (
                      <Auth
                        {...props}
                        handleSuccessfulLogin={this.handleSuccessfulLogin}
                        handleUnsuccessfulLogin={this.handleUnsuccessfulLogin}
                      />
                     )}              
              />
              <Route path='/about' component={About} />
              <Route path='/knowledge' component={Knowledge} />
              <Route path='/inventory' component={Inventory} />
              <Route path='/signup' component={SignUp} />
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}
