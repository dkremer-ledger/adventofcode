type Depth = Int
type Horizontal = Int
type Aim = Int

data Move = Up Int | Down Int | Forward Int

data Position = Position Depth Horizontal
data RealPosition = RealPosition Depth Horizontal Aim deriving Show


parseMove :: String -> Move
parseMove inputString = makeMove move value where
  [move,  _value] = words inputString
  value = read _value :: Int


makeMove :: String -> Int -> Move
makeMove move value
  | move == "up" = Up value
  | move == "down" = Down value
  | move == "forward" = Forward value

applyMove :: Move -> Position -> Position
applyMove (Up z) (Position d h) = Position (d-z) h
applyMove (Down z) (Position d h) = Position (d + z) h
applyMove (Forward x) (Position d h) = Position d (h + x)

applyMove' :: Move -> RealPosition -> RealPosition
applyMove' (Up z) (RealPosition d h a) = RealPosition d h (a - z)
applyMove' (Down z) (RealPosition d h a) = RealPosition d h (a + z)
applyMove' (Forward x) (RealPosition d h a) = RealPosition (d + (x * a)) (h + x) a


testData :: [Move]
testData = [(Forward 5), (Down 5), (Forward 8), (Up 3), (Down 8), (Forward 2)]
{-
0 5 0
0 5 5
40 13 5
40 13 2
40 13 10
60 15 
-}

main :: IO()
main = do
  content <- readFile "day2.txt"
  let moves = map parseMove (lines content) :: [Move]
  let (Position a b) = foldr applyMove (Position 0 0) moves 
  let (RealPosition c d e) = foldr applyMove' (RealPosition 0 0 0) $ reverse moves
  print ("real position: " ++ (show c) ++" " ++ (show d) ++ " " ++ (show e))
  print ("answer 1: " ++ (show (a * b)))
  print ("answer 2: " ++ (show (c * d)))
  return ()

