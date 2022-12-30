import {PathPlanningNode, VelvetDawnMap} from "../../../velvet-dawn/map";
import {Position} from "models";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";
import {Perspective} from "../../perspective";
import {RenderingConstants} from "../scene";


/** Path planning module for the game scene
 *
 * This caches path planning calls to reduce processing time
 * and renders the path in game.
 */


export class PathPlanning {

    private cachedPathAreaData: {position: Position, range: number} | undefined = undefined
    private cachedPathAreaTree: PathPlanningNode[] | undefined = undefined
    private cachedPathAreaPositions: Position[] | undefined = undefined
    private cachedPathPositionsHash: Set<string> | undefined

    private cachePathToPointPosition: Position | undefined
    private cachedPathToPoint: Position[] | undefined = undefined

    private readonly velvetDawnMap: VelvetDawnMap

    constructor(map?: VelvetDawnMap) {
        this.velvetDawnMap = map ?? VelvetDawn.map
    }


    /** Compute the paths the given position may take within a
     * given range.
     *
     * This should only be called on state update or when
     * the user selects an entity to get the path's it can
     * take. As this function builts up the initial cache.
     *
     * @param position The position to calculate paths from
     * @param range The range the unit may take
     */
    computePaths(position: Position, range: number) {
        this.clear()

        // Recompute
        this.cachedPathAreaTree = this.velvetDawnMap.getTilesInMovementRange(position, range)
        this.cachedPathAreaPositions = this.cachedPathAreaTree.map(x => x.position)
        this.cachedPathAreaData = {position: position, range: range}
        this.cachedPathPositionsHash = new Set(this.cachedPathAreaPositions.map(pos => {
            return `${pos.x}-${pos.y}`
        }))
    }

    /** Test if the given point is in the movement range of the current area
     *
     * @param position The position to check what's in range
     * @returns true if the selected unit may move to the given position.
     */
    isPointInRange(position: Position): boolean {
        if (this.cachedPathPositionsHash === undefined)
            return false

        return this.cachedPathPositionsHash.has(`${position.x}-${position.y}`);
    }

    /** Get list of positions which represents the path the
     * selected unit must take to reach the given position
     *
     * This function uses a lot of caching to ensure the position
     * takes very little processing as this will be called every
     * frame to show the unit's path.
     *
     * @param position The path the entity must take
     * @returns The list of points representing the path to take
     */
    getPathToPoint(position: Position): Position[] | undefined {
        if (this.cachedPathAreaData === undefined)
            return undefined

        if (this.cachedPathAreaTree === undefined || this.cachedPathAreaTree.length === 0)
            return undefined

        if (this.cachedPathToPoint !== undefined
            && this.cachePathToPointPosition !== undefined
            && this.cachedPathToPoint.length > 0
            && this.cachePathToPointPosition.x === position.x
            && this.cachePathToPointPosition.y === position.y)
            return this.cachedPathToPoint

        const path = this.cachedPathAreaTree.find(x => {
            return x.position.x === position.x && x.position.y === position.y
        })

        if (path) {
            let pathPoint: PathPlanningNode | undefined = path;
            let fullPath: Position[] = []
            while (pathPoint !== undefined) {
                fullPath = [pathPoint.position, ...fullPath]
                pathPoint = pathPoint.previous
            }

            this.cachedPathToPoint = fullPath
            this.cachePathToPointPosition = position
        }
        else {
            this.cachedPathToPoint = undefined
            this.cachePathToPointPosition = undefined
        }

        return this.cachedPathToPoint
    }

    /** Move an entity
     *
     * First check that the entity can move to the given position
     * then register it on the server if the path is possible.
     *
     * @param entityId The entity id to update
     * @param position The position to move the entity too.
     */
    moveUnit(entityId: number, position: Position) {
        const path = this.getPathToPoint(position)
        if (path) {
            this.velvetDawnMap.move(entityId, path)
        }
    }

    /** Render the path planning data which shows the tiles
     * the entity may move to and the path the entity moves
     * if possible.
     *
     * @param ctx The canvas context
     * @param perspective The rendering perspective
     * @param constants Rendereing constants
     * @param hoveredTilePosition The position of the hovered
     *      tile to render the path too.
     */
    render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants, hoveredTilePosition: Position) {
        if (this.cachedPathAreaPositions) {
            this.cachedPathAreaPositions.forEach(position => {
                const {
                    visible, imageStart, imageEnd, clipPoints, imageWidth, imageHeight
                } = perspective.getTileRenderingConstants(position, constants);

                if (visible) {
                    ctx.restore()
                    ctx.save();
                    // Create Hexagon to clip the image
                    ctx.beginPath();
                    ctx.moveTo(clipPoints[5].x, clipPoints[5].y);
                    clipPoints.forEach(({x, y}) => ctx.lineTo(x, y))
                    ctx.closePath();
                    ctx.clip();

                    ctx.globalAlpha = 0.3
                    ctx.fillStyle = "#00ff00"
                    ctx.rect(imageStart + 50, imageEnd + 50, imageWidth - 100, imageHeight - 100)
                    ctx.fill()
                    ctx.globalAlpha = 1

                    ctx.restore()
                }
            })

            if (hoveredTilePosition) {
                let path = this.getPathToPoint(hoveredTilePosition)
                if (path) {
                    path = path.map(x => perspective.getTileCoordinates(x))
                    ctx.restore()
                    ctx.globalAlpha = 0.3
                    ctx.beginPath()
                    ctx.moveTo(path[0].x, path[0].y)
                    path.forEach((pos, i) => {
                        if (i > 0)
                            ctx.lineTo(pos.x, pos.y)
                    })
                    ctx.strokeStyle = "#ffffff"
                    ctx.lineWidth = 5 * constants.resolution
                    ctx.stroke()

                    path.forEach((pos, i) => {
                        if (i > 0) {
                            ctx.beginPath()
                            ctx.arc(pos.x, pos.y, 5 * constants.resolution, 0, 2 * Math.PI);
                            ctx.fill()
                        }
                    })

                    ctx.globalAlpha = 1
                }
            }
        }
        ctx.restore()
    }

    /** Clear the cache
     *
     * This function should be used when resetting the cache
     * such as when the state changes as it may not be the player's
     * turn or when the user selects of a unit.
     */
    clear() {
        this.cachedPathAreaData = undefined
        this.cachedPathAreaTree = undefined
        this.cachedPathAreaPositions = undefined
        this.cachedPathPositionsHash = undefined

        this.cachePathToPointPosition = undefined
        this.cachedPathToPoint = undefined
    }
}