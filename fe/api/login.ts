import {LoginDetails} from "models/index";
import {post} from "./utils"


export function joinServer(loginDetails: LoginDetails): Promise<any> {
    return post("/join/",{
        username: loginDetails.username,
        password: loginDetails.password,
    })
}
