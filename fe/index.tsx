import * as React from "react";
import * as ReactDOM from "react-dom";
import { Login } from "ui/Login";
import {LoginDetails} from "models/login-details";
import {createTheme, ThemeProvider} from "@material-ui/core";
import { InitialResourceLoadingScreen } from "ui/ResourceLoaders/InitialResourceLoadingScreen";
import {ServerResourceLoadingScreen} from "ui/ResourceLoaders/ServerResourceLoadingScreen";
import {Lobby} from "ui/Lobby";
import {ViewContainer} from "ui/ViewContainer";

const theme = createTheme({
    typography: {
        fontFamily: "'Velvet Dawn', sans-serif",
    }
});



export default function App() {
    const [loginDetails, setLoginDetails] = React.useState<LoginDetails>({
        username: 'sam',
        password: 'bananana',
    })
    const [connected, setConnected] = React.useState(false)

    return <ThemeProvider theme={theme}>
        <InitialResourceLoadingScreen>
            <ViewContainer>
                {!connected && <Login setConnected={setConnected} loginDetails={loginDetails} setLoginDetails={setLoginDetails}/>}
                {connected && <ServerResourceLoadingScreen>
                    <Lobby />
                </ServerResourceLoadingScreen>}
            </ViewContainer>
        </InitialResourceLoadingScreen>
    </ThemeProvider>;
}


ReactDOM.render(
  <App/>,
  document.getElementById("root")
);
