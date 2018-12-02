import React, { Component } from 'react';
import './app.css';
import ReactImage from './react.png';
import Typography from '@material-ui/core/Typography';

export default class App extends Component {
  state = { username: null };

  componentDidMount() {
    fetch('/api/getUsername')
      .then(res => res.json())
      .then(user => this.setState({ username: user.username }));
  }

  render() {
    const { username } = this.state;
    return (
      <div>
        <form action="/api/signup" method="post">
          <label>Username</label>
            <input type="text" name="username" />
          <label>Password</label>
            <input type="password" name="password" />
      <button type="submit">Signup</button>
      </form>
      </div>
    );
  }
}
