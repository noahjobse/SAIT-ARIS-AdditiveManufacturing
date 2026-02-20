import { useEffect, useRef } from "react";
import createRobotScene, { type JointControls } from "../babylon/createRobotScene";

type Viewport3DProps = {
    anglesDeg: number[];
    modelPath: string;
};

function Viewport3D({ anglesDeg, modelPath }: Viewport3DProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const jointControlsRef = useRef<JointControls | null>(null);

    // Create scene one time
    useEffect(() => {
        let alive = true;

        (async () => {
            if (!canvasRef.current) return;

            const jointControls = await createRobotScene(canvasRef.current, modelPath);
            if (!alive) {
                jointControls.dispose();
                return;
            }

            jointControlsRef.current = jointControls;

            // Set initial joint angles
            anglesDeg.forEach((deg, i) => {
                jointControls.setJointAngle(i, (deg * Math.PI) / 180);
            });
            
        })();

        return () => {
            alive = false;
            jointControlsRef.current?.dispose();
            jointControlsRef.current = null;
        };

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [modelPath]);

    // Update joint angles when sliders change
    useEffect(() => {
        const jointControls = jointControlsRef.current;
        if (!jointControls) return;

        anglesDeg.forEach((deg, i) => {
            jointControls.setJointAngle(i, (deg * Math.PI) / 180);
        });
    }, [anglesDeg]);

    const handleMouseDown = () => {
        if (canvasRef.current) {
            canvasRef.current.style.cursor = 'grabbing';
        }
    };

    const handleMouseUp = () => {
        if (canvasRef.current) {
            canvasRef.current.style.cursor = 'grab';
        }
    };

    return (
        <div className="w-full h-full">
            <canvas 
                ref={canvasRef} 
                onMouseDown={handleMouseDown}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                className="w-full h-full block cursor-grab outline-none" 
            />
        </div>
    );

}    

export default Viewport3D;