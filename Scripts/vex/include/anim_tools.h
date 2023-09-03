vector get_non_collinear_vec(int geometry, start_pt; float collinear_threshold; vector normal){
    vector test_vector;
    int max_pts = npoints(geometry);
    for (int i=start_pt; i < max_pts; i++){
        test_vector = normalize(point(geometry, "P", i) - point(0, "P", 0));
        if ( 1 - abs(dot(normal, test_vector)) > collinear_threshold){
            test_vector = normalize(cross(normal, test_vector));
            start_pt = i;
            break;
        }
    }
    return test_vector;
} 