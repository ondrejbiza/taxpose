import copy
import os

import numpy as np
import plotly.graph_objects as go


def show_pcds_plotly(pcds, center: bool=False, axis_visible: bool=True):

    colorscales = ["Plotly3", "Viridis", "Blues", "Greens", "Greys", "Oranges", "Purples", "Reds"]

    if center:
        tmp = np.concatenate(list(pcds.values()), axis=0)
        m = np.mean(tmp, axis=0)
        pcds = copy.deepcopy(pcds)
        for k in pcds.keys():
            pcds[k] = pcds[k] - m[None]

    tmp = np.concatenate(list(pcds.values()), axis=0)
    lmin = np.min(tmp)
    lmax = np.max(tmp)

    data = []
    for idx, key in enumerate(pcds.keys()):
        v = pcds[key]
        colorscale = colorscales[idx % len(colorscales)]
        pl = go.Scatter3d(
            x=v[:, 0], y=v[:, 1], z=v[:, 2],
            marker={"size": 5, "color": v[:, 2], "colorscale": colorscale},
            mode="markers", opacity=1., name=key)
        data.append(pl)

    layout = {
        "xaxis": {"visible": axis_visible, "range": [lmin, lmax]},
        "yaxis": {"visible": axis_visible, "range": [lmin, lmax]},
        "zaxis": {"visible": axis_visible, "range": [lmin, lmax]},
        "aspectratio": {"x": 1, "y": 1, "z": 1}
    }

    fig = go.Figure(data=data)
    fig.update_layout(scene=layout, showlegend=True)
    fig.show()
    # input("Continue?")


# path = "data/mug_place/train_data/renders/0_teleport_obj_points.npz"
# x = np.load(path, allow_pickle=True)
# # 0: child, 1: parent, 2: gripper.
# d = {
#     "0": x["clouds"][x["classes"] == 0],
#     "1": x["clouds"][x["classes"] == 1],
#     "2": x["clouds"][x["classes"] == 2]
# }
# show_pcds_plotly(d)

# path = "../relational_ndf/src/rndf_robot/data/relation_demos/release_demos/mug_on_rack_relation/place_demo_0.npz"
# x = np.load(path, allow_pickle=True)
# # parent: tree, child: mug.
# d = {
#     "parent": x["multi_obj_final_pcd"].item()["parent"],
#     "child": x["multi_obj_final_pcd"].item()["child"]
# }
# show_pcds_plotly(d)

for name1, name2, rndf_indices in zip(["mug_on_rack_relation", "bowl_on_mug_relation", "bottle_in_container_relation"], ["mug_place", "bowl_place", "bottle_place"], [[0, 1, 2, 4, 6, 7, 8, 9], list(range(10)), [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11]]):

    new_folder = "data/rndf/{:s}/train_data/renders".format(name2)
    if not os.path.isdir(new_folder):
        os.makedirs(new_folder)

    for i in range(len(rndf_indices)):
        old_path = "../relational_ndf/src/rndf_robot/data/relation_demos/release_demos/{:s}/place_demo_{:d}.npz".format(name1, rndf_indices[i])
        new_path = os.path.join(new_folder, "{:d}_teleport_obj_points.npz".format(i))

        x = np.load(old_path, allow_pickle=True)
        parent_pcd = x["multi_obj_final_pcd"].item()["parent"]
        child_pcd = x["multi_obj_final_pcd"].item()["child"]

        pcd = np.concatenate([child_pcd, parent_pcd], axis=0)
        classes = np.concatenate([np.zeros(len(child_pcd), dtype=np.int32), np.ones(len(parent_pcd), dtype=np.int32)], axis=0)

        d = {
            "clouds": pcd,
            "classes": classes
        }
        np.savez(new_path, **d)
