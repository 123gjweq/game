def Approach(goal, current, dt):
    difference = goal - current
    if difference > dt:
        return current + dt
    if difference < -dt:
        return current - dt

    return goal