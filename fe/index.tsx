import * as React from "react";
import {Login} from "ui/Login";
import {LoginDetails} from "models/login-details";
import {InitialResourceLoadingScreen} from "ui/ResourceLoaders/InitialResourceLoadingScreen";
import {ServerResourceLoadingScreen} from "ui/ResourceLoaders/ServerResourceLoadingScreen";
import {Lobby} from "ui/Lobby";
import {ViewContainer} from "ui/ViewContainer";
import {ViewState} from "models/view-state";
import {Text} from "ui/Text"
import * as ReactDOM from 'react-dom';
import {GameView} from "ui/GameView";


export default function App() {
    const [loginDetails, setLoginDetails] = React.useState<LoginDetails>({
        username: 'sam',
        password: 'bananana',
    })
    const [view, setView] = React.useState(ViewState.Login);

    return <InitialResourceLoadingScreen>
        <>
            {view == ViewState.Login && <ViewContainer>
                <Login setView={setView} loginDetails={loginDetails} setLoginDetails={setLoginDetails}/>
            </ViewContainer>}
            {view == ViewState.Lobby && <ViewContainer>
                <ServerResourceLoadingScreen>
                    <Lobby setView={setView} />
                </ServerResourceLoadingScreen>
            </ViewContainer>}
            {view == ViewState.Game && <GameView />}
        </>
    </InitialResourceLoadingScreen>
}


ReactDOM.render(
  <App/>,
  document.getElementById("root")
);
