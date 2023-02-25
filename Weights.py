import math

#conversion functions
from cmath import cos, pi


def metres_to_feet(metre):
    feet = metre*3.28084
    return feet


def kg_to_lb(kg):
    lb = kg*2.20462
    return lb


def m2_to_ft2(m2):
    ft2 = m2*10.7639
    return ft2


def m3_to_ft3(m3):
    ft3 = m3*35.3147
    return ft3


def litre_to_gallon(litre):
    gallon = litre*0.219969
    return gallon

def pascal_to_psi(pascal):
    psi = pascal / 6895
    return psi

def tail_planes_weight(comTOtail, cyLength, totLength):
    # variable convention from Raymer pg 576, [desired] units
    p = "placeholder"  # placeholder
    A = 15.78  # aspect ratio
    Ah = 5  # htp aspect ratio
    Av = 1  # vtp aspect ratio
    Bh = metres_to_feet(8.99)  # horizontal tail span [ft]
    Bw = metres_to_feet(36.5)  # wing span [ft]
    D = metres_to_feet(3.966)  # fuselage structural depth [ft]
    Fw = metres_to_feet(2.04)  # fuselage width at horizontal tail intersection [ft]
    Ht = metres_to_feet(4.492)  # horizontal tail height above fuselage, [ft]
    HtPERHv = 1.0  # 1 for Ttail
    Hv = metres_to_feet(4.492)  # vertical tail height above fuselage [ft]
    Iyaw = 1  # yawing moment of inertia [lb.ft^2]
    Kcb = 1.0  # see book, not cross-beam gear
    Kd = p  # duct constant
    Kdoor = 1.0  # no cargo doors
    Kdw = 1.0  # no delta wing
    Kdwf = 1.0  # no delta wing
    Kh = 0.12  # requires discussion (I chose medium subsonic with hydraulics for flaps)
    Klg = 1.12  # fuselage-mounted MLG
    Kng = 1.017  # pylon
    Kp = 1.4  # engine with propeller
    Kr = 1.0  # non-reciprocating engine
    Krht = 1.0  # no rolling tail
    Ktp = 0.793  # turboprop
    Ktr = 1.0  # no thrust reverser
    Kuht = 1.0
    Kvg = 1.0
    taper_ratio = 0.45
    wing_sweep = 5
    L = metres_to_feet(cyLength)  # fuselage structural length [ft]
    Kws = 0.75 * ((1 + 2 * taper_ratio) / (1 + taper_ratio)) * (Bw / L) * math.tan(math.radians(wing_sweep))  # wing sweep factor, formula in book
    Lt = metres_to_feet(12.6)  # tail length, quarter MAC wing to quarter MAC tail [ft] horizontal, vertical 11.3
    Ky = 0.3 * Lt  # aircraft pitching radius of gyration (~0.3 Lt)
    Kz = Lt  # aircraft yawing radius of gyration (~Lt)
    La = metres_to_feet(35)  # electrical routing distance [ft]
    Lec = metres_to_feet(42)  # routing distance from engine front to cockpit [ft]
    Lf = metres_to_feet(totLength)  # total fuselage length [ft]
    Lm = p  # extended length of MLG [in]
    Ln = p  # extended length of NLG [in]
    M = 0.7  # mach number, design maximum
    Nc = 2.0  # number of crew
    Nci = 2.0
    Nen = 2.0  # number of engines
    Nf = 5.0  # number of separate functions performed by surface controls
    Ngen = 2.0
    Nlt = metres_to_feet(4.5)  # nacelle length [ft]
    Nl = p  # ultimate landing load factor, =Ngear*1.5   <<---- Understand this
    Nm = 3  # number of surface controls driven by mech not hydraulic
    Nmss = 2  # number of MLG shock struts
    Nmw = 4  # number of MLG wheels
    Nnw = 2  # number of NLG wheels
    Np = 125  # number of people on board
    Ns = 1  # number of flight control systems
    Nt = 2  # number of fuel tanks
    Nu = 5  # number of hydraulic utility functions (typ 5-15)
    Nz = 3.85  # ultimate load factor, =1.5*limit load factor
    q = p  # dynamic pressure at cruise [lb/ft^2]
    Rkva = 50  # system electrical rating [kVA]
    Scs = m2_to_ft2(9)  # total surface area of control surfaces [ft^2]
    Scsw = m2_to_ft2(4.5)  # control surface area wing-mounted [ft^2]
    Se = m2_to_ft2(2.5)  # elevator area [ft^2]
    Sf = m2_to_ft2(292.54)  # fuselage wetted area [ft^2]
    Sht = m2_to_ft2(15)  # horizontal tail area [ft^2]
    Sr = m2_to_ft2(1.3)  # rudder area [ft^2]
    Vstall = 104  # stall speed [kt]
    Svt = m2_to_ft2(20.18)  # vertical tail area [ft^2]
    Sw = m2_to_ft2(88.5)  # trapezoidal wing area [ft^2]
    tPERc = 0.18  # thickness to chord ratio
    Vi = litre_to_gallon(5500)  # integral tanks volume [gal]
    Vpr = m3_to_ft3(278)  # volume of pressurized section [ft^3]
    Vt = litre_to_gallon(5500)  # total fuel volume [gal]
    W = metres_to_feet(3.966)  # total fuselage structural width [ft]
    Pdelta = pascal_to_psi(55158)  # cabin pressure differential [psi]
    Wuav = 800  # uninstalled avionics weight [lb]
    Wl = kg_to_lb(3300)  # landing design gross weight [lb]
    Wfw = kg_to_lb(4500)  # weight of fuel in wing [lb]
    Wen = kg_to_lb(1120)  # engine weight, each [lb]
    Wec = kg_to_lb(1992)  # weight of engine and contents [lb]
    Wdg = kg_to_lb(35410)  # flight design gross weight [lb]
    htp_sweep = 5
    vtp_sweep = 30
    Wc = kg_to_lb(120*95)


    #ones i thought i wouldn't need
    Kmp = 1.0
    Knp = 1.0
    Vp = 0 #no self sealing tanks


    #new Sht, Svt
    Cht = 0.95*0.95
    Cvt = 0.085*0.95
    Lht = metres_to_feet(comTOtail)
    Lvt = metres_to_feet(comTOtail)
    Lt = metres_to_feet(comTOtail)
    MAC = metres_to_feet(2.43)

    Sht = Cht*MAC*Sw/Lht
    Svt = Cvt*Bw*Sw/Lvt


    #the equations, output in lb
    horizontalTailWeight = (0.0379*Kuht *(1+Fw/Bh)**-0.25 * Wdg**0.639 *
            Nz**0.1 * Sht**0.75 * Lt**-1 * Ky**0.704 * cos(htp_sweep*pi/180)**-1 * Ah**0.166 *(1+Se/Sht)**0.1
    )

    verticalTailWeight = (0.0026*(1+HtPERHv)**0.225 * Wdg**0.556 * Nz**0.536 * Lt**-0.5 *
            Svt**0.5 * Kz**0.875 * cos(vtp_sweep)**-1 * Av**0.35 * tPERc**-0.5
    )


    tailWeight = (horizontalTailWeight+verticalTailWeight)*0.453592 #back to kg
    tailWeight = tailWeight.real

    return(tailWeight)
