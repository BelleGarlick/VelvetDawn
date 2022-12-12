import axios from "axios";
import {LoginDetails} from "models/login-details";


export function joinServer(loginDetails: LoginDetails) {
    return axios.post("http://localhost:666/join/", {
        password: loginDetails.serverPassword,
        name: loginDetails.userName
    }, { headers: { "Content-Type": "multipart/form-data" }})
}
