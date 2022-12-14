import {Button, TextField, Typography} from "@material-ui/core";
import * as React from "react";
import * as Api from 'api'
import {LoginDetails} from "models/login-details";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";

export function Login({ loginDetails, setLoginDetails, setConnected }: { loginDetails: LoginDetails, setLoginDetails: (x: LoginDetails) => void, setConnected: (x: boolean) => void }) {
    const join = () => {
        Api.login.joinServer(loginDetails)
            .then(x => {
                VelvetDawn.audioPlayers["velvet-dawn:menu.mp3"].play()
                console.log(x)
                setConnected(true)
                VelvetDawn.loginDetails = loginDetails
            })
            .catch((err) => {
                console.error(err)
                alert("Unable to join server. Check console for output")
            })
    }

    // join()

    // @ts-ignore
    // @ts-ignore
    return <>
        <Typography variant='h5'>Welcome to Velvet Dawn</Typography>
        <TextField
            label='Name'
            value={loginDetails.username}
            onInput={(event) => {
                // @ts-ignore
                const v = event.target.value

                setLoginDetails({
                    ...loginDetails,
                    username: v
                })
            } }
            variant='outlined'
        />
        <TextField
            label='Server Password'
            value={loginDetails.password}
            onInput={(event) => {
                // @ts-ignore
                const v = event.target.value

                setLoginDetails({
                    ...loginDetails,
                    password: v
                })
            } }
            variant='outlined'
        />

        <Button onClick={() => {
            join()
        }}>Join</Button>
    </>
}