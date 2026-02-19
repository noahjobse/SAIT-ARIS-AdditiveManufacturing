MODULE SimpleJoint
    CONST jointtarget jpos1 := [[0, -30, 30, 0, 45, 0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]];

    PROC main()
        MoveJ jpos1, v500, fine, tool0;
    ENDPROC
ENDMODULE
