import matplotlib.pyplot as plt
import math

#获取最底部的点的索引
def get_bottom_point(points):
    min_index = 0
    n = len(points)
    for i in range(0, n):
        if points[i][1] < points[min_index][1] or (
                points[i][1] == points[min_index][1] and points[i][0] < points[min_index][0]):
            min_index = i
    return min_index

#点排序
def sort_polar_angle_cos(points, center_point):
    n = len(points)
    cos_value = []
    rank = []
    norm_list = []
    for i in range(0, n):
        point_ = points[i]
        point = [point_[0] - center_point[0], point_[1] - center_point[1]]
        rank.append(i)
        norm_value = math.sqrt(point[0] * point[0] + point[1] * point[1])
        norm_list.append(norm_value)
        if norm_value == 0:
            cos_value.append(1)
        else:
            cos_value.append(point[0] / norm_value)

    for i in range(0, n - 1):
        index = i + 1
        while index > 0:
            if cos_value[index] > cos_value[index - 1] or (
                    cos_value[index] == cos_value[index - 1] and norm_list[index] > norm_list[index - 1]):
                temp = cos_value[index]
                temp_rank = rank[index]
                temp_norm = norm_list[index]
                cos_value[index] = cos_value[index - 1]
                rank[index] = rank[index - 1]
                norm_list[index] = norm_list[index - 1]
                cos_value[index - 1] = temp
                rank[index - 1] = temp_rank
                norm_list[index - 1] = temp_norm
                index = index - 1
            else:
                break
    sorted_points = []
    for i in rank:
        sorted_points.append(points[i])

    return sorted_points

#向量夹角
def vector_angle(vector):
    norm_ = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    if norm_ == 0:
        return 0

    angle = math.acos(vector[0] / norm_)
    if vector[1] >= 0:
        return angle
    else:
        return 2 * math.pi - angle

#叉乘
def coss_multi(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

#graham算法获取凸包
def graham_scan(points):
    bottom_index = get_bottom_point(points)
    bottom_point = points.pop(bottom_index)
    sorted_points = sort_polar_angle_cos(points, bottom_point)

    m = len(sorted_points)
    if m < 2:
        print("点数太少")
        return

    stack = []
    stack.append(bottom_point)
    stack.append(sorted_points[0])
    stack.append(sorted_points[1])

    for i in range(2, m):
        length = len(stack)
        top = stack[length - 1]
        next_top = stack[length - 2]
        v1 = [sorted_points[i][0] - next_top[0], sorted_points[i][1] - next_top[1]]
        v2 = [top[0] - next_top[0], top[1] - next_top[1]]

        while coss_multi(v1, v2) >= 0:
            stack.pop()
            length = len(stack)
            top = stack[length - 1]
            next_top = stack[length - 2]
            v1 = [sorted_points[i][0] - next_top[0], sorted_points[i][1] - next_top[1]]
            v2 = [top[0] - next_top[0], top[1] - next_top[1]]

        stack.append(sorted_points[i])

    return stack

#绘制凸包
def draw_convex(points):


    for point in points:
        plt.scatter(point[0], point[1], marker='o', c='y')

    result = graham_scan(points)

    length = len(result)
    for i in range(0, length - 1):
        plt.plot([result[i][0], result[i + 1][0]], [result[i][1], result[i + 1][1]], c='r')
    plt.plot([result[0][0], result[length - 1][0]], [result[0][1], result[length - 1][1]], c='r')

    plt.show()


#将点集列表转化为mysql的POLYGON形式
def to_mysql_polygon(data):
    result = graham_scan(data)
    s = 'POLYGON(('
    for i in result:
        s += str(i[0]) + ' ' + str(i[1]) + ','

    s += str(result[0][0]) + ' ' + str(result[0][1])
    s += '))'

    return s


if __name__ == "__main__":
    data = [[116.236251, 40.183305], [116.246967, 40.183759], [116.238625, 40.189273], [116.234562, 40.184841],
            [116.240078, 40.181002], [116.240692, 40.183715], [116.235265, 40.184781], [116.233922, 40.186167],
            [116.247196, 40.187985], [116.238672, 40.184381], [116.243026, 40.187838], [116.234284, 40.184364],
            [116.245725, 40.182635], [116.243994, 40.186024], [116.238663, 40.184391], [116.243249, 40.185246],
            [116.243711, 40.18606], [116.242739, 40.188273], [116.235347, 40.185568], [116.239285, 40.185402],
            [116.238666, 40.184385], [116.250227, 40.180736], [116.245264, 40.189548], [116.243206, 40.184429],
            [116.242444, 40.18879], [116.241752, 40.184005], [116.238722, 40.185807], [116.241775, 40.183641],
            [116.251913, 40.184393], [116.243922, 40.183213], [116.241942, 40.183983], [116.237218, 40.184425],
            [116.25006, 40.187561], [116.24505, 40.183451], [116.248444, 40.185431], [116.247446, 40.186598],
            [116.246414, 40.185847], [116.240692, 40.183715], [116.244497, 40.182686], [116.242264, 40.183156],
            [116.243261, 40.18392], [116.245186, 40.189377], [116.243734, 40.183981], [116.239217, 40.184254],
            [116.242925, 40.188126], [116.235441, 40.184743], [116.243265, 40.187532], [116.238625, 40.189273],
            [116.235436, 40.184743], [116.240696, 40.183715], [116.233751, 40.184224], [116.243297, 40.186485],
            [116.239168, 40.183866], [116.243937, 40.185041], [116.234199, 40.185452], [116.236235, 40.185678],
            [116.243636, 40.184156], [116.246456, 40.189433], [116.243255, 40.185506], [116.243539, 40.185594],
            [116.243664, 40.182474], [116.238672, 40.184381], [116.243109, 40.183921], [116.241789, 40.183495],
            [116.251937, 40.184806], [116.243079, 40.189434], [116.242666, 40.18561], [116.247196, 40.187985],
            [116.238152, 40.184407], [116.240593, 40.183844], [116.243406, 40.188098], [116.243452, 40.18686],
            [116.243113, 40.186857], [116.243142, 40.18513], [116.245725, 40.182635], [116.243065, 40.188033],
            [116.235031, 40.185353], [116.245127, 40.185246], [116.240347, 40.188447], [116.238666, 40.184385],
            [116.238235, 40.184353], [116.241856, 40.18389], [116.235572, 40.184405], [116.235347, 40.185568],
            [116.240535, 40.181516], [116.234284, 40.184364], [116.243587, 40.185398], [116.239743, 40.184223],
            [116.243994, 40.186024], [116.238638, 40.184376], [116.245283, 40.184817], [116.238063, 40.184042],
            [116.243776, 40.183691], [116.238851, 40.184361], [116.243574, 40.185943], [116.238703, 40.185946],
            [116.246967, 40.183759], [116.23925, 40.184396], [116.243306, 40.186498], [116.240078, 40.181002],
            [116.243255, 40.187636], [116.23928, 40.185662], [116.233922, 40.186167], [116.243542, 40.186144],
            [116.238663, 40.184391], [116.243278, 40.186613], [116.240695, 40.183714], [116.243113, 40.186857],
            [116.242771, 40.183929], [116.242696, 40.188253], [116.249239, 40.187972], [116.240578, 40.181237],
            [116.239283, 40.185406], [116.236194, 40.186141], [116.247728, 40.18346], [116.239285, 40.185402],
            [116.238725, 40.188501], [116.239174, 40.186946], [116.243506, 40.185952], [116.243508, 40.186133],
            [116.238089, 40.184134], [116.234019, 40.184], [116.243343, 40.185681], [116.238463, 40.184369],
            [116.236251, 40.183305], [116.250536, 40.183761], [116.243249, 40.185246], [116.234562, 40.184841]]

    draw_convex(data)

