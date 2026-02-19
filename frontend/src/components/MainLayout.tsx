import { useState } from "react";
import SidePanel from "./SidePanel";
import Viewport3D from "./Viewport3D";

const ROBOT_MODELS = [
    { label: "ABB IRB 4600", path: "/models/robots/irb4600/Model_IRB_4600.glb" },
    { label: "ABB IRB 2600", path: "/models/robots/irb2600/Model_IRB_2600.glb" },
    { label: "ABB IRB 6700", path: "/models/robots/irb6700/Model_IRB_6700.glb" },
]
const ZERO_ANGLES = [0, 0, 0, 0, 0, 0];

function MainLayout() {
    const [anglesDeg, setAnglesDeg] = useState<number[]>([0, 0, 0, 0, 0, 0]);

    // Works for every robot model, but haven't added a selector yet (change 0 to 1 or 2 to see other models)
    const [modelPath, setModelPath] = useState<string>(ROBOT_MODELS[0].path); 

    // Haven't added a dropdown for robot models yet
    const handleRobotChange = (path: string) => {
        setModelPath(path);
        setAnglesDeg(ZERO_ANGLES);
    };

    return (
        <div className="flex flex-row h-screen w-screen">
            <div className="flex-2 ">
                <SidePanel anglesDeg={anglesDeg} setAnglesDeg={setAnglesDeg} />
            </div>

            <div className="flex-8">
                <Viewport3D anglesDeg={anglesDeg} modelPath={modelPath}/>
            </div>

        </div>
    );
}

export default MainLayout;