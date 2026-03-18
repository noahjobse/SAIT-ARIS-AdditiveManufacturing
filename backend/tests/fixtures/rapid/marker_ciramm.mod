MODULE MarkerDemo
    ! Tool: marker with 150mm TCP offset along Z (pen tip below flange)
    PERS tooldata tMarker := [TRUE, [[0, 0, 150], [1, 0, 0, 0]], [0.5, [0, 0, 75], [1, 0, 0, 0], 0, 0, 0]];

    ! Drawing surface: XY plane at Z=800mm, centered at X=1200 Y=0
    ! Letters are 60mm tall, 40mm wide, 15mm spacing
    ! Total width ~385mm (6 letters * 55mm pitch)

    ! Approach height (pen up)
    CONST robtarget pUp := [[1200, -190, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- C ---
    CONST robtarget C1 := [[1200, -160, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget C2 := [[1200, -200, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget C3 := [[1200, -200, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget C4 := [[1200, -160, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- I ---
    CONST robtarget I1 := [[1200, -140, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget I2 := [[1200, -140, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- R ---
    CONST robtarget R1 := [[1200, -120, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R2 := [[1200, -120, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R3 := [[1200, -80, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R4 := [[1200, -80, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R5 := [[1200, -120, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget R6 := [[1200, -80, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- A ---
    CONST robtarget A1 := [[1200, -60, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A2 := [[1200, -40, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A3 := [[1200, -20, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A4 := [[1200, -50, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget A5 := [[1200, -30, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- M (first) ---
    CONST robtarget M1a := [[1200, 0, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget M2a := [[1200, 0, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget M3a := [[1200, 20, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget M4a := [[1200, 40, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget M5a := [[1200, 40, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! --- M (second) ---
    CONST robtarget M1b := [[1200, 60, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget M2b := [[1200, 60, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget M3b := [[1200, 80, 830], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget M4b := [[1200, 100, 860], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget M5b := [[1200, 100, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    ! Pen-up positions for letter transitions
    CONST robtarget penUp1 := [[1200, -140, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUp2 := [[1200, -120, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUp3 := [[1200, -60, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUp4 := [[1200, -20, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUp5 := [[1200, 0, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUp6 := [[1200, 60, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpR := [[1200, -120, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget penUpA := [[1200, -50, 900], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    PROC main()
        ! Approach
        MoveL pUp, v500, fine, tMarker;

        ! --- Draw C ---
        MoveL C1, v200, fine, tMarker;
        MoveL C2, v100, fine, tMarker;
        MoveL C3, v100, fine, tMarker;
        MoveL C4, v100, fine, tMarker;

        ! Pen up, move to I
        MoveL penUp1, v300, fine, tMarker;

        ! --- Draw I ---
        MoveL I1, v200, fine, tMarker;
        MoveL I2, v100, fine, tMarker;

        ! Pen up, move to R
        MoveL penUp2, v300, fine, tMarker;

        ! --- Draw R (vertical + top loop + diagonal leg) ---
        MoveL R1, v200, fine, tMarker;
        MoveL R2, v100, fine, tMarker;
        MoveL R3, v100, fine, tMarker;
        MoveL R4, v100, fine, tMarker;
        MoveL R5, v100, fine, tMarker;
        ! Pen up for diagonal
        MoveL penUpR, v300, fine, tMarker;
        MoveL R5, v200, fine, tMarker;
        MoveL R6, v100, fine, tMarker;

        ! Pen up, move to A
        MoveL penUp3, v300, fine, tMarker;

        ! --- Draw A (left stroke, right stroke, crossbar) ---
        MoveL A1, v200, fine, tMarker;
        MoveL A2, v100, fine, tMarker;
        MoveL A3, v100, fine, tMarker;
        ! Pen up for crossbar
        MoveL penUpA, v300, fine, tMarker;
        MoveL A4, v200, fine, tMarker;
        MoveL A5, v100, fine, tMarker;

        ! Pen up, move to M1
        MoveL penUp4, v300, fine, tMarker;

        ! --- Draw M (first) ---
        MoveL M1a, v200, fine, tMarker;
        MoveL M2a, v100, fine, tMarker;
        MoveL M3a, v100, fine, tMarker;
        MoveL M4a, v100, fine, tMarker;
        MoveL M5a, v100, fine, tMarker;

        ! Pen up, move to M2
        MoveL penUp5, v300, fine, tMarker;

        ! --- Draw M (second) ---
        MoveL M1b, v200, fine, tMarker;
        MoveL M2b, v100, fine, tMarker;
        MoveL M3b, v100, fine, tMarker;
        MoveL M4b, v100, fine, tMarker;
        MoveL M5b, v100, fine, tMarker;

        ! Return to approach
        MoveL penUp6, v300, fine, tMarker;
        MoveL pUp, v500, fine, tMarker;
    ENDPROC
ENDMODULE
