## Physics based CNN for HIV drug resistance prediction
![Protein](https://cnnproteinhiv.files.wordpress.com/2017/11/biophysics.jpg)



### Introduction
The human immunodeficiency virus (HIV) is a retrovirus that causes Immunodeficiency syndrome (AIDS).  After its first clinical discovery in 1981, it has threatened a large number of the population in the world and more than 30 million people have been infected. Scientists have been doing a lot of research to fight the virus and it is still an active field of research since we still do not have medicine advanced enough to completely cure the disease .

The reason why HIV is a dangerous and challenging problem unlike other viruses is due to its ability to develop drug resistance. Once a person is infected, the virus replicates itself in the body with a huge number of variation in the genome which is also called as mutation. Even though there are many clinically available medicines that are effective at first, HIV quickly generates millions of mutants. Among these mutants, some of them become resistant to the dose of medicines and the viruses become active in our body again.

![Resistance](https://www.prezcobix.com/sites/www.prezcobix.com/files/know_your_risk_chart_621x240.jpg)

Therefore, in addition to drug design against the HIV virus, it is also important to predict which mutation would arise to avoid the medicines that not only screen out thousands of ineffective medicines but also gives us more control to selectively fight the mutation.

Predicting HIV drug resistance has received a lot of attention from both the science and machine learning community. Since this blog post is written for the greater public whom might not be from the scientific field, we will start with a short background of biology.

### Biology 101
Everyone knows that all organisms look different, have different characteristics and thus have different identities due to DNA or genome.  But how we look is not the only thing that our DNA encodes. Our DNA also encodes everything which ‘functions’ inside our body. Protein is a very important nutrient that we consume. DNA is a reservoir of various information and guidelines of what should be done in the body and protein is a functional unit which expresses the information and carries out the guideline. For example, some proteins digest our food, some proteins make various hormones or molecules that our body need, and some proteins are in charge of attacking bacteria and viruses to defend our body.

![Resistance](https://cnnproteinhiv.files.wordpress.com/2017/11/screenshot-from-2017-11-26-19-32-36.png)
As you can already guess, each section of DNA is ‘translated’ to a specific protein. More precisely, a DNA sequence is translated to an amino acid chain and this chain is folded into a 3D structure of the corresponding protein by various physical and chemical interactions. (See the figure above) Once this protein is folded, a special part of the protein binds to a target molecule to do what it is supposed to.  There are 20 different amino acids and there can be N^20 different protein structures with N-length of amino acid sequence.  Each protein will have different structures and thus have different physical characteristics. In short, protein structures determine what the protein does and how it is done.

Now, though whether a virus is a life or not, is another philosophical question, HIV virus shares the same central dogma of biology. One of the HIV proteins called ‘HIV protease’, is composed of 198 amino acid sequence and it binds to other substrates (which are colored with purple in the below image) to build something that HIV need to replicate and spread itself.

![Substrate](https://cnnproteinhiv.files.wordpress.com/2017/11/hivpr1.png?w=468&h=290)
Now how do we design a drug?  The site where this purple color substrate binds is called an ‘active site’  or a ‘binding site’. There are various types of interactions between proteins and this substrate that make the active side stable. Thus, medicines are usually designed to compete the natural substrate to bind the binding site. (Again, this is a very simple description of drug design and, of course, it is very sophisticated in reality) In the figure below, the purple colored natural substrate is substituted with a drug molecule so that it blocks the natural substrate to enter and bind.

![Ligand_bound](https://cnnproteinhiv.files.wordpress.com/2017/11/hivpr1.png?w=468&h=290)
Once we have a good analysis of the protein structure, we can target several interactions between several sites in the protein and a drug. Again, HIV will keep evolving and mutating different sites to weaken such interactions.

## Data and Methods for HIV drug resistance prediction
I covered what determines the drug resistance and how a drug is designed. Based on that, the general method for the drug resistance prediction is introduced in this part.

First, since drug resistance against HIV has been a serious concern, there have been a lot of effort to build a database of HIV mutants. One of the most well known database is HIVDB from Stanford.

![Ligand_bound](https://cnnproteinhiv.files.wordpress.com/2017/11/hivdb.jpg)
The above figure shows a set of mutations in HIV protease and the drug resistances which were experimentally measured. Each row represents a mutation. Each number on the first column is the location of mutation in the HIV amino acid chain between 1 and 99 and the following letter is the type of the mutated amino acid among 20 types. (For example, 90M means that 90th amino acid was mutated to Methionine) Each column is a set of experiment data for a drug represented with 3 letter code.  We used this data set for SQV and IDV in our project.

There are two big directions in predicting drug resistance. One is explicitly calculating the binding affinity between the binding site and the drug molecules.  Though the entire concept and practices cannot be introduced in this post, computational biologists/chemists have developed many computational tools to simulate the dynamics of proteins and chemical reactions using many sets of physical/chemical potential function. The following video is one of the example of what the simulations look like.

[Example MD simulation](https://youtu.be/fb8RBkRZwYg)

Using this molecular dynamic simulation with a given protein structure, one can calculate a binding free energy which can be directly compared to experimental measurements. This would be one of the most accurate but computationally expensive ways of predicting drug resistance. To obtain accurate results, it is required to run very long simulations to extract as many samples as possible. It usually takes more than an hour in local machines. And remember, the mutation data set have 786 different mutation samples per drug and this means that we need to independently run 786 simulations. And we might have many candidate drugs that we want to test and 786 independent simulation needs to be run for all these candidates.

On the other hand, there have been many attempts to predict the resistance by machine learning. The data input is usually just 786 different DNA sequences.  The accuracy of the prediction with this simple DNA sequences is known to be ~70%.(More sophisticated recent machine learning approach achieved more than 90% accuracy)  Of course, there is not any physical implication in this approach and using DNA sequences simply tries to find a pattern. (As explained above, what determines the function is the protein structure.) Also, the prediction is performed for each specific drug separately because there is no separable information about the drug molecules. In other words, a trained data for one drug cannot be used to predict the resistance for another drug molecule. Sometimes, this means that machine learning approach using DNA sequences is almost useless when one tries to predict the drug resistances with a newly developed drug because it would need another hundreds mutation experiment. (And at the end of the day, we would already have the whole set of resistance data by experiment even before training)

## Data Generation and Implementation
Therefore, it would be useful to develop a prediction model that is based on real physics which is not confined to one drug at a time but also fast enough to find the resistance patterns. To the best of my knowledge, there has not been a machine-learning approach based on real physical interactions other than using simple DNA/amino acid codes.

This project was inspired by the success of the deep convolutional neural network(CNN). After exhaustive simulation to calculate binding energy for a given drug molecule and mutation, scientists use visualization tools to identify and analyze the key interactions for candidate drug molecules in the target protein.

![Ligand_bound](https://cnnproteinhiv.files.wordpress.com/2017/11/drug-design.jpg?w=514&h=363)

Can’t we just use the images like above and try to find pattern that determines the resistance? Maybe. However, protein structures are too complicated for humans to perceive readily. There are literally thousands of interactions inside the protein. Moreover, we may not even have enough memory capacity to remember each observation in 786 different HIV protein structures and derive patterns.

I believe that if CNN is successful and sometimes even better than human for image pattern recognition, it can be also very useful to train the resistance patterns with the protein-drug interaction images.

Therefore, I propose a method based on explicit electrostatic interaction between the HIV protease protein and drugs using CNN. The main idea is to make a standard 3D image tensors that implicate the physical interactions. In this problem, I used protein structure with a HIV medicine, saquinavir(SQV) from Protein Data Bank . (PDB code:3D1Y) PDB files contain a x,y,z coordinate and atom type for each atom. Almost all of simulation tools use this file format as a starting point.

I first generate all 786 mutant protein structures and optimized them with steepest descent minimization to adjust the mutated amino acids. Since water molecules are important parts of biological system, water molecules are introduced and run 1ps molecular dynamic simulations. At the end of each simulation, we collect the electrostatic interaction from the entire system to each atom of drug molecules. All these structure optimization and electrostatic interactions were calculated with MOLARIS molecular dynamics package.

![Ligand_bound](https://cnnproteinhiv.files.wordpress.com/2017/11/electrostatic.jpg?w=485&h=293)

Until now, what we have is the total electrostatic interaction potential on each atom of the given drug molecule and the coordinate of each atom as shown above.  As mentioned, we want to make a ‘general’ model for prediction. The above example has a drug A and when we want to predict the resistance for a drug B,  the drug molecule may have different number of atoms and coordinates.

One way to standardize the data shape that we could think of was to make a 3D grids box around the binding site. We generate a 3D cubic box that is big enough to cover all possible drug molecules and introduce grid points with 0.5 °A space interval.
One problem of using grid box is that the coordinates of drug molecules are in continuous space while the grid points represent a prefixed position. Thus, we use each grid point to store information about the nearby atoms using the following function that we devised

![Ligand_bound](https://cnnproteinhiv.files.wordpress.com/2017/11/equation.jpg?w=320&h=52)

Ej  is the electrostatic interaction that j-th atom of the given drug molecule is receiving, dist_ij  is the distance between the j-th atom and i-th grid point.  The equation is a gaussian format which means the magnitude of electrostatic interaction, E_j, quickly vanishes if i-th grid is further than 0.5 °A which is the interval of grids that we use. We tried to use different standard deviation but if this is too big, some grids get mixed with too many interactions and if it is too narrow, some of interactions are not recorded. The data generation is depicted in the following figure.

![Ligand_bound](https://cnnproteinhiv.files.wordpress.com/2017/11/dddd1.png)

In this way, unlike the machine learning models based on sequence data which need separate training for different drugs, we only need one general training model for all types of drug molecules because we are using universal physical interactions.


## Training and results

Now we have a standardized data format as a 3D matrix and generated the data by python scripts from the calculations. HivDB cateogrize the extent of resistance into three classes but in this study, 'intermediate' and 'highly resistant' are treated as one because there are very little data for intermediate. But giving a weight for the loss function will be tried in the future.

I built a CNN model using TensorFlow. Since we have 3D matrix, we used ‘conv3d’ module with 5D input format [batch, depth, height, width, channel]. Note that each grid has only one value and, thus, the number of channels in our case is only one. However, ‘electrostatic interactions’ are not the only physical/chemical interactions, though it is one of the most dominating features. Extending the channel will be discussed at the end of this post.

Three convolutional layers and  three fully connected layers shows the best performance for now.

![Ligand_bound](https://cnnproteinhiv.files.wordpress.com/2017/11/training2.jpg)

6-fold cross-validation was performed after shuffling the whole data set. For now,  This project is still at an early stage but the validation accuracy and f1-score is in between 0.65 and 0.71. Early machine learning studies using protein/dna sequence data acheived 60~80% accuracy so I would say this is a quite optimistic start. 

## Next plan
My lab has done several computational chemistry research to directly calculate the resistance (reproducing k_cat/Km kinetics).  Many protein structural approach and machine learning algorithm neglect the importance of the 'state'. For HIV virus, it needs to mutate itself to avoid the interaction with drugs while keeping its own catalytic activity as a protease.  Thus, the elctrostatic interaciton between the mutant proteins and the natural substrate are in preparation and will be added to the network.
