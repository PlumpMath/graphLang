import matplotlib.pyplot as plt

# Part 1. High level action model

def wave2(): return besides(flip_vert(wave))
#def wave4(): return below(wave2, wave2)

def flipped_pairs(painter):
    painter2 = beside(painter, flip_vert(painter))
    return below(painter2, painter2)

def wave4() : return flipped_pairs(wave)

def right_split(painter, n):
    if n == 0 : return painter
    smaller = right_split(painter, n-1)
    return beside(painter, below(smaller, smaller))

#def up_split(painter, n) : pass
#def flip_vert(painter) : pass #defined in part 5
#def flip_horiz(painter) : pass
def identity(painter) : pass
def rotate180(painter): pass

def corner_split(painter, n):
    if n == 0 : return painter
    up = up_split(painter, n-1)
    right = right_split(painter, n-1)
    
    top_left = beside(up, up)
    bottom_right = below(right, right)
    corner = corner_split(painter, n-1)

    return beside(below(painter, top_left),
            below(bottom_right, corner))

def square_limit(painter, n):
    quarter = corner_split(painter, n)
    half = beside(flip_horiz(quarter), quarter)
    return below(flip_vert(half), half)

#Part 2. Higher level abstraction
def square_of_four(tl, tr, bl, br):
    def foo(painter):
        top = beside(tl(painter), tr(painter))
        bottom = beside(bl(painter), br(painter))
        return below(bottom, top)
    return foo

def flipped_pairs2(painter): 
    #Re-defined function with abstraction methode square_of_four
    return square_of_four(identity, flip_vert, identity, flip_vert)

def square_pairs2(painter):
    return square_of_four(flip_horiz, identity, rotate180, flip_vert)

# Right-split and up-split can be also expressed as instances of a general splitting 
# operation
def split() : pass
def right_split2() : return split(beside, below)
def up_split2() : return split(below, beside)

#Part 3. Frame
def frame_coord_map(frame):
    def foo(v):
        return add_vect(origin_frame(frame), 
                add_vect( scale_vect( xcor_vect(v),
                                    edge1_frame(frame)),
                          scale_vect( ycor_vect(v),
                                    edge2_frame(frame))))
    return foo

#One possible way to do vector calculation
def make_vect(x, y) : return (x, y)
def xcor_vect(v) : return v[0]
def ycor_vect(v) : return v[1]

def add_vect(v1, v2) : 
    return make_vect( xcor_vect(v1) + xcor_vect(v2),
            ycor_vect(v1) + ycor_vect(v2))

def sub_vect(v1, v2) : 
    return make_vect( xcor_vect(v1) - xcor_vect(v2),
            ycor_vect(v1) - ycor_vect(v2))

def scale_vect(s, v) : 
    return make_vect( s*xcor_vect(v), s*ycor_vect(v))

#One possible implementation of frame calculation
def make_frame(origin, edg1, edge2): return (origin, edg1, edge2)
def origin_frame(f): return f[0]
def edge1_frame(f) : return f[1]
def edge2_frame(f) : return f[2]

## Part 4. Painter
# A painter is represented as a procedure that, given a frame as argument, 
# draws a particular image shifted and scaled to fit the frame.
def segment2painter(segment_list):
    def foo(frame):
        for seg in segment_list:
            draw_line(frame_coord_map(frame)(segment[0]), # A bad representation here. Need abstraction
                    frame_coord_map(frame)(segment[1]))
    return foo

def draw_line(start, end) :
    #plt.plot(start, end)
    # Need to investigate into Matplotlib
    pass

# A painting example
squarePainter = segment2painter([(0, 0.5), (0.5,1), (1, 0.5), (0.5, 0)])
frame = make_frame(make_vect(0,0), make_vect(0, 5), make_vect(5, 0))
squarePainter(frame)

#Part 5. Transforming and combining painters
def transform_painter(painter, origin, corner1, corner2):
    def foo(frame):
        m = frame_coord_map(frame)
        new_origin = m(origin)
        new_frame = make_frame(new_origin, 
                sub_vect(m(corner1), new_origin),
                sub_vect(m(corner2), new_origin))
        return painter(new_frame)
    return foo

def flip_vert(painter):
    return transform_painter(painter, make_vect(0, 1.0),
            make_vect(1.0, 1.0), make_vect(0, 0))
def flip_horiz(painter):
    pass

def rotate90(painter):
	return transform_painter(painter, make_vect(1., 1.), 
            make_vect(1., 1.), make_vect(0, 0))
def ratate180(painter): pass

def beside(painter1, painter2):
    split_point = make_vect(0.5, 0)
    paint_left = transform_painter(painter1, make_vect(0,0), 
			split_point, make_vect(0, 1.))
    paint_left = transform_painter(painter2, make_vect(1.,1.), 
			split_point, make_vect(0.5, 1.))
    def foo(frame): paint_left(frame); paint_right(frame)
    return foo
def below(painter1, painter2): pass
