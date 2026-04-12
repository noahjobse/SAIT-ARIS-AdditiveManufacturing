MODULE SaitArisDemo
    ! Tool: marker with 150mm TCP offset along Z (pen tip below flange)
    PERS tooldata tMarker := [TRUE, [[0, 0, 150], [1, 0, 0, 0]], [0.5, [0, 0, 75], [1, 0, 0, 0], 0, 0, 0]];

    ! Drawing surface: XY plane at Z=800mm, letters centered around Y=0
    ! Letters 60mm tall, 40mm wide, 15mm spacing, 30mm word gap
    ! Total width ~440mm (S=-220 to S=+220)
    ! Z=800 surface, Z=860 top, Z=830 midpoint, Z=900 pen-up transit

    CONST robtarget pStart := [[1200, -220, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- S (first) Y: -220 to -180 ---
    ! TODO(human): Define waypoints for letter S
    ! S is drawn as: top-bar → down-left → mid-bar → down-right → bottom-bar
    ! Bounding box: Y from -220 (left) to -180 (right), Z from 800 (bottom) to 860 (top)
    ! Midpoint Z=830, approach from pStart at Z=900
    ! Example skeleton (replace with your stroke design):
    CONST robtarget S1_1 := [[1200, -180, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S1_2 := [[1200, -220, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S1_3 := [[1200, -220, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S1_4 := [[1200, -180, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S1_5 := [[1200, -180, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S1_6 := [[1200, -220, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- A (first) Y: -165 to -125, center -145 ---
    CONST robtarget A1_1 := [[1200, -165, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A1_2 := [[1200, -145, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A1_3 := [[1200, -125, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A1_4 := [[1200, -155, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A1_5 := [[1200, -135, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- I (first) Y: center -90 ---
    CONST robtarget I1_1 := [[1200, -90, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget I1_2 := [[1200, -90, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- T Y: -55 to -15, center -35 ---
    CONST robtarget T1_1 := [[1200, -55, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget T1_2 := [[1200, -15, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget T1_3 := [[1200, -35, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget T1_4 := [[1200, -35, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- [space gap: Y -15 to +15] ---

    ! --- A (second) Y: +15 to +55, center +35 ---
    CONST robtarget A2_1 := [[1200, 15, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A2_2 := [[1200, 35, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A2_3 := [[1200, 55, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A2_4 := [[1200, 25, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A2_5 := [[1200, 45, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- R Y: +70 to +110 ---
    CONST robtarget R2_1 := [[1200, 70, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R2_2 := [[1200, 70, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R2_3 := [[1200, 110, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R2_4 := [[1200, 110, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R2_5 := [[1200, 70, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R2_6 := [[1200, 110, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- I (second) Y: center +145 ---
    CONST robtarget I2_1 := [[1200, 145, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget I2_2 := [[1200, 145, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- S (second) Y: +180 to +220 ---
    CONST robtarget S2_1 := [[1200, 220, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S2_2 := [[1200, 180, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S2_3 := [[1200, 180, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S2_4 := [[1200, 220, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S2_5 := [[1200, 220, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget S2_6 := [[1200, 180, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! Pen-up transit points
    CONST robtarget penUpS1  := [[1200, -180, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpA1  := [[1200, -165, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpA1c := [[1200, -155, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpI1  := [[1200, -90, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpT1  := [[1200, -55, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpT1v := [[1200, -35, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpA2  := [[1200, 15, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpA2c := [[1200, 25, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpR2  := [[1200, 70, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpR2d := [[1200, 70, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpI2  := [[1200, 145, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpS2  := [[1200, 180, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget pEnd     := [[1200, 220, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    PROC main()
        ! Approach start position
        MoveL pStart, v500, fine, tMarker;

        ! --- Draw S (first) ---
        MoveL S1_1, v200, fine, tMarker;
        MoveL S1_2, v100, fine, tMarker;
        MoveL S1_3, v100, fine, tMarker;
        MoveL S1_4, v100, fine, tMarker;
        MoveL S1_5, v100, fine, tMarker;
        MoveL S1_6, v100, fine, tMarker;
        MoveL penUpS1, v300, fine, tMarker;

        ! --- Draw A (first) ---
        MoveL A1_1, v200, fine, tMarker;
        MoveL A1_2, v100, fine, tMarker;
        MoveL A1_3, v100, fine, tMarker;
        MoveL penUpA1c, v300, fine, tMarker;
        MoveL A1_4, v200, fine, tMarker;
        MoveL A1_5, v100, fine, tMarker;
        MoveL penUpI1, v300, fine, tMarker;

        ! --- Draw I (first) ---
        MoveL I1_1, v200, fine, tMarker;
        MoveL I1_2, v100, fine, tMarker;
        MoveL penUpT1, v300, fine, tMarker;

        ! --- Draw T ---
        MoveL T1_1, v200, fine, tMarker;
        MoveL T1_2, v100, fine, tMarker;
        MoveL penUpT1v, v300, fine, tMarker;
        MoveL T1_3, v200, fine, tMarker;
        MoveL T1_4, v100, fine, tMarker;

        ! [space gap] pen-up transit across word gap
        MoveL penUpA2, v300, fine, tMarker;

        ! --- Draw A (second) ---
        MoveL A2_1, v200, fine, tMarker;
        MoveL A2_2, v100, fine, tMarker;
        MoveL A2_3, v100, fine, tMarker;
        MoveL penUpA2c, v300, fine, tMarker;
        MoveL A2_4, v200, fine, tMarker;
        MoveL A2_5, v100, fine, tMarker;
        MoveL penUpR2, v300, fine, tMarker;

        ! --- Draw R ---
        MoveL R2_1, v200, fine, tMarker;
        MoveL R2_2, v100, fine, tMarker;
        MoveL R2_3, v100, fine, tMarker;
        MoveL R2_4, v100, fine, tMarker;
        MoveL R2_5, v100, fine, tMarker;
        MoveL penUpR2d, v300, fine, tMarker;
        MoveL R2_5, v200, fine, tMarker;
        MoveL R2_6, v100, fine, tMarker;
        MoveL penUpI2, v300, fine, tMarker;

        ! --- Draw I (second) ---
        MoveL I2_1, v200, fine, tMarker;
        MoveL I2_2, v100, fine, tMarker;
        MoveL penUpS2, v300, fine, tMarker;

        ! --- Draw S (second) ---
        MoveL S2_1, v200, fine, tMarker;
        MoveL S2_2, v100, fine, tMarker;
        MoveL S2_3, v100, fine, tMarker;
        MoveL S2_4, v100, fine, tMarker;
        MoveL S2_5, v100, fine, tMarker;
        MoveL S2_6, v100, fine, tMarker;
        MoveL pEnd, v300, fine, tMarker;

        ! Return to start
        MoveL pStart, v500, fine, tMarker;
    ENDPROC
ENDMODULE
