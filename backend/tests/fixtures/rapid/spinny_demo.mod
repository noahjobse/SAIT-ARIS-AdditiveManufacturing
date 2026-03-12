MODULE SpinnyDemo
    ! Dramatic fast joint sweeps — base spins + wrist flips for demo
    CONST jointtarget jHome  := [[0,   -30,  30,  0,   60,  0],   [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST jointtarget jR1    := [[90,  -60,  60,  90,  30,  90],  [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST jointtarget jL1    := [[-90, -60,  60, -90,  30, -90],  [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST jointtarget jUp    := [[0,   -80,  70,  0,  -30,  180], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST jointtarget jR2    := [[120, -40,  40,  120, 60,  -90], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST jointtarget jL2    := [[-120,-40,  40, -120, 60,   90], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST jointtarget jReach := [[0,   -85,  65,  0,   90,  180], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    PROC main()
        MoveAbsJ jHome,  v5000, z10, tool0;
        MoveAbsJ jR1,    v5000, z10, tool0;
        MoveAbsJ jL1,    v5000, z10, tool0;
        MoveAbsJ jUp,    v5000, z10, tool0;
        MoveAbsJ jR2,    v5000, z10, tool0;
        MoveAbsJ jL2,    v5000, z10, tool0;
        MoveAbsJ jReach, v5000, z10, tool0;
        MoveAbsJ jHome,  v5000, fine, tool0;
    ENDPROC
ENDMODULE
