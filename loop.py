import Game
import re
import Move

myGame = Game.Game()
pattern = r'^[a-h][1-8][a-h][1-8][qrbn]?$'
patternQ = r'^[a-h][1-8][a-h][1-8], [a-h][1-8][a-h][1-8][qrbn]?$'
retry = "yes"
helpLine = "이동을 작성하려면 UCI 표기법을 사용하여 이동을 작성하세요:\n예: b5에서 d3으로 이동하려면 'b5d3'를 작성합니다.\n만약 d3과 e2로 양자 이동을 하고 싶다면 'b5d3, b5e2'를 작성하세요.\n\n'Rules'를 작성하면 Quantum Chess의 규칙을 표시합니다.\n'Over'를 입력하면 언제든 게임을 종료할 수 있으며, 'Reset'을 입력하면 게임을 재시작합니다.\n\nStockfish 엔진을 사용하여 이동 도움을 받거나, 현재 위치를 평가하는 등 다양한 작업을 할 수 있습니다.\n'Evaluate'를 입력하면 현재 위치의 평가를 숫자로 받을 수 있습니다.\n양수는 백이 유리하다는 것을, 음수는 흑이 유리하다는 것을 의미합니다.\n'Evaluate move'를 입력한 뒤 이동을 입력하면 해당 이동이 얼마나 좋은지 숫자로 알 수 있습니다.\n'Hint'를 입력하면 Stockfish가 현재 위치에서 어떤 이동을 해야 할지 추천합니다.\n"
rules = "퀀텀 체스(Quantum Chess)는 고전 체스 게임에 몇 가지 양자 특성을 추가한 변형 게임입니다.\n이 게임에서는 때때로 말이 동시에 두 곳에 있을 수 있는데, 이를 양자 중첩(Quantum Superposition)이라고 합니다.\n이는 양자 이동(Quantum Move)을 할 때 발생합니다. 양자 이동은 두 개의 고전적인 이동이 동시에 이루어진 결과로,\n이 경우 해당 말의 정확한 위치를 알 수 없게 됩니다. 말의 위치는 관측(Observation)이 일어날 때 정의됩니다.\n관측이 일어나는 경우는 누군가가 양자 말을 잡거나, 양자 말이 다른 말을 잡을 때입니다.\n이때 말이 각기 다른 위치에 있을 확률이 50%씩 됩니다. 이는 양자 얽힘(Quantum Entanglement)을 가능하게 합니다.\n만약 양자 말이 특정 위치에 있을 확률이 있다면, 그 말이 그 자리에 없을 확률도 존재하며, 슬라이드 이동(Slide Move)을 통해\n그 말을 지나칠 수 있습니다. 이 경우, 그 말이 이동을 했는지 여부는 이전 양자 말의 최종 위치에 따라 달라질 수 있습니다.\n이는 얽힘 상태에 있습니다. 게임에서 승리하려면 상대의 왕을 잡아야 합니다.\n"

while(retry == "yes"):
    rival = input("H를 입력하면 인간 대 인간(Human vs Human) 모드로 플레이합니다. C를 입력하면 인간 대 인공지능(Human vs Machine) 모드로 플레이합니다.\n")
    rival = rival.lower()
    if rival == "h" or rival == "c":
        colour = ""
        if rival in "Cc":
            while colour != "b" and colour != "w":
                colour = input("W를 입력하면 백으로 플레이하고, B를 입력하면 흑으로 플레이합니다.\n")
                colour = colour.lower()
        print("Type 'Help' + Intro for command details\n\n")
        while (myGame.over == False):
            try:
                print(myGame.position.strOpt2())
                msg = ""
                if rival == "h" or myGame.flagList[0] == colour:
                    if myGame.flagList[0] == "w":
                        msg = "White to move\nInsert a valid move:\n"
                    else:
                        msg = "Black to move\nInsert a valid move:\n"
                    move = input(msg)
                else:
                    print("\n생각 중...\n\n")
                    hint = myGame.moveHint()  
                    hintIndex = 0 
                    move = Move.Move(hint[hintIndex][0], myGame.flagList)
                    flag = True
                    while move.isQuantic() and flag:
                        if Game.ChessUtils.isCapture(move.move0) or Game.ChessUtils.isCapture(move.move1):
                            hintIndex += 1
                            move = Move.Move(hint[hintIndex][0], myGame.flagList)
                        else:
                            flag = False
                    if move.isQuantic():
                        move = move.move0.move, ", ", move.move1.move
                    else:
                        move = move.move
                if move.lower() == "help":
                    print(helpLine)
                if move.lower() == "rules":
                    print(rules)
                if move.lower() == "evaluate":
                    print(myGame.evaluate())
                if move.lower() == "evaluate move":
                    moveEval = input("Insert move to evaluate:\n")
                    if re.search(pattern, moveEval) is not None:
                        myGame.evaluate(moveEval)

                    if re.search(patternQ, moveEval) is not None:
                        moves = moveEval.split(", ")
                        myGame.evaluate(moves[0], moves[1])

                    print(myGame.evaluate())
                if move.lower() == "hint":
                    print(myGame.moveHint())
                if move.lower() == "over":
                    sure = input("확실합니까? ")
                    if sure == "yes":
                        myGame.over = "Game ended by player"
                        break
                if move == "reset":
                    sure = input("확실합니까? ")
                    if sure == "yes":
                        myGame = Game.Game()
                        break
                if re.search(pattern, move) is not None:
                    myGame.move(move)

                if re.search(patternQ, move) is not None:
                    moves = move.split(", ")
                    myGame.qMove(moves[0], moves[1])
            except Exception as e:
                print("An error occurred:", e)
                input()
        else:
            print(myGame.position.strOpt2())
            print("게임 오버! " + str(myGame.over))
            retry = input("다시 플레이하시겠습니까? ").lower()
    else:
        print("Insert a valid rival")