import Data.Bits as Bits

type One = Int
type Zero = Int
type Position = Int
type BitValue = Int
type BitVector = [BitValue]

data Counter = Counter Zero One deriving Show


updateCounter :: [Counter] -> BitVector -> [Counter]
updateCounter ((Counter z o):rC) (currentBit:rB)
  | currentBit == 1 = (Counter z (o+1)):(updateCounter rC rB)
  | currentBit == 0 = (Counter (z+1) o):(updateCounter rC rB)
  | otherwise = undefined
updateCounter [] _ = []
updateCounter _ [] = []


fromBinString :: [Char] -> BitVector
fromBinString = map getBit where
  getBit b = (if b == '1' then 1 else if b == '0' then 0 else undefined)


applyCounter :: [BitVector] -> [Counter]
applyCounter [] = []
applyCounter bitVectors = foldl updateCounter initCounter bitVectors
  where initCounter = map fst (zip (repeat (Counter 0 0)) (head bitVectors)) 


selectOxygen :: Position -> [BitVector] -> BitVector
selectOxygen _ [x] = x
selectOxygen n bitVectors = selectOxygen (n+1) filteredResults
  where filteredResults = selectOxygen' n bitVectors


selectDioxyd :: Position -> [BitVector] -> BitVector
selectDioxyd _ [x] = x
selectDioxyd n bitVectors = selectDioxyd (n+1) filteredResults
  where filteredResults = selectDioxyd' n bitVectors


selectOxygen' :: Int -> [BitVector] -> [BitVector]
selectOxygen' bitPosition vectors = filter (\vec -> (vec !! bitPosition) == mostCommonBitValue) vectors
  where mostCommonBitValue = mostCommonAt 1 bitPosition vectors

selectDioxyd' :: Int -> [BitVector] -> [BitVector]
selectDioxyd' bitPosition vectors = filter (\vec -> (vec !! bitPosition) == leastCommonBitValue) vectors
  where leastCommonBitValue = leastCommonAt 0 bitPosition vectors


mostCommonAt :: BitValue -> Int -> [BitVector] -> BitValue
mostCommonAt defaultValue bitPosition vectors
  | (zeros > ones) = 0
  | (ones > zeros) = 1
  | otherwise = defaultValue
 where (Counter zeros ones) = (applyCounter vectors) !! bitPosition

leastCommonAt :: BitValue -> Int -> [BitVector] -> BitValue
leastCommonAt defaultValue bitPosition vectors
  | (zeros < ones) = 0
  | (ones < zeros) = 1
  | otherwise = defaultValue
 where (Counter zeros ones) = (applyCounter vectors) !! bitPosition


selectCarbonDioxyd :: [BitVector] -> BitVector
selectCarbonDioxyd = undefined


getGamma' :: [Counter] -> [Int]
getGamma' = map (\(Counter z o) -> (if z > o then 0 else 1)) 


getEpsilon' :: [Counter] -> [Int]
getEpsilon' = map (\(Counter z o) -> (if z > o then 1 else 0))


getIntFromBin :: BitVector -> Int
getIntFromBin inputBits = sum $ map (Bits.bit . snd) (filter (\(bit, bitPos) -> (bit == 1)) (zip (reverse inputBits) [0..]))


getEpsilon :: [Counter] -> Int
getEpsilon = getIntFromBin . getEpsilon'
getGamma :: [Counter] -> Int
getGamma = getIntFromBin . getGamma'


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

