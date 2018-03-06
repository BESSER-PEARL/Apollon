import * as React from "react";
import { Point } from "../../../geometry";

export default class RelationshipDragPreview extends React.Component<Props> {
    render() {
        const { connectorPosition, mousePosition } = this.props;
        const { center, outer } = connectorPosition;

        const path = [center, outer];

        if (mousePosition !== null) {
            path.push(mousePosition);
        }

        const polylinePoints = path.map(point => `${point.x} ${point.y}`).join(",");

        return (
            <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
                <polyline
                    points={polylinePoints}
                    fill="none"
                    stroke="black"
                    strokeWidth="1"
                    strokeDasharray="5,5"
                />
            </svg>
        );
    }
}

interface Props {
    connectorPosition: { center: Point; outer: Point };
    mousePosition: Point | null;
}
