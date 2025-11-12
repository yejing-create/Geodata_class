# An Analysis of Meander Migration Rates Pre- and Post-Cutoff
**Authors:** Ye JING
**Class:** AESDA G690

---

## Introduction

Meandering rivers are among the most common and recognizable features in fluvial landscapes [CITATION: camporeale2007], providing resources for industry, agriculture, and urban water use, in addition to diverse habitat for flora and fauna [CITATION: lizhi2023]. The characteristic sinuous form of meandering rivers is maintained by two recurrent planform-changing processes [CITATION: camporeale2005]. One process is meander elongation, which increases river sinuosity. By this process, the channel migrates laterally within the channel belt. An example of this river migration from 2006 (green meander scar) to 2017 (yellow meander scar) is shown in Fig. 1.
The second process is channel cut-off, which is the sudden reduction of sinuosity when a river bend is shortened by a new channel that connects two bend limbs of the same river [CITATION: camporeale2005, lizhi2023, gao2024]. A cutoff example is given in the Landsat imagery on the right side of Fig. 1. The cut-off process shortens the river length, and the abandoned channel segment can sometimes create an oxbow lake in the floodplain [CITATION: constantine2010, gallardo2011, guo2023, Maitan2024].

**Figure 1:** ![Multi-stage (modern and ancient) meander cutoffs along the Ucayali River, Peru (7$^\circ$38$'$2.15$"$ S, 75$^\circ$0$'$2.10$"$ W, affecting towns such as Santa Maria, Tumbes, San Roque, Monte de Cion, and others). Notice that the Ucayali River is dynamic inside of the geologic valley. Seven Landsat imageries (from 2006 to 2017) of the central river bend are shown, at where a cutoff occurred in 2014–2015. The maximum migration rate during this period was over 200 m/year. Figure from Li et al.,(2023).](https://github.com/yejing-create/Geodata_class/blob/main/Final_project/images/fig1.png)

Cutoffs are also known as accelerators of the migration rate over both short and long timescales. Over short time scales, cutoffs act as “shot” perturbations [CITATION: camporeale2008] to river morphodynamics by increasing the bed slope and stream power both upstream and downstream [CITATION: hooke2023], injecting downstream pulses of sediment excavated from the floodplain during chute channel formation [CITATION: zingerng], and substantially altering the local channel planform and hydrodynamics [CITATION: zingerjgr].
Over long time scales, cutoffs may influence meander migration rates through the creation of oxbow lakes that augment floodplain resistance heterogeneity [CITATION: schwenk2016].

Considerable attention has been given to local cutoff-induced channel response immediately adjacent to and within cutoffs [CITATION: hooke1995, zingerng, zingerjgr]. Recently, [AUTHOR-CITATION: schwenk2016] studied the river migration rate after 13 cutoffs in the Ucayali river in the Amazon basin and found that cutoffs nonlocally accelerate upstream and downstream migration and channel widening. However, since these previous studies are mostly case studies of cutoffs, whether and how the cutoff process affects the migration rate is still a research gap. We still need more data to understand how cutoffs change the migration rate globally.

---

## Goal

This proposal aims to analyze the meander migration rates pre- and post-cutoff based on a global dataset of cutoffs. The dataset contains 229 cutoff events and related Landsat imagery from 1984 to 2023. Using a computer vision process, I will analyze the loss and gain of water surface areas per year. Finally, I will estimate the migration rate of rivers per year and compare the migration rate of the main channel between pre-cutoff and post-cutoff cases to quantitatively understand how cutoff events change meander migration rates.

---

## Method

We will use parallelization for this project since we have 229 cases. In addition, we are doing image processing with computer vision techniques.

With help from colleagues at LSU, I obtained the global distribution of cutoffs whose widths are larger than 200 m (Fig. 2). The majority of cutoffs are concentrated in the Amazon basin. According to the position from the global distribution, our colleagues downloaded the Landsat imagery from Google Earth Engine, which is our primary data resource. We use the NDVI, a normalized value of the vegetation index in each pixel in Landsat imagery, as the criterion between water and land and generate the river mask according to this criterion. River masks are binary images, as shown in Fig. 3. Blue pixels represent the river channel whereas the shallow color pixels represent land.

In the example case shown in Fig. 3, the cutoff occurs between 1996 and 1997 (Fig. 3(b,c)). Thus it is clear that for this case, the duration 1984 - 1996 is the pre-cutoff period whereas the duration 1997 - 2023 is the post-cutoff period. Note that we neglect the period when the cutoff is occurring (1996–1997 in this case). This is because when the cutoff occurs, a new channel is generated and the previous channel is abandoned; thus, the movement of river channels is not a result of migration behavior.

**Figure 2:** ![The global distribution of cutoffs whose widths are larger than 200 m. Blue spots indicate chute cutoffs whereas red spots indicate neck cutoffs.](https://github.com/yejing-create/Geodata_class/blob/main/Final_project/images/global_distribution.png)

**Figure 3:** ![The example of river masks pre- and post-cutoff. (a) The river mask evolves to a cutoff event. (b) The river mask just before the cutoff event. (c) The river mask just after the cutoff event. (d) A river mask post-cutoff.](https://github.com/yejing-create/Geodata_class/blob/main/Final_project/images/figure2.pdf)

After obtaining this river mask, I have several methods to compute the migration rate. The first way is the easiest: by merging two river masks from two adjacent years, we compute the value difference of the blue band between the two river masks. If the value difference is negative, the pixel has switched from a deep blue (river) to a shallow blue (land), which indicates that the river has migrated away from that pixel. Conversely, if the value is positive, it means the pixel has switched from land to river. Then we compute the number of pixels with negative ($N_{neg}$) and positive ($N_{pos}$) values, respectively. We calculate the migration pixel number $M$ and channel enlargement/reduction $\Delta C$ by:

$$
\begin{aligned}
M &= \min(N_{\text{neg}}, N_{\text{pos}}) \\
\Delta C &= N_{\text{pos}} - N_{\text{neg}}
\end{aligned}
$$

By multiplying by the acreage of each pixel, we will obtain the migration rate and channel enlargement/reduction between the two adjacent years.

The second method is to apply an edge detection kernel to the river mask so we can get the boundaries between river and land for each river mask. Again, we merge boundaries from two adjacent years, get the number of pixels for river loss and gain, and apply Equation (1) to calculate the migration and channel enlargement/reduction.

Later on, for each case, I compute the average migration rate for period pre- $M_{pre}$ and post-cutoff $M_{post}$, respectively, and compute the dimensionless acceleration of migration $\frac{M_{post}}{M_{pre}}$. Similarly, I also compute the average $\Delta C_{pre}$ and $\Delta C_{post}$ and dimensionless them by the initial pixel numbers of water surface.

---

## Expected output

I expect to generate four figures.

Figure 1 will be a box chart; a sketch is shown in Fig. 4.

**Figure 4:** ![A sketch of figure 1 as the primary output. Panel 1 indicates how the migration rate accelerated by cutoffs can be differed between neck and chute cutoffs. Panel 2 indicates how the channel enlarge/reduce as a response to cutoff events.](https://github.com/yejing-create/Geodata_class/blob/main/Final_project/images/fig4.png)

In Figures 2–4, I will explore the relationship between migration rate and cutoff planform geometries. $\frac{M_{post}}{M_{pre}}$ will be plotted as a function of the length ratio of cutoff, bend curvature, and river type, respectively, to see how the acceleration of migration is affected by these parameters.

---

## References

* Camporeale, C., Perona, P., Porporato, A., & Ridolfi, L. (2005). On the long-term behavior of meandering rivers. *Water Resources Research*, *41*(12), W12409. doi: 10.1029/2005wr004109
* Camporeale, C., Perona, P., Porporato, A., & Ridolfi, L. (2007). Hierarchy of models for meandering rivers and related morphodynamic processes. *Reviews of Geophysics*, *45*(1). doi: 10.1029/2005rg000185
* Camporeale, C., Perucca, E., & Ridolfi, L. (2008). Significance of cutoff in meandering river dynamics. *Journal of Geophysical Research: Earth Surface*, *113*(F1). doi: 10.1029/2006jf000694
* Constantine, J. A., Dunne, T., Piégay, H., & Mathias Kondolf, G. (2010). Controls on the alluviation of oxbow lakes by bed-material load along the Sacramento River, California. *Sedimentology*, *57*(2), 389-407. doi: 10.1111/j.1365-3091.2009.01084.x
* Gallardo, B., Cabezas, A., Gonzalez, E., & Comín, F. A. (2011). Effectiveness of a newly created oxbow lake to mitigate habitat loss and increase biodiversity in a regulated floodplain. *Restoration Ecology*, *20*(3), 387-394. doi: 10.1111/j.1526-100X.2010.00766.x
* Gao, W., Wang, Z. B., Kleinhans, M. G., Shao, D., Zhu, Z., & Yang, Z. (2024). Bifurcation instability modulated by a connecting channel leads to periodic water partitioning in a simple channel network. *Water Resources Research*, *60*(11), e2024WR037668. doi: 10.1029/2024wr037668
* Guo, X., Gao, P., & Li, Z. (2023). Hydrologic connectivity and morphologic variation of oxbow lakes in a pristine alpine fluvial system. *Journal of Hydrology*, *623*, 129768. doi: 10.1016/j.jhydrol.2023.129768
* Hooke, J. (2023). Morphodynamics of active meandering rivers reviewed in a hierarchy of spatial and temporal scales. *Geomorphology*, *439*, 108825. doi: 10.1016/j.geomorph.2023.108825
* Hooke, J. M. (1995). River channel adjustment to meander cutoffs on the river Bollin and river Dane, northwest England. *Geomorphology*, *14*(3), 235-250. doi: 10.1016/0169-555X(95)00047-G
* Li, Z., Mendoza, A., Abad, J. D., Endreny, T. A., Han, B., Carrisoza, E., & Dominguez, R. (2023). High-resolution modeling of meander neck cutoffs: laboratory and field scales. *Frontiers in Earth Science*, *11*. doi: 10.3389/feart.2023.1208782
* Maitan, R., Finotello, A., Tognin, D., D’Alpaos, A., Fielding, C. R., Ielpi, A., & Ghinassi, M. (2024). Hydrologically driven modulation of cutoff regime in meandering rivers. *Geology*, *52*(5), 336-340. doi: 10.1130/g51783.1
* Schwenk, J., & Foufoula-Georgiou, E. (2016). Meander cutoffs nonlocally accelerate upstream and downstream migration and channel widening. *Geophysical Research Letters*, *43*(24). doi: 10.1002/2016gl071670
* Zinger, J. A., Rhoads, B. L., & Best, J. L. (2011). Extreme sediment pulses generated by bend cutoffs along a large meandering river. *Nature Geoscience*, *4*(10), 675-678. doi: 10.1038/ngeo1260
* Zinger, J. A., Rhoads, B. L., Best, J. L., & Johnson, K. K. (2013). Flow structure and channel morphodynamics of meander bend chute cutoffs: A case study of the Wabash River, USA. *Journal of Geophysical Research: Earth Surface*, *118*(4), 2468-2487. doi: 10.1002/jgrf.20155
