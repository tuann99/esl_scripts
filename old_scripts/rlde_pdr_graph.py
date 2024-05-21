import matplotlib.pyplot as plt

output_path = r'S:\ExposureScienceLab\Lead Dust\poster\pics\pdr_graph_final.png'
x_labels = ['Initial', 'Mid', 'Final']
subject_1 = [6.45, 0.63, 0.78]
subject_2 = [8.21, 14.23, 4.89]
subject_3 = [7.31, 35.55, 3.92]
subject_4 = [17.15, 0.22, 0.53]
markers = ['o', 'v', 's', 'D']

fig, ax = plt.subplots()

for i, (subject_data, marker) in enumerate(zip([subject_1, subject_2, subject_3, subject_4], markers)):
    label = f'Subject {i+1}'
    ax.plot(x_labels, subject_data, marker=marker, label=label)

ax.set_xlabel('Time Point')
ax.set_ylabel('TSP $(µg/m^3)$')
ax.set_title('Mean Total Suspended Particle (TSP)\nConcentrations Over Time ')
ax.legend()

plt.savefig(output_path, dpi=300)
plt.show()