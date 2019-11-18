import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
from imageio import imread
from skimage import color

contrast_score_matricies = [
    np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1],]),
    # np.array([
    #     [-1],
    #     [5],
    #     [-2],
    #     [-1],
    # ]),
    # np.array([
    #     [1],
    #     [2],
    #     [-5],
    #     [2],
    #     [1],
    # ]),
    # np.array([
    #     [-1, -2, 5, -2, -1],
    # ]),
    # np.array([
    #     [1, 2, -5, 2, 1],
    # ]),
    # np.array([[
    #     [-1, 0, 0, 0, 0],
    #     [0, -2, 0, 0, 0],
    #     [0, 0, 0, 0, 0],
    #     [0, 0, 0, 2, 0],
    #     [0, 0, 0, 0, 1],
    # ]]),
    # np.array([[
    #     [0, 0, 0, 0, -1],
    #     [0, 0, 0, -2, 0],
    #     [0, 0, 0, 0, 0],
    #     [0, 2, 0, 0, 0],
    #     [1, 0, 0, 1, 0],
    # ]]),
    # np.array([[
    #     [0, 1, 0],
    #     [-1, 0, 1],
    #     [0, -1, 0],
    # ]]),
    # np.array([[
    #     [0, 1, 0],
    #     [1, 0, -1],
    #     [0, -1, 0],
    # ]]),
    # np.array([[
    #     [0, -1, 0],
    #     [1, 0, -1],
    #     [0, 1, 0],
    # ]]),
    # np.array([[
    #     [0, -1, 0],
    #     [-1, 0, 1],
    #     [0, 1, 0],                mode='wrap'
    # ]]),                mode='wrap'
]

near_light_score_matricies = [
    np.array(
        [
            [1, 1, 1, 1, 1],
            [1, 2, 2, 2, 1],
            [1, 2, 0, 2, 1],
            [1, 2, 2, 2, 1],
            [1, 1, 1, 1, 1],
        ]
    ),
    # np.array([[
    #     [0, 1, 0],
    #     [-1, 0, 1],
    #     [0, -1, 0],
    # ]]),
    # np.array([[
    #     [0, 1, 0],
    #     [1, 0, -1],
    #     [0, -1, 0],
    # ]]),
    # np.array([[
    #     [0, -1, 0],
    #     [1, 0, -1],
    #     [0, 1, 0],
    # ]]),
    # np.array([[
    #     [0, -1, 0],
    #     [-1, 0, 1],
    #     [0, 1, 0],
    # ]]),
]

adjacent_colors_filter = np.array(
    [
        [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
        [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
        [[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1]],
        [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
        [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
    ]
)

adjacent_nondark_ct_filter = np.array(
    [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]
)


def cleaning_cellular_automata(cropped_text):
    state = cropped_text / 255
    single_color_channel_shape = (state.shape[0], state.shape[1], 1)

    input_lab_l = color.rgb2lab(color.rgba2rgb(cropped_text / 255))[:, :, 0] / 100
    print("input_lab_l", input_lab_l.min(), input_lab_l.max(), input_lab_l.std())
    dark_lab_thresh = np.mean(input_lab_l) - input_lab_l.std()

    all_updates_mask = np.zeros(single_color_channel_shape)

    print("dark lab thres", dark_lab_thresh)

    for i in range(30):
        state_lab_l = color.rgb2lab(color.rgba2rgb(state))[:, :, 0] / 100
        # print(state_lab_l.min(), state_lab_l.max())
        contrast_filter_scores = np.zeros(state_lab_l.shape)

        for scoring_matrix in contrast_score_matricies:
            contrast_filter_scores += np.abs(
                scipy.ndimage.filters.convolve(state_lab_l, scoring_matrix, mode="wrap")
            )

        near_light_filter_scores = np.zeros(state_lab_l.shape)
        for scoring_matrix in near_light_score_matricies:
            near_light_filter_scores += scipy.ndimage.filters.convolve(
                state_lab_l, scoring_matrix, mode="wrap"
            )

        # push values away from center, then clamp
        # v = 1 - np.abs(np.power(1 - scores, 3))
        contrasting = np.abs(contrast_filter_scores) > 0.6
        near_light = (
            (near_light_filter_scores / near_light_filter_scores.max()) > 0.4
        ).astype(np.uint8)
        dark = (state_lab_l < dark_lab_thresh).astype(np.uint8)

        print(contrasting.shape, near_light.shape, dark.shape)
        print(
            contrasting.min(),
            contrasting.max(),
            near_light.min(),
            near_light.max(),
            dark.min(),
            dark.max(),
        )

        update_mask = contrasting  # * near_light # * dark
        update_mask = np.clip(update_mask, 0, 1).astype(np.uint8)

        if __name__ == "__main__":
            plt.subplot(9, 2, 1, title="contrasting")
            plt.imshow(contrasting, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(9, 2, 2, title="near_light")
            plt.imshow(near_light, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(9, 2, 3, title="dark")
            plt.imshow(dark, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(9, 2, 4, title="update_mask")
            plt.imshow(update_mask, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)

        # print(
        #     'ahh',
        #     (1-dark).shape,
        #     adjacent_nondark_ct_filter.shape
        # )

        adj_colors_sum = np.empty(state.shape)
        for j in range(4):
            adj_colors_sum[:, :, j] = scipy.ndimage.filters.convolve(
                # filter out colors we don't consider 'dark' from the adj colors sum
                state[:, :, j] * (1 - dark),
                adjacent_nondark_ct_filter,
                mode="wrap",
            )

        adj_nondark_cts = scipy.ndimage.filters.convolve(
            (1 - dark), adjacent_nondark_ct_filter, mode="wrap"
        )

        use_new_state_mask = (update_mask) * (adj_nondark_cts != 0).astype(np.uint8)
        adj_nondark_cts_no_zeros = adj_nondark_cts + (adj_nondark_cts == 0).astype(
            np.uint8
        )

        print(update_mask.min(), update_mask.max())
        print(adj_colors_sum.min(), adj_colors_sum.max())
        print(adj_nondark_cts.min(), adj_nondark_cts.max())
        print(use_new_state_mask.min(), use_new_state_mask.max())

        new_colors = np.nan_to_num(
            adj_colors_sum / adj_nondark_cts.reshape(single_color_channel_shape)
        )

        print(
            "new colors",
            new_colors.min(),
            new_colors.max(),
            np.average(new_colors),
            new_colors.std(),
        )

        # if(i == 29):
        if __name__ == "__main__":
            plt.subplot(9, 2, 5, title="update_mask")
            plt.imshow(update_mask, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(9, 2, 6, title="adj_nondark_cts")
            plt.imshow(
                adj_nondark_cts,
                cmap=plt.get_cmap("YlGn"),
                vmin=0,
                vmax=adj_nondark_cts.max(),
            )
            plt.subplot(9, 2, 7, title="use_new_state_mask")
            plt.imshow(
                use_new_state_mask, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1
            )
            plt.subplot(9, 2, 8, title="new_colors")
            plt.imshow(new_colors.astype(np.float) / new_colors.max())
            plt.subplot(9, 2, 9, title="state")
            plt.imshow(state)
            # plt.show()

        print("new state mask:", np.histogram(use_new_state_mask.flatten()))

        if use_new_state_mask.min() == use_new_state_mask.max() == 0:
            break

        all_updates_mask = np.clip(
            all_updates_mask + use_new_state_mask.reshape(single_color_channel_shape),
            0,
            1,
        ).astype(np.uint8)

        state = state * (1 - use_new_state_mask).reshape(
            single_color_channel_shape
        ) + new_colors * use_new_state_mask.reshape(single_color_channel_shape)

        # plt.imshow(state[0], cmap='gray')
        # plt.imshow(scores[0], cmap='gray')

    print(
        "finished. state", state.min(), state.max(), np.mean(state), np.average(state)
    )

    # this hack works around issues with accumulating floating point error.
    # we only overwrite the updated pixels in the output.
    state = (state * 255).astype(np.uint8)
    cropped_text = cropped_text.astype(np.uint8)
    print(
        state.dtype, all_updates_mask.dtype, cropped_text.dtype,
    )
    finished_state = state * all_updates_mask + cropped_text * (1 - all_updates_mask)

    finished_state = np.clip(finished_state, 0, 255).astype(np.uint8)

    plt.subplot(2, 2, 1, title="original")
    plt.imshow(cropped_text)
    plt.subplot(2, 2, 2, title="state")
    plt.imshow(state)
    plt.subplot(2, 2, 3, title="finished_state")
    plt.imshow(finished_state)
    plt.subplot(2, 2, 4, title="all_updates_mask")
    plt.imshow(
        all_updates_mask.reshape(
            (all_updates_mask.shape[0], all_updates_mask.shape[1])
        ),
        cmap=plt.get_cmap("coolwarm"),
        vmin=0,
        vmax=1,
    )
    if __name__ == "__main__":
        plt.show()

    return finished_state


if __name__ == "__main__":
    # image = imread('./text_bodies/c:w+c:b_creature_merged.png')
    image = imread("./text_bodies/c:r+c:u_creature_merged.png")
    cleaning_cellular_automata(image)
