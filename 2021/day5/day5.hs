import Data.List (map)
import Data.List.Extra
import qualified Data.Map as Map
type Number = Int

data Point = Point Number Number deriving Show
data Segment = Segment Point Point deriving Show


delta' :: Number -> Number -> Number
delta' a b
  | a == b = 0
  | a > b = (-1)
  | a < b = 1


delta :: Point -> Point -> (Number, Number)
delta (Point x y) (Point xp yp) = (delta' x xp, delta' y yp)


segmentPoints :: Segment -> [Point]
segmentPoints (Segment p1 p2)
  | p1x == p2x && p1y == p2y = [p2]
  | otherwise = p1:(segmentPoints (Segment (Point (p1x + dx) (p1y + dy)) p2))
 where (dx, dy) = delta p1 p2
       (Point p1x p1y) = p1
       (Point p2x p2y) = p2


getPoint :: Point -> (Int, Int)
getPoint (Point x y) = (x, y)


parsePoint :: String -> Point
parsePoint inputString = Point (read xs :: Int) (read ys :: Int)
  where [xs, ys] = splitOn "," inputString 


updateCounter :: (Int, Int) -> Map.Map (Int, Int) Int -> Map.Map (Int, Int) Int
updateCounter (x, y) counterSet
  | Map.member (x, y) counterSet = Map.update (\v -> Just (v+1)) (x, y) counterSet
  | otherwise = Map.insert (x, y) 1 counterSet


applySegment :: Segment -> Map.Map (Int, Int) Int -> Map.Map (Int, Int) Int
applySegment segment counterSet = foldr updateCounter counterSet allPoints
  where allPoints = map getPoint (segmentPoints segment)


parseSegment :: String -> Segment
parseSegment inputData = Segment (parsePoint part1) (parsePoint part2)
  where [part1, part2] = splitOn " -> " inputData


main :: IO()
main = do
  content <- readFile "day5.txt"
  let rawContent = lines content :: [String]
  let allSegments = Data.List.map parseSegment rawContent
  let horizontalAndVerticalSegments = filter (\(Segment (Point x y) (Point xp yp)) -> (x == xp || y == yp)) allSegments
  let partOne = foldr applySegment Map.empty horizontalAndVerticalSegments
  let partTwo = foldr applySegment Map.empty allSegments
  let allPointsWithoutDiag = length $ filter (\(k, v) -> v > 1) (Map.toList partOne)
  let allPointsWithDiag = length $ filter (\(k, v) -> v > 1) (Map.toList partTwo)
  print ("only horizontal and vertical points = " ++ (show allPointsWithoutDiag))
  print ("all points = " ++ (show allPointsWithDiag))
  return ()


guestFoo :: Char -> String -> [Int]
guestFoo = (guestFoo' 0)

guestFoo' :: Int -> Char -> String -> [Int]
guestFoo' n token (x:xs)
      | (x == token) = (n:(guestFoo' 0 token xs))
      | otherwise = guestFoo' (n+1) token xs
guestFoo' n _ "" = [n]
