import math
from numbers import Number

def test_number(a, b):
    # raises exception if any x,y,z coordinate in either set is not properly numerical
    # runs  all x,y,z coordinates in each set are numerical this test 
    a = [coord_set[1] for coord_set in a] # only concerned with the x,y,z
    b = [coord_set[1] for coord_set in b] 
    all_xyz_sets = a + b
    num_test = [isinstance(coord, Number) for xyz_set in all_xyz_sets for coord in xyz_set]
    if not all(num_test):
        print "failed numerical data-type test"
        return False
    else:
        return True

def test_origin(a, b):
    # raises exception if the origins of the two coordinate sets are not equivalent
    # returns True if the origins are equivalent 
    # this code assumes only 1 xyz set in each list has the minimal z
    a = [w_coords[1] for w_coords in a] # only concerned with the x,y,z
    b = [w_coords[1] for w_coords in b] 
    
    sorted_a = sorted(a, key = lambda x: x[:][2]) # sort by lowest z-value
    sorted_b = sorted(b, key = lambda x: x[:][2])
    
    x_a, y_a, z_a = sorted_a[0] # returns the coordinate set with minimal z
    x_b, y_b, z_b = sorted_b[0]
    
    d_xyz = [x_a - x_b, y_a - y_b, z_a - z_b] # all values will be 0.0 in the passing case
    
    if any(d_xyz) != 0.0:
        print "failed origin_test"
        return False
    else:
        return True

    
def test_data_validity(func):
    print func.__name__
    def aux(*args):
        tests_list = [test_number(*args), test_origin(*args)]
        if all(tests_list):
            return func(*args)
        else:
            raise Exception("data was not valid")
    return aux

@test_data_validity
def mean_w_displacement(w_list_A, w_list_B): 
    print "in mean"
    # typically w_list_A is a reference to test against ideality
    # this function return the total displacement of x,y,z coordinates in Angstroms
    d_sqrts_list = []
    for coord_set_a in w_list_A:
        # we must ensure we are calculating displacement between corresponding coordinates
        # this is done by returning the minimum dispacement
        # this is a fail-safe in the case that the coordinates are not in the proper order
        d_sqrt_ref = float(1000.0) # an arbitrarily large value, the goal is to minimize d_sqr_tmp
        x_a, y_a, z_a = coord_set_a[1]  # take only the x,y,z values
        for coord_set_b in w_list_B:
            x_b, y_b, z_b = coord_set_b[1]
            x_d = float(x_a) - float(x_b)
            y_d = float(y_a) - float(y_b)
            z_d = float(z_a) - float(z_b) 
            d_sqrt_tmp = math.sqrt(x_d**2 + y_d**2 + z_d**2)
            if d_sqrt_tmp < d_sqrt_ref:
                d_sqrt_ref = d_sqrt_tmp
        d_sqrts_list.append(d_sqrt_ref)    
    sum_ds = sum(d_sqrts_list)

    return sum_ds

# this is the list to calculate displacements against
list_reference = [['W', [0., 0., 0.]],
                 ['W', [4.5, 4.5, 1.5]]]

# test lists
list_pass_both = [['W', [0. ,  0. ,  0.0]],
                  ['W', [4.7805,  4.7805,  1.5935]]]

list_fail_Zorigin = [['W', [0. ,  0. ,  0.1]],
                  ['W', [4.7805,  4.7805,  1.6935]]]

list_fail_reals = [['W', [0. ,  0. ,  0.0]],
                  ['W', ['string',  4.7805,  1.5935]]]

list_fail_both = [['W', [0. ,  0. ,  0.1]],
                  ['W', ['string',  4.7805,  1.5935]]]
    

#mean_w_displacement(list_reference, list_pass_both)
#mean_w_displacement(list_reference, list_fail_Zorigin)
#mean_w_displacement(list_reference, list_fail_reals)
mean_w_displacement(list_reference, list_fail_both)


