import { useEffect, useRef } from "react";
import createRobotScene, { type JointControls } from "../babylon/createRobotScene";

type Viewport3DProps = {
    anglesDeg: number[];
    modelPath: string | null;
};

function Viewport3D({ anglesDeg, modelPath }: Viewport3DProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const jointControlsRef = useRef<JointControls | null>(null);
    const latestAnglesRef = useRef<number[]>(anglesDeg);

    useEffect(() => {
        latestAnglesRef.current = anglesDeg;
    }, [anglesDeg]);

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
            latestAnglesRef.current.forEach((deg, i) => {
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
        <div className="relative w-full h-full bg-linear-to-br from-gray-900 via-gray-950 to-black">
            {/* Grid background */}
            <div
                className="absolute inset-0 opacity-60 pointer-events-none"
                style={{
                    backgroundImage: `
                        linear-gradient(rgba(139, 92, 246, 0.15) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(139, 92, 246, 0.15) 1px, transparent 1px)
                    `,
                    backgroundSize: "50px 50px",
                }}
            />

            {/* Glow overlays */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl"></div>
                <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl"></div>
            </div>

            {/* Babylon.js Canvas */}
            <canvas 
                ref={canvasRef} 
                onMouseDown={handleMouseDown}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                className="relative z-10 w-full h-full block cursor-grab outline-none" 
            />
        </div>
    );

}    

export default Viewport3D;