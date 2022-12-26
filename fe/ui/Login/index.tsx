import * as React from "react";
import * as Api from 'api'
import {LoginDetails} from "models/login-details";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {ViewState} from "models/view-state";
import {Text} from "ui/Text"

export function Login({ loginDetails, setLoginDetails, setView }: { loginDetails: LoginDetails, setLoginDetails: (x: LoginDetails) => void, setView: (x: ViewState) => void }) {
    const join = () => {
        Api.login.joinServer(loginDetails)
            .then(x => {
                // VelvetDawn.audioPlayers["velvet-dawn:menu.mp3"].play()
                console.log(x)
                setView(ViewState.Lobby)
                VelvetDawn.loginDetails = loginDetails
            })
            .catch((err) => {
                console.error(err)
                alert("Unable to join server. Check console for output")
            })
    }

    // join()

    return <>
        <Text>Welcome to Velvet Dawn</Text>
        <input
            type={'text'}
            value={loginDetails.username}
            onInput={(event) => {
                // @ts-ignore
                const v = event.target.value

                setLoginDetails({
                    ...loginDetails,
                    username: v
                })
            } }
        />
        <input
            type={'password'}
            value={loginDetails.password}
            onInput={(event) => {
                // @ts-ignore
                const v = event.target.value

                setLoginDetails({
                    ...loginDetails,
                    password: v
                })
            }}
        />

        <button onClick={() => {
            join()
        }}>Join</button>
    </>
}