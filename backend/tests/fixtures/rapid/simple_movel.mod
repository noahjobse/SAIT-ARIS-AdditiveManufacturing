MODULE SimpleMove
    CONST robtarget p10 := [[500, 0, 600], [1, 0, 0, 0], [0, 0, 0, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    PROC main()
        MoveL p10, v1000, z10, tool0;
    ENDPROC
ENDMODULE
