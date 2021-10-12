import random

speed = {
    "Rein" : 5.5,
    "Pharah" : 5.5,
    "Tracer" : 6
}

min_x = -50
min_y = -50
max_x = 50
max_y = 50

def mag(vec):
    return (sum(x**2 for x in vec))**0.5

def normalize(vec):
    m = mag(vec)
    return [x/m for x in vec]

def direction_from(startPos, endPos):
    return normalize([endPos[i] - startPos[i] for i in range(len(startPos))])

def distance(v1, v2):
    return mag([v1[i]-v2[i] for i in range(len(v1))])

def multiply(vec, n):
    return [n*x for x in vec]

def add(v1, v2):
    return [v1[i] + v2[i] for i in range(len(v1))]

def in_bounds(pos):
    global min_x, min_y, max_x, max_y
    return pos[0] > min_x and pos[0] < max_x and pos[1] > min_y and pos[1] < min_y

def move_player(startPos, direction, speed):
    return add(startPos, multiply(direction, speed))

# Won't include reinhardt but it's fine
def raycast(startPos_, endPos):
    if in_bounds(endPos):
        return endPos
    startPos = startPos_[:]
    d = direction_from(startPos, endPos)
    while True:
        tempPos = add(startPos, multiply(d, 0.1))
        if in_bounds(tempPos):
            startPos = tempPos
        else:
            break
    return startPos
    
# Returns a direction to escape in (random)
def evade_random(evaderPos, chaserPos, evaderSpeed, chaserSpeed):
    return normalize([random.uniform(-100, 100), random.uniform(-100, 100)])

def evade_avoid_walls(evaderPos, chaserPos, evaderSpeed, chaserSpeed):
    d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
    newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
    currentDist = distance(evaderPos, newPos)
    bestDist = currentDist
    bestDir = d[:]
    for i in range(7):
        d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
        newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
        currentDist = distance(evaderPos, newPos)
        if currentDist > bestDist:
            bestDist = currentDist
            bestDir = d[:]
    return bestDir

def evade_avoid_chaser(evaderPos, chaserPos, evaderSpeed, chaserSpeed):
    d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
    newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
    currentDist = distance(chaserPos, newPos)
    bestDist = currentDist
    bestDir = d[:]
    for i in range(7):
        d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
        newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
        currentDist = distance(chaserPos, newPos)
        if currentDist > bestDist:
            bestDist = currentDist
            bestDir = d[:]
    return bestDir

def evade_avoid_chaser_and_walls(evaderPos, chaserPos, evaderSpeed, chaserSpeed):
    d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
    newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
    currentDist = distance(evaderPos, newPos) + distance(chaserPos, newPos)
    bestDist = currentDist
    bestDir = d[:]
    for i in range(7):
        d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
        newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
        currentDist = distance(evaderPos, newPos) + distance(chaserPos, newPos)
        if currentDist > bestDist:
            bestDist = currentDist
            bestDir = d[:]
    return bestDir

def evade_avoid_chaser_and_walls2(evaderPos, chaserPos, evaderSpeed, chaserSpeed):
    d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
    newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
    currentDist = 5*distance(evaderPos, newPos) + distance(chaserPos, newPos)
    bestDist = currentDist
    bestDir = d[:]
    for i in range(7):
        d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
        newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
        currentDist = 5*distance(evaderPos, newPos) + distance(chaserPos, newPos)
        if currentDist > bestDist:
            bestDist = currentDist
            bestDir = d[:]
    return bestDir

def evade_avoid_chaser_and_walls3(evaderPos, chaserPos, evaderSpeed, chaserSpeed):
    d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
    newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
    currentDist = 10*distance(evaderPos, newPos) + distance(chaserPos, newPos)
    bestDist = currentDist
    bestDir = d[:]
    for i in range(7):
        d = normalize([random.uniform(-100, 100), random.uniform(-100, 100)])
        newPos = raycast(evaderPos, add(evaderPos, multiply(d, evaderSpeed)))
        currentDist = 10*distance(evaderPos, newPos) + distance(chaserPos, newPos)
        if currentDist > bestDist:
            bestDist = currentDist
            bestDir = d[:]
    return bestDir

def closest_to(who, others):
    c = others[0]
    d = distance(who, others[0])
    bestDist = d
    for x in others[1:]:
        d = distance(who, x)
        if d < bestDist:
            bestDist = d
            c = x[:]
    return c

# Returns a direction to chase in    
def chase_1(evaders, chaserPos, evaderSpeed, chaserSpeed):
    return direction_from(chaserPos, closest_to(chaserPos, evaders))

# Tells whether or not a bug dies
def is_dead(evaderPos, chaserPos):
    return distance(evaderPos, chaserPos) <= 1

# Returns a float representing the time 
def do_simulation(evade_func, chase_func, bugCount=10):
    global speed
    bugs = []
    for i in range(bugCount):
        bugs += [[random.uniform(-29,29), random.uniform(-29,29)]]
    rein = [0,0]
    
    step = 0.0
    while len(bugs) > 0:
        for bug_index in range(len(bugs)):
            bugs[bug_index] = move_player(bugs[bug_index], evade_func(bugs[bug_index], rein, speed["Tracer"], speed["Rein"]), speed["Tracer"])
        rein = move_player(rein, chase_func(bugs, rein, speed["Tracer"], speed["Rein"]), speed["Rein"])
        
        tmp_bugs = []
        for bug in bugs:
            if not is_dead(bug, rein):
                tmp_bugs += [bug]
        bugs = tmp_bugs
        # Simulate 0.1s at a time
        step += 0.1
    return step-0.1 # Bugs survived for step seconds


def do_simulations(evade_funcs, chase_func, runs=500, bugCount=20):
    for evade_func in evade_funcs:
        total = 0.0
        for i in range(runs):
            total += do_simulation(evade_func, chase_func, bugCount)
        total /= float(runs)
        print("Evasion method", evade_func.__name__, "average survival time:", total, "seconds.")

do_simulations([evade_random, evade_avoid_walls, evade_avoid_chaser, evade_avoid_chaser_and_walls, evade_avoid_chaser_and_walls2, evade_avoid_chaser_and_walls3], chase_1)



    
    
