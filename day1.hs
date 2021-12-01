stepUp :: [Int] -> Int
stepUp (x:y:z) = (+) (bigger x y) (stepUp (y:z))
  where bigger x y = if (y > x) then 1 else 0
stepUp [_] = 0


smoothData :: [Int] -> [Int]
-- Will output a list whose elements are
-- the sum of 3 adjacent elements. If the input list
-- has size N and the window size is W, then the resulting
-- list has size N - W + 1
smoothData (x:y:z:w) = (x+y+z):(smoothData (y:z:w))
smoothData (x:y:null) = null


main :: IO()
main = do
  content <- readFile "day1.txt"
  let my = map read (lines content) :: [Int]
  print ("answer 1: " ++ (show (stepUp my)))
  print ("answer 2: " ++ (show (stepUp (smoothData my))))
  return ()

