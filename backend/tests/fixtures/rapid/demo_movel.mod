MODULE DemoMove
    CONST robtarget pReady := [[1200, 0, 1400], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget pLeft  := [[1000, 400, 1000], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];
    CONST robtarget pRight := [[1000, -400, 1000], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    PROC main()
        MoveL pReady, v500, z10, tool0;
        MoveL pLeft,  v300, z10, tool0;
        MoveL pRight, v300, z10, tool0;
        MoveL pReady, v500, fine, tool0;
    ENDPROC
ENDMODULE
