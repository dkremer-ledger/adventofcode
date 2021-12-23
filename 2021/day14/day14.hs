import qualified Data.Map as Map

type Element = Char
type Polymer = [Element]
type Translator = Map.Map (Element, Element) Element

parseSequence :: String -> ((Element, Element), Element)
parseSequence inputStr = ((e1, e2), e3)
 where [e1, e2, _, _, _, _, e3] = inputStr

translator :: [String] -> Translator
translator = Map.fromList . (map parseSequence)

polymerize :: Translator -> [Element] -> [Element]
polymerize t (x:y:xs) = (x:(t Map.! (x, y)):(polymerize t (y:xs)))
polymerize _ [z] = [z]

apply :: Int -> (a -> a) -> a -> a
apply n f x
    | n > 0 = apply (n-1) f (f x)
    | n == 0 = x
    | otherwise = undefined


countElems :: (Ord a) => [a] -> Map.Map a Int
countElems = Map.fromListWith (+) . flip zip (repeat 1)

main :: IO()
main = do
  content <- readFile "input.txt"
  let all_data = lines content
  let sequence = head all_data
  let pairs = translator (tail (tail all_data))
  print (show pairs)
  print (countElems (apply 25 (polymerize pairs) sequence))
  return ()

