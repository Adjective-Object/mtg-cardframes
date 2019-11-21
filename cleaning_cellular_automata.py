import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
from imageio import imread
from skimage import color

contrast_score_matricies = [
    np.array([
        [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]],
        [[-1,-1,-1], [8,8,8], [-1,-1,-1]],
        [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]],
    ]),
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

adjacent_ct_filter = np.array(
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

    input_lab = color.rgb2lab(color.rgba2rgb(cropped_text / 255)) / 100
    l = input_lab[:,:,0]
    a = input_lab[:,:,1]
    b = input_lab[:,:,2]
    l_med = np.median(l)
    a_med = np.median(a)
    b_med = np.median(b)
    l_std = l.std()
    a_std = a.std()
    b_std = b.std()

    print("l", 'med', l_med, 'std', l_std)
    print("a", 'med', a_med, 'std', a_std)
    print("b", 'med', b_med, 'std', b_std)

    all_updates_mask = np.zeros(single_color_channel_shape)

    PERMITTED_DIFFERENCE_IN_STD_L = 1.2
    PERMITTED_DIFFERENCE_IN_STD_A = 1.5
    PERMITTED_DIFFERENCE_IN_STD_B = 1.9

    L_WEIGHT = 10
    A_WEIGHT = 1
    B_WEIGHT = 1
    NORMALZIED_WEIGHTED_COLOR_DISTANCE_THRESHOLD = 5

    for i in range(30):
        state_lab = color.rgb2lab(color.rgba2rgb(state)) / 100
        # print(state_lab_l.min(), state_lab_l.max())
        contrast_filter_scores = np.zeros(state.shape[0:-1])

        for scoring_matrix in contrast_score_matricies:
            print(state_lab.shape, scoring_matrix.shape)
            result = np.sum(np.abs(
                scipy.ndimage.filters.convolve(state_lab, scoring_matrix, mode="wrap")
            ), axis=2)
            print(result.shape, contrast_filter_scores.shape)
            contrast_filter_scores += result

        # push values away from center, then clamp
        # v = 1 - np.abs(np.power(1 - scores, 3))
        contrasting = np.abs(contrast_filter_scores) > 0.6
        different_l = (np.abs(state_lab[:,:,0] - l_med) > (l_std * PERMITTED_DIFFERENCE_IN_STD_L))
        different_a = (np.abs(state_lab[:,:,1] - a_med) > (a_std * PERMITTED_DIFFERENCE_IN_STD_A))
        different_b = (np.abs(state_lab[:,:,2] - b_med) > (b_std * PERMITTED_DIFFERENCE_IN_STD_B))
        color_distance = np.sqrt(
            np.power(
                np.abs(state_lab[:,:,0] - l_med) / l_std * L_WEIGHT,
                2,
            ) +
            np.power(
                np.abs(state_lab[:,:,1] - a_med) / a_std * A_WEIGHT,
                2,
            ) +
            np.power(
                np.abs(state_lab[:,:,2] - b_med) / b_std * B_WEIGHT,
                2,
            ),
        )
        # print("color_distance", color_distance.shape, color_distance.min(), color_distance.max())
        # different = np.bitwise_or(
        #     different_l,
        #     different_a,
        #     different_b,
        # ).astype(np.uint8)
        different = ( 
            color_distance > NORMALZIED_WEIGHTED_COLOR_DISTANCE_THRESHOLD
        ).astype(np.uint8)


        print(contrasting.shape, different.shape)
        print(
            contrasting.min(),
            contrasting.max(),
            different.min(),
            different.max(),
        )

        update_mask = contrasting  # * near_light # * dark
        update_mask = np.clip(update_mask, 0, 1).astype(np.uint8)

        if __name__ == "__main__":
            plt.subplot(4, 3, 1, title="contrasting")
            plt.imshow(contrasting, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(4, 3, 2, title="different_l")
            plt.imshow(different_l, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(4, 3, 3, title="different_a")
            plt.imshow(different_a, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(4, 3, 4, title="different_b")
            plt.imshow(different_b, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(4, 3, 12, title="color_distance")
            plt.imshow(color_distance, cmap=plt.get_cmap("coolwarm"), vmin=0)
            plt.subplot(4, 3, 5, title="different")
            plt.imshow(different, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(4, 3, 6, title="update_mask")
            plt.imshow(update_mask, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)

        # print(
        #     'ahh',
        #     (1-dark).shape,
        #     adjacent_ct_filter.shape
        # )

        adj_colors_sum = np.empty(state.shape)
        for j in range(4):
            adj_colors_sum[:, :, j] = scipy.ndimage.filters.convolve(
                # filter out colors we don't consider 'dark' from the adj colors sum
                state[:, :, j] * (1 - different),
                adjacent_ct_filter,
                mode="wrap",
            )

        adj_nondifferent_counts = scipy.ndimage.filters.convolve(
            (1 - different), adjacent_ct_filter, mode="wrap"
        )

        use_new_state_mask = (update_mask) * (adj_nondifferent_counts != 0).astype(np.uint8)
        adj_nondifferent_counts_no_zeros = adj_nondifferent_counts + (adj_nondifferent_counts == 0).astype(
            np.uint8
        )

        print(update_mask.min(), update_mask.max())
        print(adj_colors_sum.min(), adj_colors_sum.max())
        print(adj_nondifferent_counts.min(), adj_nondifferent_counts.max())
        print(use_new_state_mask.min(), use_new_state_mask.max())

        new_colors = np.nan_to_num(
            adj_colors_sum / adj_nondifferent_counts.reshape(single_color_channel_shape)
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
            plt.subplot(4, 3, 7, title="adj_nondifferent_counts")
            plt.imshow(
                adj_nondifferent_counts,
                cmap=plt.get_cmap("YlGn"),
                vmin=0,
                vmax=adj_nondifferent_counts.max(),
            )
            plt.subplot(4, 3, 8, title="use_new_state_mask")
            plt.imshow(
                use_new_state_mask, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1
            )
            plt.subplot(4, 3, 9, title="new_colors")
            plt.imshow(new_colors.astype(np.float) / new_colors.max())
            plt.subplot(4, 3, 10, title="state")
            plt.imshow(state)
            plt.show()

        print("new state mask:", np.histogram(use_new_state_mask.flatten()))
        print(use_new_state_mask.min(), use_new_state_mask.max())

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
        plt.imshow(state)
        plt.show()

    return finished_state


if __name__ == "__main__":
    # image = imread('./text_bodies/c:w+c:b_creature_merged.png')
    # image = imread("./text_bodies/c:r+c:u_creature_merged.png")
    image = imread("Crackling-Drake-Text.png")
    cleaning_cellular_automata(image)
