import numpy as np
import matplotlib.pyplot as plt
record=np.dtype([('spin', str, 20), ('ao-basis', str, 20),('System', str, 20), ('charge', int), ('unpaired', int), ('oep-basis', str, 20), ('thr_int_fai', np.float32),  ('Eigval', np.float32), ('eig_H_error', np.float32), ('eig_percent_error', np.float32), ('Hatree_Error', np.float32), ('Density_Error', np.float32)])
table = np.loadtxt('table', dtype=record)

colormap = plt.cm.gist_ncar


thresholds, systems = [], []
for line in table:
    thresholds.append(line[6])
    systems.append(line[2]+"_C:"+str(line[3])+"_S:"+str(line[4])+"_"+line[0])

print(np.sort(np.unique(thresholds))[::-1])

Eigval_Hartree_errors  = {}
Eigval_errors  = {}
Hartree_errors = {}
Density_errors = {}
Individual_errors = {}

thresholds = np.sort(np.unique(thresholds))[::-1]
systems = np.sort(np.unique(systems))[::-1]

for system in systems:
    Individual_errors[system] = {}
    Individual_errors[system]['Error'] = []
    Individual_errors[system]['threshold'] = []

for threshold in thresholds:
    Eigval_errors[threshold], Hartree_errors[threshold], Density_errors[threshold], Eigval_Hartree_errors[threshold]  = [], [], [], []

print(systems)

for line in table:
    Eigval_Hartree_errors[line[6]].append(line[8])
    Eigval_errors[line[6]].append(line[9])
    Hartree_errors[line[6]].append(line[10])
    Density_errors[line[6]].append(line[11])


if False:
    for threshold in thresholds[::3]:
        plt.hist(Eigval_errors[np.float32(threshold)], bins=30, alpha = 0.5, label=str(threshold))  # density=False would make counts
    plt.legend(loc="upper left")
    plt.show()

if False:
  Mean_Eigval_Hartree_errors  = [] 
  Mean_Eigval_errors  = [] 
  Max_Eigval_errors  = [] 
  Mean_Hartree_errors = [] 
  Mean_Density_errors = [] 
  for threshold in thresholds:
      Mean_Eigval_Hartree_errors.append(sum([abs(i) for i in Eigval_Hartree_errors[np.float32(threshold)]])/len(Eigval_Hartree_errors))
      Mean_Eigval_errors.append(sum([abs(i) for i in Eigval_errors[np.float32(threshold)]])/len(Eigval_errors))
      Mean_Hartree_errors.append(sum([abs(i) for i in Hartree_errors[np.float32(threshold)]])/len(Hartree_errors))
      Mean_Density_errors.append(sum([abs(i) for i in Density_errors[np.float32(threshold)]])/len(Density_errors))
      Max_Eigval_errors.append(max(Eigval_errors[np.float32(threshold)]))
  
  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)
  #line = ax.plot(thresholds, Mean_Eigval_Hartree_errors, color='blue', lw=2, label="Mean Eigval errors [H]")
  #line = ax.plot(thresholds, Mean_Eigval_errors, color='blue', lw=2, label="Mean Eigval errors [%]")
  #line = ax.plot(thresholds, Max_Eigval_errors, color='blue', lw=2, label="Max_Eigval_errors")
  line = ax.plot(thresholds, Mean_Hartree_errors, color='red', lw=2, label="Mean Hartree errors [H]")
  ax2 = ax.twinx()
  line = ax2.plot(thresholds, Mean_Density_errors, color='blue', lw=2, label="Mean Density errors [e⁻]")
 
# find ax 1 1x 2 label functions

  plt.legend(loc="upper left")
  plt.xlabel('threshold')
  plt.ylabel('eigval error [%]')
  
  ax.set_xscale('log')


if True:
  for line in table:
      Individual_errors[line[2]+"_C:"+str(line[3])+"_S:"+str(line[4])+"_"+line[0]]['Error'].append(line[11]) # 8 -> eig [H], 9 -> eig [%], 10 -> E_H [H], 11 \rho [e⁻]
      Individual_errors[line[2]+"_C:"+str(line[3])+"_S:"+str(line[4])+"_"+line[0]]['threshold'].append(line[6])
  
  ls = ['-', '--', '-.']
  j = 0 
  
  print(len(systems))
  for i in range(0,4):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, 14))))
    for system in systems[i*14:(i+1)*14]:
      j+=1
      cls=ls[j%3]
      ax.plot(Individual_errors[system]['threshold'], Individual_errors[system]['Error'], lw=2, label=system, linestyle=cls)
    plt.legend(loc="upper left")
    plt.xlabel('threshold')
    plt.ylabel('eigval error [%]')
    ax.set_xscale('log')


print(Individual_errors)

plt.show()

#for line in ...:
#    append(line[])
#for line in ...:
#    append(line[])
#for line in ...:
#    append(line[])
