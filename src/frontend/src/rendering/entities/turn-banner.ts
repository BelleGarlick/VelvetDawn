import {Renderable} from "./renderable";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {RenderingFacade} from "../facade";

export class TurnBanner extends Renderable {

    private _title: string = "";

    public title(_value: string) {
        this._title = _value;
        return this;
    }

    render(facade: RenderingFacade): null {
        const screenWidth = facade.constants.width - facade.constants.sidebar
        const bannerMargin = 20 * facade.constants.resolution
        const width = Math.min(600 * facade.constants.resolution, screenWidth - bannerMargin);
        const height = 110;
        const centerX = screenWidth / 2
        const bannerStart = centerX - width / 2
        const startY = bannerMargin

        const points = facade.perspective.computeHexPoints(width, height);

        facade.ctx.beginPath();
        facade.ctx.moveTo(points[5].x + bannerStart, points[5].y + startY);
        points.forEach(({x, y}) => {
            facade.ctx.lineTo(bannerStart + x,startY + y);
        })
        facade.ctx.closePath();
        facade.ctx.fillStyle = "#000000"
        facade.ctx.fill();
        facade.ctx.strokeStyle = "#ffffff"
        facade.ctx.lineWidth = 2
        facade.ctx.stroke();

        facade.ctx.fillStyle = "#ffffff"
        facade.ctx.textBaseline = "middle"
        facade.ctx.textAlign = "center"
        facade.ctx.font = "40px 'Velvet Dawn'";
        facade.ctx.fillText(this._title, centerX, bannerMargin + 38)

        facade.ctx.fillStyle = "#ffffff"
        facade.ctx.textBaseline = "middle"
        facade.ctx.textAlign = "center"
        facade.ctx.font = "26px arial";

        facade.ctx.fillText(this.getSubtitle(), centerX, bannerMargin + 86)
        facade.ctx.closePath()
        facade.ctx.restore()

        return null;
    }

    getSubtitle() {
        const currentRoundTime = (new Date().getTime() / 1000) - VelvetDawn.getState().turn.start
        let remainingTime = VelvetDawn.getState().turn.seconds - currentRoundTime
        remainingTime = Math.max(0, Math.round(remainingTime));
        const minutes = Math.floor(remainingTime / 60)
        const seconds = remainingTime % 60

        let playersReady = 0;

        const players = VelvetDawn.listCurrentTurnPlayers()
        players.forEach(player => {
            if (player.ready)
                playersReady += 1;
        })

        const teamTurn = VelvetDawn.getState().turn.team;
        const team = VelvetDawn.getState().teams.find(x => x.id === teamTurn)
        const teamName = team === undefined ? '' : `Team ${team.name}. `
        return `${teamName}${playersReady}/${players.length} players ready (${minutes}:${seconds < 10 ? '0' : ''}${seconds})`
    }
}
