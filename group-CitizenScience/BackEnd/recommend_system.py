from backend.models import *
import math
import json


def branch_recommend(this_project_list, projects):
    recommend_list = []
    this_branches = []
    for this_project_id in this_project_list:
        this_branches += projects[this_project_id]
    this_branches = list(set(this_branches))
    branch_num = len(this_branches)
    for project_id in projects:
        project_branches = projects[project_id]
        for branch in project_branches:
            if branch in this_branches:
                recommend_list.append(project_id)
    recommend_list = list(set(recommend_list))
    recommend_len = min(3 * branch_num, len(recommend_list))
    recommend_list = recommend_list[:recommend_len]
    return recommend_list


def minrkov(rating1, rating2, n):
    distance = 0
    commonRatings = False
    for key in rating1:
        if key in rating2:
            distance += abs((rating1[key] - rating2[key])**n)
            commonRatings = True
    if commonRatings:
        return distance**1/n
    else:
        return -1  # Indicates no ratings in common


def pearson_sim(rating1, rating2):
    distance = 0
    common = []
    for key in rating1:
        if key in rating2:
            common.append(key)
    if len(common) == 0:
        return 0  # 没有共同项目，直接返回0
    # 1. 评分和
    sum1 = sum([rating1[key] for key in common])
    sum2 = sum([rating2[key] for key in common])
    # 2. 评分平方和
    square_sum1 = sum([pow(rating1[key], 2) for key in common])
    square_sum2 = sum([pow(rating2[key], 2) for key in common])
    # 3. 乘积和
    product_sum = sum([rating1[key] * rating2[key] for key in common])
    # 4. 相关系数
    n = len(common)
    num = product_sum - (sum1 * sum2 / n)
    den = math.sqrt((square_sum1 - pow(sum1, 2) / n)
                    * (square_sum2 - pow(sum2, 2) / n))
    return 0 if den == 0 else num / den


def computeNearestNeighbor(user_id, users, mode="minrkov"):
    # mode: 1)minrkov 2)pearson
    if mode == "minrkov":
        distances = []
        for neighbor_user in users:
            if neighbor_user != user_id and (neighbor_user != '' and user_id != ''):
                # print(neighbor_user)
                # print(user_id)
                distance = minrkov(
                    users[int(neighbor_user)], users[int(user_id)], 2)
                if distance != -1:
                    distances.append((distance, neighbor_user))
        # sort based on distance -- closest first
        distances.sort(key=lambda tup: tup[0])
        return distances
    elif mode == "pearson":
        sims = []
        for neighbor_user in users:
            if neighbor_user != user_id and (neighbor_user != '' and user_id != ''):
                sim = pearson_sim(
                    users[int(neighbor_user)], users[int(user_id)], 2)
                sims.append((sim, neighbor_user))
        # sort based on distance -- closest first
        sims.sort(key=lambda tup: tup[0], reverse=True)
        return sims


def collaborative_recommend(user_id, users, dis_mode):
    nearest_list = computeNearestNeighbor(user_id, users, dis_mode)
    nearest_list = [nearest_list[i][1]
                    for i in range(min(5, len(nearest_list)))]
    recommendations = {}
    for nearest in nearest_list:
        neighborRatings = users[nearest]
        userRatings = users[int(user_id)]
        for project in neighborRatings:
            if not project in userRatings:
                recommendations[project] = recommendations.get(
                    project, 0) + neighborRatings[project]
    ret_list = list(recommendations.items())
    ret_list.sort(key=lambda i: i[1], reverse=True)
    return ret_list


def get_recommended(user_id):
    print(user_id)
    user_id = int(user_id)
    print(user_id)
    # 构建users   {user_id: {project_id: score}}
    user_project_list = UserProject.query.all()
    users_list = UserProject.query.with_entities(
        UserProject.user_id).distinct().all()
    users = {}
    for user in users_list:
        users.setdefault(user.user_id, {})
    for user_project in user_project_list:
        score = 0
        if user_project.is_participated:
            score += 5
        if user_project.is_starred:
            score += 3
        if user_project.is_liked:
            score += 1
        if score != 0:
            score += 8
        users[user_project.user_id].setdefault(user_project.project_id, score)
    # 构建projects    {project_id: [branches]}
    project_list = Project.query.filter_by(project_status=ProjectStatus.VERIFIED).all()
    projects = {}
    for one_project in project_list:
        projects[one_project.project_id] = json.dumps(one_project.branch)
    # 【基于主题的推荐】branch_list
    user_related_project_list = list(users[user_id].keys())
    branch_list = branch_recommend(user_related_project_list, projects)
    # 【协同过滤】collaborative_list
    dis_mode = "minrkov"
    collaborative_list = collaborative_recommend(user_id, users, dis_mode)
    collaborative_list = [i[0] for i in collaborative_list]
    project_num = len(list(users[user_id].keys()))
    collaborative_len = min(2 * project_num, len(collaborative_list))
    collaborative_list = collaborative_list[:collaborative_len]
    # 构建project_hot   {project_id: total_score}
    project_hot = {}
    for user in users:
        for project in users[user]:
            project_hot[project] = project_hot.get(
                project, 0) + users[user][project]
    # 【最热门】hot_list
    hot_list = sorted(project_hot.items(), key=lambda kv: (kv[1], kv[0]))
    hot_list = [i[0] for i in hot_list]
    print("branch_list = ", branch_list)
    print("collaborative_list =", collaborative_list)
    print("hot_list =", hot_list)
    intersection = list(set(branch_list).intersection(set(collaborative_list)))
    branch_difference = list(set(branch_list).difference(set(intersection)))
    collaborative_difference = list(
        set(collaborative_list).difference(set(intersection)))
    return_list = intersection + branch_difference + collaborative_difference
    hot_difference = list(set(hot_list).difference(set(return_list)))
    return_list += hot_difference
    return_list = return_list[:20]
    print("推荐列表 = ", return_list)
    return return_list
