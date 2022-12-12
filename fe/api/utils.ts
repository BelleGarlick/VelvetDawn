import axios from "axios";


export function get(path: string, data?: { [key: string]: any }): Promise<any> {
    let port = window.location.port
    port = '666'
    const url = window.location.protocol + "//" + window.location.hostname + ":" + 666 + "/" + path
    console.log(url)
    return axios.get(url, data).then(x => x.data)
}
