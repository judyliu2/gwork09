from display import *
from matrix import *
from math import *
from gmath import *
import random

'''
* Call in draw_polygons
* Color changes for each triangle
'''
def scanline_convert(polygons, i, screen, zbuffer ):
    bot = polygons[i]
    mid = polygons[i+1]
    top = polygons[i+2]

    if (bot[1] > top[1]):
        temp_m = top
        top = bot
        bot = temp_m
    if (bot[1]> mid[1]):
        temp_m = mid
        mid = bot
        bot = temp_m
    if (mid[1] == bot[1] and mid[0] < bot[0]):
        temp_m = mid
        mid = bot
        bot = temp_m
    if (mid[1]> top[1]):
        temp_m = top
        top = mid
        mid = temp_m
    if (mid[1] == top[1] and mid[0] < top[0]):
        temp_m = top
        top = mid
        mid = temp_m

    #x = 0
    #point in the top left is TOP
    #point in the bottom left is BOT
    '''

    y_max = max (point_0[1],point_1[1],point_2[1])
    y_min = min (point_0[1],point_1[1],point_2[1])
    a = 0
    while a < 3:
        if(y_max == triangle[a][1]):
            if(a_max):
                mid = top
                top = triangle[a]
            else:
                if (triangle[a][0]< x):
                    top = triangle[a]
                    x = triangle[a][0]
        elif(triangle[a][1] < y_max and triangle[a][1] < y_min):
                mid = triangle[a]
        elif(y_min == triangle[a][1]):
            if(a_min):
                    mid = bot
                    bot = triangle[a]
            else:
                    if (triangle[a][0] < x):
                        bot = triangle[a]
                        x = triangle[a][0]
       ''' 
    color = [random.randint(1,256),random.randint(1,256),random.randint(1,256)]
    y = bot[1]
    x0 = bot[0]
    x1 = bot[0]
    z0 = bot[2]
    z1 = bot[2]
    while y < mid[1]:
        y+=1
        if(mid[1] !=bot[1] ):
            draw_line(int(x0),int(y),z0,int(x1),int(y),z1, screen, zbuffer, color)
            x0 += (top[0] - bot[0]) / (top[1] - bot[1])
            x1 += (mid[0] - bot[0]) / (mid[1] - bot[1])
            z0 += (top[2] - bot[2]) / (top[1] - bot[1])
            z1 += (mid[2] - bot[2]) / (mid[1] - bot[1])

    x1 = mid[0]
    z1 = mid[2]
    while y< top[1]:
        y+=1
        if(mid[1] != top[1]):
            draw_line(int(x0),int(y),z0,int(x1),int(y),z1, screen, zbuffer, color)
            x0 += (top[0] - bot[0]) / (top[1] - bot[1])
            x1 += (top[0] - mid[0]) / (top[1] - mid[1])
            z0 += (top[2] - bot[2]) / (top[1] - bot[1])
            z1 += (top[2] - mid[2]) / (top[1] - mid[1])
        


def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0);
    add_point(polygons, x1, y1, z1);
    add_point(polygons, x2, y2, z2);

def draw_polygons( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print 'Need at least 3 points to draw'
        return

    point = 0
    while point < len(matrix) - 2:

        normal = calculate_normal(matrix, point)[:]

        if normal[2] > 0:
            #print matrix[point]
            '''
            draw_line( int(matrix[point][0]),
                       int(matrix[point][1]),
                       matrix[point][2],
                       int(matrix[point+1][0]),
                       int(matrix[point+1][1]),
                       matrix[point+1][2],
                       screen, zbuffer, color)
            draw_line( int(matrix[point+2][0]),
                       int(matrix[point+2][1]),
                       matrix[point+2][2],
                       int(matrix[point+1][0]),
                       int(matrix[point+1][1]),
                       matrix[point+1][2],
                       screen, zbuffer, color)
            draw_line( int(matrix[point][0]),
                       int(matrix[point][1]),
                       matrix[point][2],
                       int(matrix[point+2][0]),
                       int(matrix[point+2][1]),
                       matrix[point+2][2],
                       screen, zbuffer, color)
'''
            scanline_convert(matrix,point,screen,zbuffer)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z);
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z);

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1);
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1);

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1);
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1);
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z);
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z);

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1);
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z);
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z);
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1);

def add_sphere( edges, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)
    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( edges, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( edges, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])

def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus( edges, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)
    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(edges,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(edges,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )

def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt
        zt = z0
        z0 = z1
        z1 = zt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y
            
    start = loop_start
    z_start = z0
    
    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, z_start )
        z_start +=(z1-z0)/ (loop_end - start)
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
            
        loop_start+= 1
    plot( screen, zbuffer, color, x, y, z1 )
