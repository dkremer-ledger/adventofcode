import Data.Bits as Bits

type Number = Int
type BingoBoard = [[Number]]
type BingoSequence = [Number]

winningBoard :: BingoSequence -> BingoBoard -> Bool
winningBoard = undefined


boardWinsAt :: BingoSequence -> BingoBoard -> Int


main :: IO()
main = do
  content <- readFile "day3.txt"
  let bitVectors = map fromBinString (lines content) :: [BitVector]
  let counters = applyCounter bitVectors :: [Counter]
  print ("gamma: " ++ (show (getGamma counters)))
  print ("epsilon: " ++ (show (getEpsilon counters)))
  print ("oxygen: " ++ (show (getIntFromBin $ selectOxygen 0 bitVectors)))
  print ("dioxyd: " ++ (show (getIntFromBin $ selectDioxyd 0 bitVectors)))
  return ()

