# Section 05: Draw a neuron-level architecture diagram for the trained MLP

def draw_mlp_architecture(input_n, hidden_layers, output_n=1, max_draw=14):
    layers = [input_n] + list(hidden_layers) + [output_n]
    x = np.arange(len(layers))

    plt.figure(figsize=(10, 5))
    for i, n in enumerate(layers):
        shown = min(n, max_draw)
        ys = np.linspace(0, 1, shown)

        plt.scatter([i] * shown, ys, s=110)

        if i < len(layers) - 1:
            n2 = layers[i + 1]
            shown2 = min(n2, max_draw)
            ys2 = np.linspace(0, 1, shown2)

            for y1 in ys:
                for y2 in ys2:
                    plt.plot([i, i + 1], [y1, y2], alpha=0.25, linewidth=0.6)

        label = f"{n}" + (" (capped)" if n > max_draw else "")
        plt.text(i, 1.08, label, ha="center", fontsize=11)

    plt.xticks(x, ["Input"] + [f"Hidden {k+1}" for k in range(len(hidden_layers))] + ["Output"])
    plt.yticks([])
    plt.ylim(-0.12, 1.18)
    plt.title("MLP Architecture (neurons per layer)")
    plt.show()


hidden = mlp_model.named_steps["mlp"].hidden_layer_sizes
if isinstance(hidden, int):
    hidden = (hidden,)

draw_mlp_architecture(input_n=len(FEATURES), hidden_layers=hidden, output_n=1)
