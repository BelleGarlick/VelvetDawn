import * as React from "react";
import * as Api from 'api'
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {Text} from "../Text"
import {Button} from "../Button"
import {ViewState, LoginDetails} from "models";

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
        <Text style={{
            color: 'white',
            marginLeft: '20px',
            fontSize: '18px'
        }}>Username</Text>
        <input
            type={'text'}
            value={loginDetails.username}
            onInput={(event) => {
                setLoginDetails({
                    ...loginDetails,
                    // @ts-ignore
                    username: event.target.value
                })
            } }
        />
        <Text style={{
            color: 'white',
            marginLeft: '20px',
            fontSize: '18px'
        }}>Unique Key</Text>
        <input
            type={'password'}
            value={loginDetails.password}
            onInput={(event) => {
                setLoginDetails({
                    ...loginDetails,
                    // @ts-ignore
                    password: event.target.value
                })
            }}
        />
        <Text style={{ color: 'white', fontSize: '12px' }}>This will act like a password to prevent other's spoofing you. Do not use an actual password.</Text>

        <div style={{
            display: 'flex',
            justifyContent: 'center',
        }}>
            <Button onClick={join}>Join</Button>
        </div>
    </>
}