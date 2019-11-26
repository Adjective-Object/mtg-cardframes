import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
from imageio import imread
from skimage import color
import sys

contrast_score_matricies = [
    np.array(
        [
            [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
            [[-1, -1, -1], [8, 8, 8], [-1, -1, -1]],
            [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
        ]
    ),
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

adjacent_ct_filter = np.array(
    [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ]
)

adjacent_colors_filter = np.array(
    [
        [[0] * 4, [0] * 4, [1] * 4, [0] * 4, [0] * 4],
        [[0] * 4, [1] * 4, [1] * 4, [1] * 4, [0] * 4],
        [[1] * 4, [1] * 4, [0] * 4, [1] * 4, [1] * 4],
        [[0] * 4, [1] * 4, [1] * 4, [1] * 4, [0] * 4],
        [[0] * 4, [0] * 4, [1] * 4, [0] * 4, [0] * 4],
    ]
)


near_different_filter = np.array(
    [
        [0, 1, 1, 1, 0],
        [1, 2, 2, 2, 1],
        [1, 2, 3, 2, 1],
        [1, 2, 2, 2, 1],
        [0, 1, 1, 1, 0],
    ]
)


def d_print(*args):
    if __name__ == "__main__":
        print(*args)


def cleaning_cellular_automata(
    cropped_text,
    L_COLOR_DISTANCE_SCALE=3,
    A_COLOR_DISTANCE_SCALE=3,
    B_COLOR_DISTANCE_SCALE=3,
    NORMALIZED_WEIGHTED_COLOR_DISTANCE_THRESHOLD=0.8,
):

    state = cropped_text / 255
    single_color_channel_shape = (state.shape[0], state.shape[1], 1)

    input_lab = color.rgb2lab(color.rgba2rgb(cropped_text / 255)) / 100
    l = input_lab[:, :, 0]
    a = input_lab[:, :, 1]
    b = input_lab[:, :, 2]
    l_med = np.median(l)
    a_med = np.median(a)
    b_med = np.median(b)
    l_std = max(l.std(), 0.000000001)
    a_std = max(a.std(), 0.000000001)
    b_std = max(b.std(), 0.000000001)

    d_print("l", "med", l_med, "std", l_std, "WEIGHTED", l_std * L_COLOR_DISTANCE_SCALE)
    d_print("a", "med", a_med, "std", a_std, "WEIGHTED", a_std * A_COLOR_DISTANCE_SCALE)
    d_print("b", "med", b_med, "std", b_std, "WEIGHTED", b_std * B_COLOR_DISTANCE_SCALE)

    all_updates_mask = np.zeros(single_color_channel_shape)

    for i in range(30):
        state_lab = color.rgb2lab(color.rgba2rgb(state)) / 100
        # d_print(state_lab_l.min(), state_lab_l.max())
        contrast_filter_scores = np.zeros(state.shape[0:-1])

        for scoring_matrix in contrast_score_matricies:
            d_print(state_lab.shape, scoring_matrix.shape)
            result = np.sum(
                np.abs(
                    scipy.ndimage.filters.convolve(
                        state_lab, scoring_matrix, mode="wrap"
                    )
                ),
                axis=2,
            )
            d_print(result.shape, contrast_filter_scores.shape)
            contrast_filter_scores += result

        # push values away from center, then clamp
        # v = 1 - np.abs(np.power(1 - scores, 3))
        contrasting = np.abs(contrast_filter_scores) > 0.6
        distance_l = np.power(
            np.abs(state_lab[:, :, 0] - l_med) / l_std * L_COLOR_DISTANCE_SCALE, 2,
        )
        distance_a = np.power(
            np.abs(state_lab[:, :, 1] - a_med) / a_std * A_COLOR_DISTANCE_SCALE, 2,
        )
        distance_b = np.power(
            np.abs(state_lab[:, :, 2] - b_med) / b_std * B_COLOR_DISTANCE_SCALE, 2,
        )
        color_distance = np.sqrt(
            np.power(np.abs(state_lab[:, :, 0] - l_med) * L_COLOR_DISTANCE_SCALE, 2,)
            + np.power(np.abs(state_lab[:, :, 1] - a_med) * A_COLOR_DISTANCE_SCALE, 2,)
            + np.power(np.abs(state_lab[:, :, 2] - b_med) * B_COLOR_DISTANCE_SCALE, 2,),
        )
        d_print(
            "color_distance",
            color_distance.shape,
            color_distance.min(),
            color_distance.max(),
        )
        # different = np.bitwise_or(
        #     distance_l,
        #     distance_a,
        #     distance_b,
        # ).astype(np.uint8)
        different = (
            color_distance > NORMALIZED_WEIGHTED_COLOR_DISTANCE_THRESHOLD
        ).astype(np.uint8)

        near_different = (
            scipy.ndimage.filters.convolve(
                different, near_different_filter, mode="wrap"
            )
            > 5
        ).astype(np.uint8)

        difference_mask = near_different
        print("DIFF MASK!", np.sum(near_different))
        if np.sum(near_different) < 100:
            print("USE ACTUAL DIFFERENT")
            difference_mask = different

        d_print(contrasting.shape, different.shape)
        d_print(
            contrasting.min(), contrasting.max(), different.min(), different.max(),
        )

        update_mask = contrasting * difference_mask  # * near_light # * dark
        update_mask = np.clip(update_mask, 0, 1).astype(np.uint8)

        if __name__ == "__main__":
            plt.subplot(4, 3, 1, title="contrasting")
            plt.imshow(contrasting, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(4, 3, 2, title="distance_l")
            plt.imshow(
                distance_l, cmap=plt.get_cmap("coolwarm"), vmin=0,
            )
            plt.subplot(4, 3, 3, title="distance_a")
            plt.imshow(
                distance_a, cmap=plt.get_cmap("coolwarm"), vmin=0,
            )
            plt.subplot(4, 3, 4, title="distance_b")
            plt.imshow(
                distance_b, cmap=plt.get_cmap("coolwarm"), vmin=0,
            )
            plt.subplot(4, 3, 5, title="color_distance")
            plt.imshow(color_distance, cmap=plt.get_cmap("coolwarm"), vmin=0)
            plt.subplot(4, 3, 6, title="different")
            plt.imshow(different, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(4, 3, 7, title="near_different")
            plt.imshow(near_different, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.subplot(4, 3, 8, title="update_mask")
            plt.imshow(update_mask, cmap=plt.get_cmap("coolwarm"), vmin=-1, vmax=1)
            plt.show()

        # d_print(
        #     'ahh',
        #     (1-dark).shape,
        #     adjacent_ct_filter.shape
        # )

        adj_colors_sum = np.empty(state.shape)
        for j in range(4):
            adj_colors_sum[:, :, j] = scipy.ndimage.filters.convolve(
                # filter out colors we don't consider 'dark' from the adj colors sum
                state[:, :, j] * (1 - difference_mask),
                adjacent_ct_filter,
                mode="wrap",
            )

        adj_nondifferent_counts = scipy.ndimage.filters.convolve(
            (1 - difference_mask), adjacent_ct_filter, mode="wrap"
        )

        use_new_state_mask = (update_mask) * (adj_nondifferent_counts != 0).astype(
            np.uint8
        )
        adj_nondifferent_counts_no_zeros = adj_nondifferent_counts + (
            adj_nondifferent_counts == 0
        ).astype(np.uint8)

        d_print(update_mask.min(), update_mask.max())
        d_print(adj_colors_sum.min(), adj_colors_sum.max())
        d_print(adj_nondifferent_counts.min(), adj_nondifferent_counts.max())
        d_print(use_new_state_mask.min(), use_new_state_mask.max())

        new_colors = np.nan_to_num(
            adj_colors_sum / adj_nondifferent_counts.reshape(single_color_channel_shape)
        )

        d_print(
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
            # plt.show()

        d_print("new state mask:", np.histogram(use_new_state_mask.flatten()))
        d_print(use_new_state_mask.min(), use_new_state_mask.max())

        if use_new_state_mask.min() == use_new_state_mask.max() == 0:
            print("early exit")
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

    d_print(
        "finished. state", state.min(), state.max(), np.mean(state), np.average(state)
    )

    # this hack works around issues with accumulating floating point error.
    # we only overwrite the updated pixels in the output.
    state = (state * 255).astype(np.uint8)
    cropped_text = cropped_text.astype(np.uint8)
    d_print(
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
    image_path = sys.argv[1] if len(sys.argv) > 1 else "Crackling-Drake-Text.png"
    # image = imread('./text_bodies/c:w+c:b_creature_merged.png')
    # image = imread("./text_bodies/c:r+c:u_creature_merged.png")
    image = imread(image_path)
    # image = imread("Draconic-Disciple-Text.png")
    cleaning_cellular_automata(image)
