import numpy as np
import matplotlib.pyplot as plt
record=np.dtype([('spin', str, 20), ('ao-basis', str, 20),('System', str, 20), ('charge', int), ('unpaired', int), ('oep-basis', str, 20), ('thr_int_fai', np.float32),  ('eigval', np.float32), ('eig_H_error', np.float32), ('eig_percent_error', np.float32), ('Hatree_Error', np.float32), ('Density_Error', np.float32)])
table = np.loadtxt('table', dtype=record)

thresholds = []
for line in table:
    thresholds.append(line[6])

print(np.sort(np.unique(thresholds))[::-1])

eigval_errors = {}
thresholds = np.sort(np.unique(thresholds))[::-1]
for threshold in thresholds:
    eigval_errors[threshold] = []

for line in table:
    eigval_errors[line[6]].append(line[9])

print(eigval_errors[np.float32(0.008)])

for threshold in thresholds[::3]:
    plt.hist(eigval_errors[np.float32(threshold)], bins=30, alpha = 0.5, label=str(threshold))  # density=False would make counts
plt.legend(loc="upper left")
plt.show()
#for line in ...:
#    append(line[])
#for line in ...:
#    append(line[])
#for line in ...:
#    append(line[])
