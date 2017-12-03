from math import pi, sqrt
import numpy as np
from wcxf.parameters import p
import wcxf



# CONSTANTS

Nc = 3.
Qu = 2 / 3.
Qd = -1 / 3.
alpha_e = p['alpha_e']
alpha_s = p['alpha_s']
e = sqrt(4 * pi * alpha_e)
gs = sqrt(4 * pi * alpha_s)
mb = 4.2
ms = 0.095

# flavour indices
dflav = {'d': 0, 's': 1, 'b': 2}
uflav = {'u': 0, 'c': 1}
lflav = {'e': 0, 'mu': 1, 'tau': 2}

# WET with b,c,s,d,u

## Class I (DeltaF = 2)##

def _JMS_to_Bern_I(C, qq):
    """From JMS to BernI basis (= traditional SUSY basis in this case)
    for $\Delta F=2$ operators.
    `qq` should be 'sb', 'db', 'ds' or 'uc'"""
    if qq in ['sb', 'db', 'ds']:
        ij = tuple(dflav[q] for q in qq)
        ji = (ij[1], ij[0])
        return {
            '1' + 2*qq: C["VddLL"][ij + ij],
            '2' + 2*qq: C["S1ddRR"][ji + ji].conjugate()
                        - C["S8ddRR"][ji + ji].conjugate() / (2 * Nc),
            '3' + 2*qq: C["S8ddRR"][ji + ji].conjugate() / 2,
            '4' + 2*qq: -C["V8ddLR"][ij + ij],
            '5' + 2*qq: -2 * C["V1ddLR"][ij + ij] + C["V8ddLR"][ij + ij] / Nc,
            '1p' + 2*qq: C["VddRR"][ij + ij],
            '2p' + 2*qq: C["S1ddRR"][ij + ij] - C["S8ddRR"][ij + ij] / (2 * Nc),
            '3p' + 2*qq: C["S8ddRR"][ij + ij] / 2}
    elif qq == 'uc':
        return {
            '1' + 2*qq: C["VuuLL"][0,1,0,1],
            '2' + 2*qq: C["S1uuRR"][1,0,1,0].conjugate()
                        - C["S8uuRR"][1,0,1,0].conjugate() / (2 * Nc),
            '3' + 2*qq: C["S8uuRR"][1,0,1,0].conjugate() / 2,
            '4' + 2*qq: -C["V8uuLR"][0,1,0,1],
            '5' + 2*qq: -2 * C["V1uuLR"][0,1,0,1] + C["V8uuLR"][0,1,0,1] / Nc,
            '1p' + 2*qq: C["VuuRR"][0,1,0,1],
            '2p' + 2*qq: C["S1uuRR"][0,1,0,1] - C["S8uuRR"][0,1,0,1]/(2 * Nc),
            '3p' + 2*qq: C["S8uuRR"][0,1,0,1]/2}
    else:
        return "not in Bern_I"


def _BernI_to_Flavio_I(C, qq):
    """From BernI to FlavioI basis for down-typ $\Delta F=2$ operators.
    `qq` should be 'sb', 'db', 'ds' or 'uc'"""
    qqf = qq[::-1] # flavio used "bs" instead of "sb" etc.
    if qq in ['sb', 'db', 'ds']:
        return {
            'CVLL_' + 2*qqf: C["1" + 2*qq],
            'CSLL_' + 2*qqf: C["2" + 2*qq] + 1 / 2. * C["3" + 2*qq],
            'CTLL_' + 2*qqf: -1 / 8. * C["3" + 2*qq],
            'CVLR_' + 2*qqf: -1 / 2. * C["5" + 2*qq],
            'CVRR_' + 2*qqf: C["1p" + 2*qq],
            'CSRR_' + 2*qqf: C["2p" + 2*qq] + 1 / 2. * C["3p" + 2*qq],
            'CTRR_' + 2*qqf: -1 / 8. * C["3p" + 2*qq],
            'CSLR_' + 2*qqf: C["4" + 2*qq]}
    elif qq == 'uc':
        return {
            'CVLL_' + 2*qqf: C["1" + 2*qq],
            'CSLL_' + 2*qqf: C["2" + 2*qq] + 1 / 2. * C["3" + 2*qq],
            'CTLL_' + 2*qqf: -1 / 8. * C["3" + 2*qq],
            'CVLR_' + 2*qqf: -1 / 2. * C["5" + 2*qq],
            'CVRR_' + 2*qqf: C["1p" + 2*qq],
            'CSRR_' + 2*qqf: C["2p" + 2*qq] + 1 / 2. * C["3p" + 2*qq],
            'CTRR_' + 2*qqf: -1 / 8. * C["3p" + 2*qq],
            'CSLR_' + 2*qqf: C["4" + 2*qq]}
    else:
        return "not in Flavio_I"


## Class II ##

def _JMS_to_Bern_II(C, udlnu):
    """From JMS to Bern basis for charged current process semileptonic operators.
    `udlnu` should be of the form 'udl_enu_tau', 'cbl_munu_e' etc."""
    u = uflav[udlnu[0]]
    d = dflav[udlnu[1]]
    l = lflav[udlnu[4:udlnu.find('n')]]
    lp = lflav[udlnu[udlnu.find('_',5)+1:len(udlnu)]]
    ind = udlnu[0]+udlnu[1]+udlnu[4:udlnu.find('n')]+udlnu[udlnu.find('_',5)+1:len(udlnu)]
    return {
        '1' + ind: C["VnueduLL"][lp, l, d, u].conjugate(),
        '5' + ind: C["SnueduRL"][lp, l, d, u].conjugate(),
        '1p' + ind: C["VnueduLR"][lp, l, d, u].conjugate(),
        '5p' + ind: C["SnueduRR"][lp, l, d, u].conjugate(),
        '7p' + ind: C["TnueduRR"][lp, l, d, u].conjugate()}

def _BernII_to_ACFG(C, udlnu):
    """From BernII to ACFG basis (defined in arXiv:1512.02830)
    for charged current process semileptonic operators.
    `udlnu` should be of the form 'udl_enu_tau', 'cbl_munu_e' etc."""
    u = uflav[udlnu[0]]
    d = dflav[udlnu[1]]
    l = lflav[udlnu[4:udlnu.find('n')]]
    lp = lflav[udlnu[udlnu.find('_',5)+1:len(udlnu)]]
    ind = udlnu[0]+udlnu[1]+udlnu[4:udlnu.find('n')]+udlnu[udlnu.find('_',5)+1:len(udlnu)]
    ind2 = udlnu[1]+udlnu[0]+udlnu[4:udlnu.find('n')]+"nu"
    return {
        'CV_' + ind2: C['1' + ind],
        'CVp_'+ ind2: C['1p' + ind],
        'CSp_'+ ind2: C['5' + ind],
        'CS_'+ ind2: C['5p' + ind],
        'CT_'+ ind2: C['7p' + ind]
        }


def _BernII_to_Flavio_II(C, udlnu):
    """From BernII to FlavioII basis
    for charged current process semileptonic operators.
    `udlnu` should be of the form 'udl_enu_tau', 'cbl_munu_e' etc."""
    u = uflav[udlnu[0]]
    d = dflav[udlnu[1]]
    l = lflav[udlnu[4:udlnu.find('n')]]
    lp = lflav[udlnu[udlnu.find('_',5)+1:len(udlnu)]]
    ind = udlnu[0]+udlnu[1]+udlnu[4:udlnu.find('n')]+udlnu[udlnu.find('_',5)+1:len(udlnu)]
    ind2 = udlnu[1]+udlnu[0]+udlnu[4:udlnu.find('n')]+'nu'+udlnu[udlnu.find('_',5)+1:len(udlnu)]
    return {
        'CV_' + ind2: C['1' + ind],
        'CVp_'+ ind2: C['1p' + ind],
        'CS_'+ ind2: C['5' + ind] / mb,
        'CSp_'+ ind2: C['5p' + ind] / mb,
        'CT_'+ ind2: C['7p' + ind]
        }


## Class III ##

def _JMS_to_Fierz_III_IV_V(C, qqqq):
    """From JMS to 4-quark Fierz basis for Classes III, IV and V.
    `qqqq` should be of the form 'sbuc', 'sdcc', 'ucuu' etc."""
    #case dduu
    classIII = ['sbuc', 'sbcu', 'dbuc', 'dbcu']
    classVdduu = ['sbuu', 'bsuu' , 'dbuu', 'bduu', 'sduu', 'dsuu',
                  'sbcc', 'bscc' , 'dbcc', 'bdcc', 'sdcc', 'dscc']
    if qqqq in classIII + classVdduu:
        f1 = dflav[qqqq[0]]
        f2 = dflav[qqqq[1]]
        f3 = uflav[qqqq[2]]
        f4 = uflav[qqqq[3]]
        return {
            'F'+qqqq+'1' : C["V1udLL"][f3, f4, f1, f2] - C["V8udLL"][f3, f4, f1, f2]/(2*Nc),
            'F'+qqqq+'2' : C["V8udLL"][f3, f4, f1, f2]/2,
            'F'+qqqq+'3' : C["V1duLR"][f1, f2, f3, f4] - C["V8duLR"][f1, f2, f3, f4]/(2*Nc),
            'F'+qqqq+'4' : C["V8duLR"][f1, f2, f3, f4]/2,
            'F'+qqqq+'5' : C["S1udRR"][f3, f4, f1, f2] - C["S8udduRR"][f3, f2, f1, f4]/4
                            - C["S8udRR"][f3, f4, f1, f2]/(2*Nc),
            'F'+qqqq+'6' : -C["S1udduRR"][f3, f2, f1, f4]/2 + C["S8udduRR"][f3, f2, f1, f4]/(4*Nc)
                            + C["S8udRR"][f3, f4, f1, f2]/2,
            'F'+qqqq+'7' : -C["V8udduLR"][f4, f1, f2, f3].conjugate(),
            'F'+qqqq+'8' : -2*C["V1udduLR"][f4, f1, f2, f3].conjugate()
                            + C["V8udduLR"][f4, f1, f2, f3].conjugate()/Nc,
            'F'+qqqq+'9' : -C["S8udduRR"][f3, f2, f1, f4]/16,
            'F'+qqqq+'10' : -C["S1udduRR"][f3, f2, f1, f4]/8
                            + C["S8udduRR"][f3, f2, f1, f4]/(16*Nc),
            'F'+qqqq+'1p' : C["V1udRR"][f3, f4, f1, f2] - C["V8udRR"][f3, f4, f1, f2]/(2*Nc),
            'F'+qqqq+'2p' : C["V8udRR"][f3, f4, f1, f2]/2,
            'F'+qqqq+'3p' : C["V1udLR"][f3, f4, f1, f2] - C["V8udLR"][f3, f4, f1, f2]/(2*Nc),
            'F'+qqqq+'4p' : C["V8udLR"][f3, f4, f1, f2]/2,
            'F'+qqqq+'5p' : C["S1udRR"][f4, f4, f2, f1].conjugate() -
                            C["S8udduRR"][f4, f1, f2, f3].conjugate()/4
                            - C["S8udRR"][f4, f4, f2, f1].conjugate()/(2*Nc),
            'F'+qqqq+'6p' : -C["S1udduRR"][f4, f1, f2, f3].conjugate()/2 +
                            C["S8udduRR"][f4, f1, f2, f3].conjugate()/(4*Nc)
                            + C["S8udRR"][f4, f4, f2, f1].conjugate()/2,
            'F'+qqqq+'7p' : -C["V8udduLR"][f3, f2, f1, f4],
            'F'+qqqq+'8p' : -2*C["V1udduLR"][f3, f2, f1, f4] + C["V8udduLR"][f3, f2, f1, f4]/Nc,
            'F'+qqqq+'9p' : -C["S8udduRR"][f4, f1, f2, f3].conjugate()/16,
            'F'+qqqq+'10p' : -C["S1udduRR"][f4, f1, f2, f3].conjugate()/8
                            + C["S8udduRR"][f4, f1, f2, f3].conjugate()/(16*Nc)}
    #case dddd
    classIV = ['sbsd','dbds','bsbd']
    classVdddd = ['sbss', 'dbdd', 'bsbb', 'dsdd', 'bdbb', 'bsbb','sbbb','dbbb']
    classVddddind = ['sbdd', 'bsdd', 'sdbb', 'dsbb', 'dbss', 'bdss']
    if qqqq in classIV + classVdddd + classVddddind:
        f1 = dflav[qqqq[0]]
        f2 = dflav[qqqq[1]]
        f3 = dflav[qqqq[2]]
        f4 = dflav[qqqq[3]]
        return {
                'F'+ qqqq +'1' : C["VddLL"][f3, f4, f1, f2],
                 'F'+ qqqq +'2' : C["VddLL"][f1, f4, f3, f2],
                 'F'+ qqqq +'3' : C["V1ddLR"][f1, f2, f3, f4] - C["V8ddLR"][f1, f2, f3, f4]/(2*Nc),
                 'F'+ qqqq +'4' : C["V8ddLR"][f1, f2, f3, f4]/2,
                 'F'+ qqqq +'5' : C["S1ddRR"][f3, f4, f1, f2] - C["S8ddRR"][f3, f2, f1,f4]/4
                                  - C["S8ddRR"][f3, f4, f1, f2]/(2*Nc),
                 'F'+ qqqq +'6' : -C["S1ddRR"][f1, f4, f3, f2]/2 + C["S8ddRR"][f3, f2, f1, f4]/(4*Nc)
                                  + C["S8ddRR"][f3, f4, f1, f2]/2,
                 'F'+ qqqq +'7' : -C["V8ddLR"][f1, f4, f3, f2],
                 'F'+ qqqq +'8' : -2*C["V1ddLR"][f1, f4, f3, f2] + C["V8ddLR"][f1, f4, f3, f2]/Nc,
                 'F'+ qqqq +'9' : -C["S8ddRR"][f3, f2, f1, f4]/16,
                 'F'+ qqqq +'10' : -C["S1ddRR"][f1, f4, f3, f2]/8
                                    + C["S8ddRR"][f3, f2, f1, f4]/(16*Nc),
                 'F'+ qqqq +'1p':  C["VddRR"][f3, f4, f1, f2],
                 'F'+ qqqq +'2p': C["VddRR"][f1, f3, f4, f2],
                 'F'+ qqqq +'3p' : C["V1ddLR"][f3, f4, f1, f2] - C["V8ddLR"][f3, f4, f1,f2]/(2*Nc),
                 'F'+ qqqq +'4p' : C["V8ddLR"][f3, f4, f1, f2]/2,
                 'F'+ qqqq +'5p' : C["S1ddRR"][f4, f3, f2, f1].conjugate() -
                                    C["S8ddRR"][f4, f1, f2, f3].conjugate()/4
                                    - C["S8ddRR"][f4, f3, f2, f1].conjugate()/(2*Nc),
                 'F'+ qqqq +'6p' : -C["S1ddRR"][f4, f1, f2, f3].conjugate()/2 +
                                    C["S8ddRR"][f4, f1, f2, f3].conjugate()/(4*Nc)
                                    + C["S8ddRR"][f4, f3, f2, f1].conjugate()/2,
                 'F'+ qqqq +'7p' : -C["V8ddLR"][f3, f2, f1, f4],
                 'F'+ qqqq +'8p' : -2*C["V1ddLR"][f3, f2, f1, f4] + C["V8ddLR"][f3, f2, f1, f4]/Nc,
                 'F'+ qqqq +'9p' : -C["S8ddRR"][f4, f1, f2, f3].conjugate()/16,
                 'F'+ qqqq +'10p' : -C["S1ddRR"][f4, f1, f2, f3].conjugate()/8
                                    + C["S8ddRR"][f4, f1, f2, f3].conjugate()/(16*Nc)}
    #case uuuu
    classVuuuu = ['ucuu', 'cucc']
    if qqqq in classVuuuu:
        f1 = uflav[qqqq[0]]
        f2 = uflav[qqqq[1]]
        f3 = uflav[qqqq[2]]
        f4 = uflav[qqqq[3]]
        return {
                'F'+ qqqq +'1' : C["VuuLL"][f3, f4, f1, f2],
                 'F'+ qqqq +'2' : C["VuuLL"][f1, f4, f3, f2],
                 'F'+ qqqq +'3' : C["V1uuLR"][f1, f2, f3, f4] - C["V8uuLR"][f1, f2, f3, f4]/(2*Nc),
                 'F'+ qqqq +'4' : C["V8uuLR"][f1, f2, f3, f4]/2,
                 'F'+ qqqq +'5' : C["S1uuRR"][f3, f4, f1, f2] - C["S8uuRR"][f3, f2, f1,f4]/4
                                  - C["S8uuRR"][f3, f4, f1, f2]/(2*Nc),
                 'F'+ qqqq +'6' : -C["S1uuRR"][f1, f4, f3, f2]/2 + C["S8uuRR"][f3, f2, f1, f4]/(4*Nc)
                                  + C["S8uuRR"][f3, f4, f1, f2]/2,
                 'F'+ qqqq +'7' : -C["V8uuLR"][f1, f4, f3, f2],
                 'F'+ qqqq +'8' : -2*C["V1uuLR"][f1, f4, f3, f2] + C["V8uuLR"][f1, f4, f3, f2]/Nc,
                 'F'+ qqqq +'9' : -C["S8uuRR"][f3, f2, f1, f4]/16,
                 'F'+ qqqq +'10' : -C["S1uuRR"][f1, f4, f3, f2]/8
                                    + C["S8uuRR"][f3, f2, f1, f4]/(16*Nc),
                 'F'+ qqqq +'1p': C["VuuRR"][f3, f4, f1, f2],
                 'F'+ qqqq +'2p': C["VuuRR"][f1, f3, f4, f2],
                 'F'+ qqqq +'3p' : C["V1uuLR"][f3, f4, f1, f2] - C["V8uuLR"][f3, f4, f1,f2]/(2*Nc),
                 'F'+ qqqq +'4p' : C["V8uuLR"][f3, f4, f1, f2]/2,
                 'F'+ qqqq +'5p' : C["S1uuRR"][f4, f3, f2, f1].conjugate() -
                                    C["S8uuRR"][f4, f1, f2, f3].conjugate()/4
                                    - C["S8uuRR"][f4, f3, f2, f1].conjugate()/(2*Nc),
                 'F'+ qqqq +'6p' : -C["S1uuRR"][f4, f1, f2, f3].conjugate()/2 +
                                    C["S8uuRR"][f4, f1, f2, f3].conjugate()/(4*Nc)
                                    + C["S8uuRR"][f4, f3, f2, f1].conjugate()/2,
                 'F'+ qqqq +'7p' : -C["V8uuLR"][f3, f2, f1, f4],
                 'F'+ qqqq +'8p' : -2*C["V1uuLR"][f3, f2, f1, f4] + C["V8uuLR"][f3, f2, f1, f4]/Nc,
                 'F'+ qqqq +'9p' : -C["S8uuRR"][f4, f1, f2, f3].conjugate()/16,
                 'F'+ qqqq +'10p' : -C["S1uuRR"][f4, f1, f2, f3].conjugate()/8
                                    + C["S8uuRR"][f4, f1, f2, f3].conjugate()/(16*Nc)}
    else:
        "not in Fqqqq"


## for bern Basis

# for all flavour same rotation matrix! as well as for prime and non-prime
def _Fierz_to_Bern_III_IV_V(Fqqqq, qqqq):
    """From Fierz to 4-quark Bern basis for Classes III, IV and V.
    `qqqq` should be of the form 'sbuc', 'sdcc', 'ucuu' etc."""

    if qqqq in ['sbss','dbdd','dbbb','sbbb','dbds','sbsd']:
        return {
        '1'+qqqq : -Fqqqq['F'+qqqq+'1']/3 + (4*Fqqqq['F'+qqqq+'3'])/3
                         - Fqqqq['F'+qqqq+'2']/(3*Nc)
                         + (4*Fqqqq['F'+qqqq+'4'])/(3*Nc),
        '3'+qqqq : Fqqqq['F'+qqqq+'1']/12 - Fqqqq['F'+qqqq+'3']/12
                         + Fqqqq['F'+qqqq+'2']/(12*Nc)
                         - Fqqqq['F'+qqqq+'4']/(12*Nc),
        '5'+ qqqq : -Fqqqq['F'+qqqq+'5p']/3
                            + (4*Fqqqq['F'+qqqq+'7p'])/3,
        '7'+qqqq : Fqqqq['F'+qqqq+'5p']/3 - Fqqqq['F'+qqqq+'7p']/3
                         + Fqqqq['F'+qqqq+'9p'],
        '9'+qqqq : Fqqqq['F'+qqqq+'5p']/48 - Fqqqq['F'+qqqq+'7p']/48,
        '1p'+qqqq : -Fqqqq['F'+qqqq+'1p']/3
                            + (4*Fqqqq['F'+qqqq+'3p'])/3
                            - Fqqqq['F'+qqqq+'2p']/(3*Nc)
                            + (4*Fqqqq['F'+qqqq+'4p'])/(3*Nc),
        '3p'+qqqq : Fqqqq['F'+qqqq+'1p']/12 - Fqqqq['F'+qqqq+'3p']/12
                            + Fqqqq['F'+qqqq+'2p']/(12*Nc)
                            - Fqqqq['F'+qqqq+'4p']/(12*Nc),
        '5p'+qqqq : -Fqqqq['F'+qqqq+'5']/3
                            + (4*Fqqqq['F'+qqqq+'7'])/3,
        '7p'+qqqq : Fqqqq['F'+qqqq+'5']/3
                            - Fqqqq['F'+qqqq+'7']/3
                            + Fqqqq['F'+qqqq+'9'],
        '9p'+qqqq : Fqqqq['F'+qqqq+'5']/48 - Fqqqq['F'+qqqq+'7']/48
                            }
    else:
        return {
        '1'+qqqq : -Fqqqq['F'+qqqq+'1']/3 + (4*Fqqqq['F'+qqqq+'3'])/3
                         - Fqqqq['F'+qqqq+'2']/(3*Nc)
                         + (4*Fqqqq['F'+qqqq+'4'])/(3*Nc),
        '2'+qqqq : (-2*Fqqqq['F'+qqqq+'2'])/3 + (8*Fqqqq['F'+qqqq+'4'])/3,
        '3'+qqqq : Fqqqq['F'+qqqq+'1']/12 - Fqqqq['F'+qqqq+'3']/12
                         + Fqqqq['F'+qqqq+'2']/(12*Nc)
                         - Fqqqq['F'+qqqq+'4']/(12*Nc),
        '4'+ qqqq : Fqqqq['F'+qqqq+'2']/6 - Fqqqq['F'+qqqq+'4']/6,
        '5'+ qqqq : -Fqqqq['F'+qqqq+'5']/3
                            + (4*Fqqqq['F'+qqqq+'7'])/3
                            - Fqqqq['F'+qqqq+'6']/(3*Nc)
                            + (4*Fqqqq['F'+qqqq+'8'])/(3*Nc),
        '6'+qqqq : (-2*Fqqqq['F'+qqqq+'6'])/3 + (8*Fqqqq['F'+qqqq+'8'])/3,
        '7'+qqqq : Fqqqq['F'+qqqq+'5']/3 - Fqqqq['F'+qqqq+'7']/3
                         + Fqqqq['F'+qqqq+'9'] + Fqqqq['F'+qqqq+'10']/Nc
                         + Fqqqq['F'+qqqq+'6']/(3*Nc)
                         - Fqqqq['F'+qqqq+'8']/(3*Nc),
        '8'+qqqq : 2*Fqqqq['F'+qqqq+'10']
                         + (2*Fqqqq['F'+qqqq+'6'])/3
                         - (2*Fqqqq['F'+qqqq+'8'])/3,
        '9'+qqqq : Fqqqq['F'+qqqq+'5']/48 - Fqqqq['F'+qqqq+'7']/48
                            + Fqqqq['F'+qqqq+'6']/(48*Nc)
                            - Fqqqq['F'+qqqq+'8']/(48*Nc),
        '10'+qqqq : Fqqqq['F'+qqqq+'6']/24 - Fqqqq['F'+qqqq+'8']/24,
        '1p'+qqqq : -Fqqqq['F'+qqqq+'1p']/3
                            + (4*Fqqqq['F'+qqqq+'3p'])/3
                            - Fqqqq['F'+qqqq+'2p']/(3*Nc)
                            + (4*Fqqqq['F'+qqqq+'4p'])/(3*Nc),
        '2p'+qqqq : (-2*Fqqqq['F'+qqqq+'2p'])/3
                            + (8*Fqqqq['F'+qqqq+'4p'])/3,
        '3p'+qqqq : Fqqqq['F'+qqqq+'1p']/12 - Fqqqq['F'+qqqq+'3p']/12
                            + Fqqqq['F'+qqqq+'2p']/(12*Nc)
                            - Fqqqq['F'+qqqq+'4p']/(12*Nc),
        '4p'+qqqq : Fqqqq['F'+qqqq+'2p']/6 - Fqqqq['F'+qqqq+'4p']/6,
        '5p'+qqqq : -Fqqqq['F'+qqqq+'5p']/3
                            + (4*Fqqqq['F'+qqqq+'7p'])/3
                            - Fqqqq['F'+qqqq+'6p']/(3*Nc)
                            + (4*Fqqqq['F'+qqqq+'8p'])/(3*Nc),
        '6p'+qqqq : (-2*Fqqqq['F'+qqqq+'6p'])/3
                            + (8*Fqqqq['F'+qqqq+'8p'])/3,
        '7p'+qqqq : Fqqqq['F'+qqqq+'5p']/3
                            - Fqqqq['F'+qqqq+'7p']/3
                            + Fqqqq['F'+qqqq+'9p']
                            + Fqqqq['F'+qqqq+'10p']/Nc
                            + Fqqqq['F'+qqqq+'6p']/(3*Nc)
                            - Fqqqq['F'+qqqq+'8p']/(3*Nc),
        '8p'+qqqq : 2*Fqqqq['F'+qqqq+'10p']
                            + (2*Fqqqq['F'+qqqq+'6p'])/3
                            - (2*Fqqqq['F'+qqqq+'8p'])/3,
        '9p'+qqqq : Fqqqq['F'+qqqq+'5p']/48 - Fqqqq['F'+qqqq+'7p']/48
                            + Fqqqq['F'+qqqq+'6p']/(48*Nc)
                            - Fqqqq['F'+qqqq+'8p']/(48*Nc),
        '10p'+qqqq : Fqqqq['F'+qqqq+'6p']/24 - Fqqqq['F'+qqqq+'8p']/24}

def _Fierz_to_Flavio_V(Fsbuu,Fsbdd,Fsbcc,Fsbss,Fsbbb,dd):
    """From Fierz to the Flavio basis for b ->s transitions.
    The arguments are dictionaries of the corresponding Fierz bases and dd to 'sb' 'db' """
    ddflav = dd[::-1]
    return {
    'C1_' + ddflav : 2*Fsbcc['F' + dd + 'cc1'] - 2*Fsbuu['F' + dd + 'uu1'],
    'C2_' + ddflav : Fsbcc['F' + dd + 'cc1']/3 + Fsbcc['F' + dd + 'cc2']
            - Fsbuu['F' + dd + 'uu1']/3 - Fsbuu['F' + dd + 'uu2'],
    'C3_' + ddflav : -8*Fsbbb['F' + dd + 'bb1']/135 + 8*Fsbbb['F' + dd + 'bb3']/27
                + 8*Fsbbb['F' + dd + 'bb4']/81 + 2*Fsbcc['F' + dd + 'cc3']/9
                + 2*Fsbcc['F' + dd + 'cc4']/27 - 14*Fsbdd['F' + dd + 'dd1']/135
                + (2*Fsbdd['F' + dd + 'dd2'])/45 + (8*Fsbdd['F' + dd + 'dd3'])/27
                + (8*Fsbdd['F' + dd + 'dd4'])/81
                - (8*Fsbss['F' + dd + 'ss1'])/135 + (8*Fsbss['F' + dd + 'ss3'])/27
                + (8*Fsbss['F' + dd + 'ss4'])/81
                - Fsbuu['F' + dd + 'uu1']/9 - Fsbuu['F' + dd + 'uu2']/27
                + (2*Fsbuu['F' + dd + 'uu3'])/9 + (2*Fsbuu['F' + dd + 'uu4'])/27,
     'C4_' + ddflav : (-4*Fsbbb['F' + dd + 'bb1'])/45 + (16*Fsbbb['F' + dd + 'bb4'])/27
                + (4*Fsbcc['F' + dd + 'cc4'])/9 + (8*Fsbdd['F' + dd + 'dd1'])/45
                - (4*Fsbdd['F' + dd + 'dd2'])/15 + (16*Fsbdd['F' + dd + 'dd4'])/27
                - (4*Fsbss['F' + dd + 'ss1'])/45 + (16*Fsbss['F' + dd + 'ss4'])/27
                - (2*Fsbuu['F' + dd + 'uu2'])/9 + (4*Fsbuu['F' + dd + 'uu4'])/9,
     'C5_' + ddflav : (2*Fsbbb['F' + dd + 'bb1'])/135 - Fsbbb['F' + dd + 'bb3']/54
                - Fsbbb['F' + dd + 'bb4']/162 - Fsbcc['F' + dd + 'cc3']/72 - Fsbcc['F' + dd + 'cc4']/216
                + (7*Fsbdd['F' + dd + 'dd1'])/270 - Fsbdd['F' + dd + 'dd2']/90
                - Fsbdd['F' + dd + 'dd3']/54 - Fsbdd['F' + dd + 'dd4']/162
                + (2*Fsbss['F' + dd + 'ss1'])/135 - Fsbss['F' + dd + 'ss3']/54
                - Fsbss['F' + dd + 'ss4']/162 + Fsbuu['F' + dd + 'uu1']/36 + Fsbuu['F' + dd + 'uu2']/108
                - Fsbuu['F' + dd + 'uu3']/72 - Fsbuu['F' + dd + 'uu4']/216,
     'C6_' + ddflav: Fsbbb['F' + dd + 'bb1']/45 - Fsbbb['F' + dd + 'bb4']/27 - Fsbcc['F' + dd + 'cc4']/36
                - (2*Fsbdd['F' + dd + 'dd1'])/45 + Fsbdd['F' + dd + 'dd2']/15
                - Fsbdd['F' + dd + 'dd4']/27 + Fsbss['F' + dd + 'ss1']/45 - Fsbss['F' + dd + 'ss4']/27
                + Fsbuu['F' + dd + 'uu2']/18 - Fsbuu['F' + dd + 'uu4']/36,
     'C3Q_' + ddflav: (4*Fsbbb['F' + dd + 'bb1'])/45 - (4*Fsbbb['F' + dd + 'bb3'])/9
                - (4*Fsbbb['F' + dd + 'bb4'])/27 + (2*Fsbcc['F' + dd + 'cc3'])/3
                + (2*Fsbcc['F' + dd + 'cc4'])/9 + (7*Fsbdd['F' + dd + 'dd1'])/45
                - Fsbdd['F' + dd + 'dd2']/15 - (4*Fsbdd['F' + dd + 'dd3'])/9
                - (4*Fsbdd['F' + dd + 'dd4'])/27 + (4*Fsbss['F' + dd + 'ss1'])/45
                - (4*Fsbss['F' + dd + 'ss3'])/9 - (4*Fsbss['F' + dd + 'ss4'])/27
                - Fsbuu['F' + dd + 'uu1']/3 - Fsbuu['F' + dd + 'uu2']/9 + (2*Fsbuu['F' + dd + 'uu3'])/3
                + (2*Fsbuu['F' + dd + 'uu4'])/9,
     'C4Q_' + ddflav: (2*Fsbbb['F' + dd + 'bb1'])/15 - (8*Fsbbb['F' + dd + 'bb4'])/9
                + (4*Fsbcc['F' + dd + 'cc4'])/3 - (4*Fsbdd['F' + dd + 'dd1'])/15
                + (2*Fsbdd['F' + dd + 'dd2'])/5 - (8*Fsbdd['F' + dd + 'dd4'])/9
                + (2*Fsbss['F' + dd + 'ss1'])/15 - (8*Fsbss['F' + dd + 'ss4'])/9
                - (2*Fsbuu['F' + dd + 'uu2'])/3 + (4*Fsbuu['F' + dd + 'uu4'])/3,
     'C5Q_' + ddflav: -Fsbbb['F' + dd + 'bb1']/45 + Fsbbb['F' + dd + 'bb3']/36 + Fsbbb['F' + dd + 'bb4']/108
                - Fsbcc['F' + dd + 'cc3']/24 - Fsbcc['F' + dd + 'cc4']/72
                - (7*Fsbdd['F' + dd + 'dd1'])/180 + Fsbdd['F' + dd + 'dd2']/60
                + Fsbdd['F' + dd + 'dd3']/36 + Fsbdd['F' + dd + 'dd4']/108 - Fsbss['F' + dd + 'ss1']/45
                + Fsbss['F' + dd + 'ss3']/36 + Fsbss['F' + dd + 'ss4']/108 + Fsbuu['F' + dd + 'uu1']/12
                + Fsbuu['F' + dd + 'uu2']/36 - Fsbuu['F' + dd + 'uu3']/24 - Fsbuu['F' + dd + 'uu4']/72,
     'C6Q_' + ddflav: -Fsbbb['F' + dd + 'bb1']/30 + Fsbbb['F' + dd + 'bb4']/18
                - Fsbcc['F' + dd + 'cc4']/12 + Fsbdd['F' + dd + 'dd1']/15 - Fsbdd['F' + dd + 'dd2']/10
                + Fsbdd['F' + dd + 'dd4']/18 - Fsbss['F' + dd + 'ss1']/30 + Fsbss['F' + dd + 'ss4']/18
                + Fsbuu['F' + dd + 'uu2']/6 - Fsbuu['F' + dd + 'uu4']/12,
     'C1p_' + ddflav: 2*Fsbcc['F' + dd + 'cc1p'] - 2*Fsbuu['F' + dd + 'uu1p'],
     'C2p_' + ddflav: Fsbcc['F' + dd + 'cc1p']/3 + Fsbcc['F' + dd + 'cc2p'] - Fsbuu['F' + dd + 'uu1p']/3
                - Fsbuu['F' + dd + 'uu2p'],
     'C3p_' + ddflav: (-8*Fsbbb['F' + dd + 'bb1p'])/135 + (8*Fsbbb['F' + dd + 'bb3p'])/27
                + (8*Fsbbb['F' + dd + 'bb4p'])/81 + (2*Fsbcc['F' + dd + 'cc3p'])/9
                + (2*Fsbcc['F' + dd + 'cc4p'])/27 - (14*Fsbdd['F' + dd + 'dd1p'])/135
                + (2*Fsbdd['F' + dd + 'dd2p'])/45 + (8*Fsbdd['F' + dd + 'dd3p'])/27
                + (8*Fsbdd['F' + dd + 'dd4p'])/81 - (8*Fsbss['F' + dd + 'ss1p'])/135
                + (8*Fsbss['F' + dd + 'ss3p'])/27 + (8*Fsbss['F' + dd + 'ss4p'])/81
                - Fsbuu['F' + dd + 'uu1p']/9 - Fsbuu['F' + dd + 'uu2p']/27
                + (2*Fsbuu['F' + dd + 'uu3p'])/9 + (2*Fsbuu['F' + dd + 'uu4p'])/27,
     'C4p_' + ddflav: (-4*Fsbbb['F' + dd + 'bb1p'])/45 + (16*Fsbbb['F' + dd + 'bb4p'])/27
                + (4*Fsbcc['F' + dd + 'cc4p'])/9 + (8*Fsbdd['F' + dd + 'dd1p'])/45
                - (4*Fsbdd['F' + dd + 'dd2p'])/15 + (16*Fsbdd['F' + dd + 'dd4p'])/27
                - (4*Fsbss['F' + dd + 'ss1p'])/45 + (16*Fsbss['F' + dd + 'ss4p'])/27
                - (2*Fsbuu['F' + dd + 'uu2p'])/9 + (4*Fsbuu['F' + dd + 'uu4p'])/9,
     'C5p_' + ddflav: (2*Fsbbb['F' + dd + 'bb1p'])/135 - Fsbbb['F' + dd + 'bb3p']/54
                - Fsbbb['F' + dd + 'bb4p']/162 - Fsbcc['F' + dd + 'cc3p']/72
                - Fsbcc['F' + dd + 'cc4p']/216 + (7*Fsbdd['F' + dd + 'dd1p'])/270
                - Fsbdd['F' + dd + 'dd2p']/90 - Fsbdd['F' + dd + 'dd3p']/54
                - Fsbdd['F' + dd + 'dd4p']/162 + (2*Fsbss['F' + dd + 'ss1p'])/135
                - Fsbss['F' + dd + 'ss3p']/54 - Fsbss['F' + dd + 'ss4p']/162
                + Fsbuu['F' + dd + 'uu1p']/36 + Fsbuu['F' + dd + 'uu2p']/108
                - Fsbuu['F' + dd + 'uu3p']/72 - Fsbuu['F' + dd + 'uu4p']/216,
     'C6p_' + ddflav: Fsbbb['F' + dd + 'bb1p']/45 - Fsbbb['F' + dd + 'bb4p']/27 - Fsbcc['F' + dd + 'cc4p']/36
                - (2*Fsbdd['F' + dd + 'dd1p'])/45 + Fsbdd['F' + dd + 'dd2p']/15
                - Fsbdd['F' + dd + 'dd4p']/27 + Fsbss['F' + dd + 'ss1p']/45
                - Fsbss['F' + dd + 'ss4p']/27 + Fsbuu['F' + dd + 'uu2p']/18
                - Fsbuu['F' + dd + 'uu4p']/36,
     'C3Qp_' + ddflav: (4*Fsbbb['F' + dd + 'bb1p'])/45 - (4*Fsbbb['F' + dd + 'bb3p'])/9
                - (4*Fsbbb['F' + dd + 'bb4p'])/27 + (2*Fsbcc['F' + dd + 'cc3p'])/3
                + (2*Fsbcc['F' + dd + 'cc4p'])/9 + (7*Fsbdd['F' + dd + 'dd1p'])/45
                - Fsbdd['F' + dd + 'dd2p']/15 - (4*Fsbdd['F' + dd + 'dd3p'])/9
                - (4*Fsbdd['F' + dd + 'dd4p'])/27 + (4*Fsbss['F' + dd + 'ss1p'])/45
                - (4*Fsbss['F' + dd + 'ss3p'])/9 - (4*Fsbss['F' + dd + 'ss4p'])/27
                - Fsbuu['F' + dd + 'uu1p']/3 - Fsbuu['F' + dd + 'uu2p']/9
                + (2*Fsbuu['F' + dd + 'uu3p'])/3 + (2*Fsbuu['F' + dd + 'uu4p'])/9,
     'C4Qp_' + ddflav: (2*Fsbbb['F' + dd + 'bb1p'])/15 - (8*Fsbbb['F' + dd + 'bb4p'])/9
                + (4*Fsbcc['F' + dd + 'cc4p'])/3 - (4*Fsbdd['F' + dd + 'dd1p'])/15
                + (2*Fsbdd['F' + dd + 'dd2p'])/5 - (8*Fsbdd['F' + dd + 'dd4p'])/9
                + (2*Fsbss['F' + dd + 'ss1p'])/15 - (8*Fsbss['F' + dd + 'ss4p'])/9
                - (2*Fsbuu['F' + dd + 'uu2p'])/3 + (4*Fsbuu['F' + dd + 'uu4p'])/3,
     'C5Qp_' + ddflav: -Fsbbb['F' + dd + 'bb1p']/45 + Fsbbb['F' + dd + 'bb3p']/36
                + Fsbbb['F' + dd + 'bb4p']/108 - Fsbcc['F' + dd + 'cc3p']/24
                - Fsbcc['F' + dd + 'cc4p']/72 - (7*Fsbdd['F' + dd + 'dd1p'])/180
                + Fsbdd['F' + dd + 'dd2p']/60 + Fsbdd['F' + dd + 'dd3p']/36
                + Fsbdd['F' + dd + 'dd4p']/108 - Fsbss['F' + dd + 'ss1p']/45
                + Fsbss['F' + dd + 'ss3p']/36 + Fsbss['F' + dd + 'ss4p']/108
                + Fsbuu['F' + dd + 'uu1p']/12 + Fsbuu['F' + dd + 'uu2p']/36
                - Fsbuu['F' + dd + 'uu3p']/24 - Fsbuu['F' + dd + 'uu4p']/72,
     'C6Qp_' + ddflav: -Fsbbb['F' + dd + 'bb1p']/30 + Fsbbb['F' + dd + 'bb4p']/18
                - Fsbcc['F' + dd + 'cc4p']/12 + Fsbdd['F' + dd + 'dd1p']/15
                - Fsbdd['F' + dd + 'dd2p']/10 + Fsbdd['F' + dd + 'dd4p']/18
                - Fsbss['F' + dd + 'ss1p']/30 + Fsbss['F' + dd + 'ss4p']/18 + Fsbuu['F' + dd + 'uu2p']/6
                - Fsbuu['F' + dd + 'uu4p']/12}

# semileptonic operators

def JMS_to_Fierz_lep(C, ddll):
    """From JMS to semileptonic Fierz basis for Classes V.
    `ddll` should be of the form 'sbl_eni_tau', 'dbl_munu_e' etc."""
    s = dflav[ddll[0]]
    b = dflav[ddll[1]]
    l = lflav[ddll[4:ddll.find('n')]]
    lp = lflav[ddll[ddll.find('_',5)+1:len(ddll)]]
    ind = ddll.replace('l_','').replace('nu_','')
    return {
        'F' + ind + '9': C["VdeLR"][s, b, l, lp]/2 + C["VedLL"][l, lp, s, b]/2,
        'F' + ind + '10': C["VdeLR"][s, b, l, lp]/2 - C["VedLL"][l, lp, s, b]/2,
        'F' + ind + 'S': C["SedRL"][lp, l, b, s].conjugate()/2
                    + C["SedRR"][l, lp, s, b]/2,
        'F' + ind + 'P': C["SedRL"][lp, l, b, s].conjugate()/2
                    + C["SedRR"][l, lp, s, b]/2,
        'F' + ind + 'T': C["TedRR"][l, lp, s, b]/2
                    + C["TedRR"][lp, l, b, s].conjugate()/2,
        'F' + ind + 'T5': C["TedRR"][l, lp, s, b]/2
                    - C["TedRR"][l, lp, s, b].conjugate()/2,
        'F' + ind + '9p': C["VedLR"][l, lp, s, b]/2 + C["VedRR"][l, lp, s, b]/2,
        'F' + ind + '10p': -C["VedLR"][l, lp, s, b]/2 + C["VedRR"][l, lp, s, b]/2,
        'F' + ind + 'Sp': C["SedRL"][l, lp, s, b]/2
                    + C["SedRR"][lp, l, b, s].conjugate()/2,
        'F' + ind + 'Pp': C["SedRL"][l, lp, s, b]/2
                    - C["SedRR"][lp, l, b, s].conjugate() / 2,
        'F' + ind + 'nu': C["VnudLL"][l, lp, s, b],
        'F' + ind + 'nup': C["VnudLR"][l, lp, s, b]}


def Fierz_to_Bern_lep(C,ddll):
    """From semileptonic Fierz basis to Bern semileptonic basis for Class V.
    `ddll` should be of the form 'sbl_enu_tau', 'dbl_munu_e' etc."""
    ind = ddll.replace('l_','').replace('nu_','')
    return {'1'+ind : (5*C['F'+ind+'10'])/3+C['F'+ind+'9'],
            '3'+ind : -((C['F'+ind+'10'])/6),
            '5'+ind : C['F'+ind+'S'] - 5*C['F'+ind+'P']/3,
            '7'+ind : (2*C['F'+ind+'P'])/3+C['F'+ind+'T']
                        +C['F'+ind+'T5'],
            '9'+ind : (C['F'+ind+'P'])/24,
            '1p'+ind : C['F'+ind+'9p']-(5*C['F'+ind+'10p'])/3,
            '3p'+ind : (C['F'+ind+'10p'])/6,
            '5p'+ind : (5*C['F'+ind+'Pp'])/3 + C['F'+ind+'Sp'],
            '7p'+ind : -((2*C['F'+ind+'Pp'])/3) + C['F'+ind+'T']
                        - C['F'+ind+'T5'],
            '9p'+ind : -((C['F'+ind+'Pp'])/24),
            'nu1'+ind : C['F'+ind+'nu'],
            'nu1p'+ind : C['F'+ind+'nup']
            }



def Fierz_to_Flavio_lep(C,ddll):
    """From semileptonic Fierz basis to Flavio semileptonic basis for Class V.
    `ddll` should be of the form 'sbl_enu_tau', 'dbl_munu_e' etc."""
    ind = ddll.replace('l_','').replace('nu_','')
    dd = ddll[1::-1]+ind[2:]
    indnu = ddll[1::-1]+ddll.replace('l_','nu').replace('nu_','nu')[2:]
    return {
        "C9_" + dd: (16 * pi**2) / e**2 * C['F' + ind + '9'],
        "C9p_" + dd: (16 * pi**2) / e**2 * C['F' + ind + '9p'],
        "C10_" + dd: (16 * pi**2) / e**2 * C['F' + ind + '10'],
        "C10p_" + dd: (16 * pi**2) / e**2 * C['F' + ind + '10p'],
        "CS_" + dd: (16 * pi**2) / e**2 / mb * C['F' + ind + 'S'],
        "CSp_" + dd: (16 * pi**2) / e**2 / mb * C['F' + ind + 'Sp'],
        "CP_" + dd: (16 * pi**2) / e**2 / mb * C['F' + ind + 'P'],
        "CPp_" + dd: (16 * pi**2) / e**2 / mb * C['F' + ind + 'Pp'],
        "CL_" + indnu: (8 * pi**2) / e**2 * C['F' + ind + 'nu'],
        "CR_" + indnu: (8 * pi**2) / e**2 * C['F' + ind + 'nup']
        }


# chromomagnetic operators
def JMS_to_Fierz_chrom(C, dd):
    """From JMS to chromomagnetic Fierz basis for Class V.
    `dd` should be of the form 'sb', 'ds' etc."""
    s = dflav[dd[0]]
    b = dflav[dd[1]]
    return {
        'F7gamma' + dd: C['dgamma'][s, b],
        "F8g" + dd: C['dG'][s, b],
        "F7pgamma" + dd: C['dgamma'][b, s].conjugate(),
        "F8pg" + dd: C['dG'][b, s].conjugate()
    }

def Fierz_to_Bern_chrom(C, dd):
    """From Fierz to chromomagnetic Bern basis for Class V.
    `dd` should be of the form 'sb', 'ds' etc."""
    return {
        "7gamma"+dd: (gs**2) / e / mb * C['F7gamma' + dd ],
        "8g"+dd: gs / mb * C['F8g' + dd ],
        "7pgamma"+dd: (gs**2)/e/mb* C['F7pgamma' + dd],
        "8pg"+dd: gs/mb*C['F8pg' + dd]
    }



def Fierz_to_Flavio_chrom(C, dd):
    """From Fierz to chromomagnetic Flavio basis for Class V.
    `dd` should be of the form 'sb', 'ds' etc."""
    ddfl=dd[::-1]
    return {
        "C7_" + ddfl: (16 * pi**2) / e / mb * C['F7gamma' + dd],
        "C8_" + ddfl: (16 * pi**2) / gs / mb * C['F8g' + dd],
        "C7p_" + ddfl: (16 * pi**2) / e / mb * C['F7pgamma' + dd],
        "C8p_" + ddfl: (16 * pi**2) / gs / mb * C['F8pg' + dd]
    }


# symmetrize JMS basis

def _scalar2array(d):
    """Convert a dictionary with scalar elements and string indices '_1234'
    to a dictionary of arrays. Unspecified entries are np.nan."""
    da = {}
    for k, v in d.items():
        if '_' not in k:
            da[k] = v
        else:
            name = ''.join(k.split('_')[:-1])
            ind = k.split('_')[-1]
            dim = len(ind)
            if name not in da:
                shape = tuple(3 for i in range(dim))
                da[name] = np.empty(shape, dtype=complex)
                da[name][:] = np.nan
            da[name][tuple(int(i) - 1 for i in ind)] = v
    return da


def _symm_herm(C):
    """To get rid of NaNs produced by _scalar2array, symmetrize operators
    where C_ijkl = C_jilk*"""
    nans = np.isnan(C)
    C[nans] = np.einsum('jilk', C)[nans].conj()
    return C


def _symm_current(C):
    """To get rid of NaNs produced by _scalar2array, symmetrize operators
    where C_ijkl = C_klij"""
    nans = np.isnan(C)
    C[nans] = np.einsum('klij', C)[nans]
    return C

def _JMS_to_array(C):
    """For a dictionary with JMS Wilson coefficients, return an dictionary
    of arrays."""
    wc_keys = wcxf.Basis['WET', 'JMS'].all_wcs
    # fill in zeros for missing coefficients
    C_complete = {k: C.get(k, 0) for k in wc_keys}
    Ca = _scalar2array(C_complete)
    for k in Ca:
        if k in ["VnueLL", "VnuuLL", "VnudLL", "VeuLL", "VedLL", "V1udLL", "V8udLL",
                "VeuRR", "VedRR", "V1udRR", "V8udRR", "VnueLR", "VeeLR", "VnuuLR",
                "VnudLR", "VeuLR", "VedLR", "VueLR", "VdeLR", "V1uuLR", "V8uuLR",
                "V1udLR", "V8udLR", "V1duLR", "V8duLR", "V1ddLR", "V8ddLR", "SeuRL",
                "SedRL", "SeuRR", "TeuRR", "SedRR", "TedRR"]:
            Ca[k] = _symm_herm(Ca[k])
        if k in ["S1uuRR", "S8uuRR", "S1ddRR", "S8ddRR", "SeeRR"]:
            Ca[k] = _symm_current(Ca[k])
        if k in ["VuuLL", "VddLL", "VuuRR", "VddRR"]:
            Ca[k] = _symm_herm(_symm_current(Ca[k]))
    return Ca


# final dicitonaries

def JMS_to_flavio(Cflat):
    C = _JMS_to_array(Cflat)
    d={}
    # Class I
    for qq in ['sb', 'db', 'ds']:
        d.update(_BernI_to_Flavio_I(_JMS_to_Bern_I(C, qq), qq))
    # Class II
    for l in lflav.keys():
        for lp in lflav.keys():
            d.update(_BernII_to_Flavio_II(_JMS_to_Bern_II(C, 'cb'+'l_'+l+'nu_'+lp),'cb'+'l_'+l+'nu_'+lp))
            d.update(_BernII_to_Flavio_II(_JMS_to_Bern_II(C, 'ub'+'l_'+l+'nu_'+lp),'ub'+'l_'+l+'nu_'+lp))
            d.update(_BernII_to_Flavio_II(_JMS_to_Bern_II(C, 'us'+'l_'+l+'nu_'+lp),'us'+'l_'+l+'nu_'+lp))
    # Class V
    Fsbuu = _JMS_to_Fierz_III_IV_V(C, 'sbuu')
    Fsbdd = _JMS_to_Fierz_III_IV_V(C, 'sbdd')
    Fsbcc = _JMS_to_Fierz_III_IV_V(C, 'sbcc')
    Fsbss = _JMS_to_Fierz_III_IV_V(C, 'sbss')
    Fsbbb = _JMS_to_Fierz_III_IV_V(C, 'sbbb')

    Fdbuu = _JMS_to_Fierz_III_IV_V(C, 'dbuu')
    Fdbdd = _JMS_to_Fierz_III_IV_V(C, 'dbdd')
    Fdbcc = _JMS_to_Fierz_III_IV_V(C, 'dbcc')
    Fdbss = _JMS_to_Fierz_III_IV_V(C, 'dbss')
    Fdbbb = _JMS_to_Fierz_III_IV_V(C, 'dbbb')
    d.update(_Fierz_to_Flavio_V(Fsbuu,Fsbdd,Fsbcc,Fsbss,Fsbbb,'sb'))
    d.update(_Fierz_to_Flavio_V(Fdbuu,Fdbdd,Fdbcc,Fdbss,Fdbbb,'db'))
    # Class V semileptonic
    for l in lflav.keys():
        for lp in lflav.keys():
            d.update(Fierz_to_Flavio_lep(JMS_to_Fierz_lep(C, 'sb'+'l_'+l+'nu_'+lp),'sb'+'l_'+l+'nu_'+lp))
            d.update(Fierz_to_Flavio_lep(JMS_to_Fierz_lep(C, 'db'+'l_'+l+'nu_'+lp),'db'+'l_'+l+'nu_'+lp))

    # Class V chromomagnetic
    d.update(Fierz_to_Flavio_chrom(JMS_to_Fierz_chrom(C, 'sb'), 'sb'))
    d.update(Fierz_to_Flavio_chrom(JMS_to_Fierz_chrom(C, 'db'), 'db'))
    return d


def JMS_to_Bern(Cflat):
    C = _JMS_to_array(Cflat)
    d={}
    # Class I
    for qq in ['sb', 'db', 'ds']:
        d.update(_JMS_to_Bern_I(C, qq))
    # Class II
    for l in lflav.keys():
        for lp in lflav.keys():
            d.update(_JMS_to_Bern_II(C, 'cb'+'l_'+l+'nu_'+lp))
            d.update(_JMS_to_Bern_II(C, 'ub'+'l_'+l+'nu_'+lp))
            d.update(_JMS_to_Bern_II(C, 'us'+'l_'+l+'nu_'+lp))
    # Class V
    for u1 in uflav.keys():
        for u2 in uflav.keys():
            d.update(_Fierz_to_Bern_III_IV_V(_JMS_to_Fierz_III_IV_V(C, 'sb'+u1+u2), 'sb'+u1+u2))
            d.update(_Fierz_to_Bern_III_IV_V(_JMS_to_Fierz_III_IV_V(C, 'db'+u1+u2), 'db'+u1+u2))
    for qqqq in ['sbdd','sbss','dbdd','dbss','dbbb','sbbb','dbds','sbsd','dsbb']:
        d.update(_Fierz_to_Bern_III_IV_V(_JMS_to_Fierz_III_IV_V(C, qqqq), qqqq))

    # Class V semileptonic
    for l in lflav.keys():
        for lp in lflav.keys():
            d.update(Fierz_to_Bern_lep(JMS_to_Fierz_lep(C, 'sb'+'l_'+l+'nu_'+lp),'sb'+'l_'+l+'nu_'+lp))
            d.update(Fierz_to_Bern_lep(JMS_to_Fierz_lep(C, 'db'+'l_'+l+'nu_'+lp),'db'+'l_'+l+'nu_'+lp))

    # Class V chromomagnetic
    d.update(Fierz_to_Bern_chrom(JMS_to_Fierz_chrom(C, 'sb'), 'sb'))
    d.update(Fierz_to_Bern_chrom(JMS_to_Fierz_chrom(C, 'db'), 'db'))
    return d
