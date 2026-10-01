from src.pose_tools import angle
def test_right_angle():
    assert abs(angle((1,0),(0,0),(0,1))-90)<1e-6
