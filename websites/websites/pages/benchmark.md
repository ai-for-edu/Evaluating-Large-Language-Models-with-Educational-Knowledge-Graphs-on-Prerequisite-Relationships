---
title: Benchmarking LLMs on KGs with KCs and prerequisite relationships.
description: Here comes the benchmarking results.
background: /assets/theme/images/Background_4_LLMS.png
permalink: /benchmark/
toc: true
---

## Benchmarking on One-hop Relationship Verification

The results shown in the tables are the accuracy of investigated LLMs on the task of one-hop relationship verification. 

### a) AUROC values (in %) of investigated structural inference methods on BN trajectories.

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">LLM</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>96.12 &#177; 0.40</td>
        <td>98.08 &#177; 0.22</td>
        <td>98.83 &#177; 0.09</td>
        <td>99.43 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>93.14 &#177; 0.67</td>
        <td>96.44 &#177; 0.76</td>
        <td>97.72 &#177; 0.26</td>
        <td>98.72 &#177; 0.04</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>94.10 &#177; 0.66</td>
        <td>96.45 &#177; 0.31</td>
        <td>97.78 &#177; 0.19</td>
        <td>98.83 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>95.39 &#177; 0.48</td>
        <td>96.72 &#177; 0.56</td>
        <td>97.73 &#177; 0.19</td>
        <td>98.84 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>88.45 &#177; 0.61</td>
        <td>93.16 &#177; 0.69</td>
        <td>94.28 &#177; 0.26</td>
        <td>96.17 &#177; 0.12</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>48.71 &#177; 1.37</td>
        <td>62.41 &#177; 1.64</td>
        <td>68.79 &#177; 2.53</td>
        <td>69.36 &#177; 1.50</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>90.70 &#177; 2.97</td>
        <td>99.87 &#177; 0.01</td>
        <td>99.89 &#177; 0.00</td>
        <td>99.97 &#177; 0.00</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>100.00 &#177; 0.00</td>
        <td>100.00 &#177; 0.00</td>
        <td>100.00 &#177; 0.00</td>
        <td>100.00 &#177; 0.00</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>99.75 &#177; 0.00</td>
        <td>99.57 &#177; 0.00</td>
        <td>99.12 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">97.54 &#177; 0.02</td>
        <td>99.79 &#177; 0.00</td>
        <td>98.73 &#177; 0.00</td>
        <td>76.08 &#177; 0.01</td>
        <td>75.26 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>99.75 &#177; 0.00</td>
        <td>99.60 &#177; 0.00</td>
        <td>98.96 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">99.57 &#177; 0.01</td>
        <td>99.87 &#177; 0.00</td>
        <td>98.95 &#177; 0.00</td>
        <td>80.96 &#177; 0.01</td>
        <td>79.88 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>99.98 &#177; 0.00</td>
        <td>99.95 &#177; 0.00</td>
        <td>99.97 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">98.69 &#177; 0.01</td>
        <td>99.95 &#177; 0.00</td>
        <td>99.56 &#177; 0.00</td>
        <td>98.60 &#177; 0.01</td>
        <td>79.92 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>99.97 &#177; 0.00</td>
        <td>99.94 &#177; 0.00</td>
        <td>99.95 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">98.92 &#177; 0.01</td>
        <td>99.91 &#177; 0.00</td>
        <td>99.62 &#177; 0.00</td>
        <td>98.59 &#177; 0.01</td>
        <td>76.41 &#177; 0.01</td>
    </tr>
</table>


### b) AUROC values (in %) of investigated structural inference methods on CRNA trajectories

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>91.37 &#177; 1.10</td>
        <td>90.35 &#177; 0.39</td>
        <td>90.26 &#177; 0.54</td>
        <td>89.16 &#177; 0.55</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>84.40 &#177; 2.84</td>
        <td>74.88 &#177; 0.64</td>
        <td>69.41 &#177; 0.64</td>
        <td>60.10 &#177; 0.46</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>78.11 &#177; 1.50</td>
        <td>77.93 &#177; 1.00</td>
        <td>77.55 &#177; 0.80</td>
        <td>75.74 &#177; 0.89</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>86.01 &#177; 1.98</td>
        <td>86.59 &#177; 1.06</td>
        <td>84.24 &#177; 0.76</td>
        <td>81.14 &#177; 1.24</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>85.70 &#177; 3.35</td>
        <td>75.38 &#177; 0.42</td>
        <td>70.81 &#177; 1.99</td>
        <td>82.74 &#177; 0.88</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>55.19 &#177; 3.80</td>
        <td>52.19 &#177; 0.22</td>
        <td>50.78 &#177; 0.25</td>
        <td>50.94 &#177; 0.74</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>56.92 &#177; 6.83</td>
        <td>50.32 &#177; 1.36</td>
        <td>50.12 &#177; 0.84</td>
        <td>50.35 &#177; 0.60</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>99.60 &#177; 0.30</td>
        <td>99.58 &#177; 0.13</td>
        <td>97.40 &#177; 0.52</td>
        <td>51.48 &#177; 0.22</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>83.91 &#177; 0.03</td>
        <td>72.81 &#177; 0.05</td>
        <td>70.73 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">65.32 &#177; 0.02</td>
        <td>49.47 &#177; 0.02</td>
        <td>49.03 &#177; 0.03</td>
        <td>50.06 &#177; 0.02</td>
        <td>50.65 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>85.90 &#177; 0.04</td>
        <td>75.41 &#177; 0.01</td>
        <td>69.97 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">64.51 &#177; 0.02</td>
        <td>48.26 &#177; 0.02</td>
        <td>48.40 &#177; 0.03</td>
        <td>51.42 &#177; 0.01</td>
        <td>50.21 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>85.75 &#177; 0.03</td>
        <td>73.71 &#177; 0.01</td>
        <td>68.25 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">64.87 &#177; 0.02</td>
        <td>49.72 &#177; 0.01</td>
        <td>51.16 &#177; 0.04</td>
        <td>50.06 &#177; 0.01</td>
        <td>50.56 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>87.01 &#177; 0.02</td>
        <td>78.21 &#177; 0.05</td>
        <td>70.72 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">62.31 &#177; 0.02</td>
        <td>51.04 &#177; 0.01</td>
        <td>50.24 &#177; 0.04</td>
        <td>51.26 &#177; 0.01</td>
        <td>50.87 &#177; 0.02</td>
    </tr>
</table>

### c) AUROC values (in %) of investigated structural inference methods on FW trajectories.

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>78.21 &#177; 1.57</td>
        <td>73.63 &#177; 1.75</td>
        <td>72.76 &#177; 1.04</td>
        <td>71.72 &#177; 0.15</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>64.15 &#177; 1.55</td>
        <td>58.00 &#177; 0.61</td>
        <td>57.92 &#177; 0.84</td>
        <td>53.97 &#177; 0.44</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>66.07 &#177; 4.26</td>
        <td>65.40 &#177; 3.82</td>
        <td>68.39 &#177; 0.24</td>
        <td>53.18 &#177; 2.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>79.69 &#177; 3.33</td>
        <td>74.20 &#177; 1.57</td>
        <td>73.94 &#177; 1.01</td>
        <td>44.50 &#177; 2.24</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>78.82 &#177; 3.75</td>
        <td>50.00 &#177; 0.00</td>
        <td>50.00 &#177; 0.00</td>
        <td>64.72 &#177; 1.39</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>52.96 &#177; 2.66</td>
        <td>54.25 &#177; 1.16</td>
        <td>51.02 &#177; 1.59</td>
        <td>51.73 &#177; 0.92</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>47.98 &#177; 2.67</td>
        <td>49.89 &#177; 1.29</td>
        <td>49.40 &#177; 0.58</td>
        <td>51.26 &#177; 1.07</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>84.84 &#177; 1.90</td>
        <td>73.00 &#177; 4.00</td>
        <td>52.36 &#177; 0.35</td>
        <td>49.11 &#177; 0.77</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>81.80 &#177; 0.01</td>
        <td>76.75 &#177; 0.02</td>
        <td>74.15 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">71.57 &#177; 0.01</td>
        <td>49.30 &#177; 0.03</td>
        <td>48.50 &#177; 0.03</td>
        <td>50.75 &#177; 0.02</td>
        <td>47.56 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>81.89 &#177; 0.01</td>
        <td>76.38 &#177; 0.02</td>
        <td>73.50 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">71.12 &#177; 0.01</td>
        <td>50.74 &#177; 0.06</td>
        <td>50.19 &#177; 0.01</td>
        <td>50.49 &#177; 0.03</td>
        <td>49.82 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>81.87 &#177; 0.02</td>
        <td>75.97 &#177; 0.01</td>
        <td>73.59 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">71.52 &#177; 0.01</td>
        <td>53.01 &#177; 0.08</td>
        <td>50.66 &#177; 0.01</td>
        <td>51.22 &#177; 0.03</td>
        <td>53.01 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>81.95 &#177; 0.01</td>
        <td>76.75 &#177; 0.01</td>
        <td>74.38 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">72.21 &#177; 0.02</td>
        <td>53.36 &#177; 0.03</td>
        <td>50.78 &#177; 0.03</td>
        <td>50.46 &#177; 0.03</td>
        <td>51.07 &#177; 0.01</td>
    </tr>
</table>

### d) AUROC values (in %) of investigated structural inference methods on GCN trajectories.

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>96.72 &#177; 1.64</td>
        <td>98.48 &#177; 0.35</td>
        <td>98.55 &#177; 0.22</td>
        <td>98.20 &#177; 0.42</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>91.72 &#177; 4.28</td>
        <td>87.90 &#177; 1.44</td>
        <td>80.44 &#177; 1.78</td>
        <td>78.12 &#177; 0.15</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>95.24 &#177; 0.00</td>
        <td>91.15 &#177; 2.18</td>
        <td>92.75 &#177; 1.94</td>
        <td>94.04 &#177; 0.71</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>94.57 &#177; 2.14</td>
        <td>97.48 &#177; 0.54</td>
        <td>97.25 &#177; 0.76</td>
        <td>96.40 &#177; 0.21</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>92.75 &#177; 3.92</td>
        <td>91.98 &#177; 0.90</td>
        <td>92.01 &#177; 1.23</td>
        <td>94.17 &#177; 1.25</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>50.47 &#177; 2.55</td>
        <td>49.31 &#177; 1.72</td>
        <td>48.17 &#177; 2.80</td>
        <td>49.51 &#177; 0.77</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>46.70 &#177; 5.05</td>
        <td>47.86 &#177; 4.04</td>
        <td>50.46 &#177; 1.93</td>
        <td>49.58 &#177; 1.37</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>93.28 &#177; 2.47</td>
        <td>96.71 &#177; 0.51</td>
        <td>96.74 &#177; 0.62</td>
        <td>94.95 &#177; 0.33</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>97.42 &#177; 0.00</td>
        <td>93.38 &#177; 0.01</td>
        <td>89.54 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">83.78 &#177; 0.01</td>
        <td>43.46 &#177; 0.02</td>
        <td>52.74 &#177; 0.06</td>
        <td>50.98 &#177; 0.02</td>
        <td>50.34 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>97.95 &#177; 0.01</td>
        <td>92.62 &#177; 0.01</td>
        <td>89.96 &#177; 0.03</td>
        <td style="border-right: 2px solid white;">90.73 &#177; 0.02</td>
        <td>42.23 &#177; 0.03</td>
        <td>46.12 &#177; 0.04</td>
        <td>47.66 &#177; 0.03</td>
        <td>49.87 &#177; 0.04</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>98.82 &#177; 0.01</td>
        <td>92.68 &#177; 0.02</td>
        <td>85.81 &#177; 0.03</td>
        <td style="border-right: 2px solid white;">84.98 &#177; 0.02</td>
        <td>52.59 &#177; 0.03</td>
        <td>66.65 &#177; 0.07</td>
        <td>63.01 &#177; 0.07</td>
        <td>53.07 &#177; 0.06</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>98.93 &#177; 0.01</td>
        <td>93.16 &#177; 0.01</td>
        <td>89.53 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">87.60 &#177; 0.01</td>
        <td>56.41 &#177; 0.06</td>
        <td>52.07 &#177; 0.03</td>
        <td>52.96 &#177; 0.03</td>
        <td>50.78 &#177; 0.03</td>
    </tr>
</table>

### e) AUROC values (in %) of investigated structural inference methods on GGN trajectories.

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>86.12 &#177; 0.98</td>
        <td>88.72 &#177; 1.33</td>
        <td>89.83 &#177; 0.89</td>
        <td>89.61 &#177; 0.93</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>79.09 &#177; 1.07</td>
        <td>85.16 &#177; 2.26</td>
        <td>85.85 &#177; 1.96</td>
        <td>87.41 &#177; 2.73</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>70.46 &#177; 3.52</td>
        <td>70.05 &#177; 2.10</td>
        <td>70.73 &#177; 1.90</td>
        <td>69.48 &#177; 2.10</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>78.25 &#177; 0.49</td>
        <td>76.48 &#177; 1.91</td>
        <td>75.67 &#177; 1.29</td>
        <td>73.09 &#177; 2.10</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>57.49 &#177; 3.59</td>
        <td>63.51 &#177; 2.69</td>
        <td>65.95 &#177; 1.41</td>
        <td>63.85 &#177; 2.00</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>44.89 &#177; 7.52</td>
        <td>47.79 &#177; 3.50</td>
        <td>45.50 &#177; 3.03</td>
        <td>46.15 &#177; 2.41</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>64.23 &#177; 4.75</td>
        <td>59.69 &#177; 6.09</td>
        <td>54.38 &#177; 3.18</td>
        <td>58.53 &#177; 3.94</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>80.08 &#177; 3.81</td>
        <td>83.77 &#177; 0.49</td>
        <td>84.51 &#177; 0.43</td>
        <td>83.47 &#177; 1.31</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>91.65 &#177; 0.01</td>
        <td>90.45 &#177; 0.01</td>
        <td>90.35 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">88.14 &#177; 0.02</td>
        <td>78.08 &#177; 0.03</td>
        <td>57.01 &#177; 0.05</td>
        <td>55.71 &#177; 0.05</td>
        <td>58.33 &#177; 0.04</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>91.10 &#177; 0.00</td>
        <td>88.21 &#177; 0.01</td>
        <td>86.78 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">90.07 &#177; 0.03</td>
        <td>80.18 &#177; 0.04</td>
        <td>69.78 &#177; 0.07</td>
        <td>62.65 &#177; 0.02</td>
        <td>53.99 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>94.02 &#177; 0.01</td>
        <td>93.25 &#177; 0.02</td>
        <td>84.60 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">85.30 &#177; 0.02</td>
        <td>70.46 &#177; 0.04</td>
        <td>57.36 &#177; 0.03</td>
        <td>72.25 &#177; 0.05</td>
        <td>66.74 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>92.91 &#177; 0.01</td>
        <td>90.06 &#177; 0.01</td>
        <td>90.15 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">87.94 &#177; 0.04</td>
        <td>71.11 &#177; 0.04</td>
        <td>56.25 &#177; 0.02</td>
        <td>57.15 &#177; 0.02</td>
        <td>62.13 &#177; 0.02</td>
    </tr>
</table>

### f) AUROC values (in %) of investigated structural inference methods on IN trajectories.

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>94.14 &#177; 0.54</td>
        <td>96.13 &#177; 1.65</td>
        <td>97.64 &#177; 0.11</td>
        <td>97.61 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>94.39 &#177; 1.34</td>
        <td>91.79 &#177; 5.82</td>
        <td>86.31 &#177; 1.42</td>
        <td>78.25 &#177; 0.52</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>85.82 &#177; 3.90</td>
        <td>87.77 &#177; 5.36</td>
        <td>83.05 &#177; 2.84</td>
        <td>86.14 &#177; 0.54</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>87.17 &#177; 0.26</td>
        <td>92.45 &#177; 2.50</td>
        <td>89.58 &#177; 3.93</td>
        <td>92.82 &#177; 1.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>81.90 &#177; 1.92</td>
        <td>85.16 &#177; 1.59</td>
        <td>84.84 &#177; 2.89</td>
        <td>89.35 &#177; 0.48</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>54.29 &#177; 4.17</td>
        <td>50.81 &#177; 1.34</td>
        <td>50.68 &#177; 3.52</td>
        <td>50.76 &#177; 0.53</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>58.18 &#177; 4.97</td>
        <td>70.18 &#177; 15.42</td>
        <td>68.08 &#177; 8.25</td>
        <td>50.22 &#177; 1.78</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>99.00 &#177; 0.85</td>
        <td>99.69 &#177; 0.07</td>
        <td>99.90 &#177; 0.04</td>
        <td>99.91 &#177; 0.05</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>93.09 &#177; 0.01</td>
        <td>90.54 &#177; 0.05</td>
        <td>88.10 &#177; 0.03</td>
        <td style="border-right: 2px solid white;">82.51 &#177; 0.03</td>
        <td>60.47 &#177; 0.04</td>
        <td>61.78 &#177; 0.06</td>
        <td>56.45 &#177; 0.04</td>
        <td>53.96 &#177; 0.04</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>93.33 &#177; 0.02</td>
        <td>89.12 &#177; 0.05</td>
        <td>87.69 &#177; 0.04</td>
        <td style="border-right: 2px solid white;">81.37 &#177; 0.02</td>
        <td>68.39 &#177; 0.06</td>
        <td>55.11 &#177; 0.08</td>
        <td>53.88 &#177; 0.02</td>
        <td>53.04 &#177; 0.05</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>95.61 &#177; 0.02</td>
        <td>89.59 &#177; 0.05</td>
        <td>86.47 &#177; 0.03</td>
        <td style="border-right: 2px solid white;">83.45 &#177; 0.03</td>
        <td>63.83 &#177; 0.03</td>
        <td>64.70 &#177; 0.09</td>
        <td>54.18 &#177; 0.03</td>
        <td>54.37 &#177; 0.04</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>95.37 &#177; 0.02</td>
        <td>90.72 &#177; 0.05</td>
        <td>87.79 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">84.00 &#177; 0.02</td>
        <td>62.18 &#177; 0.03</td>
        <td>61.91 &#177; 0.01</td>
        <td>56.50 &#177; 0.02</td>
        <td>53.85 &#177; 0.02</td>
    </tr>
</table>

### g) AUROC values (in %) of investigated structural inference methods on LN trajectories

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>99.49 &#177; 0.56</td>
        <td>95.04 &#177; 5.20</td>
        <td>86.75 &#177; 1.66</td>
        <td>79.32 &#177; 4.32</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>84.15 &#177; 1.16</td>
        <td>87.38 &#177; 3.32</td>
        <td>92.22 &#177; 0.42</td>
        <td>93.97 &#177; 1.96</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>92.33 &#177; 4.84</td>
        <td>80.36 &#177; 5.67</td>
        <td>71.17 &#177; 0.48</td>
        <td>62.82 &#177; 8.36</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>97.35 &#177; 3.17</td>
        <td>96.56 &#177; 4.87</td>
        <td>91.04 &#177; 2.35</td>
        <td>95.04 &#177; 0.53</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>97.53 &#177; 1.01</td>
        <td>82.03 &#177; 7.28</td>
        <td>88.58 &#177; 1.69</td>
        <td>94.18 &#177; 2.28</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>54.22 &#177; 3.98</td>
        <td>56.16 &#177; 3.88</td>
        <td>52.12 &#177; 2.49</td>
        <td>52.55 &#177; 1.62</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>51.32 &#177; 5.21</td>
        <td>50.12 &#177; 2.42</td>
        <td>50.49 &#177; 1.22</td>
        <td>67.32 &#177; 14.23</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>97.21 &#177; 1.13</td>
        <td>96.95 &#177; 2.10</td>
        <td>96.90 &#177; 0.83</td>
        <td>97.99 &#177; 0.93</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>97.01 &#177; 0.02</td>
        <td>94.94 &#177; 0.00</td>
        <td>87.10 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">82.80 &#177; 0.01</td>
        <td>56.00 &#177; 0.04</td>
        <td>53.94 &#177; 0.02</td>
        <td>54.36 &#177; 0.02</td>
        <td>51.75 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>96.99 &#177; 0.02</td>
        <td>95.79 &#177; 0.01</td>
        <td>87.58 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">83.92 &#177; 0.02</td>
        <td>61.94 &#177; 0.03</td>
        <td>61.56 &#177; 0.04</td>
        <td>53.36 &#177; 0.02</td>
        <td>50.19 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>97.92 &#177; 0.01</td>
        <td>95.53 &#177; 0.02</td>
        <td>86.92 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">84.22 &#177; 0.03</td>
        <td>52.18 &#177; 0.02</td>
        <td>62.08 &#177; 0.05</td>
        <td>53.44 &#177; 0.01</td>
        <td>50.42 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>97.38 &#177; 0.02</td>
        <td>94.70 &#177; 0.02</td>
        <td>87.44 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">83.15 &#177; 0.02</td>
        <td>59.19 &#177; 0.05</td>
        <td>56.18 &#177; 0.03</td>
        <td>55.73 &#177; 0.03</td>
        <td>52.30 &#177; 0.02</td>
    </tr>
</table>

### h) AUROC values (in %) of investigated structural inference methods on MMO trajectories

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>96.42 &#177; 0.02</td>
        <td>98.28 &#177; 0.00</td>
        <td>98.98 &#177; 0.00</td>
        <td>99.49 &#177; 0.00</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>99.88 &#177; 0.01</td>
        <td>99.98 &#177; 0.00</td>
        <td>100.00 &#177; 0.00</td>
        <td>100.00 &#177; 0.00</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>89.76 &#177; 0.16</td>
        <td>96.60 &#177; 1.51</td>
        <td>97.09 &#177; 1.07</td>
        <td>98.11 &#177; 0.79</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>96.43 &#177; 0.00</td>
        <td>98.28 &#177; 0.00</td>
        <td>98.98 &#177; 0.00</td>
        <td>98.81 &#177; 0.37</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>44.74 &#177; 4.70</td>
        <td>70.03 &#177; 7.65</td>
        <td>77.24 &#177; 1.02</td>
        <td>75.01 &#177; 0.29</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>69.85 &#177; 12.21</td>
        <td>38.03 &#177; 25.86</td>
        <td>20.70 &#177; 10.19</td>
        <td>23.88 &#177; 15.76</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>16.90 &#177; 2.38</td>
        <td>23.49 &#177; 5.12</td>
        <td>23.31 &#177; 4.03</td>
        <td>45.89 &#177; 20.23</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>59.77 &#177; 2.14</td>
        <td>81.64 &#177; 6.68</td>
        <td>72.13 &#177; 11.09</td>
        <td>63.83 &#177; 6.71</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>99.62 &#177; 0.00</td>
        <td>84.96 &#177; 0.02</td>
        <td>77.66 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">78.04 &#177; 0.02</td>
        <td>68.34 &#177; 0.03</td>
        <td>66.21 &#177; 0.06</td>
        <td>57.84 &#177; 0.03</td>
        <td>56.10 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>99.68 &#177; 0.00</td>
        <td>93.89 &#177; 0.01</td>
        <td>85.53 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">85.46 &#177; 0.01</td>
        <td>71.88 &#177; 0.03</td>
        <td>59.46 &#177; 0.06</td>
        <td>64.14 &#177; 0.03</td>
        <td>58.05 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>99.83 &#177; 0.00</td>
        <td>88.32 &#177; 0.01</td>
        <td>87.02 &#177; 0.03</td>
        <td style="border-right: 2px solid white;">86.75 &#177; 0.02</td>
        <td>79.34 &#177; 0.04</td>
        <td>65.48 &#177; 0.07</td>
        <td>54.78 &#177; 0.04</td>
        <td>57.06 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>99.84 &#177; 0.00</td>
        <td>89.77 &#177; 0.01</td>
        <td>87.47 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">85.47 &#177; 0.01</td>
        <td>74.58 &#177; 0.03</td>
        <td>64.71 &#177; 0.06</td>
        <td>56.07 &#177; 0.04</td>
        <td>58.80 &#177; 0.01</td>
    </tr>
</table>

### i) AUROC values (in %) of investigated structural inference methods on RNLO trajectories

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>96.36 &#177; 0.10</td>
        <td>98.28 &#177; 0.00</td>
        <td>98.95 &#177; 0.04</td>
        <td>99.25 &#177; 0.38</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>99.82 &#177; 0.06</td>
        <td>99.98 &#177; 0.00</td>
        <td>99.99 &#177; 0.00</td>
        <td>99.99 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>93.47 &#177; 2.99</td>
        <td>95.67 &#177; 1.61</td>
        <td>97.02 &#177; 0.86</td>
        <td>98.03 &#177; 0.43</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>96.35 &#177; 0.12</td>
        <td>98.28 &#177; 0.00</td>
        <td>98.72 &#177; 0.31</td>
        <td>98.62 &#177; 0.29</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>56.18 &#177; 6.51</td>
        <td>72.67 &#177; 10.76</td>
        <td>74.36 &#177; 6.83</td>
        <td>71.95 &#177; 2.31</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>38.49 &#177; 1.57</td>
        <td>47.15 &#177; 18.16</td>
        <td>46.52 &#177; 26.84</td>
        <td>20.23 &#177; 13.56</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>15.96 &#177; 2.97</td>
        <td>21.37 &#177; 8.84</td>
        <td>27.57 &#177; 7.69</td>
        <td>56.44 &#177; 21.63</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>83.55 &#177; 8.24</td>
        <td>81.05 &#177; 5.42</td>
        <td>81.82 &#177; 5.07</td>
        <td>67.30 &#177; 12.31</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>95.54 &#177; 0.02</td>
        <td>72.53 &#177; 0.08</td>
        <td>72.72 &#177; 0.03</td>
        <td style="border-right: 2px solid white;">75.07 &#177; 0.02</td>
        <td>69.43 &#177; 0.04</td>
        <td>67.70 &#177; 0.08</td>
        <td>60.55 &#177; 0.03</td>
        <td>62.42 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>96.20 &#177; 0.02</td>
        <td>93.44 &#177; 0.03</td>
        <td>75.83 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">79.14 &#177; 0.02</td>
        <td>57.32 &#177; 0.05</td>
        <td>53.75 &#177; 0.01</td>
        <td>61.68 &#177; 0.05</td>
        <td>65.45 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>97.40 &#177; 0.01</td>
        <td>83.70 &#177; 0.06</td>
        <td>78.50 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">79.36 &#177; 0.02</td>
        <td>72.62 &#177; 0.03</td>
        <td>62.34 &#177; 0.01</td>
        <td>56.90 &#177; 0.05</td>
        <td>60.05 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>97.45 &#177; 0.01</td>
        <td>81.60 &#177; 0.05</td>
        <td>78.51 &#177; 0.03</td>
        <td style="border-right: 2px solid white;">79.08 &#177; 0.03</td>
        <td>64.79 &#177; 0.05</td>
        <td>57.10 &#177; 0.02</td>
        <td>64.50 &#177; 0.05</td>
        <td>66.01 &#177; 0.02</td>
    </tr>
</table>

### j) AUROC values (in %) of investigated structural inference methods on SN trajectories

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>93.77 &#177; 0.59</td>
        <td>94.17 &#177; 0.28</td>
        <td>94.74 &#177; 0.44</td>
        <td>94.37 &#177; 0.05</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>90.20 &#177; 1.52</td>
        <td>82.82 &#177; 0.30</td>
        <td>78.22 &#177; 1.92</td>
        <td>67.98 &#177; 0.57</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>80.80 &#177; 3.58</td>
        <td>78.78 &#177; 3.00</td>
        <td>80.42 &#177; 1.00</td>
        <td>81.49 &#177; 0.32</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>85.08 &#177; 0.54</td>
        <td>87.70 &#177; 1.11</td>
        <td>89.81 &#177; 0.74</td>
        <td>88.24 &#177; 0.60</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>83.96 &#177; 2.44</td>
        <td>84.29 &#177; 1.00</td>
        <td>84.66 &#177; 0.70</td>
        <td>91.76 &#177; 0.25</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>56.52 &#177; 2.94</td>
        <td>51.30 &#177; 0.50</td>
        <td>50.38 &#177; 0.50</td>
        <td>50.74 &#177; 1.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>62.48 &#177; 5.44</td>
        <td>55.74 &#177; 3.23</td>
        <td>50.00 &#177; 1.70</td>
        <td>50.20 &#177; 0.77</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>99.83 &#177; 0.21</td>
        <td>99.88 &#177; 0.07</td>
        <td>99.74 &#177; 0.12</td>
        <td>98.81 &#177; 0.12</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>93.26 &#177; 0.01</td>
        <td>79.96 &#177; 0.02</td>
        <td>80.40 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">71.84 &#177; 0.01</td>
        <td>58.41 &#177; 0.04</td>
        <td>51.43 &#177; 0.01</td>
        <td>49.57 &#177; 0.03</td>
        <td>50.16 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>93.47 &#177; 0.01</td>
        <td>81.17 &#177; 0.01</td>
        <td>79.63 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">68.76 &#177; 0.02</td>
        <td>65.24 &#177; 0.05</td>
        <td>52.96 &#177; 0.03</td>
        <td>49.28 &#177; 0.02</td>
        <td>50.76 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>92.68 &#177; 0.00</td>
        <td>79.32 &#177; 0.01</td>
        <td>75.90 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">69.36 &#177; 0.03</td>
        <td>67.42 &#177; 0.02</td>
        <td>50.87 &#177; 0.01</td>
        <td>53.12 &#177; 0.03</td>
        <td>50.08 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>93.51 &#177; 0.00</td>
        <td>81.38 &#177; 0.01</td>
        <td>80.80 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">69.25 &#177; 0.01</td>
        <td>66.14 &#177; 0.04</td>
        <td>53.79 &#177; 0.03</td>
        <td>54.83 &#177; 0.01</td>
        <td>51.72 &#177; 0.02</td>
    </tr>
</table>

### k) AUROC values (in %) of investigated structural inference methods on VN trajectories

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">Springs</th>
        <th style="border-bottom: 2px solid white;" colspan="4">NetSims</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>96.68 &#177; 0.01</td>
        <td>98.33 &#177; 0.01</td>
        <td>99.00 &#177; 0.00</td>
        <td>99.50 &#177; 0.00</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>99.28 &#177; 0.18</td>
        <td>99.41 &#177; 0.15</td>
        <td>99.62 &#177; 0.09</td>
        <td>99.84 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>96.66 &#177; 0.03</td>
        <td>97.85 &#177; 0.09</td>
        <td>98.54 &#177; 0.01</td>
        <td>99.08 &#177; 0.00</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>96.68 &#177; 0.00</td>
        <td>98.34 &#177; 0.00</td>
        <td>99.00 &#177; 0.00</td>
        <td>99.50 &#177; 0.00</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>76.51 &#177; 2.67</td>
        <td>85.70 &#177; 3.99</td>
        <td>91.80 &#177; 0.43</td>
        <td>95.01 &#177; 0.70</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>51.56 &#177; 5.64</td>
        <td>52.71 &#177; 4.98</td>
        <td>57.68 &#177; 2.56</td>
        <td>59.50 &#177; 0.83</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>92.81 &#177; 2.83</td>
        <td>97.33 &#177; 1.01</td>
        <td>97.87 &#177; 0.66</td>
        <td>97.30 &#177; 1.26</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td style="border-right: 2px solid white;">-</td>
        <td>97.99 &#177; 0.49</td>
        <td>98.54 &#177; 0.38</td>
        <td>99.21 &#177; 0.12</td>
        <td>99.59 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>94.58 &#177; 0.01</td>
        <td>95.12 &#177; 0.01</td>
        <td>94.65 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">89.17 &#177; 0.02</td>
        <td>90.31 &#177; 0.01</td>
        <td>74.64 &#177; 0.04</td>
        <td>69.78 &#177; 0.03</td>
        <td>68.80 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>94.34 &#177; 0.01</td>
        <td>93.73 &#177; 0.01</td>
        <td>87.54 &#177; 0.03</td>
        <td style="border-right: 2px solid white;">90.49 &#177; 0.03</td>
        <td>80.32 &#177; 0.02</td>
        <td>65.36 &#177; 0.06</td>
        <td>69.01 &#177; 0.03</td>
        <td>68.72 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>96.56 &#177; 0.01</td>
        <td>89.71 &#177; 0.04</td>
        <td>85.07 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">84.56 &#177; 0.03</td>
        <td>91.18 &#177; 0.01</td>
        <td>83.37 &#177; 0.03</td>
        <td>72.66 &#177; 0.04</td>
        <td>70.34 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>96.59 &#177; 0.02</td>
        <td>95.66 &#177; 0.01</td>
        <td>95.72 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">85.07 &#177; 0.02</td>
        <td>91.20 &#177; 0.02</td>
        <td>78.08 &#177; 0.06</td>
        <td>73.68 &#177; 0.02</td>
        <td>68.81 &#177; 0.02</td>
    </tr>
</table>

## Benchmarking on Trajectories with Noise

The results shown in the tables are the average AUROC values of 10 runs on the trajectories generated by a BN trajectories with a certain level of noise. The column headers represent the level of noise, e.g., "N1" denotes the trajectories have one level of added Gaussian noise. 

### a) AUROC values (in %) of investigated structural inference methods on BN trajectories with 1 (N1) and 2 (N2) levels of Gaussian noise.

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">N1</th>
        <th style="border-bottom: 2px solid white;" colspan="4">N2</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>92.66 &#177; 0.80</td>
        <td>97.16 &#177; 0.59</td>
        <td>98.48 &#177; 0.19</td>
        <td style="border-right: 2px solid white;">99.30 &#177; 0.02</td>
        <td>91.25 &#177; 0.75</td>
        <td>96.68 &#177; 0.64</td>
        <td>98.28 &#177; 0.22</td>
        <td>99.21 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>93.08 &#177; 0.76</td>
        <td>96.42 &#177; 0.67</td>
        <td>97.59 &#177; 0.23</td>
        <td style="border-right: 2px solid white;">98.65 &#177; 0.05</td>
        <td>93.12 &#177; 0.80</td>
        <td>96.43 &#177; 0.62</td>
        <td>97.55 &#177; 0.24</td>
        <td>98.59 &#177; 0.05</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>84.73 &#177; 1.20</td>
        <td>91.90 &#177; 1.00</td>
        <td>95.84 &#177; 0.33</td>
        <td style="border-right: 2px solid white;">98.11 &#177; 0.11</td>
        <td>84.39 &#177; 1.04</td>
        <td>92.37 &#177; 0.98</td>
        <td>95.73 &#177; 0.34</td>
        <td>97.76 &#177; 0.13</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>91.46 &#177; 0.45</td>
        <td>96.48 &#177; 0.64</td>
        <td>97.97 &#177; 0.24</td>
        <td style="border-right: 2px solid white;">98.97 &#177; 0.03</td>
        <td>90.88 &#177; 0.73</td>
        <td>96.55 &#177; 0.67</td>
        <td>98.12 &#177; 0.20</td>
        <td>99.04 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>87.87 &#177; 0.64</td>
        <td>94.54 &#177; 0.41</td>
        <td>95.84 &#177; 0.10</td>
        <td style="border-right: 2px solid white;">96.77 &#177; 0.08</td>
        <td>88.58 &#177; 0.66</td>
        <td>95.02 &#177; 0.75</td>
        <td>96.78 &#177; 0.19</td>
        <td>97.56 &#177; 0.06</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>47.75 &#177; 6.78</td>
        <td>63.04 &#177; 2.33</td>
        <td>73.37 &#177; 1.11</td>
        <td style="border-right: 2px solid white;">70.95 &#177; 1.87</td>
        <td>46.19 &#177; 5.58</td>
        <td>63.42 &#177; 4.19</td>
        <td>72.37 &#177; 1.98</td>
        <td>71.36 &#177; 1.12</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>83.60 &#177; 3.35</td>
        <td>90.28 &#177; 1.63</td>
        <td>92.28 &#177; 2.10</td>
        <td style="border-right: 2px solid white;">98.00 &#177; 0.45</td>
        <td>76.46 &#177; 0.64</td>
        <td>88.32 &#177; 3.03</td>
        <td>90.96 &#177; 1.39</td>
        <td>97.93 &#177; 0.04</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>93.72 &#177; 1.08</td>
        <td>98.35 &#177; 0.21</td>
        <td>98.63 &#177; 0.18</td>
        <td style="border-right: 2px solid white;">99.40 &#177; 0.01</td>
        <td>86.78 &#177; 2.19</td>
        <td>96.92 &#177; 1.00</td>
        <td>97.94 &#177; 0.28</td>
        <td>99.07 &#177; 0.05</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>72.98 &#177; 0.01</td>
        <td>73.85 &#177; 0.02</td>
        <td>74.12 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">74.70 &#177; 0.02</td>
        <td>56.76 &#177; 0.02</td>
        <td>59.64 &#177; 0.03</td>
        <td>62.52 &#177; 0.03</td>
        <td>63.52 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>65.62 &#177; 0.02</td>
        <td>63.47 &#177; 0.01</td>
        <td>66.69 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">61.56 &#177; 0.03</td>
        <td>62.08 &#177; 0.02</td>
        <td>58.14 &#177; 0.03</td>
        <td>61.73 &#177; 0.02</td>
        <td>59.04 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>70.23 &#177; 0.02</td>
        <td>74.37 &#177; 0.02</td>
        <td>75.72 &#177; 0.03</td>
        <td style="border-right: 2px solid white;">75.60 &#177; 0.03</td>
        <td>62.83 &#177; 0.02</td>
        <td>65.22 &#177; 0.02</td>
        <td>66.52 &#177; 0.02</td>
        <td>66.88 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>74.33 &#177; 0.03</td>
        <td>76.06 &#177; 0.02</td>
        <td>76.29 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">76.54 &#177; 0.03</td>
        <td>63.40 &#177; 0.04</td>
        <td>66.44 &#177; 0.03</td>
        <td>67.52 &#177; 0.03</td>
        <td>68.75 &#177; 0.02</td>
    </tr>
</table>

### b) AUROC values (in %) of investigated structural inference methods on BN trajectories with 3 (N3) and 4 (N4) levels of Gaussian noise.

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">N3</th>
        <th style="border-bottom: 2px solid white;" colspan="4">N4</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;">n100</td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>90.87 &#177; 0.66</td>
        <td>96.36 &#177; 0.62</td>
        <td>98.16 &#177; 0.19</td>
        <td style="border-right: 2px solid white;">99.15 &#177; 0.04</td>
        <td>90.81 &#177; 0.67</td>
        <td>96.10 &#177; 0.65</td>
        <td>98.09 &#177; 0.19</td>
        <td>99.09 &#177; 0.04</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>93.11 &#177; 0.65</td>
        <td>96.45 &#177; 0.62</td>
        <td>97.59 &#177; 0.21</td>
        <td style="border-right: 2px solid white;">98.56 &#177; 0.05</td>
        <td>93.00 &#177; 0.38</td>
        <td>96.44 &#177; 0.60</td>
        <td>97.64 &#177; 0.22</td>
        <td>98.57 &#177; 0.05</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>88.04 &#177; 1.01</td>
        <td>93.42 &#177; 0.85</td>
        <td>96.02 &#177; 0.34</td>
        <td style="border-right: 2px solid white;">97.80 &#177; 0.11</td>
        <td>89.51 &#177; 0.73</td>
        <td>93.89 &#177; 0.79</td>
        <td>96.22 &#177; 0.35</td>
        <td>97.85 &#177; 0.12</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>91.22 &#177; 0.82</td>
        <td>96.57 &#177; 0.70</td>
        <td>98.20 &#177; 0.20</td>
        <td style="border-right: 2px solid white;">99.07 &#177; 0.03</td>
        <td>91.40 &#177; 0.86</td>
        <td>96.63 &#177; 0.71</td>
        <td>98.26 &#177; 0.20</td>
        <td>99.09 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>90.24 &#177; 0.56</td>
        <td>95.17 &#177; 0.75</td>
        <td>96.93 &#177; 0.23</td>
        <td style="border-right: 2px solid white;">97.98 &#177; 0.04</td>
        <td>91.53 &#177; 1.11</td>
        <td>95.17 &#177; 0.84</td>
        <td>97.03 &#177; 0.28</td>
        <td>98.12 &#177; 0.04</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>51.12 &#177; 2.82</td>
        <td>61.51 &#177; 3.27</td>
        <td>71.40 &#177; 3.26</td>
        <td style="border-right: 2px solid white;">72.10 &#177; 0.97</td>
        <td>48.14 &#177; 2.15</td>
        <td>60.82 &#177; 2.68</td>
        <td>67.96 &#177; 2.52</td>
        <td>70.71 &#177; 1.81</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>63.28 &#177; 2.16</td>
        <td>80.56 &#177; 2.28</td>
        <td>87.03 &#177; 2.73</td>
        <td style="border-right: 2px solid white;">98.04 &#177; 0.03</td>
        <td>52.46 &#177; 0.55</td>
        <td>73.68 &#177; 1.60</td>
        <td>81.89 &#177; 4.03</td>
        <td>97.77 &#177; 0.01</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>86.90 &#177; 1.19</td>
        <td>96.38 &#177; 1.00</td>
        <td>97.55 &#177; 0.32</td>
        <td style="border-right: 2px solid white;">98.88 &#177; 0.06</td>
        <td>85.29 &#177; 0.62</td>
        <td>95.74 &#177; 1.21</td>
        <td>97.37 &#177; 0.31</td>
        <td>98.75 &#177; 0.07</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>50.67 &#177; 0.02</td>
        <td>51.68 &#177; 0.01</td>
        <td>54.40 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">58.16 &#177; 0.02</td>
        <td>50.91 &#177; 0.03</td>
        <td>51.11 &#177; 0.02</td>
        <td>51.24 &#177; 0.02</td>
        <td>52.89 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>50.09 &#177; 0.03</td>
        <td>54.38 &#177; 0.02</td>
        <td>56.42 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">56.12 &#177; 0.02</td>
        <td>51.89 &#177; 0.02</td>
        <td>54.65 &#177; 0.02</td>
        <td>55.73 &#177; 0.03</td>
        <td>55.02 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>55.29 &#177; 0.03</td>
        <td>56.81 &#177; 0.03</td>
        <td>57.41 &#177; 0.02</td>
        <td style="border-right: 2px solid white;">59.23 &#177; 0.02</td>
        <td>55.85 &#177; 0.03</td>
        <td>57.48 &#177; 0.01</td>
        <td>59.76 &#177; 0.02</td>
        <td>59.90 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>56.73 &#177; 0.02</td>
        <td>56.79 &#177; 0.02</td>
        <td>57.71 &#177; 0.01</td>
        <td style="border-right: 2px solid white;">60.60 &#177; 0.03</td>
        <td>54.59 &#177; 0.04</td>
        <td>57.82 &#177; 0.03</td>
        <td>58.08 &#177; 0.02</td>
        <td>59.70 &#177; 0.02</td>
    </tr>
</table>

### c) AUROC values (in %) of investigated structural inference methods on BN trajectories with 5 level of Gaussian noise.

<table class="table table-dark table-striped">
    <thead>
        <th style="border-right: 2px solid white;" rowspan="2">Method</th>
        <th style="border-bottom: 2px solid white; border-right: 2px solid white;" colspan="4">N5</th>
    </thead>
    <tr>
        <td style="border-bottom: 2px solid white; border-right: 2px solid white;"></td>
        <td style="border-bottom: 2px solid white;">n15</td>
        <td style="border-bottom: 2px solid white;">n30</td>
        <td style="border-bottom: 2px solid white;">n50</td>
        <td style="border-bottom: 2px solid white;">n100</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ppcor</td>
        <td>91.11 &#177; 0.69</td>
        <td>95.81 &#177; 0.61</td>
        <td>97.97 &#177; 0.18</td>
        <td>99.04 &#177; 0.05</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">TIGRESS</td>
        <td>92.95 &#177; 0.42</td>
        <td>96.38 &#177; 0.64</td>
        <td>97.66 &#177; 0.18</td>
        <td>98.57 &#177; 0.05</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ARACNe</td>
        <td>90.22 &#177; 0.96</td>
        <td>94.15 &#177; 0.70</td>
        <td>96.33 &#177; 0.35</td>
        <td>97.90 &#177; 0.11</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">CLR</td>
        <td>91.59 &#177; 0.90</td>
        <td>96.65 &#177; 0.70</td>
        <td>98.31 &#177; 0.20</td>
        <td>99.10 &#177; 0.04</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">PIDC</td>
        <td>91.18 &#177; 1.61</td>
        <td>95.11 &#177; 0.95</td>
        <td>96.90 &#177; 0.32</td>
        <td>98.17 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">Scribe</td>
        <td>52.20 &#177; 6.61</td>
        <td>58.31 &#177; 2.98</td>
        <td>66.41 &#177; 2.87</td>
        <td>69.35 &#177; 1.47</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">dynGENIE3</td>
        <td>47.84 &#177; 1.10</td>
        <td>67.07 &#177; 2.68</td>
        <td>74.14 &#177; 4.26</td>
        <td>97.46 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">XGBGRN</td>
        <td>85.18 &#177; 0.34</td>
        <td>95.41 &#177; 1.22</td>
        <td>97.27 &#177; 0.28</td>
        <td>98.70 &#177; 0.08</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">NRI</td>
        <td>46.68 &#177; 0.03</td>
        <td>46.70 &#177; 0.02</td>
        <td>49.57 &#177; 0.03</td>
        <td>49.79 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">ACD</td>
        <td>46.21 &#177; 0.03</td>
        <td>46.34 &#177; 0.05</td>
        <td>44.06 &#177; 0.02</td>
        <td>44.41 &#177; 0.02</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">MPM</td>
        <td>55.39 &#177; 0.05</td>
        <td>58.87 &#177; 0.02</td>
        <td>59.07 &#177; 0.03</td>
        <td>60.45 &#177; 0.03</td>
    </tr>
    <tr>
        <td style="border-right: 2px solid white;">iSIDG</td>
        <td>55.59 &#177; 0.03</td>
        <td>58.82 &#177; 0.03</td>
        <td>59.08 &#177; 0.01</td>
        <td>60.70 &#177; 0.02</td>
    </tr>
</table>

## Benchmarking over Data-Efficiency

![Average AUROC results with trajectories of different lengths](/assets/theme/images/lengths_comparison.png)



