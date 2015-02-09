from matplotlib import pyplot as plt

for idx, c in enumerate(diff.histogram()):
    plt.bar(idx, c)

plt.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "hist", image.replace("jpg", "png")))