from reusableClasses.vector2 import Vector2

def Swap(v1, v2):
    return v2, v1

class Collision:
    @staticmethod
    def PointOnPoint(p1, p2):
        if p1.x == p2.x and p1.y == p2.y:
            return True
        return False

    @staticmethod
    def PointOnCircle(p, cPos, cRad):
        length = (p - cPos).length
        if length <= cRad:
            return True
        return False

    @staticmethod
    def PointOnRect(p, rPos, rWidth, rHeight):
        if rPos.x <= p.x <= rPos.x + rWidth and rPos.y <= p.y <= rPos.y + rHeight:
            return True
        return False

    @staticmethod
    def CircleOnCircle(c1Pos, c1Rad, c2Pos, c2Rad):
        length = (c2Pos - c1Pos).length
        if length <= c1Rad + c2Rad:
            return True
        return False

    @staticmethod
    def CircleOnRect(circlePos, circleRadius, rPos, rWidth, rHeight):
        # nearest is the closest point on the rect to the middle of the circle
        nearest = Vector2()
        nearest.x = max(rPos.x, min(circlePos.x, rPos.x + rWidth))
        nearest.y = max(rPos.y, min(circlePos.y, rPos.y + rHeight))

        if (nearest - circlePos).length <= circleRadius:
            return True

        return False

    @staticmethod
    def RectOnRect(r1Pos, r1w, r1h, r2Pos, r2w, r2h):  # this function takes in bottom left points
        if r1Pos.x + r1w >= r2Pos.x >= r1Pos.x - r2w and r1Pos.y + r1h >= r2Pos.y >= r1Pos.y - r2h:
            return True

        return False

    @staticmethod
    def PointOnLine(p, lineP1, lineP2, buffer=0.05):  # buffer is how strict you want the point touching the line to be
        l1ToPoint = (lineP1 - p).length
        l2ToPoint = (lineP2 - p).length

        lengthOfLine = (lineP2 - lineP1).length

        if abs(l1ToPoint + l2ToPoint - lengthOfLine) < buffer:
            return True
        return False

    @staticmethod
    def CircleOnLine(cPos, cRad, lineP1, lineP2):
        # if circle is on any of the points of the line
        if Collision.PointOnCircle(lineP1, cPos, cRad) or Collision.PointOnCircle(lineP2, cPos, cRad):
            return True

        line = (lineP2 - lineP1)  # creating a vector from the line Points
        p1ToCPos = cPos - lineP1

        # dot is how much you multiply the direction by to get the closest point of the line
        dot = line.DotProduct(p1ToCPos) / line.length ** 2

        closestPointOnLine = lineP1 + line * dot

        # if closestPointOnLine is actually on the line, and the circle is colliding with closestPointOnLine
        if Collision.PointOnLine(closestPointOnLine, lineP1, lineP2) and (closestPointOnLine - cPos).length < cRad:
            return True

        return False

    @staticmethod
    def LineOnLine(p0, p1, p2, p3, intersection=Vector2()):
        # i have no idea whats going on here anymore
        denominator = ((p3.y - p2.y) * (p1.x - p0.x) - (p3.x - p2.x) * (p1.y - p0.y))
        if denominator == 0:
            return False

        uA = ((p3.x - p2.x) * (p0.y - p2.y) - (p3.y - p2.y) * (p0.x - p2.x)) / denominator
        uB = ((p1.x - p0.x) * (p0.y - p2.y) - (p1.y - p0.y) * (p0.x - p2.x)) / denominator

        if 0 <= uA <= 1 and 0 <= uB <= 1:
            intersection.x = p0.x + (uA * (p1.x - p0.x))
            intersection.y = p0.y + (uA * (p1.y - p0.y))
            return True
        return False

    @staticmethod
    def RectOnLine(rPos, rWidth, rHeight, p1, p2):  # this function only checks if the line is colliding with the edges
        topColliding = Collision.LineOnLine(p1, p2, rPos, Vector2(rPos.x + rWidth, rPos.y))
        leftColliding = Collision.LineOnLine(p1, p2, rPos, Vector2(rPos.x, rPos.y + rHeight))
        botColliding = Collision.LineOnLine(p1, p2, Vector2(rPos.x, rPos.y + rHeight), rPos + Vector2(rWidth, rHeight))
        rightColliding = Collision.LineOnLine(p1, p2, rPos + Vector2(rWidth, rHeight), Vector2(rPos.x + rWidth, rPos.y))

        if topColliding or leftColliding or botColliding or rightColliding:
            return True
        return False

    @staticmethod
    def RectOnPoly(rectPos, rWidth, rHeight, vertices):
        n = 0
        for current in range(len(vertices)):
            n = current + 1
            if n == len(vertices):
                n = 0

            vc = vertices[current]
            vn = vertices[n]

            collision = Collision.RectOnLine(rectPos, rWidth, rHeight, vc, vn)
            if collision:
                return True

            # not testing if the rect is inside the polygon
        return False