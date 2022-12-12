import * as React from "react";
import * as ReactDOM from "react-dom";
import { Login } from "ui/Login";
import {LoginDetails} from "models/login-details";
import {VelvetDawn} from "./velvet-dawn/velvet-dawn";


export default function App() {
    const [logginIn, setLoaded] = React.useState(false)
    const [loginDetails, setLoginDetails] = React.useState<LoginDetails>({
        serverAddress: 'localhost:5012',
        serverPassword: 'bananana',
        userName: 'sam'
    })

    React.useEffect(() => {
        VelvetDawn.init()
    }, [])

    return <>
        <Login loginDetails={loginDetails} setLoginDetails={setLoginDetails} />
    </>;
}


ReactDOM.render(
  <App/>,
  document.getElementById("root")
);
