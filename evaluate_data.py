import numpy as np
import matplotlib.pyplot as plt

# data type for laodtext, with this declaration np.loadtext can read any kind of table, otherwise it requires one datatype for all cells
record=np.dtype([('spin', str, 20), ('ao-basis', str, 20),('System', str, 20), ('charge', int), ('unpaired', int), ('oep-basis', str, 20), ('thr_int_fai', np.float32),  ('Eigval', np.float32), ('eig_H_error', np.float32), ('eig_percent_error', np.float32), ('Hatree_Error', np.float32), ('Density_Error', np.float32)])
table = np.loadtxt('Table', dtype=record)

# adapt other color map to allow for identificatio of many lines in one plot
colormap = plt.cm.gist_ncar


thresholds, systems, ao_basis_sets, oep_basis_sets  = [], [], [], []
for line in table:
    thresholds.append(line[6])
    ao_basis_sets.append(line[1])
    oep_basis_sets.append(line[5])
    systems.append(line[2]+"_C:"+str(line[3])+"_S:"+str(line[4])+"_"+line[0])




thresholds = np.sort(np.unique(thresholds))[::-1]
systems = np.sort(np.unique(systems))[::-1]
ao_basis_sets = np.sort(np.unique(ao_basis_sets))[:]
oep_basis_sets = np.sort(np.unique(oep_basis_sets))[:]

Eigval_Hartree_errors, Eigval_errors, Hartree_errors, Density_errors, RHS_errors, Individual_errors  = {}, {}, {}, {}, {}, {}

for system in systems:
    Individual_errors[system] = {}
    Individual_errors[system]['Error'] = []
    Individual_errors[system]['threshold'] = []


for ao_basis in ao_basis_sets:
    Eigval_errors[ao_basis] = {} 
    Hartree_errors[ao_basis]= {} 
    Density_errors[ao_basis]= {} 
    Eigval_Hartree_errors[ao_basis]= {}
    for oep_basis in oep_basis_sets:
         Eigval_errors[ao_basis][oep_basis] = {} 
         Hartree_errors[ao_basis][oep_basis] = {} 
         Density_errors[ao_basis][oep_basis] = {} 
         Eigval_Hartree_errors[ao_basis][oep_basis] = {}
         for threshold in thresholds:
             Eigval_errors[ao_basis][oep_basis][threshold] = []
             Hartree_errors[ao_basis][oep_basis][threshold] = []
             Density_errors[ao_basis][oep_basis][threshold] = []
             Eigval_Hartree_errors[ao_basis][oep_basis][threshold] = []

print(ao_basis_sets)

for line in table:
    Eigval_Hartree_errors[line[1]][line[5]][line[6]].append(line[8])
    Eigval_errors[line[1]][line[5]][line[6]].append(line[9])
    Hartree_errors[line[1]][line[5]][line[6]].append(line[10])
    Density_errors[line[1]][line[5]][line[6]].append(line[11])

print(ao_basis, oep_basis)
if True:
    for ao_basis in ao_basis_sets:
        for oep_basis in oep_basis_sets:
            # Mean Errors of available Types 
            Mean_Eigval_Hartree_errors  = [] 
            Mean_Eigval_errors  = [] 
            Max_Eigval_errors  = [] 
            Mean_Hartree_errors = [] 
            Mean_Density_errors = []
            for threshold in thresholds:
                if len(Density_errors[ao_basis][oep_basis][np.float32(threshold)]) > 0:
                    #Mean_Eigval_Hartree_errors.append(sum([abs(i) for i in Eigval_Hartree_errors[np.float32(threshold)]])/len(Eigval_Hartree_errors))
                    Mean_Eigval_errors.append(sum([abs(i) for i in Eigval_errors[ao_basis][oep_basis][np.float32(threshold)]])/len(Eigval_errors[ao_basis][oep_basis][np.float32(threshold)]))
                    #Mean_Hartree_errors.append(sum([abs(i) for i in Hartree_errors[np.float32(threshold)]])/len(Hartree_errors))
                    #print("a",ao_basis,oep_basis, len(Density_errors[ao_basis][oep_basis][np.float32(threshold)]))
                    #print("b",ao_basis,oep_basis, len(Density_errors))
                    #Mean_Density_errors.append(sum([abs(i) for i in Density_errors[ao_basis][oep_basis][np.float32(threshold)]])/len(Density_errors[ao_basis][oep_basis][np.float32(threshold)]))
                    #Max_Eigval_errors.append(max(Eigval_errors[np.float32(threshold)]))
            
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            line = ax.plot(thresholds, Mean_Eigval_errors, color='blue', lw=2, label="Mean Eigval errors [H]")
            #line = ax.plot(thresholds, Mean_Density_errors, color='blue', lw=2, label="Mean Eigval errors [%]")
    
            #line = ax.plot(thresholds, Max_Eigval_errors, color='blue', lw=2, label="Max_Eigval_errors")
            #line = ax.plot(thresholds, Mean_Hartree_errors, color='red', lw=2, label="Mean Hartree errors [H]")
    
            #ax2 = ax.twinx()
            #line = ax2.plot(thresholds, Mean_Density_errors, color='blue', lw=2, label="Mean Density errors [e⁻]")
     
    #       find ax 1 1x 2 label functions
    
            plt.legend(loc="upper left")
            plt.title(ao_basis+" + "+oep_basis)
            plt.xlabel('threshold')
            plt.ylabel('eigval error [%]')
            
            ax.set_xscale('log')


if False:
    #4 spearate images, Eigval Errors in Percent
    for threshold in thresholds[::4]:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.hist(RHS_errors[np.float32(threshold)], bins=np.logspace(-8,2,20), alpha = 0.5, label=str(threshold))  # density=False would make counts
        ax.set_xscale('log')
        plt.legend(loc="upper left")
    plt.show()

if False:
    # 4 seperate images
    # Eigval Error Histograms in H
    for threshold in thresholds[::2]:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_ylim([0, 15])
        plt.hist(Eigval_Hartree_errors[np.float32(threshold)], bins=np.logspace(-4,0,20), alpha = 0.5, label=str(threshold), edgecolor='black',)  # density=False would make counts
        ax.set_xscale('log')
        plt.legend(loc="upper left")
    plt.show()



if False:
# 4 figures with individual line charts showing one of five possible error metrics for all 56 systems over all thresholds
  for line in table:
      Individual_errors[line[2]+"_C:"+str(line[3])+"_S:"+str(line[4])+"_"+line[0]]['Error'].append(line[9]) # 8 -> eig [H], 9 -> eig [%], 10 -> E_H [H], 11 \rho [e⁻], 12 t~
      Individual_errors[line[2]+"_C:"+str(line[3])+"_S:"+str(line[4])+"_"+line[0]]['threshold'].append(line[6])
  
  ls = ['-', '--', '-.']
  j = 0 
  
  print(len(systems))
  for i in range(0,4):
    fig = plt.figure(figsize=(16,8))
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


#print(Individual_errors)

plt.show()

#for line in ...:
#    append(line[])
#for line in ...:
#    append(line[])
#for line in ...:
#    append(line[])
