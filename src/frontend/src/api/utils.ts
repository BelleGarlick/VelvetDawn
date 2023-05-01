import axios from "axios";
import { inDevMove } from "../constants";
import {VelvetDawn} from "../velvet-dawn/velvet-dawn";


export function getUrl() {
    if (inDevMove())
        return "http://localhost:1642"

    let url = window.location.href;
    return url.substring(0, url.length - 1);
}


export function getResourceUrl(resourceId: string) {
    return `${getUrl()}/datapacks/${resourceId}`
}


export function get(path: string, data?: { [key: string]: any }): Promise<any> {
    return axios.get(getUrl() + path, {
        ...(data ?? {}),
        headers: {
            "username": VelvetDawn.loginDetails.username,
            "password": VelvetDawn.loginDetails.password
        }
    }).then(x => x.data)
}


export function post(path: string, data: { [key: string]: any }): Promise<any> {
    return axios.post(
        getUrl() + path,
        data,
        { headers: {
            "Content-Type": "multipart/form-data",
            "username": VelvetDawn.loginDetails.username,
            "password": VelvetDawn.loginDetails.password,
        }}
    ).then(x => x.data)
}
