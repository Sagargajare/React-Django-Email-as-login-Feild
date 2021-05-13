import React, { Component } from "react";
import { render } from "react-dom";

import Headers from "./Headers";
import Root from "./Users/Root";
import { Route, Switch } from "react-router-dom";
import Home from "./Home";
import { ToastContainer } from "react-toastify";

import Signup from "./Users/Signup";
import Login from "./Users/Login";
import Dashboard from "./Dashboard";
import requireAuth from "../utils/RequireAuth";
export default function App() {
    return (
        <div>
        <Root>
          <Switch>
            <Route path="/signup" component={Signup} />
            <Route path="/login" component={Login} />
            <Route path="/dashboard" component={requireAuth(Dashboard)} />
            <Route exact path="/" component={Home} />
          </Switch>
        </Root>
        <ToastContainer hideProgressBar={true} newestOnTop={true} />
      </div>
    ) 
}



const container = document.getElementById("app");
render(<App />, container);