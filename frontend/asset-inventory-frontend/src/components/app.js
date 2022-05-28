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
  render() {
    return (
      <div className='app'>
        <Router>
          <div>
            <NavigationContainer />

            <Switch>
              <Route exact path='/' component={Home} />
              <Route path='/auth' component={Auth} />
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
