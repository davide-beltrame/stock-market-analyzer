def query(stock : str, corr_level : int) -> list:
    queue=[stock]
    print(queue)
    visited=[stock]
    lvl_container = [stock]
    temporary_lvl_container= []
    sorted_lvl_container=[]
    counter = 0
    while counter<corr_level:
        if len(queue)==0:
            return 
        lvl_container.pop(0)
        a=queue.pop(0)
        for i in corr_graph_adj[a]:
            if i not in visited:
                visited.append(i)
                queue.append(i)
                temporary_lvl_container.append(i)
        if len(lvl_container) == 0:
            lvl_container = temporary_lvl_container
            temporary_lvl_container= []
            counter+=1
            
    while len(lvl_container)>0:
        minimum=min(lvl_container)
        sorted_lvl_container.append(minimum)
        lvl_container.remove(minimum)
    return sorted_lvl_container

def query(stock : str, corr_level : int) -> list:
    queue=[stock]
    marked_list=[stock]
    level_list = [stock]
    temporary_level_list= []
    sorted_level_list=[]
    counter = 0
    while counter<corr_level:
        if len(queue)==0:
            return 
        level_list.pop(0)
        a=queue.pop(0)
        for i in adjacency_list[a]:
            if i not in marked_list:
                marked_list.append(i)
                queue.append(i)
                temporary_level_list.append(i)
        if len(level_list) == 0:
            level_list = temporary_level_list
            temporary_level_list= []
            counter+=1
            
    while len(level_list)>0:
        minimum=min(level_list)
        sorted_level_list.append(minimum)
        level_list.remove(minimum)
    return sorted_level_list