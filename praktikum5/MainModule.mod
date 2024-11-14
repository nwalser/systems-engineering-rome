 MODULE MainModule

  TASK PERS tooldata tool1 := [TRUE, [[0, 0, 100], [1, 0, 0, 0]], [1, [1, 1, 1], [1, 0, 0, 0], 0, 0, 0]];
  TASK PERS tooldata distanceSensor := [TRUE,[[-150,0,30],[0.5,-0.5,-0.5,0.5]],[0.2,[0,0,30],[1,0,0,0],0.0001,0.0001,0.0001]];
  
  CONST string SERVER_ADDRESS := "192.168.125.1";
  CONST num SERVER_PORT := 8400;
  CONST string CR := "\0D";
  CONST string LF := "\0A";

  PROC main()

    VAR socketdev serverSocket;
    VAR socketdev clientSocket;
    VAR string response;
    VAR string receiveString;
    VAR string buffer;

    SocketCreate serverSocket;
    SocketBind serverSocket, SERVER_ADDRESS, SERVER_PORT;
    SocketListen serverSocket;

    WHILE TRUE DO

      SocketAccept serverSocket, clientSocket; ! wait for connection from client

      response := "OK";
      buffer := "";

      WHILE StrLen(response) > 0 DO

        SocketReceive clientSocket \Str := receiveString;
        buffer := buffer+receiveString;

        IF StrFind(buffer, 1, LF) <= StrLen(buffer) THEN
          buffer := StrPart(buffer, 1, StrFind(buffer, 1, CR+LF)-1);
          response := processCommand(buffer);
          buffer := "";
          SocketSend clientSocket \Str := response+CR+LF;
        ENDIF

      ENDWHILE

      SocketClose clientSocket;

    ENDWHILE

    ERROR
      RETRY;
 
  ENDPROC

  ! this function processes a received string and executes
  ! the desired command with the robot controller
  FUNC string processCommand(string buffer)

    VAR string command;
    VAR num value;
    VAR speeddata velocity;
    VAR zonedata zone;
    VAR egmident egmID1;

    IF StrFind(buffer, 1, STR_WHITE) <= StrLen(buffer) THEN
      command := StrPart(buffer, 1, StrFind(buffer, 1, STR_WHITE)-1);
    ELSE
      command := buffer;
    ENDIF

    TEST command
      
      CASE "Close": RETURN "";
      
      CASE "Home": MoveAbsJ [[0, 0, 0, 0, 45, 0],[9E+09, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]] \NoEOffs, v100, fine, tool1;
      
      CASE "MoveAbsJ": MoveAbsJ [[parseNumber(buffer,1), parseNumber(buffer,2), parseNumber(buffer,3), parseNumber(buffer,4), parseNumber(buffer,5), parseNumber(buffer,6)], [9E+09, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]] \NoEOffs, v100, fine, tool1;
      
      CASE "MoveJ": velocity := [parseNumber(buffer,12), 180, 5000, 1000];
                    IF parseNumber(buffer,13) > 0 THEN
                        zone := [FALSE, parseNumber(buffer,13), parseNumber(buffer,13), 1, 1, 1, 1];
                    ELSE
                        zone := fine;
                    ENDIF
                    MoveJ [[parseNumber(buffer,1), parseNumber(buffer,2), parseNumber(buffer,3)], [parseNumber(buffer,4), parseNumber(buffer,5), parseNumber(buffer,6), parseNumber(buffer,7)], [parseNumber(buffer,8), parseNumber(buffer,9), parseNumber(buffer,10), parseNumber(buffer,11)], [9E+09, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]], velocity, zone, tool1;
      
      CASE "MoveL": velocity := [parseNumber(buffer,12), 180, 5000, 1000];
                    IF parseNumber(buffer,13) > 0 THEN
                        zone := [FALSE, parseNumber(buffer,13), parseNumber(buffer,13), 1, 1, 1, 1];
                    ELSE
                        zone := fine;
                    ENDIF
                    MoveL [[parseNumber(buffer,1), parseNumber(buffer,2), parseNumber(buffer,3)], [parseNumber(buffer,4), parseNumber(buffer,5), parseNumber(buffer,6), parseNumber(buffer,7)], [parseNumber(buffer,8), parseNumber(buffer,9), parseNumber(buffer,10), parseNumber(buffer,11)], [9E+09, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]], velocity, zone, tool1;
      
      CASE "EGM": velocity := [parseNumber(buffer,12), 180, 5000, 1000];
                  EGMGetId egmID1;
                  EGMSetupUC ROB_1, egmID1, "pathCorr", "egmSensor"\PathCorr\APTR\CommTimeout:=20;
                  EGMActMove egmID1, distanceSensor.tframe \SampleRate:=120;
                  EGMMoveL egmID1, [[parseNumber(buffer,1), parseNumber(buffer,2), parseNumber(buffer,3)], [parseNumber(buffer,4), parseNumber(buffer,5), parseNumber(buffer,6), parseNumber(buffer,7)], [parseNumber(buffer,8), parseNumber(buffer,9), parseNumber(buffer,10), parseNumber(buffer,11)], [9E+09, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]], velocity, fine, distanceSensor;
                  EGMReset egmID1;
      
    ENDTEST

    RETURN "OK";

  ENDFUNC

  ! this function receives a text string with one or several numbers
  ! and returns the value of the number i as a numerical value
  FUNC num parseNumber(string buffer, num i)

    VAR num index;
    VAR num value;

    FOR j FROM 1 TO i DO
      index := StrFind(buffer, 1, STR_WHITE);
      IF index < StrLen(buffer) THEN
        buffer := StrPart(buffer, index+1, StrLen(buffer)-index);
      ENDIF
    ENDFOR

    index := StrFind(buffer, 1, STR_WHITE);
    IF index <= StrLen(buffer) THEN
      buffer := StrPart(buffer, 1, index-1);
    ENDIF

    IF StrToVal(buffer, value) THEN
      RETURN value;
    ENDIF

    RETURN 0;

  ENDFUNC

ENDMODULE
