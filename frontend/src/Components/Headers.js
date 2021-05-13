import React from 'react'
import { BrowserRouter, Route, Switch } from "react-router-dom";
export default function Headers() {
    return (
        <div>
            <BrowserRouter>
          <Switch>
            <Route exact path="/" component={Home} />
          </Switch>
        </BrowserRouter>
        </div> 
    )
} 
