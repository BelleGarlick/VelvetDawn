import {Renderable} from "./renderable";
import {Perspective} from "../perspective";
import {RenderingConstants} from "../phases/scene";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";

export class TurnBanner extends Renderable {

    private _title: string = "";

    public title(_value: string) {
        this._title = _value;
        return this;
    }

    render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): null {
        const screenWidth = constants.width - constants.sidebar
        const bannerMargin = 20 * constants.resolution
        const width = Math.min(600 * constants.resolution, screenWidth - bannerMargin);
        const height = 110;
        const centerX = screenWidth / 2
        const bannerStart = centerX - width / 2
        const startY = bannerMargin

        const points = perspective.computeHexPoints(width, height);

        ctx.beginPath();
        ctx.moveTo(points[5].x + bannerStart, points[5].y + startY);
        points.forEach(({x, y}) => {
            ctx.lineTo(bannerStart + x,startY + y);
        })
        ctx.closePath();
        ctx.fillStyle = "#000000"
        ctx.fill();
        ctx.strokeStyle = "#ffffff"
        ctx.lineWidth = 2
        ctx.stroke();

        ctx.fillStyle = "#ffffff"
        ctx.textBaseline = "middle"
        ctx.textAlign = "center"
        ctx.font = "40px 'Velvet Dawn'";
        ctx.fillText(this._title, centerX, bannerMargin + 38)

        ctx.fillStyle = "#ffffff"
        ctx.textBaseline = "middle"
        ctx.textAlign = "center"
        ctx.font = "26px arial";

        ctx.fillText(this.getSubtitle(), centerX, bannerMargin + 86)

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

        return `${playersReady}/${players.length} players ready (${minutes}:${seconds < 10 ? '0' : ''}${seconds})`
    }
}
