MODULE PickAndPlace
    CONST robtarget pHome := [[600, 0, 800], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget pPick := [[400, 200, 100], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget pPlace := [[400, -200, 100], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    PROC main()
        MoveL pHome, v1000, z10, tool0;
        MoveL pPick, v500, fine, tool0;
        ! Grip object here
        MoveL pHome, v1000, z10, tool0;
        MoveL pPlace, v500, fine, tool0;
        ! Release object here
        MoveL pHome, v1000, z10, tool0;
    ENDPROC
ENDMODULE
