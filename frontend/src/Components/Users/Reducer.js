import { combineReducers } from "redux";
import { connectRouter } from "connected-react-router";
import { signupReducer } from './SignupReducer'
import { loginReducer } from "./LoginReducer";
const createRootReducer = history =>
  combineReducers({
    router: connectRouter(history),
    createUser: signupReducer,
    auth: loginReducer 
  });

export default createRootReducer;