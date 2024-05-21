import matplotlib.pyplot as plt

output_path = r'S:\ExposureScienceLab\Lead Dust\poster\pics\dust_wipe_graph_final.png'
x_labels = ['Initial', 'Mid', 'Final']
subject_1 = [0.9768864, 0.90, 0.38]
subject_2 = [33.8850768, 10.64, 15.66]
subject_3 = [1.2217632, 1.53, 0.83]
subject_4 = [2.67, 2.09, 1.15]
markers = ['o', 'v', 's', 'D']

f, (ax, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]})  # break y-axis into two parts

def plot_subject(ax, ax2, x_labels, data, marker, label):
    ax.plot(x_labels, data, marker=marker, label=label)
    ax2.plot(x_labels, data, marker=marker)

for i, (subject, data) in enumerate(zip(['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4'], [subject_1, subject_2, subject_3, subject_4])):
    marker = markers[i]
    label = subject
    plot_subject(ax, ax2, x_labels, data, marker, label)

ax.set_ylim(10, 35)  # Set y-axis limits for the top plot (high values)
ax2.set_ylim(0, 3)  # Set y-axis limits for the bottom plot (most of the data)

ax.spines['bottom'].set_visible(False) # bottom border of top plot off
ax2.spines['top'].set_visible(False) # top border of bottom plot off

ax.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
ax2.xaxis.tick_bottom()
ax.legend(loc='upper right')

d = .015  # how big to make the diagonal lines in axes coordinates
plt_args = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **plt_args)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-d, +d), **plt_args)  # top-right diagonal
plt_args.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **plt_args)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **plt_args)  # bottom-right diagonal

ax.title.set_text('Dust wipe Pb concentrations over time')
plt.xlabel('Time Point')
plt.subplots_adjust(hspace=0.2)
plt.savefig(output_path, dpi=300)
plt.show()