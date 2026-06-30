"""
Room Maze 2D -- Top-Down View
WASD / Arrow Keys: Move   R: New Maze   ESC: Quit
"""
import pygame, sys, math, random, heapq, copy, time, os
# random_seed_injected
random.seed(12345)
from collections import deque 
from dataclasses import dataclass, field
from pygame.locals import *

# =============================================================================
#  benchmark seeds
# -----------------------------------------------------------------------------
# a fixed list of 500 unique world seeds used for the cross-agent comparison.
# seeding the global rng with one of these before world generation produces a
# deterministic maze (walls, traps, enemies, start/exit), so every agent mode
# faces an identical environment for a given seed 
#
# derivation (for the record / regeneration):
# r = random.random(20240617)
# benchmark_seeds = sorted(r.sample(range(1, 1_000_000), 500))
# =============================================================================
BENCHMARK_SEEDS = [
       754,   2592,   6768,   7125,   7554,  12587,  18799,  34111,  37319,  38029,
     38911,  38949,  41857,  44329,  46578,  46953,  48010,  48700,  51765,  51848,
     51855,  53326,  55494,  56190,  57607,  58404,  58889,  62566,  62673,  66168,
     76503,  76926,  78463,  79396,  86072,  86950,  87820,  89165,  89206,  92254,
     93225, 101431, 106893, 111410, 111927, 113084, 117506, 118476, 119814, 121259,
    123269, 126613, 127538, 130076, 130241, 130749, 130841, 132006, 136584, 139499,
    144563, 145111, 148487, 152899, 155171, 160538, 163216, 163936, 164601, 167112,
    167267, 168146, 170451, 170591, 170738, 171467, 172404, 175158, 176158, 177470,
    179079, 180577, 183184, 185868, 187153, 188948, 188953, 189643, 194875, 202115,
    207868, 208492, 211913, 213643, 213950, 215431, 215638, 218312, 218397, 223537,
    225113, 231552, 233477, 234237, 235919, 236977, 238739, 240952, 244013, 244688,
    248400, 250634, 250784, 254355, 257837, 257920, 266508, 266890, 267583, 272422,
    273363, 273840, 277964, 281647, 282233, 282238, 285367, 286432, 286676, 287299,
    287425, 289041, 292627, 293802, 294142, 297766, 298720, 299071, 300560, 304808,
    305295, 306950, 309032, 309190, 309537, 311029, 312614, 323783, 325224, 340689,
    343382, 346530, 349465, 354670, 355675, 356447, 359835, 359904, 360136, 361406,
    361942, 362697, 363232, 369598, 373266, 378246, 379226, 379517, 381162, 383004,
    383440, 383666, 384086, 386082, 387483, 389616, 391544, 396612, 396730, 397402,
    398424, 399042, 403294, 403581, 404158, 404930, 405804, 405856, 407307, 410035,
    412271, 413728, 415158, 416688, 417476, 417839, 418974, 420734, 423013, 423449,
    427951, 430066, 430113, 431823, 434988, 436156, 438378, 438709, 441623, 442981,
    445434, 446821, 447178, 448273, 449978, 452436, 452475, 452864, 454656, 454680,
    455029, 455038, 459764, 461280, 463005, 464863, 471958, 474549, 474626, 475261,
    478312, 478701, 482229, 484708, 485955, 487399, 487726, 493624, 493819, 497214,
    499951, 500286, 503670, 505083, 506160, 506554, 506848, 509155, 513672, 516236,
    523516, 524348, 528266, 536055, 536105, 537589, 537777, 538306, 538575, 540395,
    540584, 540665, 543683, 544860, 545846, 549111, 549420, 552428, 552946, 555330,
    555949, 556676, 556730, 561293, 562555, 564478, 565032, 568158, 571313, 579988,
    580955, 581292, 581734, 582786, 585206, 593919, 594412, 595544, 598595, 599450,
    601226, 606984, 607772, 608880, 611112, 611739, 612389, 613011, 614068, 614828,
    616151, 616246, 617096, 618323, 619134, 619855, 620255, 627259, 628023, 628120,
    629354, 632317, 636094, 636172, 637629, 638135, 639368, 642852, 645459, 646729,
    648106, 648652, 649644, 658527, 661612, 662428, 670337, 670978, 671590, 674298,
    677723, 680855, 683548, 683894, 684873, 689171, 693889, 694280, 700275, 702331,
    705313, 708428, 708486, 710966, 713650, 716011, 717457, 718587, 719804, 720723,
    720899, 726526, 729347, 730878, 732384, 737515, 739002, 739834, 741718, 745260,
    748205, 753145, 753377, 753516, 753828, 754332, 755576, 756082, 756614, 756786,
    762174, 764458, 768028, 769846, 771240, 771852, 778571, 778712, 781856, 782943,
    782992, 783987, 788955, 789602, 791610, 793235, 797225, 797396, 799446, 801441,
    802227, 808342, 810156, 813346, 816451, 817639, 818215, 818757, 822388, 828384,
    828527, 829361, 829835, 831714, 832758, 833924, 834434, 837006, 839640, 841340,
    843118, 844967, 845623, 850502, 851636, 852746, 853365, 858374, 860616, 860891,
    861195, 861626, 864043, 865189, 868084, 868804, 870110, 871120, 875846, 880936,
    882288, 882480, 882713, 882872, 884535, 885523, 886575, 887418, 890942, 894757,
    895703, 895723, 899254, 901961, 903285, 904395, 912956, 915244, 915578, 916179,
    916328, 918256, 921873, 924796, 924855, 925073, 928425, 928431, 929490, 929532,
    932375, 933969, 934035, 938514, 939062, 941211, 941793, 945267, 948753, 950088,
    951895, 952364, 954539, 955226, 956215, 956375, 956753, 962205, 962523, 963428,
    964353, 968418, 969123, 970524, 979514, 979992, 980956, 983094, 983101, 984760,
    986531, 986809, 988681, 990131, 990849, 994424, 998274, 998915, 998918, 999452,
]


# -- window -------------------------------------------------------------------
W, H   = 960, 640
HUD_H  = 64
WIN_H  = H + HUD_H
# width of the reused-expectations side panel
SIDE_W = 250
# width of the "imagination" panel (internal-model rollout)
IMAG_W = 300
FPS    = 60

# whole-attempt time budget for the interactive/live game, in world ticks.
# matches the headless benchmark and mcts-baseline default (9000 ticks) so a
# live run is bounded exactly like a benchmarked one: reach the exit within
# this many ticks or the attempt ends as a timeout (then auto-restarts in
# agent mode).  kept identical to the --compare default so live and headless
# results are directly comparable.
LIVE_TIMEOUT_TICKS = 9000

# -- uncertainty / non-stationarity -------------------------------------------
# these settings make the world hostile to trial-and-error (rl) agents:
# 1. traps relocate when you re-enter a room (can't memorise layout)
# 2. trap timing has stochastic jitter each activation cycle
# 3. roaming enemies patrol random waypoints unpredictably
# 4. random room-wide hazard pulses at irregular intervals
# 5. fog of war hides traps until close (no global map exploitation)
# legacy radial cap (kept; the fov below is the real limit)
FOG_REVEAL_DIST = 999

# ── directional field of view ────────────────────────────────────────────────
# the agent perceives a forward-facing cone rather than the whole map: it can
# see ahead along its current heading and a few tiles to either side
# (peripheral vision), but is blind to whatever is behind it.  heading is the
# agent's last cardinal move (defaults to "down" before it first moves).
#
# • vision_forward   — how many tiles ahead it can see.
# • vision_peripheral— lateral half-width (3 ⇒ 3 tiles out on each side).
# • vision_behind    — tiles visible behind the agent (0 ⇒ fully blind behind).
# a tile at body-relative offset (ox,oy) with heading (hx,hy) is visible iff
# forward = ox·hx + oy·hy ∈ [-vision_behind, vision_forward]   and
# lateral = |ox·(-hy) + oy·hx| ≤ vision_peripheral.
# the agent's own tile is always visible.
VISION_ENABLED     = True
VISION_FORWARD     = 6
VISION_PERIPHERAL  = 2
VISION_BEHIND      = 0

def _heading_from(action):
    """Cardinal heading (hx,hy) from a last action; default 'down' (0,1)."""
    if action in ((-1,0),(1,0),(0,-1),(0,1)):
        return action
    return (0, 1)

def _in_fov(ox, oy, heading):
    """True if body-relative offset (ox,oy) is inside the forward FOV cone."""
    if ox == 0 and oy == 0:
        # own tile always seen
        return True
    hx, hy = heading
    forward = ox * hx + oy * hy
    lateral = abs(ox * (-hy) + oy * hx)
    return (-VISION_BEHIND <= forward <= VISION_FORWARD
            and lateral <= VISION_PERIPHERAL)

# traps shuffle positions each room visit
RELOC_ON_REENTRY = True

# body-corner offsets used to test whether a simulated enemy's half-extent (m)
# overlaps a wall tile. hoisted to module scope so the hot rollout path does not
# rebuild this list on every call.
_ENEMY_BODY_OFFSETS = ((0.32, 0), (-0.32, 0), (0, 0.32), (0, -0.32))
# roaming enemies per room (added at world-gen)
ENEMY_COUNT = 2
# min ticks between room-wide pulses
HAZARD_PULSE_MIN = 180
# max ticks between room-wide pulses
HAZARD_PULSE_MAX = 480

# -- world --------------------------------------------------------------------
COLS, ROWS = 55, 43
# tile size in pixels
TS     = 24
START_SAFE_RADIUS = 3
EXIT_SAFE_RADIUS  = 4

# -- colours ------------------------------------------------------------------
BLACK = (0,0,0); WHITE = (255,255,255)

# ── render style flags ───────────────────────────────────────────────────────
# formal_style: flat "academic figure" look (grey structure, category-coloured
# flat hazards).  left available but off by default — the original themed
# sprites and colours are used instead.
# reduce_effects: keep the original shapes and colours, but calm the visuals —
# no ambient particles, no additive glow halos, and dampened pulsing.  this
# is the default: coloured environment, just far fewer effects.
FORMAL_STYLE   = False
REDUCE_EFFECTS = True

# neutral structural palette (used for all room themes when formal_style)
FML = dict(
    bg        = (244, 245, 247),  # canvas / paper
    floor     = (255, 255, 255),  # walkable interior
    floor2    = (248, 249, 251),  # subtle checker
    wall      = (210, 214, 220),  # wall fill
    wall_hi   = (188, 193, 201),  # wall edge
    grid      = (228, 230, 234),  # tile gridlines
    ink       = (44, 50, 60),  # primary text / outlines
    ink_soft  = (120, 128, 140),  # secondary text
    panel_bg  = (250, 251, 252),  # side panel / hud background
    panel_ln  = (214, 218, 224),  # panel separators
    agent     = (38, 92, 168),  # the agent (process blue)
    agent_ed  = (24, 64, 124),
    goal      = (40, 140, 90),  # exit marker (green)
    start     = (150, 156, 166),  # start marker (grey)
)

# hazard colour by functional category (flat, distinguishable, muted):
# kinetic  — moving/striking bodies (axes, boulders, bars, sweepers, darts)
# thermal  — heat/cold area hazards (lava, fire, ice beams, geysers)
# area     — expanding/zone hazards (spore ring, gravity well, thorn wall…)
# trap     — static floor traps (plates, glyphs, mines, pits)
# red-brown
HZ_KINETIC = (196, 64, 48)
# amber
HZ_THERMAL = (210, 120, 40)
# slate blue
HZ_AREA    = (110, 120, 200)
# tan
HZ_TRAP    = (150, 100, 60)
# muted violet
HZ_ENEMY   = (120, 60, 140)

_HZ_CATEGORY = {
    # kinetic
    "pendulum_axe": HZ_KINETIC, "ceiling_crusher": HZ_KINETIC,
    "rolling_boulder": HZ_KINETIC, "ice_sweeper": HZ_KINETIC,
    "wall_dart": HZ_KINETIC, "frozen_spike_row": HZ_KINETIC,
    "mummy_wrap": HZ_KINETIC, "sarcophagus": HZ_KINETIC,
    "mirror_clone": HZ_KINETIC,
    # thermal / beam
    "fire_bar": HZ_THERMAL, "ice_beam": HZ_THERMAL, "lava_tide": HZ_THERMAL,
    # area / zone
    "spore_burst": HZ_AREA, "gravity_pull": HZ_AREA, "thorn_wall": HZ_AREA,
}

def hazard_color(kind):
    """Flat functional colour for a hazard kind (formal style)."""
    return _HZ_CATEGORY.get(kind, HZ_TRAP)


# ── hazard predictability (death-cause diagnostic) ───────────────────────────
# a death is only a legitimate "unavoidable" outcome when the killer's future
# could not be exactly known to the agent's forward model.  two sources of
# genuine unpredictability exist in this sim:
# 1. roamingenemy — chooses random waypoints, so its path is stochastic.
# 2. dynamic traps that seek the player or fire on a randomised next-cycle
# clock (the period after the current one is drawn from random.randint),
# so the model can track the current cycle but not the one after it.
# everything else — all static traps, and dynamic traps whose geometry is a
# pure function of time — is fully determined by the present world state.  if
# the agent dies to one of those, the internal model failed to foresee a
# knowable collision: that is a simulation bug, not bad luck.
#
# note: kinds here are the dynamic traps that call random.* inside update()
# (verified against dynamictrap.update) or actively chase the player.
_NONDETERMINISTIC_DTRAPS = frozenset({
    "ceiling_crusher",  # next "up" dwell = random.randint(60,120)
    "frozen_spike_row",  # next "wait" = random.randint(40,80)
    "sarcophagus",  # fires shots + random re-arm
    "gravity_pull",  # random re-arm timer
    "mirror_clone",  # mirrors player position (depends on player path)
    "reality_crack",  # teleports to a random floor tile
    "mummy_wrap",  # random launch timer (randint) and homes on the
                         # player's position at fire time — both the when and
                         # the where depend on un-forecastable inputs, exactly
                         # like mirror_clone.  the dormant-ring + active-dart
                         # forecasts let the agent dodge most launches, but a
                         # dart fired at point-blank during the random timer's
                         # expiry is not reliably avoidable, so a death to it is
                         # not a pure planning bug.
})
# spore_burst is now deterministic (fixed period + slowed expansion), so it is
# treated as predictable: a death to it indicates the agent failed to handle a
# fully knowable hazard.

def hazard_is_predictable(kind: str) -> bool:
    """True when *kind*'s lethal geometry is a pure function of the CURRENT
    world state, so the forward model could foresee a collision exactly.
    Death to a predictable hazard indicates a simulation/planning bug."""
    if kind in _NONDETERMINISTIC_DTRAPS:
        return False
    # roamingenemy reports kind="enemy" (see take_damage call site).
    if kind == "enemy":
        return False
    return True


THEMES = {
    # floor        floor2       wall         wall_hi      acc            detail
    "dungeon": dict(floor=(45,38,55),  floor2=(38,30,48), wall=(32,25,42),  wall_hi=(55,44,68), acc=(140,100,200), detail=(65,55,80)),
    "lava":    dict(floor=(72,30,12),  floor2=(58,20,6),  wall=(42,14,5),   wall_hi=(70,25,8),  acc=(255,120,30),  detail=(180,55,10)),
    "ice":     dict(floor=(58,92,138), floor2=(44,72,112),wall=(30,48,78),  wall_hi=(55,88,130),acc=(110,230,255), detail=(80,160,220)),
    "forest":  dict(floor=(34,68,25),  floor2=(24,52,16), wall=(16,32,10),  wall_hi=(28,55,18), acc=(90,220,65),   detail=(55,140,35)),
    "tomb":    dict(floor=(75,62,46),  floor2=(60,48,34), wall=(32,26,18),  wall_hi=(52,42,28), acc=(220,195,110), detail=(140,115,65)),
    "void":    dict(floor=(24,15,44),  floor2=(14,8,32),  wall=(10,6,20),   wall_hi=(20,12,38), acc=(180,70,255),  detail=(100,35,160)),
}

RTYPES = {
    # each room type gets 2 static floor hazards + 2 dynamic/moving hazards — all thematic
    "dungeon": {"theme":"dungeon",
                "straps":["pressure_plate","wall_dart"],
                "dtraps":["pendulum_axe","ceiling_crusher","fire_bar"]},
    "lava":    {"theme":"lava",
                "straps":["lava_geyser","magma_crack"],
                "dtraps":["lava_tide","rolling_boulder","fire_bar"]},
    "ice":     {"theme":"ice",
                "straps":["ice_vent","cracked_ice"],
                "dtraps":["ice_sweeper","frozen_spike_row","ice_beam"]},
    "forest":  {"theme":"forest",
                "straps":["bear_trap","poison_mushroom"],
                "dtraps":["thorn_wall","spore_burst"]},
    "tomb":    {"theme":"tomb",
                "straps":["floor_glyph","sand_pit"],
                "dtraps":["mummy_wrap","sarcophagus"]},
    "void":    {"theme":"void",
                "straps":["void_eye","reality_crack"],
                "dtraps":["gravity_pull","ice_beam"]},
}

TDEFS = {
    # ── dungeon ──────────────────────────────────────────────────────────────
    "pressure_plate": dict(col=(200,60,60),   dmg=99,eff=None,      cd=80, lbl="Pressure Plate"),
    "wall_dart":      dict(col=(160,140,80),  dmg=99,eff=None,      cd=60, lbl="Wall Dart"),
    "pendulum_axe":   dict(col=(180,140,60),  dmg=99,eff=None,      cd=30, lbl="Pendulum Axe"),
    "ceiling_crusher":dict(col=(140,120,100), dmg=99,eff="stun",    cd=90, lbl="Ceiling Crusher"),
    # ── lava ─────────────────────────────────────────────────────────────────
    "lava_geyser":    dict(col=(255,100,10),  dmg=99,eff="burn",    cd=40, lbl="Lava Geyser"),
    "magma_crack":    dict(col=(220,70,10),   dmg=99,eff="burn",    cd=50, lbl="Magma Crack"),
    "lava_tide":      dict(col=(255,80,0),    dmg=99,eff="burn",    cd=20, lbl="Lava Tide"),
    "rolling_boulder":dict(col=(160,90,40),   dmg=99,eff=None,      cd=30, lbl="Rolling Boulder"),
    # ── ice ──────────────────────────────────────────────────────────────────
    "ice_vent":       dict(col=(120,210,255), dmg=99,eff="freeze",  cd=45, lbl="Ice Vent"),
    "cracked_ice":    dict(col=(80,170,220),  dmg=99,eff=None,      cd=70, lbl="Cracked Ice"),
    "ice_sweeper":    dict(col=(140,220,255), dmg=99,eff="freeze",  cd=25, lbl="Ice Sweeper"),
    "frozen_spike_row":dict(col=(170,235,255),dmg=99,eff="freeze",  cd=35, lbl="Spike Row"),
    # ── forest ───────────────────────────────────────────────────────────────
    "bear_trap":      dict(col=(140,100,50),  dmg=99,eff="snare",   cd=100,lbl="Bear Trap"),
    "poison_mushroom":dict(col=(120,200,50),  dmg=99,eff="poison",  cd=50, lbl="Poison Mushroom"),
    "thorn_wall":     dict(col=(80,160,40),   dmg=99,eff="snare",   cd=25, lbl="Thorn Wall"),
    "spore_burst":    dict(col=(140,220,60),  dmg=99,eff="poison",  cd=35, lbl="Spore Burst"),
    # ── tomb ─────────────────────────────────────────────────────────────────
    "floor_glyph":    dict(col=(200,180,80),  dmg=99,eff="curse",   cd=60, lbl="Floor Glyph"),
    "sand_pit":       dict(col=(190,160,80),  dmg=99,eff="slow",    cd=40, lbl="Sand Pit"),
    "mummy_wrap":     dict(col=(210,195,150), dmg=99,eff="snare",   cd=30, lbl="Mummy Wrap"),
    "sarcophagus":    dict(col=(180,150,70),  dmg=99,eff="curse",   cd=50, lbl="Sarcophagus"),
    # ── void ─────────────────────────────────────────────────────────────────
    "void_eye":       dict(col=(160,60,255),  dmg=99,eff="curse",   cd=50, lbl="Void Eye"),
    "reality_crack":  dict(col=(200,80,255),  dmg=99,eff="teleport",cd=70, lbl="Reality Crack"),
    "gravity_pull":   dict(col=(130,40,220),  dmg=99,eff=None,      cd=25, lbl="Gravity Pull"),
    "mirror_clone":   dict(col=(180,100,255), dmg=99,eff=None,      cd=30, lbl="Mirror Clone"),
    # ── spinners (shared) ────────────────────────────────────────────────────
    "fire_bar":       dict(col=(255,140,20),  dmg=99,eff="burn",    cd=20, lbl="Fire Bar"),
    "ice_beam":       dict(col=(120,215,255), dmg=99,eff="freeze",  cd=25, lbl="Ice Beam"),
}

# spore burst is drawn as a thin expanding ring. keep its lethal annulus
# close to the visible stroke/dots plus the player's body radius; wider values
# make the trap feel like it hits well beyond what is on screen.
PLAYER_HIT_RADIUS = 0.32
ENEMY_HIT_RADIUS = 0.38
PLAYER_WALL_RADIUS = 0.40
THIN_HAZARD_HALF_WIDTH = 0.07
SMALL_PROJECTILE_RADIUS = 0.08
SPORE_RING_HIT_HALF_WIDTH = PLAYER_HIT_RADIUS + THIN_HAZARD_HALF_WIDTH
# spore burst is a fully deterministic periodic hazard: fixed fire period and a
# slowed expansion so the agent has time to clear the blast disc between firings.
# ticks between firings (was random 50-90)
SPORE_FIRE_PERIOD = 75
# ring radius growth per tick (was 0.12)
SPORE_EXPAND_SPEED = 0.085

# physical sensor properties per trap — agent perceives these, not the kind name.
# hardcoding stops here: sensors describe embodied reality, not game semantics.
TRAP_SENSORS = {
    # temp  toxicity  impact  moving  constrict  unstable  corrupting
    "pressure_plate": dict(temp= 20, tox=0.0, imp=250, mov=False, con=False, unst=False, cor=False),
    "wall_dart":      dict(temp= 20, tox=0.0, imp=180, mov=True,  con=False, unst=False, cor=False),
    "pendulum_axe":   dict(temp= 20, tox=0.0, imp=420, mov=True,  con=False, unst=False, cor=False),
    "ceiling_crusher":dict(temp= 20, tox=0.0, imp=600, mov=True,  con=False, unst=False, cor=False),
    "fire_bar":       dict(temp=750, tox=0.0, imp=200, mov=True,  con=False, unst=False, cor=False),
    "lava_geyser":    dict(temp=820, tox=0.0, imp= 90, mov=True,  con=False, unst=False, cor=False),
    "magma_crack":    dict(temp=650, tox=0.0, imp= 40, mov=False, con=False, unst=True,  cor=False),
    "lava_tide":      dict(temp=900, tox=0.0, imp=130, mov=True,  con=False, unst=False, cor=False),
    "rolling_boulder":dict(temp= 20, tox=0.0, imp=700, mov=True,  con=False, unst=False, cor=False),
    "ice_vent":       dict(temp=-45, tox=0.0, imp= 60, mov=True,  con=False, unst=False, cor=False),
    "cracked_ice":    dict(temp=-15, tox=0.0, imp= 30, mov=False, con=False, unst=True,  cor=False),
    "ice_sweeper":    dict(temp=-30, tox=0.0, imp=150, mov=True,  con=False, unst=False, cor=False),
    "frozen_spike_row":dict(temp=-25,tox=0.0, imp=300, mov=True,  con=False, unst=False, cor=False),
    "ice_beam":       dict(temp=-55, tox=0.0, imp=100, mov=True,  con=False, unst=False, cor=False),
    "bear_trap":      dict(temp= 20, tox=0.0, imp=360, mov=False, con=True,  unst=False, cor=False),
    "poison_mushroom":dict(temp= 20, tox=0.9, imp= 10, mov=False, con=False, unst=False, cor=False),
    "thorn_wall":     dict(temp= 20, tox=0.3, imp=100, mov=True,  con=True,  unst=False, cor=False),
    "spore_burst":    dict(temp= 20, tox=0.7, imp= 20, mov=True,  con=False, unst=False, cor=False),
    "floor_glyph":    dict(temp= 20, tox=0.0, imp=  0, mov=False, con=True,  unst=False, cor=True),
    "sand_pit":       dict(temp= 30, tox=0.0, imp= 20, mov=False, con=True,  unst=True,  cor=False),
    "mummy_wrap":     dict(temp= 20, tox=0.0, imp=150, mov=True,  con=True,  unst=False, cor=False),
    "sarcophagus":    dict(temp= 20, tox=0.0, imp=200, mov=True,  con=False, unst=False, cor=True),
    "void_eye":       dict(temp= 20, tox=0.0, imp=  0, mov=False, con=False, unst=False, cor=True),
    "reality_crack":  dict(temp= 20, tox=0.0, imp=  0, mov=False, con=False, unst=True,  cor=True),
    "gravity_pull":   dict(temp= 20, tox=0.0, imp=300, mov=True,  con=False, unst=False, cor=False),
    "mirror_clone":   dict(temp= 20, tox=0.0, imp=200, mov=True,  con=False, unst=False, cor=False),
}

# agent survivability thresholds — hardcode embodiment, not game knowledge
# °c above which thermal damage occurs
AGENT_MAX_TEMP     = 45
# °c below which cold damage occurs
AGENT_MIN_TEMP     = -5
# toxin tolerance fraction
AGENT_MAX_TOXICITY = 0.1
# newtons — impact force tolerance
AGENT_MAX_IMPACT   = 150

SDEFS = {
    "burn":    dict(col=(255,120,30), tick=4, dur=120, slow=0.0),
    "freeze":  dict(col=(80,200,255), tick=0, dur=150, slow=0.35),
    "snare":   dict(col=(60,160,40),  tick=0, dur=120, slow=0.20),
    "poison":  dict(col=(120,220,60), tick=3, dur=200, slow=0.0),
    "curse":   dict(col=(200,150,255),tick=5, dur=180, slow=0.10),
    "slow":    dict(col=(180,150,80), tick=0, dur=100, slow=0.25),
    "stun":    dict(col=(220,220,80), tick=0, dur=60,  slow=1.0),
    "teleport":dict(col=(155,55,255), tick=0, dur=0,   slow=0.0),
}

def lerpc(a, b, t):
    return tuple(max(0,min(255,int(a[i]+t*(b[i]-a[i])))) for i in range(3))

def asurf(w, h):
    return pygame.Surface((w,h), pygame.SRCALPHA)

_FORMAL_FONT_CACHE = {}
def _formal_font(size=11, bold=False):
    """Cached small monospace font for in-world hazard/agent labels."""
    key = (size, bold)
    f = _FORMAL_FONT_CACHE.get(key)
    if f is None:
        try:
            f = pygame.font.SysFont("consolas", size, bold=bold)
        except Exception:
            f = pygame.font.Font(None, size + 2)
        _FORMAL_FONT_CACHE[key] = f
    return f


# =============================================================================
# world generation
# =============================================================================
class Room:
    def __init__(self, x, y, w, h, rtype):
        self.x=x; self.y=y; self.w=w; self.h=h; self.rtype=rtype
        self.cx=x+w//2; self.cy=y+h//2
        self.straps=[]; self.dtraps=[]
    def overlaps(self, o, m=2):
        return (self.x-m < o.x+o.w and self.x+self.w+m > o.x and
                self.y-m < o.y+o.h and self.y+self.h+m > o.y)
    def inner(self):
        return [(x,y) for y in range(self.y+1,self.y+self.h-1)
                      for x in range(self.x+1,self.x+self.w-1)]

def carve_h(g, x0, x1, y):
    for x in range(max(0,x0), min(COLS,x1+1)):
        for d in (-1,0,1):
            ny=y+d
            if 0<=ny<ROWS: g[ny][x]=0

def carve_v(g, y0, y1, x):
    for y in range(max(0,y0), min(ROWS,y1+1)):
        for d in (-1,0,1):
            nx=x+d
            if 0<=nx<COLS: g[y][nx]=0

def carve_corridor(g, r1, r2):
    x1,y1=r1.cx,r1.cy; x2,y2=r2.cx,r2.cy
    if random.random() < .5:
        carve_h(g,min(x1,x2),max(x1,x2),y1)
        carve_v(g,min(y1,y2),max(y1,y2),x2)
    else:
        carve_v(g,min(y1,y2),max(y1,y2),x1)
        carve_h(g,min(x1,x2),max(x1,x2),y2)

def safe_zone_tiles(cx, cy, radius):
    """Chebyshev-radius tile buffer used to keep spawn/exit hazard-free."""
    return {(cx + dx, cy + dy)
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)}

def _room_floor_tiles(room, grid):
    return [(x, y) for y in range(room.y, room.y + room.h)
            for x in range(room.x, room.x + room.w)
            if 0 <= x < COLS and 0 <= y < ROWS and grid[y][x] == 0]

def _room_deep_tiles(room, grid):
    return [(x, y) for y in range(room.y + 2, room.y + room.h - 2)
            for x in range(room.x + 2, room.x + room.w - 2)
            if 0 <= x < COLS and 0 <= y < ROWS and grid[y][x] == 0]

def _room_door_tiles(room, grid):
    doors = []
    for x, y in _room_floor_tiles(room, grid):
        edge = (x == room.x or x == room.x + room.w - 1 or
                y == room.y or y == room.y + room.h - 1)
        if not edge:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            outside = not (room.x <= nx < room.x + room.w and
                           room.y <= ny < room.y + room.h)
            if outside and 0 <= nx < COLS and 0 <= ny < ROWS and grid[ny][nx] == 0:
                doors.append((x, y))
                break
    return doors or [(room.cx, room.cy)]

def _room_connected_with_blocks(room, grid, blocked):
    floors = set(_room_floor_tiles(room, grid)) - set(blocked)
    if not floors:
        return False
    targets = [t for t in _room_door_tiles(room, grid) if t in floors]
    if not targets:
        return False
    start = targets[0]
    seen = {start}
    stack = [start]
    while stack:
        x, y = stack.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nt = (x + dx, y + dy)
            if nt in floors and nt not in seen:
                seen.add(nt)
                stack.append(nt)
    if any(t not in seen for t in targets):
        return False
    return len(seen) >= max(6, len(floors) // 3)

def _dynamic_tiles_in_room(dt, room):
    tmp = {}
    _map_dtrap_tiles(dt, tmp)
    return {tile for tile in tmp
            if room.x <= tile[0] < room.x + room.w
            and room.y <= tile[1] < room.y + room.h}

def _room_hazard_layout_passable(room, grid, straps, dtraps,
                                 ticks=180, stride=5):
    """Conservative room validator for random trap layouts.

    Static traps may not disconnect the room. Dynamic traps may create timing
    puzzles, but they must leave frequent passable windows and must not occupy
    most of a small room at once.
    """
    floors = set(_room_floor_tiles(room, grid))
    if len(floors) < 8:
        return not straps and not dtraps

    static_blocked = {(t.tx, t.ty) for t in straps}
    if not _room_connected_with_blocks(room, grid, static_blocked):
        return False
    if not dtraps:
        return True

    clones = [_clone_dtrap(dt) for dt in dtraps]
    stub = _SimPlayer(room.cx, room.cy)
    safe_windows = 0
    gap = 0
    # 12 samples * 5 ticks = about one second
    max_gap = 12
    max_live_block = max(4, int(len(floors) * 0.45))

    for tick in range(ticks + 1):
        if tick > 0:
            for dt in clones:
                _sim_update_dtrap(dt, stub)
        if tick % stride != 0:
            continue
        live_blocked = set()
        for dt in clones:
            live_blocked |= _dynamic_tiles_in_room(dt, room)
        if len(live_blocked) > max_live_block:
            return False
        if _room_connected_with_blocks(room, grid, static_blocked | live_blocked):
            safe_windows += 1
            gap = 0
        else:
            gap += 1
            if gap > max_gap:
                return False
    return safe_windows >= 3

def _spaced_static_traps(room, grid, safe_tiles, n, kinds):
    candidates = [t for t in _room_deep_tiles(room, grid) if t not in safe_tiles]
    avail = candidates[:]
    random.shuffle(avail)
    chosen = []
    for tx, ty in avail:
        if len(chosen) >= n:
            break
        if all(abs(tx - cx) > 3 or abs(ty - cy) > 3 for cx, cy in chosen):
            chosen.append((tx, ty))
    return [StaticTrap(tx, ty, random.choice(kinds), room.rtype)
            for tx, ty in chosen]

def populate_room_hazards(room, grid, safe_tiles):
    """Place a varied hazard mix in every room that can hold one.

    Priority is on DYNAMIC traps (spinners, sweepers, crushers, etc.) for
    variety and challenge — every room that fits one gets at least one dynamic
    trap, and larger rooms get two, alongside a smaller number of static traps.
    Only the room-wide sweeps (lava_tide / ice_sweeper) need real width; the
    rest fit comfortably in modest rooms, so dynamic traps are gated per-KIND by
    the space they need rather than excluded wholesale from small rooms.
    """
    room.straps = []
    room.dtraps = []
    deep = [t for t in _room_deep_tiles(room, grid) if t not in safe_tiles]
    if not deep:
        # no interior tile at all — enemies only
        return

    sp = RTYPES[room.rtype]["straps"]
    dp = RTYPES[room.rtype]["dtraps"]

    # dynamic kinds that need a wide/large room to be fair; everything else can
    # go in a modest room.
    WIDE_ONLY = {"lava_tide", "ice_sweeper"}
    room_is_big = (room.w >= 9 and room.h >= 7 and len(deep) >= 16)
    # any spinner needs a little space
    room_fits_dyn = (len(deep) >= 4)

    # fewer static traps so dynamic hazards stand out and rooms stay passable.
    base_static = min(2, max(1, len(deep) // 14))
    # target dynamic count: 2 in big rooms, 1 in any room that fits a spinner.
    target_dyn = 2 if room_is_big else (1 if room_fits_dyn else 0)

    def _eligible_dyn_kinds():
        kinds = [k for k in dp if (k not in WIDE_ONLY) or room_is_big]
        random.shuffle(kinds)
        return kinds

    def _try_place(n_static, n_dyn):
        """Attempt a layout with n_static static + n_dyn dynamic traps. Returns
        (straps, dtraps) on success or None."""
        for _ in range(25):
            straps = _spaced_static_traps(room, grid, safe_tiles, n_static, sp)
            if n_static > 0 and not straps:
                continue
            if not _room_hazard_layout_passable(room, grid, straps, []):
                continue
            if n_dyn == 0:
                return straps, []
            placed = []
            dtries = deep[:]
            random.shuffle(dtries)
            kinds = _eligible_dyn_kinds()
            for kind in kinds:
                if len(placed) >= n_dyn:
                    break
                for ox, oy in dtries[:14]:
                    # keep dynamic traps spaced apart from each other
                    if any(abs(ox - p.ox) <= 2 and abs(oy - p.oy) <= 2
                           for p in placed):
                        continue
                    dt = DynamicTrap(ox, oy, kind, room, grid)
                    if _room_hazard_layout_passable(room, grid, straps,
                                                    placed + [dt]):
                        placed.append(dt)
                        break
            if placed:
                return straps, placed
        return None

    # try richest layout first, then degrade gracefully.
    for ns, nd in [(base_static, target_dyn),
                   (base_static, max(1, target_dyn - 1)),
                   (1, 1), (base_static, 0), (1, 0)]:
        if nd > 0 and not room_fits_dyn:
            continue
        res = _try_place(ns, nd)
        if res is not None:
            room.straps, room.dtraps = res
            return

    # last resort: a single static trap on any deep tile that stays connected.
    singles = deep[:]
    random.shuffle(singles)
    for tx, ty in singles:
        cand = [StaticTrap(tx, ty, random.choice(sp), room.rtype)]
        if _room_hazard_layout_passable(room, grid, cand, []):
            room.straps = cand
            return

def generate_world():
    grid = [[1]*COLS for _ in range(ROWS)]
    rooms=[]; rtypes=list(RTYPES.keys()); att=0
    while len(rooms)<20 and att<3000:
        att+=1
        rw=random.randint(6,13); rh=random.randint(5,10)
        rx=random.randint(1,COLS-rw-1); ry=random.randint(1,ROWS-rh-1)
        c=Room(rx,ry,rw,rh,random.choice(rtypes))
        if any(c.overlaps(r) for r in rooms): continue
        rooms.append(c)
        for ty in range(ry,ry+rh):
            for tx in range(rx,rx+rw): grid[ty][tx]=0
    # mst
    conn={0}; unconn=set(range(1,len(rooms)))
    while unconn:
        bd=1e9; bf=bt=-1
        for ci in conn:
            for ui in unconn:
                d=abs(rooms[ci].cx-rooms[ui].cx)+abs(rooms[ci].cy-rooms[ui].cy)
                if d<bd: bd=d; bf=ci; bt=ui
        if bt==-1: break
        carve_corridor(grid,rooms[bf],rooms[bt])
        conn.add(bt); unconn.remove(bt)
    # start/end
    s_room,e_room=rooms[0],rooms[-1]; bd2=0
    for i,r1 in enumerate(rooms):
        for r2 in rooms[i+1:]:
            dd=abs(r1.cx-r2.cx)+abs(r1.cy-r2.cy)
            if dd>bd2: bd2=dd; s_room,e_room=r1,r2
    # safe zones
    safe_tiles=set()
    safe_tiles |= safe_zone_tiles(s_room.cx, s_room.cy, START_SAFE_RADIUS)
    safe_tiles |= safe_zone_tiles(e_room.cx, e_room.cy, EXIT_SAFE_RADIUS)
    floors=[(cx2,ry2) for ry2 in range(ROWS) for cx2 in range(COLS) if grid[ry2][cx2]==0]
    # traps — only place in room interior, at least 2 tiles from room edge
    for room in rooms:
        if room is s_room or room is e_room:
            room.straps = []
            room.dtraps = []
            continue
        populate_room_hazards(room, grid, safe_tiles)
        continue
    # spawn roaming enemies — one set per room, stored on room object
    for room in rooms:
        room.enemies = []
        if room is s_room:
            continue
        for _ in range(ENEMY_COUNT):
            room.enemies.append(RoamingEnemy(room, grid))
    return grid, rooms, floors, [e for r in rooms for e in r.enemies]

def _spawn_enemies_for_room(room, grid):
    """Spawn ENEMY_COUNT roaming enemies in a room (called on re-entry too)."""
    enemies = []
    for _ in range(ENEMY_COUNT):
        enemies.append(RoamingEnemy(room, grid))
    return enemies


# =============================================================================
# static trap — floor hazards, each drawn to match their room
# =============================================================================
class StaticTrap:
    def __init__(self, tx, ty, kind, rtype):
        self.tx=tx; self.ty=ty; self.kind=kind; self.rtype=rtype
        self.d=TDEFS[kind]
        self.t=random.randint(0,300); self.ph=random.random()*math.pi*2
        self.hit_cd=0
        # private rng for the one live draw a static trap can make — a teleport
        # plate choosing a destination on contact.  seeded from the construction
        # stream so it's identical across agents; using its own stream keeps the
        # (player-triggered) teleport from perturbing other hazards' sequences.
        self.rng = random.Random(random.getrandbits(32))
        # per-kind state
        if kind=="pressure_plate":
            self.triggered=False; self.trigger_t=0
        elif kind=="cracked_ice":
            # 0=whole, 1=fully cracked
            self.crack=0.0
        elif kind=="bear_trap":
            self.open=True; self.snap_t=0

    def update(self):
        self.t+=1
        if self.hit_cd>0: self.hit_cd-=1
        if self.kind=="pressure_plate":
            if self.triggered:
                self.trigger_t+=1
                if self.trigger_t>40: self.triggered=False; self.trigger_t=0
        elif self.kind=="bear_trap":
            if not self.open:
                self.snap_t+=1
                if self.snap_t>80: self.open=True; self.snap_t=0

    def check_hit(self, player, floors):
        if self.hit_cd>0: return
        if player.dead: return
        dist=math.hypot(self.tx-player.x, self.ty-player.y)
        if dist < 0.55:
            # if player is invincible, don't consume the cooldown — the trap
            # would otherwise silently "waste" its trigger and look like a
            # phantom miss on screen.  without inv, this branch always fires.
            if player.inv > 0:
                return
            self.hit_cd=self.d["cd"]
            k=self.kind
            if k=="pressure_plate": self.triggered=True; self.trigger_t=0
            elif k=="bear_trap": self.open=False; self.snap_t=0
            elif k=="cracked_ice": self.crack=1.0
            if self.d["eff"]=="teleport":
                dest=self.rng.choice(floors)
                player.tx,player.ty=dest
                player.x,player.y=float(dest[0]),float(dest[1])
                player.push_msg("REALITY CRACK!",self.d["col"])
            else:
                player.take_damage(self.d["dmg"],self.d["eff"],self.d["lbl"],self.d["col"],kind=self.kind)

    # ── short codes for hazard labels (formal style) ─────────────────────────
    _CODE = {
        "pressure_plate":"PLT", "wall_dart":"DRT", "lava_geyser":"GYS",
        "magma_crack":"CRK", "frost_mine":"MIN", "cracked_ice":"ICE",
        "bear_trap":"TRP", "poison_mushroom":"PSN", "floor_glyph":"GLY",
        "sand_pit":"PIT", "void_eye":"EYE", "reality_crack":"RFT",
    }

    def _draw_formal(self, surf, cx, cy, ts):
        """Flat single-tile hazard marker: category-coloured outlined square
        with a short type code.  Fill intensity rises when armed/triggered."""
        col = hazard_color(self.kind)
        armed = (getattr(self, "triggered", False) or
                 getattr(self, "active", False) or
                 not getattr(self, "open", True))
        half = ts // 2 - 2
        rect = pygame.Rect(cx - half, cy - half, half * 2, half * 2)
        if armed:
            pygame.draw.rect(surf, col, rect)
            txtcol = (255, 255, 255)
        else:
            pygame.draw.rect(surf, lerpc(FML["floor"], col, 0.20), rect)
            txtcol = col
        pygame.draw.rect(surf, col, rect, 1)
        f = _formal_font()
        t = f.render(self._CODE.get(self.kind, "HZ"), True, txtcol)
        surf.blit(t, (cx - t.get_width() // 2, cy - t.get_height() // 2))

    def draw(self, surf, cam_x, cam_y, ts):
        cx=int((self.tx-cam_x)*ts)
        cy=int((self.ty-cam_y)*ts)
        if not (-ts*2<cx<W+ts*2 and -ts*2<cy<H+ts*2): return
        if FORMAL_STYLE:
            self._draw_formal(surf, cx, cy, ts)
            return
        col=self.d["col"]
        pulse=(0.90+0.10*math.sin(self.t*0.10+self.ph)) if REDUCE_EFFECTS else (0.5+0.5*math.sin(self.t*0.10+self.ph))
        pc=tuple(min(255,int(c*pulse)) for c in col)
        glow_pulse = 0.0 if REDUCE_EFFECTS else pulse
        bright=tuple(min(255,int(c*1.35)) for c in col)
        k=self.kind
        r=max(4,int(ts*0.44))
        half=ts//2

        # dark floor plate
        plate=asurf(ts-2,ts-2)
        plate.fill((*tuple(c//3 for c in col),140))
        surf.blit(plate,(cx-half+1,cy-half+1))

        if k=="pressure_plate":
            # stone plate with seams, glows red when triggered
            triggered=self.triggered
            base=(80,65,70) if not triggered else (200,40,40)
            pygame.draw.rect(surf,base,pygame.Rect(cx-r,cy-r,r*2,r*2))
            # stone seam lines
            pygame.draw.line(surf,lerpc(base,(0,0,0),0.4),(cx-r,cy),(cx+r,cy),1)
            pygame.draw.line(surf,lerpc(base,(0,0,0),0.4),(cx,cy-r),(cx,cy+r),1)
            # edge bevel
            pygame.draw.rect(surf,lerpc(base,WHITE,0.25),pygame.Rect(cx-r,cy-r,r*2,r*2),1)
            if triggered:
                # glow aura
                ga=int(glow_pulse*140)
                gs=asurf(r*3,r*3); pygame.draw.circle(gs,(220,40,40,ga),(r+r//2,r+r//2),int(r*1.4))
                surf.blit(gs,(cx-r-r//2,cy-r-r//2))

        elif k=="wall_dart":
            # floor trigger plate + dart flying across
            # base plate (stone trigger)
            pygame.draw.rect(surf,(55,48,38),pygame.Rect(cx-r+2,cy-r+2,r*2-4,r*2-4))
            pygame.draw.rect(surf,(80,70,55),pygame.Rect(cx-r+2,cy-r+2,r*2-4,r*2-4),1)
            # crosshair target on plate
            pygame.draw.line(surf,(120,100,70),(cx-r//2,cy),(cx+r//2,cy),1)
            pygame.draw.line(surf,(120,100,70),(cx,cy-r//2),(cx,cy+r//2),1)
            # flying dart (moves outward with pulse)
            for ang_off in [0, math.pi/2, math.pi, 3*math.pi/2]:
                dart_d=int(pulse*(r+6))
                dx2=int(math.cos(self.ph+ang_off)*dart_d)
                dy2=int(math.sin(self.ph+ang_off)*dart_d)
                tip=(cx+dx2,cy+dy2)
                perp=(cx+int(math.cos(self.ph+ang_off+math.pi/2)*3),
                      cy+int(math.sin(self.ph+ang_off+math.pi/2)*3))
                perp2=(cx+int(math.cos(self.ph+ang_off-math.pi/2)*3),
                       cy+int(math.sin(self.ph+ang_off-math.pi/2)*3))
                try: pygame.draw.polygon(surf,(180,155,80),[tip,perp,perp2])
                except: pass
            if glow_pulse>0.75:
                gs=asurf(r*3,r*3); pygame.draw.circle(gs,(*col,int((pulse-0.75)/0.25*100)),(r+r//2,r+r//2),r+4,2)
                surf.blit(gs,(cx-r-r//2,cy-r-r//2))

        elif k=="lava_geyser":
            # cracked floor vent with eruption
            pygame.draw.circle(surf,(80,20,5),(cx,cy),r)
            pygame.draw.circle(surf,(140,40,8),(cx,cy),r-3)
            # crack lines
            for i in range(4):
                a=self.ph+i*math.pi/2
                x1=cx+int(math.cos(a)*3); y1=cy+int(math.sin(a)*3)
                x2=cx+int(math.cos(a)*(r-1)); y2=cy+int(math.sin(a)*(r-1))
                pygame.draw.line(surf,(255,80,10),(x1,y1),(x2,y2),2)
            # eruption jets
            if glow_pulse>0.6:
                jet_h=int((pulse-0.6)/0.4*r*1.8)
                for i in range(3):
                    jx=cx+random.randint(-3,3)
                    for seg in range(jet_h//3):
                        jy=cy-seg*3
                        jr=max(1,4-seg//2)
                        alpha=int(200*(1-seg*3/jet_h))
                        gc=asurf(jr*2+2,jr*2+2)
                        pygame.draw.circle(gc,(255,random.randint(100,180),10,alpha),(jr+1,jr+1),jr)
                        surf.blit(gc,(jx-jr-1,jy-jr-1))

        elif k=="magma_crack":
            # glowing floor crack
            pygame.draw.ellipse(surf,(60,18,5),pygame.Rect(cx-r,cy-r//2,r*2,r))
            # crack path
            pts=[(cx-r+i*r//3,cy+int(math.sin(i*1.8+self.ph)*3)) for i in range(7)]
            if len(pts)>=2:
                pygame.draw.lines(surf,(255,100,10),False,pts,3)
                pygame.draw.lines(surf,(255,200,50),False,pts,1)
            # glow
            for gw in (r,r-3):
                gc=asurf(gw*2+2,gw//2+2)
                pygame.draw.ellipse(gc,(*col,int(pulse*80)),(0,0,gw*2+2,gw//2+2))
                surf.blit(gc,(cx-gw-1,cy-gw//4-1))

        elif k=="ice_vent":
            # cold floor vent blasting ice crystals upward
            pygame.draw.circle(surf,(30,55,90),(cx,cy),r)
            pygame.draw.circle(surf,(50,90,140),(cx,cy),r-3)
            # vent holes
            for i in range(4):
                a=i*math.pi/2+self.ph
                vx=cx+int(math.cos(a)*(r-4)); vy=cy+int(math.sin(a)*(r-4))
                pygame.draw.circle(surf,(20,40,70),(vx,vy),2)
            # crystal jets
            if glow_pulse>0.55:
                for i in range(4):
                    jlen=int((pulse-0.55)/0.45*r*1.5)
                    a=self.t*0.05+i*math.pi/2
                    for seg in range(0,jlen,3):
                        jx=cx+int(math.cos(a)*seg); jy=cy+int(math.sin(a)*seg)
                        jc=asurf(5,5); pygame.draw.polygon(jc,(200,240,255,200),[(2,0),(4,4),(0,4)])
                        surf.blit(jc,(jx-2,jy-2))

        elif k=="cracked_ice":
            # ice panel that cracks when stepped on
            crack=self.crack
            base=lerpc((60,120,180),(200,230,255),0.5+0.5*math.sin(self.t*0.04))
            pygame.draw.rect(surf,base,pygame.Rect(cx-r,cy-r,r*2,r*2))
            # highlight facets
            pygame.draw.line(surf,(200,240,255),(cx-r,cy-r),(cx+r,cy-r),1)
            pygame.draw.line(surf,(200,240,255),(cx-r,cy-r),(cx-r,cy+r),1)
            if crack>0:
                # crack lines radiating out
                for i in range(5):
                    a=self.ph+i*math.pi*2/5
                    ex=cx+int(math.cos(a)*r*crack); ey=cy+int(math.sin(a)*r*crack)
                    pygame.draw.line(surf,(20,40,80),(cx,cy),(ex,ey),max(1,int(crack*2)))
                # shatter glow
                gc=asurf(r*2+2,r*2+2); pygame.draw.rect(gc,(100,180,255,int(crack*80)),(0,0,r*2+2,r*2+2))
                surf.blit(gc,(cx-r-1,cy-r-1))

        elif k=="bear_trap":
            # metal bear trap jaws
            jaw_col=(120,105,85)
            is_open=self.open
            # base plate
            pygame.draw.circle(surf,(50,42,32),(cx,cy),r-2)
            # spring coil
            for i in range(3):
                a=i*math.pi*2/3
                sx2=cx+int(math.cos(a)*5); sy2=cy+int(math.sin(a)*5)
                pygame.draw.circle(surf,(80,70,55),(sx2,sy2),2)
            if is_open:
                # open jaw — two semicircles of teeth
                for side,sign in [("left",-1),("right",1)]:
                    for tooth in range(4):
                        pygame.draw.polygon(surf,jaw_col,[
                            (cx+sign*4,cy),(cx+sign*4+sign*8,cy-6),(cx+sign*4+sign*8,cy+6)])
                # trigger pan
                pygame.draw.circle(surf,(160,140,100),(cx,cy),4)
                pygame.draw.circle(surf,(200,180,130),(cx,cy),2)
            else:
                # snapped shut — solid bar across
                pygame.draw.rect(surf,jaw_col,pygame.Rect(cx-r,cy-3,r*2,6))
                pygame.draw.rect(surf,(200,180,130),pygame.Rect(cx-r,cy-3,r*2,6),1)
                # shake effect
                shake=int((1-self.snap_t/80)*3)
                pygame.draw.rect(surf,(255,60,40),pygame.Rect(cx-r-shake,cy-3,r*2+shake*2,6),1)

        elif k=="poison_mushroom":
            # spotted mushroom cap
            stem_col=(180,155,110)
            cap_col=(120,190,50)
            # stem
            pygame.draw.rect(surf,stem_col,pygame.Rect(cx-4,cy,8,r-2))
            # cap
            pygame.draw.ellipse(surf,cap_col,pygame.Rect(cx-r,cy-r//2,r*2,r))
            # spots
            for i in range(4):
                a=self.ph+i*math.pi/2
                sx2=cx+int(math.cos(a)*r*0.45); sy2=cy-r//4+int(math.sin(a)*r*0.25)
                pygame.draw.circle(surf,WHITE,(sx2,sy2),3)
            # spore puff when pulsing
            if glow_pulse>0.65:
                for i in range(3):
                    a=self.ph+i*2.1+self.t*0.03
                    sr=int(2+3*(pulse-0.65)/0.35)
                    sx2=cx+int(math.cos(a)*(r+sr)); sy2=cy+int(math.sin(a)*(r+sr))
                    gc=asurf(sr*2+2,sr*2+2)
                    pygame.draw.circle(gc,(140,220,60,int(160*(pulse-0.65)/0.35)),(sr+1,sr+1),sr)
                    surf.blit(gc,(sx2-sr-1,sy2-sr-1))

        elif k=="floor_glyph":
            # ancient arcane rune carved into floor
            pygame.draw.circle(surf,(55,42,28),(cx,cy),r)
            # outer ring
            pygame.draw.circle(surf,col,(cx,cy),r-1,1)
            # inner rotating triangle
            for i in range(3):
                a=self.t*0.03+i*math.pi*2/3
                x1=cx+int(math.cos(a)*(r-3)); y1=cy+int(math.sin(a)*(r-3))
                a2=self.t*0.03+(i+1)*math.pi*2/3
                x2=cx+int(math.cos(a2)*(r-3)); y2=cy+int(math.sin(a2)*(r-3))
                pygame.draw.line(surf,pc,(x1,y1),(x2,y2),2)
            # centre dot
            pygame.draw.circle(surf,bright,(cx,cy),int(3*pulse))
            # glyph runes (small marks on ring)
            for i in range(6):
                a=self.ph+i*math.pi/3
                rx2=cx+int(math.cos(a)*(r-2)); ry2=cy+int(math.sin(a)*(r-2))
                pygame.draw.circle(surf,col,(rx2,ry2),1)

        elif k=="sand_pit":
            # swirling sand vortex
            pygame.draw.ellipse(surf,(160,130,70),pygame.Rect(cx-r,cy-r//2,r*2,r))
            for arm in range(3):
                for seg in range(5):
                    a=self.t*0.05+arm*math.pi*2/3+seg*0.3
                    sr=int((seg/5)*r*0.8)
                    sx2=cx+int(math.cos(a)*sr); sy2=cy+int(math.sin(a)*sr//2)
                    pygame.draw.circle(surf,(200,165,90),(sx2,sy2),max(1,3-seg//2))

        elif k=="void_eye":
            # a watching eye that tracks the player direction
            # eyeball
            pygame.draw.circle(surf,(8,4,18),(cx,cy),r)
            pygame.draw.circle(surf,(25,12,45),(cx,cy),r-1)
            # iris
            pygame.draw.circle(surf,col,(cx,cy),int(r*0.55))
            pygame.draw.circle(surf,lerpc(col,(0,0,0),0.5),(cx,cy),int(r*0.55)-1)
            # pupil — pulsing
            pygame.draw.circle(surf,(0,0,0),(cx,cy),int(r*0.28))
            # sclera veins
            for i in range(4):
                a=self.ph+i*math.pi/2
                vx=cx+int(math.cos(a)*r*0.65); vy=cy+int(math.sin(a)*r*0.65)
                pygame.draw.line(surf,(180,60,255,150),(cx,cy),(vx,vy),1)
            # glow when pulsing
            if glow_pulse>0.7:
                gc=asurf(r*3,r*3)
                pygame.draw.circle(gc,(*col,int((pulse-0.7)/0.3*100)),(r+r//2,r+r//2),r+4)
                surf.blit(gc,(cx-r-r//2,cy-r-r//2))

        elif k=="reality_crack":
            # a jagged rift in space
            pygame.draw.ellipse(surf,(15,5,25),pygame.Rect(cx-r,cy-r//2,r*2,r))
            # crack zigzag
            pts=[]
            for i in range(8):
                t2=i/7
                px2=cx-r+int(t2*r*2)
                py2=cy+int(math.sin(self.ph+i*1.3)*(r//3))
                pts.append((px2,py2))
            if len(pts)>=2:
                pygame.draw.lines(surf,(80,20,120),False,pts,3)
                pygame.draw.lines(surf,pc,False,pts,1)
            # stars/sparkles along crack
            for pt in pts[::2]:
                gc=asurf(6,6); pygame.draw.circle(gc,(*bright,int(160*pulse)),(3,3),2)
                surf.blit(gc,(pt[0]-3,pt[1]-3))

        else:
            # generic fallback
            gc=asurf(r*2+2,r*2+2)
            pygame.draw.circle(gc,(*pc,180),(r+1,r+1),r)
            surf.blit(gc,(cx-r-1,cy-r-1))


# =============================================================================
# dynamic trap — room-specific moving hazards
# =============================================================================
class DynamicTrap:
    def __init__(self, tx, ty, kind, room, grid):
        self.ox=float(tx); self.oy=float(ty)
        self.kind=kind; self.room=room; self.grid=grid
        self.d=TDEFS[kind]
        self.t=random.randint(0,300); self.ph=random.random()*math.pi*2
        self.hit_cd={}
        self.px=self.ox; self.py=self.oy
        self.trail=[]
        self._init()
        # private rng for all live re-arm draws inside update().  seeded from the
        # construction stream (the seed-pinned global rng during world-gen, or
        # the per-visit relocation rng), which is identical across agents — so
        # this hazard's re-arm sequence is identical across agents.  because the
        # hazard reads from its own stream, *when* it happens to re-arm (which
        # can depend on the player's position, e.g. a homing mummy_wrap) no
        # longer shifts any other hazard's draws.
        self.rng = random.Random(random.getrandbits(32))

    def _init(self):
        k=self.kind; rm=self.room
        if k=="pendulum_axe":
            # pivot on ceiling of room, swings across room width
            self.pivot_x=float(rm.cx)
            # top edge of room interior
            self.pivot_y=float(rm.y+1)
            self.arm_len=min(float(rm.h-3), random.uniform(2.2,3.5))
            # pointing straight down
            self.pivot_base=math.pi/2
            # start pointing down
            self.angle=math.pi/2
            self.speed=random.choice([-1,1])*random.uniform(0.025,0.05)
            self.max_angle=random.uniform(0.5,0.9)
        elif k=="ceiling_crusher":
            # drops from ceiling (visually) then rises — stays on floor tile
            self.state="up"; self.timer=random.randint(60,120)
            # resting position (on the floor tile)
            self.drop_y=self.oy
            # 0=down on floor, 1=raised (shown faded above)
            self.raised_frac=0.0
            self.crush_w=random.uniform(1.2,2.0)
            self.py=self.drop_y
        elif k=="lava_tide":
            # a wave of lava that sweeps across the room
            self.tide_x=float(rm.x+1)
            self.dir=1
            self.spd=random.uniform(0.04,0.08)
            self.min_x=float(rm.x+1); self.max_x=float(rm.x+rm.w-2)
            self.tide_w=random.uniform(1.5,2.5)
        elif k=="rolling_boulder":
            # rolls back and forth along the room
            ang=random.choice([0,math.pi/2,math.pi,3*math.pi/2])
            self.vx=math.cos(ang)*0.07; self.vy=math.sin(ang)*0.07
            self.radius=0.6
        elif k=="ice_sweeper":
            # ice beam that sweeps across the room floor
            self.sweep_x=float(rm.x+1)
            self.spd=random.choice([-1,1])*random.uniform(0.05,0.09)
            self.min_x=float(rm.x+1); self.max_x=float(rm.x+rm.w-2)
            # sweeps horizontally at room centre row
            self.height=float(rm.cy)
        elif k=="frozen_spike_row":
            # a row of ice spikes that erupts across the room then retracts
            self.state="wait"; self.timer=random.randint(40,80)
            self.row_y=float(rm.cy+random.randint(-rm.h//4,rm.h//4))
            self.spikes=[(rm.x+1+i*2, self.row_y) for i in range((rm.w-2)//2)]
            self.rise=0.0
        elif k=="thorn_wall":
            # wall of thorns that grows across room then retracts
            self.state="wait"; self.timer=60
            self.wall_x=float(rm.x+1)
            self.dir=1; self.wall_w=0.0
            self.max_w=float(rm.w-2)
        elif k=="spore_burst":
            # periodic spore explosion from centre.  fixed period + slower
            # expansion so the ring is fully predictable and the agent has time
            # to clear the blast disc between firings (deterministic hazard).
            self.burst_r=0.0; self.max_r=min(rm.w,rm.h)*0.4
            self.state="wait"; self.timer=SPORE_FIRE_PERIOD
        elif k=="mummy_wrap":
            # bandage projectile that seeks player
            self.px=self.ox; self.py=self.oy
            self.vx=0.; self.vy=0.
            self.active=False; self.timer=random.randint(60,100)
        elif k=="sarcophagus":
            # lid opens then fires a spread of death projectiles
            self.state="closed"; self.timer=random.randint(80,140)
            # list of (px,py,vx,vy,life)
            self.shots=[]
        elif k=="gravity_pull":
            # pulls player toward centre when active
            self.active=False; self.timer=random.randint(50,80)
            self.pull_r=random.uniform(2.5,4.0)
            self.ring_r=0.0
        elif k=="mirror_clone":
            # a ghostly copy that mirrors player movement toward them
            self.px=self.ox; self.py=self.oy
            self.trail=[]
        elif k=="fire_bar":
            # spinning fire arms — mario style, anchored to centre of room
            self.angle=self.ph
            self.arm_len=random.uniform(1.8, min(3.2, (rm.w-2)*0.45))
            self.speed=random.choice([-1,1])*random.uniform(0.028,0.055)
            self.n_arms=random.choice([1,2])
        elif k=="ice_beam":
            # rotating dual ice beams — void/ice variant of fire_bar
            self.angle=self.ph
            self.beam_len=random.uniform(2.0, min(3.5, (rm.w-2)*0.45))
            self.speed=random.choice([-1,1])*random.uniform(0.018,0.038)

    def _in_floor(self, x, y):
        tx=int(x); ty=int(y)
        return 0<=tx<COLS and 0<=ty<ROWS and self.grid[ty][tx]==0

    def update(self, player):
        self.t+=1
        if self.hit_cd:
            for pid in list(self.hit_cd):
                self.hit_cd[pid]-=1
                if self.hit_cd[pid]<=0: del self.hit_cd[pid]
        k=self.kind

        if k=="pendulum_axe":
            self.angle+=self.speed
            if abs(self.angle-self.pivot_base)>self.max_angle:
                self.speed*=-1
            # blade tip position in world coords
            self.px=self.pivot_x+math.cos(self.angle)*self.arm_len
            self.py=self.pivot_y+math.sin(self.angle)*self.arm_len

        elif k=="ceiling_crusher":
            self.timer-=1
            if self.state=="up" and self.timer<=0:
                self.state="dropping"; self.timer=14
            elif self.state=="dropping":
                # fades from high to low
                self.raised_frac=self.timer/14
                self.timer-=1
                if self.timer<=0: self.state="down"; self.timer=30
            elif self.state=="down" and self.timer<=0:
                self.state="rising"; self.timer=22
            elif self.state=="rising":
                self.raised_frac=1.0-self.timer/22
                self.timer-=1
                if self.timer<=0: self.state="up"; self.timer=self.rng.randint(60,120); self.raised_frac=1.0

        elif k=="lava_tide":
            self.tide_x+=self.spd*self.dir
            if self.tide_x>self.max_x or self.tide_x<self.min_x:
                self.dir*=-1

        elif k=="rolling_boulder":
            nx=self.px+self.vx; ny=self.py+self.vy
            if self._in_floor(nx,ny): self.px=nx; self.py=ny
            else:
                if not self._in_floor(self.px+self.vx,self.py): self.vx*=-1
                if not self._in_floor(self.px,self.py+self.vy): self.vy*=-1
                self.px+=self.vx; self.py+=self.vy
            self.trail.append((self.px,self.py))
            if len(self.trail)>12: self.trail.pop(0)

        elif k=="ice_sweeper":
            self.sweep_x+=self.spd
            if self.sweep_x<self.min_x or self.sweep_x>self.max_x: self.spd*=-1

        elif k=="frozen_spike_row":
            if self.state=="wait":
                self.timer-=1
                if self.timer<=0: self.state="rising"; self.rise=0.0
            elif self.state=="rising":
                self.rise=min(1.0,self.rise+0.06)
                if self.rise>=1.0: self.state="hold"; self.timer=30
            elif self.state=="hold":
                self.timer-=1
                if self.timer<=0: self.state="falling"
            elif self.state=="falling":
                self.rise=max(0.0,self.rise-0.08)
                if self.rise<=0.0: self.state="wait"; self.timer=self.rng.randint(40,80)

        elif k=="thorn_wall":
            if self.state=="wait":
                self.timer-=1
                if self.timer<=0: self.state="growing"
            elif self.state=="growing":
                self.wall_w=min(self.max_w,self.wall_w+0.12)
                if self.wall_w>=self.max_w: self.state="hold"; self.timer=40
            elif self.state=="hold":
                self.timer-=1
                if self.timer<=0: self.state="shrinking"
            elif self.state=="shrinking":
                self.wall_w=max(0,self.wall_w-0.15)
                if self.wall_w<=0: self.state="wait"; self.timer=60

        elif k=="spore_burst":
            if self.state=="wait":
                self.timer-=1
                if self.timer<=0: self.state="expanding"; self.burst_r=0.
            elif self.state=="expanding":
                self.burst_r+=SPORE_EXPAND_SPEED
                if self.burst_r>=self.max_r: self.state="wait"; self.timer=SPORE_FIRE_PERIOD

        elif k=="mummy_wrap":
            if not self.active:
                self.timer-=1
                if self.timer<=0:
                    self.active=True
                    dx=player.x-self.ox; dy=player.y-self.oy
                    d=math.hypot(dx,dy)
                    if d>0.1: self.vx=dx/d*0.10; self.vy=dy/d*0.10
                    else: self.vx=0.10; self.vy=0
                    self.px=self.ox; self.py=self.oy
            if self.active:
                nx=self.px+self.vx; ny=self.py+self.vy
                if self._in_floor(nx,ny): self.px=nx; self.py=ny
                else:
                    if not self._in_floor(self.px+self.vx,self.py): self.vx*=-1
                    if not self._in_floor(self.px,self.py+self.vy): self.vy*=-1
                    self.px+=self.vx; self.py+=self.vy
                self.trail.append((self.px,self.py))
                if len(self.trail)>20: self.trail.pop(0)
                dist=math.hypot(self.px-self.ox,self.py-self.oy)
                if dist>9 or not self._in_floor(int(self.px),int(self.py)):
                    self.active=False; self.timer=self.rng.randint(50,90); self.trail.clear()

        elif k=="sarcophagus":
            self.timer-=1
            if self.state=="closed" and self.timer<=0:
                self.state="opening"; self.timer=30
            elif self.state=="opening" and self.timer<=0:
                self.state="firing"
                for i in range(5):
                    ang=self.ph+i*math.pi*2/5
                    self.shots.append([self.ox,self.oy,math.cos(ang)*0.08,math.sin(ang)*0.08,80])
            elif self.state=="firing":
                for shot in self.shots:
                    nx=shot[0]+shot[2]; ny=shot[1]+shot[3]
                    if self._in_floor(nx,ny): shot[0]=nx; shot[1]=ny
                    else: shot[2]*=-1; shot[3]*=-1
                    shot[4]-=1
                self.shots=[s for s in self.shots if s[4]>0]
                if not self.shots: self.state="closed"; self.timer=self.rng.randint(80,140)

        elif k=="gravity_pull":
            self.timer-=1
            if not self.active and self.timer<=0:
                self.active=True; self.ring_r=0.; self.timer=100
            if self.active:
                self.ring_r=min(self.pull_r,self.ring_r+0.08)
                # pull player
                dx=self.ox-player.x; dy=self.oy-player.y
                d=math.hypot(dx,dy)
                if d<self.pull_r and d>0.2:
                    strength=(1-d/self.pull_r)*0.025
                    player.x+=dx/d*strength; player.y+=dy/d*strength
                if self.timer<=0: self.active=False; self.timer=self.rng.randint(50,80); self.ring_r=0.

        elif k=="mirror_clone":
            # mirror moves opposite to player relative to clone's position
            dx=player.x-self.px; dy=player.y-self.py
            d=math.hypot(dx,dy)
            if d>0.3 and d<8:
                spd=min(0.055, d*0.04)
                self.px+=dx/d*spd; self.py+=dy/d*spd
                if not self._in_floor(int(self.px),int(self.py)):
                    self.px=self.ox; self.py=self.oy
            self.trail.append((self.px,self.py))
            if len(self.trail)>15: self.trail.pop(0)
        elif k=="fire_bar":
            self.angle+=self.speed
        elif k=="ice_beam":
            self.angle+=self.speed

    def check_hit(self, player):
        pid=id(player); k=self.kind
        if pid in self.hit_cd: return
        hit=False

        if k=="pendulum_axe":
            if math.hypot(self.px-player.x,self.py-player.y)<PLAYER_HIT_RADIUS+0.14: hit=True
            # also check along arm
            for seg in range(10):
                t2=seg/10
                ax=self.pivot_x+math.cos(self.angle)*self.arm_len*t2
                ay=self.pivot_y+math.sin(self.angle)*self.arm_len*t2
                if math.hypot(ax-player.x,ay-player.y)<PLAYER_HIT_RADIUS+THIN_HAZARD_HALF_WIDTH: hit=True; break
        elif k=="ceiling_crusher":
            if self.state in ("dropping","down"):
                if (abs(player.x-self.ox)<self.crush_w and
                    abs(player.y-self.py)<0.6): hit=True
        elif k=="lava_tide":
            rm=self.room
            in_room=(rm.y+1<=player.y<=rm.y+rm.h-2)
            if abs(player.x-self.tide_x)<self.tide_w*0.7 and in_room: hit=True
        elif k=="rolling_boulder":
            if math.hypot(self.px-player.x,self.py-player.y)<self.radius+PLAYER_HIT_RADIUS: hit=True
        elif k=="ice_sweeper":
            rm=self.room
            in_room=(rm.y+1<=player.y<=rm.y+rm.h-2)
            if abs(player.x-self.sweep_x)<PLAYER_HIT_RADIUS+0.18 and in_room: hit=True
        elif k=="frozen_spike_row":
            if self.state in ("rising","hold") and self.rise>0.3:
                for sx,sy in self.spikes:
                    if math.hypot(sx-player.x,sy-player.y)<PLAYER_HIT_RADIUS+0.14: hit=True; break
        elif k=="thorn_wall":
            if self.wall_w>0.2:
                rm=self.room
                wx_end=rm.x+1+self.wall_w
                if (rm.x+1<=player.x<=wx_end and rm.y+1<=player.y<=rm.y+rm.h-2): hit=True
        elif k=="spore_burst":
            if self.state=="expanding":
                d=math.hypot(self.ox-player.x,self.oy-player.y)
                if (abs(d-self.burst_r) < SPORE_RING_HIT_HALF_WIDTH
                        and self.burst_r>0.5):
                    hit=True
        elif k=="mummy_wrap":
            if self.active and math.hypot(self.px-player.x,self.py-player.y)<PLAYER_HIT_RADIUS+0.14: hit=True
        elif k=="sarcophagus":
            for shot in self.shots:
                if math.hypot(shot[0]-player.x,shot[1]-player.y)<PLAYER_HIT_RADIUS+SMALL_PROJECTILE_RADIUS: hit=True; break
        elif k=="gravity_pull":
            if self.active and math.hypot(self.ox-player.x,self.oy-player.y)<PLAYER_HIT_RADIUS: hit=True
        elif k=="mirror_clone":
            if math.hypot(self.px-player.x,self.py-player.y)<PLAYER_HIT_RADIUS+0.14: hit=True
        elif k=="fire_bar":
            for arm in range(self.n_arms):
                ba=self.angle+arm*math.pi
                for seg in range(16):
                    t2=seg/16
                    ax=self.ox+math.cos(ba)*self.arm_len*t2
                    ay=self.oy+math.sin(ba)*self.arm_len*t2
                    if math.hypot(ax-player.x,ay-player.y)<PLAYER_HIT_RADIUS+THIN_HAZARD_HALF_WIDTH: hit=True; break
        elif k=="ice_beam":
            for sign in (1,-1):
                for seg in range(16):
                    t2=seg/16
                    bx=self.ox+math.cos(self.angle)*sign*self.beam_len*t2
                    by=self.oy+math.sin(self.angle)*sign*self.beam_len*t2
                    if math.hypot(bx-player.x,by-player.y)<PLAYER_HIT_RADIUS+THIN_HAZARD_HALF_WIDTH: hit=True; break

        if hit:
            if player.dead or player.inv > 0:
                # don't consume per-player cooldown on inv/dead
                return
            self.hit_cd[pid]=self.d["cd"]
            player.take_damage(self.d["dmg"],self.d["eff"],self.d["lbl"],self.d["col"],kind=self.kind)

    def _draw_formal(self, surf, cam_x, cam_y, ts):
        """Flat rendering of a dynamic hazard: shade the exact tiles its
        current geometry occupies (same footprint the simulator reasons over,
        so the picture matches the hitbox), category-coloured.  Active hazards
        are filled solid; dormant ones are shown as a faint outline at origin.
        A short type code is drawn at the trap's origin tile."""
        k = self.kind
        active, _ = _dtrap_phase(self)
        col = hazard_color(k)
        # collect the lethal footprint via the same mapper the sim uses
        footprint = {}
        _map_dtrap_tiles(self, footprint)
        origin = (int(round(self.ox)), int(round(self.oy)))
        for (tx, ty), _kind in footprint.items():
            sx = int((tx - 0.5 - cam_x) * ts); sy = int((ty - 0.5 - cam_y) * ts)
            if not (-ts < sx < W + ts and -ts < sy < H + ts):
                continue
            rect = pygame.Rect(sx + 1, sy + 1, ts - 1, ts - 1)
            if (tx, ty) == origin and not active:
                pygame.draw.rect(surf, lerpc(FML["floor"], col, 0.18), rect)
                pygame.draw.rect(surf, col, rect, 1)
            else:
                pygame.draw.rect(surf, col, rect)
        # type code at origin
        ox = int((self.ox - cam_x) * ts); oy = int((self.oy - cam_y) * ts)
        if -ts < ox < W + ts and -ts < oy < H + ts:
            f = _formal_font()
            code = StaticTrap._CODE.get(k) or {
                "pendulum_axe":"AXE","ceiling_crusher":"CRU","fire_bar":"BAR",
                "rolling_boulder":"BLD","ice_sweeper":"SWP","lava_tide":"TID",
                "frozen_spike_row":"SPK","thorn_wall":"WAL","spore_burst":"RNG",
                "mummy_wrap":"WRP","sarcophagus":"SAR","gravity_pull":"GRV",
                "ice_beam":"BEM","mirror_clone":"CLN",
            }.get(k, "DYN")
            txtcol = (255,255,255) if active else col
            # readability backing on origin when active
            t = f.render(code, True, txtcol)
            surf.blit(t, (ox - t.get_width()//2, oy - t.get_height()//2))

    def draw(self, surf, cam_x, cam_y, ts):
        if FORMAL_STYLE:
            self._draw_formal(surf, cam_x, cam_y, ts)
            return
        col=self.d["col"]
        pulse=(0.90+0.10*math.sin(self.t*0.08+self.ph)) if REDUCE_EFFECTS else (0.5+0.5*math.sin(self.t*0.08+self.ph))
        pc=tuple(min(255,int(c*pulse)) for c in col)
        bright=tuple(min(255,int(c*1.4)) for c in col)
        k=self.kind

        def s(wx,wy): return int((wx-cam_x)*ts), int((wy-cam_y)*ts)
        # raw, no +0.5
        def sr(wx,wy): return int((wx-cam_x)*ts), int((wy-cam_y)*ts)

        if k=="pendulum_axe":
            px2,py2=int((self.pivot_x-cam_x)*ts), int((self.pivot_y-cam_y)*ts)
            bx,by=int((self.px-cam_x)*ts), int((self.py-cam_y)*ts)
            # draw rope in segments (slight curve)
            segs=8
            for i in range(segs):
                t1=i/segs; t2=(i+1)/segs
                lx1=int(px2+(bx-px2)*t1); ly1=int(py2+(by-py2)*t1)
                lx2=int(px2+(bx-px2)*t2); ly2=int(py2+(by-py2)*t2)
                pygame.draw.line(surf,(140,115,75),(lx1,ly1),(lx2,ly2),2)
            # axe head — crescent shape
            axe_ang=self.angle+math.pi/2
            size=12
            pygame.draw.polygon(surf,(160,130,50),[
                (bx+int(math.cos(axe_ang)*size),by+int(math.sin(axe_ang)*size)),
                (bx+int(math.cos(axe_ang+math.pi)*size),by+int(math.sin(axe_ang+math.pi)*size)),
                (bx+int(math.cos(self.angle)*size*1.2),by+int(math.sin(self.angle)*size*1.2))])
            pygame.draw.polygon(surf,(210,185,90),[
                (bx+int(math.cos(axe_ang)*size),by+int(math.sin(axe_ang)*size)),
                (bx+int(math.cos(axe_ang+math.pi)*size),by+int(math.sin(axe_ang+math.pi)*size)),
                (bx+int(math.cos(self.angle)*size*1.2),by+int(math.sin(self.angle)*size*1.2))],1)
            # handle
            pygame.draw.line(surf,(100,80,50),(bx,by),(bx+int(math.cos(self.angle+math.pi)*8),by+int(math.sin(self.angle+math.pi)*8)),3)
            # pivot pin
            pygame.draw.circle(surf,(80,65,45),(px2,py2),5)
            pygame.draw.circle(surf,(160,130,80),(px2,py2),3)

        elif k=="ceiling_crusher":
            # floor position
            ox2,oy2=s(self.ox-0.5,self.oy-0.5)
            cw=int(self.crush_w*ts); ch=int(ts*0.6)
            # raise offset — when raised_frac=1 block is high, =0 it's at floor
            raise_px=int(self.raised_frac*ts*1.2)
            draw_y=oy2-raise_px
            alpha=100+int(self.raised_frac*155)
            # stone block
            block=asurf(cw*2+2,ch)
            block.fill((100,88,75,alpha))
            pygame.draw.rect(block,(130,115,95,alpha),(0,0,cw*2+2,4))
            # cracks
            for i in range(3):
                cx2=cw//2*i+cw//4
                pygame.draw.line(block,(60,50,38),(cx2,0),(cx2+random.randint(-3,3),ch),1)
            pygame.draw.rect(block,(70,60,45,alpha),(0,0,cw*2+2,ch),2)
            surf.blit(block,(ox2-cw-1,draw_y))
            # warning when about to drop — chains
            if self.state=="up" and self.timer<30:
                for i in range(3):
                    cx2=ox2-cw+i*cw
                    for seg in range(4):
                        gc=asurf(6,6); pygame.draw.circle(gc,(180,150,90,180),(3,3),2)
                        surf.blit(gc,(cx2-3,oy2-14-seg*6))
            # impact shadow on floor when dropping
            if self.state=="dropping":
                shadow_a=int((1-self.raised_frac)*160)
                sc=asurf(cw*2+4,8)
                sc.fill((0,0,0,shadow_a))
                surf.blit(sc,(ox2-cw-2,oy2+ch-4))

        elif k=="lava_tide":
            tx_s,ty_s=sr(self.tide_x,self.room.y+1)
            tw=int(self.tide_w*ts); th_h=int((self.room.h-2)*ts)
            # lava wave body
            gc=asurf(tw*2+4,th_h)
            gc.fill((200,50,5,160))
            # wave top
            for i in range(tw*2+4):
                wave_h=int(6+4*math.sin(i*0.3+self.t*0.1))
                pygame.draw.line(gc,(255,120,20),(i,0),(i,wave_h),1)
            surf.blit(gc,(tx_s-tw-2,ty_s))
            # bright leading edge
            pygame.draw.line(surf,(255,200,50),(tx_s+tw*self.dir,ty_s),(tx_s+tw*self.dir,ty_s+th_h),2)

        elif k=="rolling_boulder":
            for i,pos in enumerate(self.trail):
                lr=(i+1)/max(1,len(self.trail))
                bsx,bsy=sr(pos[0],pos[1])
                tr2=max(1,int(ts*0.35*lr))
                gc=asurf(tr2*2+2,tr2*2+2)
                pygame.draw.circle(gc,(140,90,40,int(120*lr)),(tr2+1,tr2+1),tr2)
                surf.blit(gc,(bsx-tr2-1,bsy-tr2-1))
            bsx,bsy=sr(self.px,self.py)
            br=int(ts*0.38)
            # rock body
            pygame.draw.circle(surf,(130,95,55),(bsx,bsy),br)
            pygame.draw.circle(surf,(160,120,70),(bsx,bsy),br-2)
            # rock texture
            for i in range(4):
                a=self.t*0.05+i*math.pi/2
                pygame.draw.arc(surf,(100,72,40),
                    pygame.Rect(bsx-br+4,bsy-br+4,br*2-8,br*2-8),a,a+1.0,1)
            pygame.draw.circle(surf,(180,140,80),(bsx,bsy),br,1)

        elif k=="ice_sweeper":
            isx,isy=sr(self.sweep_x,self.room.y+1)
            sh=int((self.room.h-2)*ts)
            # ice slab
            gc=asurf(int(ts*0.35)+4,sh)
            gc.fill((100,190,240,160))
            pygame.draw.line(gc,(200,240,255,220),( 2,0),(2,sh),2)
            surf.blit(gc,(isx-int(ts*0.18)-2,isy))
            # crystal sparkles
            for i in range(3):
                spy=isy+i*(sh//3)+sh//6
                pygame.draw.line(surf,(220,245,255),(isx-5,spy-5),(isx+5,spy+5),1)
                pygame.draw.line(surf,(220,245,255),(isx+5,spy-5),(isx-5,spy+5),1)

        elif k=="frozen_spike_row":
            if self.rise>0:
                for sx2,sy2 in self.spikes:
                    ssx,ssy=sr(sx2,sy2)
                    spike_h=int(self.rise*ts*0.7)
                    # ice spike triangle
                    pygame.draw.polygon(surf,(160,225,255),[
                        (ssx-5,ssy),(ssx+5,ssy),(ssx,ssy-spike_h)])
                    pygame.draw.polygon(surf,(210,245,255),[
                        (ssx-3,ssy),(ssx+3,ssy),(ssx,ssy-spike_h)],1)

        elif k=="thorn_wall":
            if self.wall_w>0:
                wx0=int((self.room.x+1-cam_x)*ts)
                wy0=int((self.room.y+1-cam_y)*ts)
                ww=int(self.wall_w*ts)
                wh=int((self.room.h-2)*ts)
                # wall body
                gc=asurf(ww+2,wh)
                gc.fill((40,80,20,180))
                # thorns
                for i in range(0,wh,int(ts*0.5)):
                    for side,sign in [(0,-1),(ww,1)]:
                        tlen=random.randint(4,9)
                        pygame.draw.line(gc,(80,160,40),(side,i),(side+sign*tlen,i-tlen//2),2)
                        pygame.draw.line(gc,(80,160,40),(side,i+4),(side+sign*tlen,i+4+tlen//2),2)
                surf.blit(gc,(wx0,wy0))

        elif k=="spore_burst":
            if self.burst_r>0:
                ocx,ocy=s(self.ox-0.5,self.oy-0.5)
                r_pix=int(self.burst_r*ts)
                fade=max(0,1-self.burst_r/self.max_r)
                if r_pix>2:
                    gc=asurf(r_pix*2+4,r_pix*2+4)
                    pygame.draw.circle(gc,(*col,int(180*fade)),(r_pix+2,r_pix+2),r_pix,3)
                    surf.blit(gc,(ocx-r_pix-2,ocy-r_pix-2))
                # spore dots on ring
                for i in range(8):
                    a=self.t*0.04+i*math.pi/4
                    sx2=ocx+int(math.cos(a)*r_pix); sy2=ocy+int(math.sin(a)*r_pix)
                    gc2=asurf(8,8); pygame.draw.circle(gc2,(*bright,int(200*fade)),(4,4),4)
                    surf.blit(gc2,(sx2-4,sy2-4))
            # mushroom centre
            ocx,ocy=s(self.ox-0.5,self.oy-0.5)
            pygame.draw.circle(surf,(90,60,20),(ocx,ocy),8)
            pygame.draw.ellipse(surf,col,pygame.Rect(ocx-10,ocy-6,20,10))

        elif k=="mummy_wrap":
            # source sarcophagus marker
            ocx,ocy=s(self.ox-0.5,self.oy-0.5)
            pygame.draw.rect(surf,(160,140,100),pygame.Rect(ocx-8,ocy-12,16,20))
            pygame.draw.rect(surf,(200,180,130),pygame.Rect(ocx-8,ocy-12,16,20),1)
            # bandage lines on sarcophagus
            for i in range(3):
                y2=ocy-12+i*7
                pygame.draw.line(surf,(180,165,120),(ocx-8,y2),(ocx+8,y2),1)
            if self.active:
                # trail
                for i,pos in enumerate(self.trail):
                    lr=(i+1)/max(1,len(self.trail))
                    tsx2,tsy2=sr(pos[0],pos[1])
                    gc=asurf(8,4); gc.fill((210,195,150,int(180*lr)))
                    surf.blit(gc,(tsx2-4,tsy2-2))
                # wrap head
                wx2,wy2=sr(self.px,self.py)
                pygame.draw.circle(surf,(210,195,150),(wx2,wy2),7)
                pygame.draw.circle(surf,(240,225,180),(wx2,wy2),5)
                for i in range(3):
                    a=i*math.pi*2/3+self.t*0.1
                    pygame.draw.arc(surf,(190,175,135),
                        pygame.Rect(wx2-8,wy2-8,16,16),a,a+1.5,2)

        elif k=="sarcophagus":
            ocx,ocy=s(self.ox-0.5,self.oy-0.5)
            # stone coffin
            pygame.draw.rect(surf,(100,82,58),pygame.Rect(ocx-14,ocy-18,28,28))
            pygame.draw.rect(surf,(140,115,80),pygame.Rect(ocx-12,ocy-16,24,24))
            # hieroglyph lines
            for i in range(3):
                pygame.draw.line(surf,(160,135,95),(ocx-8,ocy-12+i*8),(ocx+8,ocy-12+i*8),1)
            # lid open animation
            if self.state=="opening":
                lid_angle=int((1-self.timer/30)*20)
                pygame.draw.polygon(surf,(120,100,70),[
                    (ocx-14,ocy-18),(ocx+14,ocy-18),
                    (ocx+14-lid_angle,ocy-26),(ocx-14+lid_angle//3,ocy-26)])
            # shots
            for shot in self.shots:
                sx2,sy2=sr(shot[0],shot[1])
                gc=asurf(10,10); pygame.draw.circle(gc,(*col,220),(5,5),5)
                pygame.draw.circle(gc,(255,255,200,200),(5,5),2)
                surf.blit(gc,(sx2-5,sy2-5))

        elif k=="gravity_pull":
            ocx,ocy=s(self.ox-0.5,self.oy-0.5)
            if self.active:
                r_pix=int(self.ring_r*ts)
                if r_pix>2:
                    gc=asurf(r_pix*2+4,r_pix*2+4)
                    pygame.draw.circle(gc,(*col,80),(r_pix+2,r_pix+2),r_pix,3)
                    surf.blit(gc,(ocx-r_pix-2,ocy-r_pix-2))
                # inward arrows
                for i in range(6):
                    a=self.t*0.03+i*math.pi/3
                    dist=int(self.ring_r*ts*0.7)
                    ax=ocx+int(math.cos(a)*dist); ay=ocy+int(math.sin(a)*dist)
                    ex=ocx+int(math.cos(a)*int(ts*0.4)); ey=ocy+int(math.sin(a)*int(ts*0.4))
                    pygame.draw.line(surf,pc,(ax,ay),(ex,ey),2)
                    # arrowhead
                    perp=a+math.pi/2
                    pygame.draw.polygon(surf,pc,[
                        (ex,ey),(ex+int(math.cos(perp)*4)-int(math.cos(a)*6),
                                 ey+int(math.sin(perp)*4)-int(math.sin(a)*6)),
                        (ex-int(math.cos(perp)*4)-int(math.cos(a)*6),
                                 ey-int(math.sin(perp)*4)-int(math.sin(a)*6))])
            # singularity centre
            pygame.draw.circle(surf,(0,0,0),(ocx,ocy),8)
            pygame.draw.circle(surf,col,(ocx,ocy),6)
            pygame.draw.circle(surf,bright,(ocx,ocy),3)

        elif k=="mirror_clone":
            # ghostly trail
            for i,pos in enumerate(self.trail):
                lr=(i+1)/max(1,len(self.trail))
                tsx2,tsy2=sr(pos[0],pos[1])
                gc=asurf(16,16); pygame.draw.circle(gc,(*col,int(80*lr)),(8,8),7)
                surf.blit(gc,(tsx2-8,tsy2-8))
            # clone body — mirrors player appearance but ghostly
            mcx,mcy=sr(self.px,self.py)
            r2=int(ts*0.44)
            pygame.draw.circle(surf,(0,0,0,0),(mcx,mcy),r2)
            gc=asurf(r2*2+4,r2*2+4)
            pygame.draw.circle(gc,(*col,160),(r2+2,r2+2),r2)
            pygame.draw.circle(gc,(255,255,255,80),(r2+2,r2+2),r2-2)
            surf.blit(gc,(mcx-r2-2,mcy-r2-2))
            # eyes
            pygame.draw.circle(surf,(255,255,255),(mcx-4,mcy-3),3)
            pygame.draw.circle(surf,(255,255,255),(mcx+4,mcy-3),3)
            pygame.draw.circle(surf,(0,0,0),(mcx-4,mcy-3),1)
            pygame.draw.circle(surf,(0,0,0),(mcx+4,mcy-3),1)

        elif k=="fire_bar":
            ocx=int((self.ox-cam_x)*ts); ocy=int((self.oy-cam_y)*ts)
            bright=(255,240,80)
            for arm in range(self.n_arms):
                ba=self.angle+arm*math.pi
                segs=18
                pts=[]
                for i in range(segs+1):
                    t2=i/segs
                    wx=self.ox+math.cos(ba)*self.arm_len*t2
                    wy=self.oy+math.sin(ba)*self.arm_len*t2
                    pts.append((int((wx-cam_x)*ts), int((wy-cam_y)*ts)))
                # thick glowing arm — draw from wide at pivot to narrow at tip
                for i in range(len(pts)-1):
                    t2=i/segs
                    w=max(1,int(7*(1-t2*0.6)))
                    fc=lerpc(bright,col,t2)
                    try: pygame.draw.line(surf,fc,pts[i],pts[i+1],w)
                    except: pass
                # flame balls along arm
                for i in range(0,segs,3):
                    t2=i/segs
                    fx=int((self.ox+math.cos(ba)*self.arm_len*t2-cam_x)*ts)
                    fy=int((self.oy+math.sin(ba)*self.arm_len*t2-cam_y)*ts)
                    fr=max(2,int(8*(1-t2*0.5)*(0.7+0.3*pulse)))
                    gc=asurf(fr*2+2,fr*2+2)
                    fc2=lerpc(bright,col,t2)
                    pygame.draw.circle(gc,(*fc2,int(220*(1-t2*0.4))),(fr+1,fr+1),fr)
                    surf.blit(gc,(fx-fr-1,fy-fr-1))
                # white-hot tip
                if pts:
                    pygame.draw.circle(surf,WHITE,pts[-1],3)
            # pivot hub
            pygame.draw.circle(surf,(180,130,50),(ocx,ocy),6)
            pygame.draw.circle(surf,(240,200,100),(ocx,ocy),3)

        elif k=="ice_beam":
            ocx=int((self.ox-cam_x)*ts); ocy=int((self.oy-cam_y)*ts)
            beam_bright=(210,248,255)
            for sign in (1,-1):
                segs=16
                pts=[]
                for i in range(segs+1):
                    t2=i/segs
                    wx=self.ox+math.cos(self.angle)*sign*self.beam_len*t2
                    wy=self.oy+math.sin(self.angle)*sign*self.beam_len*t2
                    pts.append((int((wx-cam_x)*ts), int((wy-cam_y)*ts)))
                if len(pts)>=2:
                    pygame.draw.lines(surf,col,False,pts,4)
                    pygame.draw.lines(surf,beam_bright,False,pts,1)
                # crystal tip
                if pts:
                    tx2,ty2=pts[-1]
                    pygame.draw.circle(surf,WHITE,(tx2,ty2),5)
                    pygame.draw.circle(surf,beam_bright,(tx2,ty2),3)
                    # spiky tip
                    for i in range(4):
                        a2=self.angle*sign+i*math.pi/2
                        pygame.draw.line(surf,beam_bright,(tx2,ty2),
                            (tx2+int(math.cos(a2)*6),ty2+int(math.sin(a2)*6)),1)
            # centre pivot
            pygame.draw.circle(surf,(40,100,180),(ocx,ocy),6)
            pygame.draw.circle(surf,beam_bright,(ocx,ocy),3)



# =============================================================================
# roamingenemy — non-stationary patrol agent that defeats rl trial-and-error
# each enemy picks a random waypoint inside its room, walks to it, waits a
# random duration, then picks another.  speed and wait times have bounded-
# random jitter every cycle, so no fixed temporal pattern can be learned.
# =============================================================================
class RoamingEnemy:
    RADIUS = ENEMY_HIT_RADIUS

    def __init__(self, room, grid):
        self.room = room
        self.grid = grid
        inner = room.inner()
        if not inner:
            inner = [(room.cx, room.cy)]
        # start at random floor tile inside room
        start = random.choice([t for t in inner if grid[t[1]][t[0]] == 0] or inner)
        self.x = float(start[0]); self.y = float(start[1])
        # private rng for live re-arm draws (new waypoints, pauses, speed
        # jitter) inside update().  seeded from the construction stream, which
        # is identical across agents, so this enemy's motion sequence is
        # identical across agents.  reading from its own stream means the tick
        # at which it arrives/gets stuck (player-path dependent) cannot shift
        # any other enemy's or hazard's draws.
        self.rng = random.Random(random.getrandbits(32))
        self.waypoint = self._new_waypoint(initial=True)
        self.wait = 0
        # random speed in [0.035, 0.08] — varied per enemy so pack timing differs
        self.base_spd = random.uniform(0.035, 0.08)
        self.spd = self.base_spd
        self.hit_cd = 0
        self.t = random.randint(0, 200)
        # colour varies by room theme
        th = THEMES[RTYPES[room.rtype]["theme"]]
        self.col = lerpc(th["acc"], (255, 80, 80), 0.55)

    def _new_waypoint(self, initial=False):
        inner = self.room.inner()
        candidates = [t for t in inner if self.grid[t[1]][t[0]] == 0]
        if not candidates:
            return (self.room.cx, self.room.cy)
        # the very first waypoint is part of world construction (global stream);
        # every later re-pick is live motion (the enemy's private stream).
        rng = random if initial else self.rng
        return rng.choice(candidates)

    def update(self, player):
        self.t += 1
        if self.hit_cd > 0:
            self.hit_cd -= 1

        if self.wait > 0:
            self.wait -= 1
            return

        # walk toward waypoint
        dx = self.waypoint[0] - self.x
        dy = self.waypoint[1] - self.y
        dist = math.hypot(dx, dy)
        if dist < 0.25:
            # arrived — pick new waypoint and wait a stochastic amount
            self.waypoint = self._new_waypoint()
            # unpredictable pause
            self.wait = self.rng.randint(20, 90)
            # re-randomise speed slightly so timing patterns shift each leg
            self.spd = self.base_spd * self.rng.uniform(0.7, 1.4)
            return

        nx = self.x + (dx / dist) * self.spd
        ny = self.y + (dy / dist) * self.spd
        # simple wall avoidance: slide along walls
        m = 0.32
        def floor_ok(px, py):
            for odx, ody in [(m,0),(-m,0),(0,m),(0,-m)]:
                tx2 = int(px + odx); ty2 = int(py + ody)
                if not (0 <= tx2 < COLS and 0 <= ty2 < ROWS):
                    return False
                if self.grid[ty2][tx2] == 1:
                    return False
            return True
        if floor_ok(nx, self.y): self.x = nx
        if floor_ok(self.x, ny): self.y = ny

        # if stuck, pick a new waypoint immediately
        if not floor_ok(self.x + (dx/max(dist,0.01))*self.spd,
                         self.y + (dy/max(dist,0.01))*self.spd):
            self.waypoint = self._new_waypoint()

    def check_hit(self, player):
        if self.hit_cd > 0: return
        if player.dead: return
        if math.hypot(self.x - player.x, self.y - player.y) < self.RADIUS + PLAYER_HIT_RADIUS:
            if player.inv > 0:
                # don't consume cooldown on an invincible player
                return
            self.hit_cd = 90
            player.take_damage(99, None, "Roaming Enemy", self.col, kind="enemy")

    def draw(self, surf, cam_x, cam_y, ts, player):
        # only visible within fog-of-war radius
        if math.hypot(self.x - player.x, self.y - player.y) > FOG_REVEAL_DIST + 2:
            return
        sx = int((self.x - cam_x) * ts)
        sy = int((self.y - cam_y) * ts)
        if FORMAL_STYLE:
            r = int(ts * self.RADIUS)
            # flat triangle marker (mobile agent), category-violet, with code
            pts = [(sx, sy - r), (sx - r, sy + r), (sx + r, sy + r)]
            pygame.draw.polygon(surf, HZ_ENEMY, pts)
            pygame.draw.polygon(surf, lerpc(HZ_ENEMY, (0,0,0), 0.3), pts, 1)
            f = _formal_font(9)
            t = f.render("E", True, (255,255,255))
            surf.blit(t, (sx - t.get_width()//2, sy - t.get_height()//2 + 2))
            return
        r = max(5, int(ts * self.RADIUS))
        pulse = (0.90 + 0.10 * math.sin(self.t * 0.12)) if REDUCE_EFFECTS else (0.5 + 0.5 * math.sin(self.t * 0.12))
        glow_pulse = 0.0 if REDUCE_EFFECTS else pulse
        # shadow
        gs = asurf(r*2+6, r+4)
        pygame.draw.ellipse(gs, (0,0,0,50), (0,0,r*2+6,r+4))
        surf.blit(gs, (sx-r-3, sy-2))
        # body
        pygame.draw.circle(surf, lerpc(self.col,(0,0,0),0.5), (sx,sy), r)
        pygame.draw.circle(surf, self.col, (sx,sy), r-1)
        # pulse glow ring
        ga = asurf(r*3, r*3)
        pygame.draw.circle(ga, (*self.col, int(glow_pulse*80)), (r+r//2, r+r//2), r+4, 2)
        surf.blit(ga, (sx-r-r//2, sy-r-r//2))


# =============================================================================
# hazardpulse — room-wide environmental event at stochastic intervals
# when triggered, dims the room (vision penalty) and may push the player.
# this breaks any timing-based exploitation by rl agents.
# =============================================================================
class HazardPulse:
    def __init__(self, rng=None):
        # private rng so the pulse's kind/duration/speed-mod draws form a fixed
        # per-seed sequence, independent of any agent's behaviour.  falls back
        # to the global stream only if constructed without a seed.
        self.rng = rng if rng is not None else random
        self.active = False
        self.timer = self.rng.randint(HAZARD_PULSE_MIN, HAZARD_PULSE_MAX)
        self.duration = 0
        # 'dark' | 'push' | 'speed'
        self.kind = None
        self.alpha = 0

    def update(self, player, grid):
        if not self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = True
                # random kind each pulse — unpredictable
                self.kind = self.rng.choice(['dark', 'speed'])
                self.duration = self.rng.randint(60, 160)
                self.alpha = 0
        else:
            self.duration -= 1
            # fade in/out alpha for overlay
            progress = 1.0 - self.duration / 160
            self.alpha = int(min(progress, 1-progress) * 2 * 160)

            if self.kind == 'speed' and self.duration % 4 == 0:
                # temporarily alter speed perception
                player.pulse_spd_mod = self.rng.choice([0.5, 1.8])

            if self.duration <= 0:
                self.active = False
                self.timer = self.rng.randint(HAZARD_PULSE_MIN, HAZARD_PULSE_MAX)
                player.pulse_spd_mod = 1.0

    def draw_overlay(self, surf):
        if not self.active or self.alpha <= 0:
            return
        k = self.kind
        if k == 'dark':
            ov = asurf(W, H)
            ov.fill((0, 0, 0, min(200, self.alpha * 2)))
            surf.blit(ov, (0, 0))
        elif k == 'speed':
            ov = asurf(W, H)
            ov.fill((30, 30, 180, min(80, self.alpha)))
            surf.blit(ov, (0, 0))

    def hud_label(self):
        if not self.active: return None
        labels = {'dark': ('BLACKOUT', (80,80,80)),
                  'speed': ('FLUX', (80,120,255))}
        return labels.get(self.kind)


# =============================================================================
# popperian expectations — eec storage + autonomous maze agent
#
# architecture (paper §iii, 7 components):
# 1. robot controller      → peagent.choose_action  (generates + executes actions)
# 2. object tracker-loc.   → peagent.observe        (otl: sensor model → obs dict)
# 3. internal model        → consequenceevaluator._sim_step (simulates candidate moves)
# 4. consequence evaluator → consequenceevaluator.evaluate (+ chained_danger)
# 5. eec expectation form. → consequenceevaluator._form_expectations (algorithm 1)
# 6. expectation memory    → expectationmemory (algorithm 1 form + algorithm 2 update)
# 7. expectation update    → peagent.feedback + expectationmemory.update (algorithm 2)
#
# eecreasoner implements the formal ec temporal reasoning engine (§iii-b):
# happens(e,t) ∧ holdsat(f₁..fₙ,t) → initiates(g, t+d) | terminates(g, t+d) | holdsat(g, t+d)
# used by consequenceevaluator for chained multi-step danger detection.
#
# functional loop (paper §iv, 8 steps):
# otl→internalmodel→consequenceeval→eecformation→memory→robotcontroller→feedback
# memory-first: step 3-5 skipped when expectationmemory has confident prior.
# ============================================================================

# =============================================================================
# formal eec datatypes  (event, fluent, eectemporalrule)
#
# these implement the typed objects described in the paper:
# happens(event, t) ∧ holdsat(fluent₁..fₙ, t) → initiates/terminates(g, t+delay)
# =============================================================================

@dataclass(frozen=True)
class Event:
    """A discrete action event: Happens(name, args, t)"""
    name: str
    args: tuple = ()

@dataclass(frozen=True)
class Fluent:
    """A state property that holds over time: HoldsAt(name, args, t)"""
    name: str
    args: tuple = ()


def _is_var(x) -> bool:
    return isinstance(x, str) and x.startswith("?")


def _subst_value(x, subst: dict):
    if _is_var(x):
        return subst.get(x, x)
    if isinstance(x, tuple):
        return tuple(_subst_value(v, subst) for v in x)
    return x


def _instantiate_atom(atom, subst: dict):
    if atom is None:
        return None
    return atom.__class__(atom.name, tuple(_subst_value(a, subst) for a in atom.args))


def _unify_value(pattern, fact, subst: dict):
    if _is_var(pattern):
        bound = subst.get(pattern)
        if bound is None:
            out = dict(subst)
            out[pattern] = fact
            return out
        return subst if bound == fact else None
    if isinstance(pattern, tuple) and isinstance(fact, tuple):
        if len(pattern) != len(fact):
            return None
        out = subst
        for p, f in zip(pattern, fact):
            out = _unify_value(p, f, out)
            if out is None:
                return None
        return out
    return subst if pattern == fact else None


def _unify_atom(pattern, fact, subst: dict):
    if pattern.name != fact.name or len(pattern.args) != len(fact.args):
        return None
    out = subst
    for p, f in zip(pattern.args, fact.args):
        out = _unify_value(p, f, out)
        if out is None:
            return None
    return out

@dataclass
class EECTemporalRule:
    """Unified EEC rule implementing the paper's formal expectation representation.

    Formal EEC encoding (paper §III-C):
        Happens(event, t) ∧ HoldsAt(f₁, t) ∧ … ∧ HoldsAt(fₙ, t)
            → Initiates(effect, t+delay)   [effect_type="Initiates"]
            | Terminates(effect, t+delay)  [effect_type="Terminates"]
            | HoldsAt(effect, t+delay)     [effect_type="HoldsAt"]  ← persistence (inertia)

    event=None means the rule fires from fluents alone (no Happens condition required).
    effect_type="HoldsAt" encodes the EEC inertia axiom: fluents persist unless Terminated.

    Learning metadata (confidence, confirmations, violations, generalised,
    last_observed_time) are updated by ExpectationMemory according to
    the paper's delta-rule Algorithm 2 (eqs. 2-4) and generalised per eq. 5.

    Confidence C(e) ∈ [0,1]:
        C_INIT         = 0.50  — prior for simulation-derived rules
        C_INIT_SURPRISE= 0.65  — elevated prior for surprise-learned rules
        (These are defined as module-level constants below.)
    """
    # happens(...) trigger; none for fluent-only rules
    event: 'Event'
    # holdsat(f, t) conditions — tuple of fluent
    preconditions: tuple
    # "initiates", "terminates", or "holdsat"
    effect_type: str
    effect: 'Fluent'
    delay: int = 1
    # c(e) ∈ [0, 1] — initialised to c_init
    confidence: float = 0.5
    confirmations: int = 0
    violations: int = 0
    generalised: bool = False
    last_observed_time: int = 0
    # "innate" | "learned" | "derived"
    origin: str = "learned"
    # innate  — embodiment priors the agent starts with.  fully revisable by
    # eqs. 2-3 (popperian: bold conjectures, open to refutation) but
    # exempt from pruning (eq. 4) and staleness decay — they encode
    # physical constraints, not environment-specific knowledge.
    # learned — formed from internal simulation or real-world observation.
    # derived — produced by generalisation (eq. 5) or specialisation.
    confirm_ctx: list = field(default_factory=list)
    # ring buffer (≤ 6) of recent confirming contexts — frozensets of the
    # fluents that held when this rule's prediction came true.  used by
    # violation-driven specialisation to discover the discriminating
    # condition that separates the contexts where the rule works from the
    # one where it just failed.

    def reliability_lcb(self, z: float = 1.645) -> float:
        """Wilson-score LOWER bound on this rule's empirical reliability.

        reliability ≈ confirmations / (confirmations + violations), but the
        point estimate is reckless at small n (1/1 = 100%).  The Wilson lower
        bound is what the evidence statistically guarantees at ~95% one-sided
        confidence: 3 clean confirmations ⇒ ≈0.53, 11 ⇒ ≈0.80, and any
        violation pushes it down hard until many confirmations outweigh it.

        This is the quantity that decides whether an expectation may REPLACE
        an internal simulation: memory must not be less safe than simming, so
        a rule earns that right only when its reliability is statistically
        demonstrated, not merely asserted by its confidence scalar (which
        eq. 2 can saturate after a couple of lucky confirmations).
        """
        n = self.confirmations + self.violations
        if n == 0:
            return 0.0
        p  = self.confirmations / n
        z2 = z * z
        centre = p + z2 / (2 * n)
        margin = z * ((p * (1 - p) / n + z2 / (4 * n * n)) ** 0.5)
        return max(0.0, (centre - margin) / (1 + z2 / n))


# confidence initialisation constants (paper §iii-g, eqs. 1-3)
class EECFactBase:
    """Time-indexed Expectation Event Calculus fact base."""
    def __init__(self):
        self.happens: dict = {}
        self.holds: dict = {}
        self.initiates: dict = {}
        self.terminates: dict = {}
        self.trace: list = []

    def add_happens(self, event: Event, t: int):
        self.happens.setdefault(t, set()).add(event)

    def add_holds(self, fluent: Fluent, t: int):
        self.holds.setdefault(t, set()).add(fluent)

    def add_initiates(self, event: Event | None, fluent: Fluent,
                      t_from: int, t_to: int, rule: EECTemporalRule):
        self.initiates.setdefault(t_to, set()).add(fluent)
        self.trace.append((t_from, t_to, "Initiates", rule))

    def add_terminates(self, event: Event | None, fluent: Fluent,
                       t_from: int, t_to: int, rule: EECTemporalRule):
        self.terminates.setdefault(t_to, set()).add(fluent)
        self.trace.append((t_from, t_to, "Terminates", rule))

    def holds_at(self, fluent: Fluent, t: int) -> bool:
        bucket = self.holds.get(t, set())
        if fluent.args:
            return fluent in bucket
        return any(f.name == fluent.name for f in bucket)

    def clipped(self, fluent: Fluent, t_from: int, t_to: int) -> bool:
        for t in range(t_from + 1, t_to + 1):
            terms = self.terminates.get(t, set())
            if fluent.args and fluent in terms:
                return True
            if not fluent.args and any(f.name == fluent.name for f in terms):
                return True
        return False

    def events_at(self, t: int) -> set:
        return self.happens.get(t, set())

    def fluents_at(self, t: int) -> set:
        return self.holds.get(t, set())

    def _rule_is_tested(self, rule: EECTemporalRule) -> bool:
        return rule.origin == "innate" or rule.confirmations >= 1

    def initiated_by_tested_rule(self, fluent: Fluent, t: int,
                                 _seen: frozenset | None = None) -> bool:
        """True if the fluent's appearance at time *t* is supported by a chain in
        which EVERY rule is REALITY-TESTED (innate, or with >=1 confirmation)
        AND which grounds out in fluents actually PERCEIVED at t0.

        The chained-danger veto must not be triggered by a pure conjecture: an
        unconfirmed learned rule (confirmations == 0, reliability LCB 0.0) that
        predicts Damaged several steps out should not hard-veto the only path
        forward, the way the direct t+1 verdict path already refuses to let
        untested rules suppress simulation (require_tested=True).  This restores
        the Popperian discipline — act on a conjecture until it is FALSIFIED,
        rather than freezing because an unfalsified, never-confirmed conjecture
        merely *asserts* danger.

        A chain is only as trustworthy as its WEAKEST link.  The earlier
        shallow check validated only the terminal Damaged-initiating rule, so a
        tested innate rule (e.g. Curse -> Damaged) could be fired off a fluent
        (Curse) that was itself fabricated one step earlier by an UNtested
        learned conjecture (e.g. Room -> Curse, confirmations == 0).  Because
        Room holds on essentially every in-room tile, that conjecture injected a
        phantom Curse — and hence a permanent phantom veto — on every clear room
        tile, freezing the agent at room mouths.  We therefore require the
        whole support chain to be tested, recursing on each non-ground
        precondition fluent of every candidate rule.
        """
        if _seen is None:
            _seen = frozenset()
        # ground truth: fluents that genuinely held at t0 (the perceived state).
        # a precondition satisfied directly by perception needs no rule support.
        ground0 = self.holds.get(0, set())
        for (t_from, t_to, kind, rule) in self.trace:
            if t_to != t or kind != "Initiates":
                continue
            if fluent.args:
                if rule.effect != fluent:
                    continue
            elif rule.effect.name != fluent.name:
                continue
            if not self._rule_is_tested(rule):
                # weakest-link: an untested producer disqualifies this path
                continue
            # every precondition of this tested rule must itself be grounded in
            # perception at t0 or produced by a tested chain at the time it was
            # consumed (t_from).  guard against precondition cycles via _seen.
            ok = True
            for pre in rule.preconditions:
                if pre.name in ("ClearAhead", "Clear", "NoStatus", "Room",
                                "HazardPresent"):
                    # perceptual / structural context fluents: trusted as given
                    # iff they were actually perceived at t0.  (room, clear,
                    # etc. describe the real tile, not a conjectured status.)
                    held0 = (pre in ground0 if pre.args
                             else any(f.name == pre.name for f in ground0))
                    if held0:
                        continue
                # otherwise the precondition is a state the chain must have
                # produced by t_from through a tested derivation.
                held0 = (pre in ground0 if pre.args
                         else any(f.name == pre.name for f in ground0))
                if held0:
                    continue
                key = (pre.name, pre.args, t_from)
                if key in _seen:
                    ok = False
                    break
                if not self.initiated_by_tested_rule(
                        pre, t_from, _seen | {key}):
                    ok = False
                    break
            if ok:
                return True
        return False


# prior for all simulation-derived rules
C_INIT          = 0.50
# elevated prior for popperian surprise rules
C_INIT_SURPRISE = 0.65

# ── innate world-knowledge priors (ablation flag) ─────────────────────────────
# false → the agent starts with no hand-written sensor→effect rules
# (hightemperature → burn, hazardpresent → damaged, …).  all environmental
# causal links must be learned — from internal simulation (algorithm 1),
# real-world surprises, and vicarious observation — and their preconditions
# are screened for causal relevance by the causalledger below.
# true restores the original hand-written priors for a/b comparison.
INNATE_WORLD_PRIORS = False


# =============================================================================
# causalledger — learned causal relevance of fluents (replaces hand whitelists)
# =============================================================================
class CausalLedger:
    """Contingency-based causal attribution over (fluent, effect) pairs.

    The original implementation decided which fluents may appear as causal
    preconditions of an EEC rule with a HAND-WRITTEN whitelist — i.e. the
    designer, not the agent, decided what is causally relevant.  This class
    replaces that prior with the probabilistic-contrast model of causal
    induction (Cheng & Novick's ΔP):

        ΔP(f, e) = P(e | f present) − P(e | f absent)

    estimated from every outcome the agent observes — internal-simulation
    results (Algorithm 1), real-world feedback (Algorithm 2), and vicarious
    observations of other entities.  A fluent f is admitted as a causal
    precondition of an Initiates(e) rule only when ΔP(f, e) is reliably
    positive; fluents that merely co-occur (e.g. Room(lava) holds on every
    tile of a lava room, safe floor included) wash out and are dropped.

    EEC reading: ΔP estimates whether HoldsAt(f, t) genuinely participates in
    Happens(a, t) ∧ HoldsAt(f, t) → Initiates(e, t+1), or is incidental
    context.  This is the screening-off step that makes stored expectations
    *causal* expectations rather than correlational ones.

    Epistemics (deliberately Popperian):
      • While evidence is insufficient (< MIN_OBS on either margin) the fluent
        is RETAINED — a bold, over-specific conjecture that later evidence can
        refute by generalisation (precondition dropping), never the reverse.
      • Laplace smoothing keeps estimates defined from the first observation.
    """
    # |δp| above which a fluent counts as causally relevant
    DELTA_P_MIN = 0.15
    # min observations on both margins before screening —
    MIN_OBS     = 30
                         # a premature 'irrelevant' verdict licenses ignoring a
                         # condition, so it demands substantial evidence

    def __init__(self):
        # sufficient statistics: co-occurrence + marginals.  the full 2×2
        # contingency table for any (fluent, effect) pair is derived:
        # n_f_e   = co[(fk, e)]
        # n_f_¬e  = fluent_counts[fk] − n_f_e
        # n_¬f_e  = effect_counts[e]  − n_f_e
        # n_¬f_¬e = observations − fluent_counts[fk] − n_¬f_e
        # this is retroactively correct for late-appearing fluents/effects:
        # a fluent first observed at obs #500 is automatically counted as
        # absent in the 499 prior observations (fluents are perceptual —
        # had it held, it would have been seen).
        # (fluent_key, effect_name) → co-count
        self.co: dict = {}
        # fluent_key → times present
        self.fluent_counts: dict = {}
        # effect_name → times observed
        self.effect_counts: dict = {}
        # every fluent key ever observed
        self.fluent_vocab: set = set()
        # every effect name ever observed
        self.effect_vocab: set = set()
        self.observations  = 0
        # (fkey, effect) → (verdict, obs_at)
        self._rel_cache: dict = {}

    # fluent identity for the ledger: args kept so room('lava') ≠ room('ice').
    @staticmethod
    def _fkey(f: 'Fluent'):
        return (f.name, f.args)

    def record(self, present_fluents, observed_effects):
        """Log one outcome observation.

        present_fluents : iterable[Fluent] — HoldsAt(f, t) context of the action
        observed_effects: iterable[str]    — effect names that became true at t+1
                          ('Damaged', 'Burn', …).  'Safe' is NOT tracked as an
                          effect: Safe ≡ ¬Damaged, so the Damaged column carries
                          all the information for both rule polarities.
        """
        present = {self._fkey(f) for f in present_fluents}
        effects = {e for e in observed_effects if e != 'Safe'}
        self.fluent_vocab |= present
        self.effect_vocab |= effects
        self.observations += 1
        for fk in present:
            self.fluent_counts[fk] = self.fluent_counts.get(fk, 0) + 1
        for e in effects:
            self.effect_counts[e] = self.effect_counts.get(e, 0) + 1
            for fk in present:
                self.co[(fk, e)] = self.co.get((fk, e), 0) + 1

    def delta_p(self, f: 'Fluent', effect: str) -> tuple:
        """Return (ΔP, n_present, n_absent) with Laplace smoothing."""
        fk = self._fkey(f)
        if fk not in self.fluent_vocab or effect not in self.effect_counts:
            return 0.0, self.fluent_counts.get(fk, 0), 0
        n_fe  = self.co.get((fk, effect), 0)
        n_p   = self.fluent_counts.get(fk, 0)
        n_a   = self.observations - n_p
        n_nfe = self.effect_counts[effect] - n_fe
        p_e_f  = (n_fe  + 1) / (n_p + 2)
        p_e_nf = (n_nfe + 1) / (n_a + 2)
        return p_e_f - p_e_nf, n_p, n_a

    def relevance(self, f: 'Fluent', effect: str) -> bool | None:
        """True/False once evidence suffices; None while undetermined.

        TWO-SIDED: a fluent is causally implicated if |ΔP| is large in EITHER
        direction — generative (raises P(effect)) or preventive (lowers it,
        e.g. TrapInactive vs Damaged).  A preventive condition is exactly the
        kind that must NOT be ignorable when absent: a Safe rule conditioned
        on TrapInactive means nothing on a tile where the trap is not dormant.

        Verdicts are memoized and refreshed every 200 observations — this
        method sits on the hot path of graded rule matching.
        """
        key = (self._fkey(f), effect)
        cached = self._rel_cache.get(key)
        if cached is not None and self.observations - cached[1] < 200:
            return cached[0]
        dp, n_p, n_a = self.delta_p(f, effect)
        if n_p < self.MIN_OBS or n_a < self.MIN_OBS:
            verdict = None
        else:
            verdict = abs(dp) >= self.DELTA_P_MIN
        self._rel_cache[key] = (verdict, self.observations)
        return verdict

    def screen(self, fluents, effect: str) -> tuple:
        """Causally screened precondition set for an Initiates(effect) rule.

        Keeps fluents that are (a) demonstrably relevant or (b) still
        undetermined (bold conjecture).  Drops only fluents demonstrably
        irrelevant.  For 'Safe' rules, relevance to 'Damaged' is used:
        a fluent that raises/leaves-unchanged P(Damaged) is what a Safe
        rule must condition on (or may safely omit) respectively.
        """
        target = 'Damaged' if effect == 'Safe' else effect
        kept = tuple(sorted(
            (f for f in fluents if self.relevance(f, target) is not False),
            key=lambda f: (f.name, f.args)))
        return kept


# =============================================================================
# sensorcalibration — learned fuzzy membership over continuous sensor values
# =============================================================================
class SensorCalibration:
    """Data-derived membership functions for the continuous sensor channels.

    Crisp perception (tile_sensor_fluents) binarises continuous readings at
    hand-set embodiment thresholds: 51 °C produces HoldsAt(HighTemperature),
    49 °C produces nothing, and every expectation downstream inherits that
    cliff.  Fuzzy inference is the right tool for this vagueness — but
    hand-drawn membership functions would re-introduce exactly the designer
    priors the CausalLedger removed.  So the membership curves are LEARNED:
    observed outcomes are binned by channel value, and

        μ_danger(channel, v) ≈ P(Damaged | value ∈ bin(v))

    estimated from the same evidence streams as the ledger (simulated
    outcomes and vicarious observations).  degree() normalises against the
    most dangerous observed bin of the channel, yielding a [floor, 1] scale:
    the agent's own experience decides how much a 55 °C floor counts compared
    to an 80 °C geyser.

    SAFETY DIRECTION (by construction): degrees scale the activation of
    DANGER-side rules only, and only downward.  Fuzziness can therefore make
    the agent fall back to simulation more often (a weak danger vote misses
    the threshold → the Internal Model runs), but can never strengthen a
    danger claim beyond its evidence and never touches Safe rules — those
    remain governed solely by crisp matching plus the Wilson gates.  The
    two-level separation is deliberate: fuzzy degrees model VAGUENESS of
    predicates at the fluent level; Wilson-gated confidence models EPISTEMIC
    uncertainty about rules at the rule level.
    """
    # (bin width, value range) per continuous channel
    CHANNELS = {
        'temp': (50.0,  (-100.0, 950.0)),
        'tox':  (0.1,   (0.0, 1.0)),
        'imp':  (50.0,  (0.0, 750.0)),
    }
    # never extinguish a danger vote entirely
    FLOOR = 0.25
    # bin observations before the curve has an opinion
    MIN_N = 8

    # which crisp sensor fluents are graded by which channel
    FLUENT_CHANNEL = {
        'HighTemperature': 'temp', 'LowTemperature': 'temp',
        'Toxic': 'tox', 'HeavyImpact': 'imp',
    }

    def __init__(self):
        # (channel, bin_idx) → [n_damage, n_total]
        self.bins: dict = {}
        self.observations = 0

    def _idx(self, channel: str, v: float) -> int:
        width, (lo, hi) = self.CHANNELS[channel]
        return int((min(max(v, lo), hi) - lo) // width)

    def record(self, kind: str | None, damaged: bool):
        """Log one outcome at a tile of the given hazard kind."""
        if kind is None:
            return
        p = TRAP_SENSORS.get(kind)
        if not p:
            return
        self.observations += 1
        for ch in self.CHANNELS:
            v = p.get(ch)
            if v is None:
                continue
            cell = self.bins.setdefault((ch, self._idx(ch, v)), [0, 0])
            cell[1] += 1
            if damaged:
                cell[0] += 1

    def mu(self, channel: str, v: float) -> float | None:
        """Smoothed P(Damaged | bin(v)), or None below the evidence floor."""
        cell = self.bins.get((channel, self._idx(channel, v)))
        if cell is None or cell[1] < self.MIN_N:
            return None
        return (cell[0] + 1) / (cell[1] + 2)

    def degree(self, channel: str, v: float) -> float:
        """Relative danger membership of value v on its channel, ∈ [FLOOR, 1].

        Normalised against the channel's most dangerous well-observed bin so
        the worst values the agent has experienced keep full activation and
        milder ones shrink proportionally.  Returns 1.0 (no opinion) while
        evidence is insufficient — unknown is treated as fully dangerous.
        """
        m = self.mu(channel, v)
        if m is None:
            return 1.0
        peak = max((c[0] + 1) / (c[1] + 2)
                   for (ch, _), c in self.bins.items()
                   if ch == channel and c[1] >= self.MIN_N)
        if peak <= 0:
            return 1.0
        return max(self.FLOOR, min(1.0, m / peak))

    def degrees_for(self, kind: str | None) -> dict:
        """Map sensor-fluent names → learned danger degree for this hazard."""
        if kind is None:
            return {}
        p = TRAP_SENSORS.get(kind)
        if not p:
            return {}
        out = {}
        for fname, ch in self.FLUENT_CHANNEL.items():
            v = p.get(ch)
            if v is not None:
                out[fname] = self.degree(ch, v)
        return out


def tile_sensor_fluents(kind: str, in_kinetic_path: bool = False) -> set:
    """Map a trap kind to physical sensor fluents.

    The agent perceives properties (temperature, toxicity, impact force, …),
    NOT the kind name.  What it LEARNS is the causal link between those
    properties and outcomes — e.g. HighTemperature → Burn, not lava_geyser → burn.
    """
    if kind is None:
        return set()
    p = TRAP_SENSORS.get(kind, {})
    fluents: set = set()

    temp = p.get('temp', 20)
    if temp > AGENT_MAX_TEMP:
        fluents.add(Fluent("HighTemperature"))
    elif temp < AGENT_MIN_TEMP:
        fluents.add(Fluent("LowTemperature"))

    if p.get('tox', 0) > AGENT_MAX_TOXICITY:
        fluents.add(Fluent("Toxic"))

    if p.get('imp', 0) > AGENT_MAX_IMPACT:
        fluents.add(Fluent("HeavyImpact"))

    if p.get('mov', False):
        fluents.add(Fluent("MovingHazard"))
        if in_kinetic_path:
            fluents.add(Fluent("CollisionPath"))

    if p.get('con', False):
        fluents.add(Fluent("Constricting"))

    if p.get('unst', False):
        fluents.add(Fluent("Unstable"))

    if p.get('cor', False):
        fluents.add(Fluent("Corrupting"))

    if fluents:
        # generic "something dangerous here"
        fluents.add(Fluent("HazardPresent"))

    return fluents


def _dtrap_phase(dt) -> tuple:
    """Return (is_active: bool, ticks_until_active: int) for a DynamicTrap.

    'active' means the trap is currently in its dangerous sweep/strike phase.
    Used by predict_physical_harm() to tell whether a cyclical trap will be
    in its dangerous state when the agent arrives (~STEP_TICKS ticks from now).
    Continuously-moving traps (sweepers, pendulums) are always active.
    """
    k = dt.kind
    # continuously sweeping — always dangerous when in path
    if k in ('pendulum_axe', 'fire_bar', 'ice_beam', 'lava_tide', 'ice_sweeper',
             'rolling_boulder', 'mirror_clone', 'wall_dart'):
        return (True, 0)
    if k == 'ceiling_crusher':
        state = getattr(dt, 'state', 'up')
        if state in ('dropping', 'down'):
            return (True, 0)
        return (False, max(1, getattr(dt, 'timer', 60)))
    if k == 'frozen_spike_row':
        state = getattr(dt, 'state', 'wait')
        if state in ('rising', 'hold'):
            return (True, 0)
        return (False, max(1, getattr(dt, 'timer', 40)))
    if k == 'thorn_wall':
        state = getattr(dt, 'state', 'wait')
        if state in ('growing', 'hold'):
            return (True, 0)
        return (False, max(1, getattr(dt, 'timer', 60)))
    if k == 'spore_burst':
        state = getattr(dt, 'state', 'wait')
        if state == 'expanding':
            return (True, 0)
        # an imminent burst (timer about to hit zero) is treated as nearly
        # active so the agent treats the vent core as a hazard in time.
        return (False, max(1, getattr(dt, 'timer', 50)))
    if k == 'mummy_wrap':
        active = getattr(dt, 'active', False)
        return (active, 0 if active else max(1, getattr(dt, 'timer', 70)))
    if k == 'sarcophagus':
        state = getattr(dt, 'state', 'closed')
        if state in ('opening', 'firing'):
            return (True, 0)
        return (False, max(1, getattr(dt, 'timer', 80)))
    if k == 'gravity_pull':
        active = getattr(dt, 'active', False)
        return (active, 0 if active else max(1, getattr(dt, 'timer', 50)))
    # static traps or unrecognised — always active
    return (True, 0)


def _dtrap_activity_for_tile(kind: str, obs: dict, tx: int, ty: int) -> tuple:
    """Return phase timing for the specific dynamic hazard occupying a tile."""
    if not kind:
        return (True, 0)

    tile_activity = obs.get('dtrap_activity_by_tile', {})
    entry = tile_activity.get((tx, ty))
    if entry is not None:
        ekind, active, ticks = entry
        if ekind == kind:
            return active, ticks

    best = None
    tracked = list(obs.get('dtraps', [])) + list(obs.get('_sim_dtraps', []))
    for dt in tracked:
        if dt.kind != kind:
            continue
        tmp: dict = {}
        _map_dtrap_tiles(dt, tmp)
        if (tx, ty) not in tmp:
            continue
        active, ticks = _dtrap_phase(dt)
        if best is None or active or ticks < best[1]:
            best = (active, ticks)
            if active:
                break
    if best is not None:
        return best

    return obs.get('dtrap_activity', {}).get(kind, (True, 0))


class _SimPlayer:
    """Minimal player stub passed to DynamicTrap.update() and RoamingEnemy.update()
    during forward simulation.  Holds position so seeking/gravity traps behave
    correctly; all damage calls are silently swallowed.
    """
    def __init__(self, x: float, y: float):
        self.x = x; self.y = y
        self.dead = False
        self.death_kind = None
        self.inv = 0
        self.pulse_push = (0.0, 0.0)
        self.pulse_spd_mod = 1.0
    def take_damage(self, dmg, eff=None, lbl=None, col=None, kind=None):
        # the real check_hit() signals a hit by calling take_damage (it does not
        # return a boolean).  previously this was a no-op, so every dynamic-trap
        # hit was silently swallowed and the internal model detected no trap
        # deaths — the death model was effectively blind.  now we mirror the real
        # player.take_damage just enough to register the kill, so consequence
        # checks see exactly the deaths the real game would inflict.
        if self.inv > 0:
            return
        self.dead = True
        self.death_kind = kind


def _sim_player_speed(statuses: dict, pulse_spd_mod: float = 1.0) -> float:
    """Mirror Player.update speed from status slows and pulse modifier."""
    slow = 0.0
    for eff in statuses:
        sd = SDEFS.get(eff)
        if sd:
            slow = max(slow, sd["slow"])
    return Player.SPEED * (1 - slow) * pulse_spd_mod


def _sim_move_body(x: float, y: float, mx: float, my: float,
                   spd: float, grid: list) -> tuple:
    """Axis-separated body movement using the same wall probes as Player.update."""
    ml = math.hypot(mx, my)
    if ml > 0:
        mx /= ml
        my /= ml
    m = PLAYER_WALL_RADIUS

    def blocked(px, py):
        for dx2, dy2 in [(m, 0), (-m, 0), (0, m), (0, -m)]:
            tx2 = int(px + dx2 + .5)
            ty2 = int(py + dy2 + .5)
            if 0 <= tx2 < COLS and 0 <= ty2 < ROWS and grid[ty2][tx2] == 1:
                return True
        return False

    nx = x + mx * spd
    ny = y + my * spd
    if not blocked(nx, y):
        x = nx
    if not blocked(x, ny):
        y = ny
    return x, y


def _map_dtrap_tiles(dt, trap_map: dict) -> None:
    """Write the tiles currently occupied by DynamicTrap *dt* into *trap_map*.
    Extracted from observe() so the same logic can be reused during forward
    simulation without going through the full observe() path.
    """
    k = dt.kind
    if k == 'pendulum_axe':
        # the blade does not sit still — it swings deterministically across the
        # arc [pivot_base - max_angle, pivot_base + max_angle] and back.  marking
        # only the current angle let the planner route through tiles the blade is
        # momentarily clear of but will swing back through, so the agent stepped
        # into the arc and was struck on the return sweep.  mark the whole swept
        # region (every tile any point on the arm passes over across the full
        # swing) so route planning treats the swing as a no-go area; the timed-
        # crossing logic, which uses the exact current angle + phase, still
        # handles dashing through a verified gap when a crossing is unavoidable.
        base = getattr(dt, 'pivot_base', math.pi / 2)
        max_a = getattr(dt, 'max_angle', 0.0)
        a_lo, a_hi = base - max_a, base + max_a
        # sample the arc finely enough that adjacent samples are < 1 tile apart
        # even at the blade tip (arc length ≈ arm_len * angular span).
        span = max(1e-3, a_hi - a_lo)
        n_ang = max(8, int(math.ceil(dt.arm_len * span)) * 2 + 1)
        for ai in range(n_ang + 1):
            a = a_lo + span * (ai / n_ang)
            ca, sa = math.cos(a), math.sin(a)
            for seg in range(11):
                ax = dt.pivot_x + ca * dt.arm_len * (seg / 10)
                ay = dt.pivot_y + sa * dt.arm_len * (seg / 10)
                trap_map.setdefault((int(ax + 0.5), int(ay + 0.5)), k)
    elif k == 'ceiling_crusher':
        w = int(dt.crush_w) + 1
        oy_t = int(dt.oy + 0.5)
        for dxw in range(-w, w + 1):
            trap_map[(int(dt.ox + 0.5) + dxw, oy_t)] = k
    elif k == 'lava_tide':
        tide_tx = int(dt.tide_x + 0.5)
        w = max(1, int(dt.tide_w * 0.7) + 1)
        for dxw in range(-w, w + 1):
            for ry in range(dt.room.y + 1, dt.room.y + dt.room.h - 1):
                trap_map[(tide_tx + dxw, ry)] = k
    elif k == 'ice_sweeper':
        sweep_tx = int(dt.sweep_x + 0.5)
        for ry in range(dt.room.y + 1, dt.room.y + dt.room.h - 1):
            trap_map[(sweep_tx, ry)] = k
    elif k == 'frozen_spike_row':
        if dt.state in ('rising', 'hold') and dt.rise > 0.2:
            for sx, sy in dt.spikes:
                trap_map[(int(sx + 0.5), int(sy + 0.5))] = k
        else:
            trap_map[(int(dt.ox + 0.5), int(dt.oy + 0.5))] = k
    elif k == 'thorn_wall':
        if dt.wall_w > 0.1:
            for wx in range(dt.room.x + 1, int(dt.room.x + 1 + dt.wall_w) + 2):
                for wy in range(dt.room.y + 1, dt.room.y + dt.room.h - 1):
                    trap_map[(wx, wy)] = k
        else:
            trap_map[(int(dt.ox + 0.5), int(dt.oy + 0.5))] = k
    elif k == 'spore_burst':
        if dt.state == 'expanding' and dt.burst_r > 0.5:
            # the real hitbox is an annulus: abs(dist - burst_r) <
            # spore_ring_hit_half_width (see
            # dynamictrap.check_hit / _dtrap_hits_point).  the old code sampled
            # only 16 points around the ring, so at larger radii adjacent
            # samples were >1 tile apart and the lethal band had gaps — the
            # planner stepped "through" the ring and clipped its edge.
            # scan the tiles in the ring's bounding box and mark exactly those
            # whose centre lies in the lethal band: no gaps, no over-marking.
            outer = dt.burst_r + SPORE_RING_HIT_HALF_WIDTH
            r_t = int(math.ceil(outer)) + 1
            ox_t, oy_t = int(round(dt.ox)), int(round(dt.oy))
            _inner_b = dt.burst_r - SPORE_RING_HIT_HALF_WIDTH
            _lo = _inner_b * _inner_b if _inner_b > 0 else -1.0
            _hi = outer * outer
            _ox, _oy = dt.ox, dt.oy
            for dxs in range(-r_t, r_t + 1):
                tx = ox_t + dxs
                _ex = _ox - tx
                _ex2 = _ex * _ex
                for dys in range(-r_t, r_t + 1):
                    ty = oy_t + dys
                    _ey = _oy - ty
                    d2 = _ex2 + _ey * _ey
                    if _lo < d2 < _hi:
                        trap_map.setdefault((tx, ty), k)
        elif dt.state == 'wait' and getattr(dt, 'timer', 99) <= 12:
            # a burst is about to begin and will sweep outward from the origin.
            # the expanding annulus first becomes lethal once burst_r > 0.5, so
            # within ~step_ticks of activation any tile within ~1.3 of the
            # centre will be swept.  mark that core so the planner never parks
            # the agent on top of a spore vent that is about to fire — the old
            # map left this region empty during 'wait', so the agent could be
            # standing on the vent when it erupted.
            ox_t, oy_t = int(round(dt.ox)), int(round(dt.oy))
            for dxs in range(-2, 3):
                for dys in range(-2, 3):
                    if math.hypot(dxs, dys) <= 1.4:
                        trap_map.setdefault((ox_t + dxs, oy_t + dys), k)
    elif k == 'mummy_wrap':
        # anchor is always lethal-adjacent; the active projectile tile too.
        ox_t, oy_t = int(dt.ox + 0.5), int(dt.oy + 0.5)
        trap_map[(ox_t, oy_t)] = k
        if getattr(dt, 'active', False):
            # mark the live dart and its full remaining straight-line flight
            # path: the dart travels at 0.10 u/tick (the player's own speed) in
            # a fixed direction until it leaves the floor or its travel distance
            # from the anchor exceeds the launch range, so any tile on that line
            # is lethal to step into.  marking only the current tile let the
            # agent walk through the airborne dart's path several tiles ahead of
            # it and die (observed: mid-flight mummy_wrap kills).
            px_t, py_t = int(dt.px + 0.5), int(dt.py + 0.5)
            trap_map[(px_t, py_t)] = k
            spd = math.hypot(getattr(dt, 'vx', 0.0), getattr(dt, 'vy', 0.0))
            if spd > 1e-6:
                ux, uy = dt.vx / spd, dt.vy / spd
                # dist>9 from anchor → dart expires
                MW_DEACTIVATE_DIST = 9
                fx, fy = dt.px, dt.py
                # cap iterations; one tile per ~10 steps
                for _ in range(64):
                    fx += ux; fy += uy
                    if math.hypot(fx - dt.ox, fy - dt.oy) > MW_DEACTIVATE_DIST:
                        break
                    trap_map.setdefault((int(fx + 0.5), int(fy + 0.5)), k)
        else:
            # dormant-phase forecast (sim-bug fix): when the timer expires the
            # mummy_wrap fires a homing dart from the anchor straight at the
            # player's then-current position.  the dart travels at 0.10 u/tick
            # — exactly the player's speed — so within a few tiles of the anchor
            # there is no time to clear the firing line and a launch is an
            # unavoidable point-blank hit.  beyond that the player can sidestep,
            # so we only fence off the close-range no-reaction disc rather than
            # the full flight range (which would wall off whole rooms and trade
            # deaths for timeouts).  without this the dormant trap read as
            # harmless and the agent walked into range — the predictable deaths.
            MW_NO_REACTION_R = 2
            for dxg in range(-MW_NO_REACTION_R, MW_NO_REACTION_R + 1):
                for dyg in range(-MW_NO_REACTION_R, MW_NO_REACTION_R + 1):
                    if math.hypot(dxg, dyg) <= MW_NO_REACTION_R:
                        trap_map.setdefault((ox_t + dxg, oy_t + dyg), k)
    elif k == 'sarcophagus':
        trap_map[(int(dt.ox + 0.5), int(dt.oy + 0.5))] = k
        for shot in dt.shots:
            trap_map[(int(shot[0] + 0.5), int(shot[1] + 0.5))] = k
    elif k == 'gravity_pull':
        trap_map[(int(dt.ox + 0.5), int(dt.oy + 0.5))] = k
        if dt.active:
            r = int(dt.pull_r) + 1
            ox_t, oy_t = int(dt.ox + 0.5), int(dt.oy + 0.5)
            for dxg in range(-r, r + 1):
                for dyg in range(-r, r + 1):
                    if math.hypot(dxg, dyg) <= dt.pull_r:
                        trap_map[(ox_t + dxg, oy_t + dyg)] = k
    elif k == 'fire_bar':
        # the arms rotate a full 360° (angle += speed every tick, unbounded), so
        # over one revolution every tile within arm_len of the hub is swept.
        # marking only the current orientation let the planner route through the
        # part of the disc the bar was momentarily clear of, and the spinning bar
        # rotated into it.  mark the whole swept disc so routing treats the spin
        # as a no-go area; the timed-crossing logic still handles a dash through
        # the rotating gap using the exact current angle.
        ox_t, oy_t = int(dt.ox + 0.5), int(dt.oy + 0.5)
        reach = dt.arm_len
        r = int(math.ceil(reach)) + 1
        for dxg in range(-r, r + 1):
            for dyg in range(-r, r + 1):
                if dxg * dxg + dyg * dyg <= reach * reach:
                    trap_map.setdefault((ox_t + dxg, oy_t + dyg), k)
    elif k == 'ice_beam':
        # dual beams rotate a full 360° just like fire_bar, sweeping the entire
        # disc of radius beam_len around the hub.  same fix: mark the swept disc.
        ox_t, oy_t = int(dt.ox + 0.5), int(dt.oy + 0.5)
        reach = dt.beam_len
        r = int(math.ceil(reach)) + 1
        for dxg in range(-r, r + 1):
            for dyg in range(-r, r + 1):
                if dxg * dxg + dyg * dyg <= reach * reach:
                    trap_map.setdefault((ox_t + dxg, oy_t + dyg), k)
    elif k in ('rolling_boulder', 'mummy_wrap', 'mirror_clone'):
        trap_map[(int(dt.ox + 0.5), int(dt.oy + 0.5))] = k
        trap_map[(int(dt.px + 0.5), int(dt.py + 0.5))] = k
    else:
        trap_map[(int(dt.ox + 0.5), int(dt.oy + 0.5))] = k


def _enemy_tiles_from_list(enemies) -> set:
    """Build an enemy_tiles set from a list of RoamingEnemy (or _SimPlayer) objects."""
    tiles: set = set()
    for e in enemies:
        ex, ey = int(e.x + 0.5), int(e.y + 0.5)
        tiles.add((ex, ey))
        for ddx, ddy in ((1,0),(-1,0),(0,1),(0,-1)):
            tiles.add((ex+ddx, ey+ddy))
    return tiles


def _enemy_hits_point(enemy, x: float, y: float, margin: float = PLAYER_HIT_RADIUS) -> bool:
    """Exact circular collision check used by the forward model."""
    return math.hypot(enemy.x - x, enemy.y - y) < getattr(enemy, "RADIUS", 0.45) + margin


def _dtrap_hits_point(dt, x: float, y: float, margin: float = PLAYER_HIT_RADIUS) -> bool:
    """Approximate DynamicTrap.check_hit() against an arbitrary simulated point.

    Tile occupancy is too coarse for thin/rotating hazards such as fire bars and
    beams: they can clip the player's body while never owning the rounded target
    tile at a sampled endpoint.  This mirrors the draw/check geometry closely
    enough for planning without mutating cooldowns or the real player.
    """
    k = dt.kind
    if k == "pendulum_axe":
        if math.hypot(dt.px - x, dt.py - y) < PLAYER_HIT_RADIUS + 0.14:
            return True
        _ca = math.cos(dt.angle) * dt.arm_len
        _sa = math.sin(dt.angle) * dt.arm_len
        _thr = PLAYER_HIT_RADIUS + THIN_HAZARD_HALF_WIDTH
        for seg in range(12):
            t2 = seg / 11
            ax = dt.pivot_x + _ca * t2
            ay = dt.pivot_y + _sa * t2
            if math.hypot(ax - x, ay - y) < _thr:
                return True
    elif k == "ceiling_crusher":
        return (dt.state in ("dropping", "down") and
                abs(x - dt.ox) < dt.crush_w and
                abs(y - dt.py) < 0.6)
    elif k == "lava_tide":
        rm = dt.room
        # real check_hit: abs(player.x - tide_x) < tide_w * 0.7  (no extra margin —
        # the constant already folds in the combined player+tide half-widths).
        # a small fixed buffer (+0.10) keeps planning slightly conservative without
        # blocking corridors that are safe in reality.
        return (rm.y + 1 <= y <= rm.y + rm.h - 2 and
                abs(x - dt.tide_x) < dt.tide_w * 0.7)
    elif k == "rolling_boulder":
        _r = dt.radius + PLAYER_HIT_RADIUS
        _ddx = dt.px - x; _ddy = dt.py - y
        return _ddx * _ddx + _ddy * _ddy < _r * _r
    elif k == "ice_sweeper":
        rm = dt.room
        # real check_hit: abs(player.x - sweep_x) < 0.55  (combined radius built in).
        # old sim used 0.55 + margin (0.42) = 0.97 — nearly 2× reality, blocking
        # corridors that are genuinely passable and causing the agent to deadlock
        # waiting for a "gap" that the real game already considers safe.
        return (rm.y + 1 <= y <= rm.y + rm.h - 2 and
                abs(x - dt.sweep_x) < PLAYER_HIT_RADIUS + 0.18)
    elif k == "frozen_spike_row":
        if dt.state in ("rising", "hold") and dt.rise > 0.3:
            return any(math.hypot(sx - x, sy - y) < PLAYER_HIT_RADIUS + 0.14
                       for sx, sy in dt.spikes)
    elif k == "thorn_wall":
        if dt.wall_w > 0.2:
            rm = dt.room
            return (rm.x + 1 <= x <= rm.x + 1 + dt.wall_w and
                    rm.y + 1 <= y <= rm.y + rm.h - 2)
    elif k == "spore_burst":
        if dt.state == "expanding" and dt.burst_r > 0.5:
            d = math.hypot(dt.ox - x, dt.oy - y)
            return abs(d - dt.burst_r) < SPORE_RING_HIT_HALF_WIDTH
    elif k == "mummy_wrap":
        return dt.active and math.hypot(dt.px - x, dt.py - y) < PLAYER_HIT_RADIUS + 0.14
    elif k == "sarcophagus":
        return any(math.hypot(shot[0] - x, shot[1] - y) < PLAYER_HIT_RADIUS + SMALL_PROJECTILE_RADIUS
                   for shot in dt.shots)
    elif k == "gravity_pull":
        return dt.active and math.hypot(dt.ox - x, dt.oy - y) < PLAYER_HIT_RADIUS
    elif k == "mirror_clone":
        return math.hypot(dt.px - x, dt.py - y) < PLAYER_HIT_RADIUS + 0.14
    elif k == "fire_bar":
        _thr = PLAYER_HIT_RADIUS + THIN_HAZARD_HALF_WIDTH
        # cheap bounding-circle reject: nothing on any arm can be closer than
        # (dist-from-hub − arm_len), so skip the per-segment scan when the point
        # is clearly outside the swept disc.
        if math.hypot(dt.ox - x, dt.oy - y) > dt.arm_len + _thr:
            return False
        for arm in range(dt.n_arms):
            ba = dt.angle + arm * math.pi
            _ca = math.cos(ba) * dt.arm_len
            _sa = math.sin(ba) * dt.arm_len
            for seg in range(24):
                t2 = seg / 23
                ax = dt.ox + _ca * t2
                ay = dt.oy + _sa * t2
                if math.hypot(ax - x, ay - y) < _thr:
                    return True
    elif k == "ice_beam":
        _thr = PLAYER_HIT_RADIUS + THIN_HAZARD_HALF_WIDTH
        if math.hypot(dt.ox - x, dt.oy - y) > dt.beam_len + _thr:
            return False
        _cb = math.cos(dt.angle) * dt.beam_len
        _sb = math.sin(dt.angle) * dt.beam_len
        for sign in (1, -1):
            _cs, _ss = _cb * sign, _sb * sign
            for seg in range(24):
                t2 = seg / 23
                bx = dt.ox + _cs * t2
                by = dt.oy + _ss * t2
                if math.hypot(bx - x, by - y) < _thr:
                    return True
    return False


def _dtrap_ticks_to_hit(dt, x: float, y: float, max_ticks: int = 30) -> int | None:
    """Predict ticks until dynamic trap geometry intersects a stationary point.

    This gives expectation formation a timing fact for traps whose dangerous
    geometry is not well represented by a tile map: rotating fire/ice arms and
    the expanding spore ring. It runs on a clone so it never mutates reality.
    """
    cl = _clone_dtrap(dt)
    stub = _SimPlayer(x, y)
    if _dtrap_hits_point(cl, x, y):
        return 0
    for tick in range(1, max_ticks + 1):
        cl.update(stub)
        if _dtrap_hits_point(cl, x, y):
            return tick
    return None


def _dynamic_motion_fluents(dt) -> set:
    """Physical timing/geometry fluents for dynamic hazards."""
    k = dt.kind
    out = set()
    if k in ("fire_bar", "ice_beam", "pendulum_axe"):
        out.add(Fluent("RotatingHazard"))
    if k == "spore_burst":
        out.add(Fluent("ExpandingRing"))
        if getattr(dt, "state", None) == "expanding":
            out.add(Fluent("TrapExpanding"))
    if hasattr(dt, "timer"):
        timer = max(0, int(getattr(dt, "timer", 0)))
        if timer <= 10:
            out.add(Fluent("TimerSoon"))
        elif timer <= 30:
            out.add(Fluent("TimerMedium"))
        else:
            out.add(Fluent("TimerLong"))
    return out


def _clone_dtrap(dt):
    """Shallow-copy a DynamicTrap, deep-copying only its mutable list attributes.
    room and grid are intentionally shared (read-only during simulation).
    """
    cl = copy.copy(dt)
    if hasattr(dt, 'trail'):  cl.trail  = list(dt.trail)
    if hasattr(dt, 'shots'):  cl.shots  = [list(s) for s in dt.shots]
    if hasattr(dt, 'spikes'): cl.spikes = list(dt.spikes)
    # shallow copy shares the private re-arm rng by reference; a rollout that
    # advances the clone would otherwise consume the real hazard's stream and
    # break cross-agent reproducibility.  give the clone an independent rng
    # snapshot (same current state, separate object) so imagined futures never
    # disturb the real hazard.
    if hasattr(dt, 'rng'):    cl.rng    = copy.deepcopy(dt.rng)
    return cl


import zlib as _zlib


def _stable_hash(*parts) -> int:
    """A process-independent 31-bit hash.

    Python's built-in hash() is randomised per process (PYTHONHASHSEED), so it
    can NOT be used to derive reproducible seeds — two runs would diverge.  This
    folds a stable string rendering of the arguments through CRC32, which is
    fixed across processes and platforms.
    """
    s = "|".join(repr(p) for p in parts)
    return _zlib.crc32(s.encode("utf-8")) & 0x7FFFFFFF


def _sim_update_dtrap(dt, player):
    """Advance a cloned DynamicTrap without consuming the real world's RNG.

    Several DynamicTrap.update() branches call random.* when a cycle re-arms.
    Rollouts must not perturb the global RNG stream, or merely thinking about
    futures changes the generated maze/trap/enemy sequence.
    """
    rng_state = random.getstate()
    try:
        dt.update(player)
    finally:
        random.setstate(rng_state)


def _clone_enemy(e):
    """Shallow-copy a RoamingEnemy — all mutable state is primitive values.

    The private re-arm RNG is deep-copied so a rollout advancing the clone can
    never consume the real enemy's stream (which would break reproducibility).
    """
    cl = copy.copy(e)
    if hasattr(e, 'rng'):
        cl.rng = copy.deepcopy(e.rng)
    return cl


def _sim_update_enemy(e):
    """Deterministic enemy update for rollouts.

    Real enemies pick random new waypoints when they arrive.  The forward model
    should not consume global randomness or hallucinate a precise new waypoint,
    so simulated enemies continue their current leg and then pause.
    """
    if getattr(e, "wait", 0) > 0:
        e.wait -= 1
        return

    dx = e.waypoint[0] - e.x
    dy = e.waypoint[1] - e.y
    dist = math.hypot(dx, dy)
    if dist < 0.25:
        e.wait = 30
        return

    nx = e.x + (dx / dist) * e.spd
    ny = e.y + (dy / dist) * e.spd

    grid = e.grid
    ex, ey = e.x, e.y

    # inline floor test (was a per-call closure): does any body corner overlap a
    # wall tile?  unrolled over the 4 fixed offsets and short-circuited.
    ok_x = True
    for odx, ody in _ENEMY_BODY_OFFSETS:
        tx2 = int(nx + odx); ty2 = int(ey + ody)
        if not (0 <= tx2 < COLS and 0 <= ty2 < ROWS) or grid[ty2][tx2] == 1:
            ok_x = False
            break
    if ok_x:
        e.x = nx
        ex = nx

    ok_y = True
    for odx, ody in _ENEMY_BODY_OFFSETS:
        tx2 = int(ex + odx); ty2 = int(ny + ody)
        if not (0 <= tx2 < COLS and 0 <= ty2 < ROWS) or grid[ty2][tx2] == 1:
            ok_y = False
            break
    if ok_y:
        e.y = ny


class InternalWorldModel:
    """A standalone, forkable simulation of the agent-in-its-world.

    This is the Internal Model of the architecture diagram made concrete: a
    single coherent World Model (grid + dynamic traps + roaming enemies) plus
    a Robot Model (the simulated body, _SimPlayer).  Unlike the previous
    one-ply consequence check — which read hazards piecemeal from obs and asked
    "does THIS one given step hurt?" — this object can be FORKED and STEPPED
    FORWARD repeatedly, so a copy of the Robot Controller can drive the body
    through it for several plies, generating and testing whole action sequences
    before any physical commitment (Winfield's recursive internal simulation).

    The bidirectional Robot-Controller <-> World-Model coupling in the diagram
    is realised by `rollout()`: at each ply it asks a supplied controller-policy
    for the next action GIVEN the current internal state, applies it to the
    body, advances the world, and feeds the resulting state back to the policy
    for the next ply.  The Consequence Engine then judges the trajectory.

    RNG-safety: trap/enemy updates here never consume the global RNG stream
    (they go through _sim_update_dtrap / _sim_update_enemy), so imagining
    futures never perturbs the real maze/trap/enemy generation.
    """

    __slots__ = ("grid", "body", "dtraps", "enemies", "statuses", "t")

    def __init__(self, grid, body, dtraps, enemies, statuses=None, t=0):
        self.grid     = grid
        # _simplayer
        self.body     = body
        # list[cloned dynamictrap]
        self.dtraps   = dtraps
        # list[cloned roamingenemy]
        self.enemies  = enemies
        self.statuses = dict(statuses or {})
        self.t        = t

    @classmethod
    def from_observation(cls, grid, ptx, pty, dtraps, enemies, statuses=None,
                         t=0, px=None, py=None):
        """Build an internal world seeded from the agent's current perception
        (the Object Tracker-Localiser output)."""
        body = _SimPlayer(px if px is not None else ptx,
                          py if py is not None else pty)
        return cls(grid,
                   body,
                   [_clone_dtrap(d) for d in dtraps],
                   [_clone_enemy(e) for e in enemies],
                   statuses, t)

    def fork(self):
        """Return an independent copy so a candidate action sequence can be
        explored without disturbing the parent world (branching the rollout)."""
        nb = _SimPlayer(self.body.x, self.body.y)
        nb.dead          = self.body.dead
        nb.inv           = self.body.inv
        nb.pulse_push    = self.body.pulse_push
        nb.pulse_spd_mod = self.body.pulse_spd_mod
        return InternalWorldModel(
            self.grid, nb,
            [_clone_dtrap(d) for d in self.dtraps],
            [_clone_enemy(e) for e in self.enemies],
            self.statuses, self.t)

    def _body_lethal_here(self):
        """Consequence test for the body's current position: does any trap or
        enemy overlap it right now?  Mirrors the real check_hit geometry."""
        bx, by = self.body.x, self.body.y
        # the real check_hit() does not return a hit flag — it registers a hit by
        # calling player.take_damage(), which (on _simplayer) sets body.dead and
        # body.death_kind.  so we clear the flag, run each trap's real check_hit
        # against the body, and read back whether it killed us.  this makes the
        # internal model's lethality identical to the real game's for every kind.
        self.body.dead = False
        self.body.death_kind = None
        for dt in self.dtraps:
            # check_hit uses a per-player hit cooldown keyed on id(player); make
            # sure the imagined body is never on cooldown so a real overlap is
            # always detected during a rollout.
            try:
                if hasattr(dt, 'hit_cd'):
                    dt.hit_cd.pop(id(self.body), None)
            except Exception:
                pass
            try:
                dt.check_hit(self.body)
            except Exception:
                # trap assumed a real-player attribute; fall back to overlap.
                if abs(getattr(dt, "ox", 1e9) - bx) < 0.6 and \
                   abs(getattr(dt, "oy", 1e9) - by) < 0.6:
                    return dt.kind
            if self.body.dead:
                return self.body.death_kind or dt.kind
        for e in self.enemies:
            try:
                if isinstance(getattr(e, 'hit_cd', None), dict):
                    e.hit_cd.pop(id(self.body), None)
                else:
                    # enemy cooldown is an int
                    e.hit_cd = 0
            except Exception:
                pass
            try:
                e.check_hit(self.body)
            except Exception:
                if math.hypot(e.x - bx, e.y - by) < ENEMY_HIT_RADIUS + PLAYER_HIT_RADIUS:
                    return "enemy"
            if self.body.dead:
                return self.body.death_kind or "enemy"
        return None

    def step_world(self):
        """Advance every world entity one controller-tick (the World Model
        running forward), without moving the body."""
        for dt in self.dtraps:
            _sim_update_dtrap(dt, self.body)
        for e in self.enemies:
            _sim_update_enemy(e)
        self.t += 1

    def apply_action(self, dx, dy, frame_sink=None):
        """Drive the Robot Model: move the simulated body one tile-step worth of
        travel over STEP_TICKS sub-ticks, advancing the world each sub-tick and
        reporting the first lethal contact encountered en route (so a hazard
        sweeping across the path mid-transit is caught, not just the endpoint).

        If frame_sink is a list, a snapshot is appended EVERY sub-tick (not just
        once per ply), so the visualisation interpolates between small per-tick
        steps and the imagined hazards move smoothly instead of jumping a whole
        ply of motion at once (the source of the unsmooth rotation/sweep)."""
        spd = _sim_player_speed(self.statuses, self.body.pulse_spd_mod)
        steps = max(1, int(round(1.0 / max(spd, 1e-6))))
        tx, ty = self.body.x + dx, self.body.y + dy
        hit = None
        for _ in range(steps):
            nx, ny = _sim_move_body(self.body.x, self.body.y, dx, dy,
                                    spd, self.grid)
            self.body.x, self.body.y = nx, ny
            self.step_world()
            if frame_sink is not None:
                frame_sink.append(self._snapshot())
            k = self._body_lethal_here()
            if k is not None:
                hit = k
                self.body.dead = True
                break
            if abs(self.body.x - tx) < 0.06 and abs(self.body.y - ty) < 0.06:
                # arrived at the target tile centre: snap exactly so the next
                # ply's route-following sees a clean tile-aligned position.
                self.body.x, self.body.y = tx, ty
                if frame_sink is not None:
                    frame_sink[-1] = self._snapshot()
                break
        return hit

    def _snapshot(self):
        """Capture a lightweight visual record of the imagined world this ply:
        body position plus each trap's drawable geometry, so a side panel can
        replay how the agent PICTURES the hazards moving during its rollout."""
        traps = []
        for dt in self.dtraps:
            # capture the trap's true lethal-tile footprint using the same mapper
            # the agent reasons with (_map_dtrap_tiles).  this guarantees every
            # trap kind — column crushers, lava tides, sweepers, projectiles,
            # rings, rotating bars — is drawn with its real danger geometry,
            # rather than relying on a per-kind draw branch that silently omits
            # kinds it doesn't recognise (the "missing traps" symptom).
            fp = {}
            try:
                _map_dtrap_tiles(dt, fp)
            except Exception:
                fp = {}
            # activation countdown: ticks until this trap next enters its
            # dangerous phase (0 if already active).  this is the timing the
            # agent's dynamicsmodel learns from observation; surfacing it as a
            # countdown shows what the internal model "expects" about when each
            # hazard will trigger.
            try:
                ph_active, ph_ticks = _dtrap_phase(dt)
            except Exception:
                ph_active, ph_ticks = True, 0
            rec = {'kind': dt.kind,
                   'ox': getattr(dt, 'ox', None), 'oy': getattr(dt, 'oy', None),
                   'px': getattr(dt, 'px', None), 'py': getattr(dt, 'py', None),
                   'angle': getattr(dt, 'angle', None),
                   'arm_len': getattr(dt, 'arm_len', getattr(dt, 'beam_len', None)),
                   'burst_r': getattr(dt, 'burst_r', None),
                   'state': getattr(dt, 'state', None),
                   'active': getattr(dt, 'active', None),
                   'n_arms': getattr(dt, 'n_arms', None),
                   'pivot_x': getattr(dt, 'pivot_x', None),
                   'pivot_y': getattr(dt, 'pivot_y', None),
                   'footprint': list(fp.keys()),
                   'cd_active': bool(ph_active),
                   'cd_ticks': int(ph_ticks),
                   'shots': [(s[0], s[1]) for s in getattr(dt, 'shots', [])
                             ] if getattr(dt, 'shots', None) else None,
                   'crush_w': getattr(dt, 'crush_w', None),
                   'raised_frac': getattr(dt, 'raised_frac', None),
                   'rise': getattr(dt, 'rise', None),
                   'spikes': list(getattr(dt, 'spikes', []))
                             if getattr(dt, 'spikes', None) else None,
                   'row_y': getattr(dt, 'row_y', None)}
            traps.append(rec)
        # each imagined enemy carries an 'unknown' flag: true once it has reached
        # its current waypoint and entered the wait phase, i.e. the point where
        # its next move is randomly chosen and therefore not predictable by the
        # internal model.  the panel renders these dimmed/with a marker so it is
        # visually clear the model is being honestly agnostic — it predicts the
        # observable current leg, then stops claiming to know the random future.
        enemies = [(e.x, e.y, bool(getattr(e, 'wait', 0) > 0)) for e in self.enemies]
        return {'body': (self.body.x, self.body.y),
                'traps': traps, 'enemies': enemies}

    def rollout(self, policy, plies, branch=True, record=False):
        """Recursive internal simulation: a copy of the Robot Controller
        (`policy`) drives the body through this world for up to `plies` steps.

        policy(world) -> (dx, dy) | None         (None ⇒ hold / no move)
        Returns a dict trajectory summary for the Consequence Engine:
            {'plies', 'died', 'death_ply', 'death_kind', 'path', 'reached_goal'}
        If record=True, also returns 'frames': a per-ply list of imagined-world
        snapshots for visualisation.

        This closes the Robot-Controller <-> World-Model loop the diagram shows:
        the controller picks an action GIVEN the imagined state, the action acts
        ON the world model, and the resulting state feeds back for the next ply.
        """
        w = self.fork() if branch else self
        path = [(w.body.x, w.body.y)]
        frames = [w._snapshot()] if record else None
        died = False
        death_ply = -1
        death_kind = None
        # index into `frames` (sub-tick res)
        death_frame = -1
        for ply in range(plies):
            action = policy(w)
            if action is None:
                # holding: still advance the world (a sweeping hazard can reach
                # a stationary body) and consequence-check the held tile.
                w.step_world()
                if record: frames.append(w._snapshot())
                if w._body_lethal_here() is not None:
                    died = True; death_ply = ply
                    death_kind = w._body_lethal_here()
                    if record: death_frame = len(frames) - 1
                    break
                path.append((w.body.x, w.body.y))
                continue
            dx, dy = action
            # sub-tick frame capture for smooth playback (every controller tick,
            # not just once per ply).
            kind = w.apply_action(dx, dy, frame_sink=frames if record else None)
            path.append((w.body.x, w.body.y))
            if kind is not None:
                died = True; death_ply = ply; death_kind = kind
                if record: death_frame = len(frames) - 1
                break
        result = {
            'plies': len(path) - 1,
            'died': died,
            'death_ply': death_ply,
            'death_kind': death_kind,
            'path': path,
            'final': (w.body.x, w.body.y),
        }
        if record:
            result['frames'] = frames
            result['death_frame'] = death_frame
        return result


def _rule_has_specific_motion_context(rule: 'EECTemporalRule') -> bool:
    """True when a reused rule is specific enough for moving scenes.

    For fast-expanding hazards (spore ring) danger rules are only trustworthy
    when they also carry contact-timing fluents (TrapContactNow / TrapContactSoon).
    Without timing the rule was almost certainly formed from a transit-hit
    *endpoint* state where the ring had already swept past the target tile —
    the fluents no longer locate the ring relative to the tile, so reusing
    that verdict would block movement even when the path is genuinely clear.
    Forcing a fresh simulation in those cases costs a rollout but prevents the
    agent from freezing in place for the entire duration of a spore expansion.
    """
    names = {f.name for f in rule.preconditions}
    # expandingring / trapexpanding without contact-timing → too broad to reuse
    if (names & {"ExpandingRing", "TrapExpanding"}
            and not (names & {"TrapContactNow", "TrapContactSoon"})):
        return False
    return bool(names & {
        "MovingHazard", "DynamicHazard", "TrapActive", "TrapImminent",
        "TrapInactive", "PredictedCollision", "CollisionPath",
        "TrapContactNow", "TrapContactSoon", "TrapContactLater",
        "RotatingHazard", "ExpandingRing", "TrapExpanding",
        "TimerSoon", "TimerMedium", "TimerLong",
        "EnemyNearby", "HeavyImpact", "HighTemperature", "LowTemperature",
        "Toxic", "Constricting", "Unstable", "Corrupting",
    })


_PHASE_SAFE_ANCHORS = {"TrapInactive", "TrapContactLater", "TimerLong"}
_MOTION_TIMING_FLUENTS = {
    "MovingHazard", "DynamicHazard", "TrapActive", "TrapImminent",
    "TrapInactive", "PredictedCollision", "CollisionPath", "TrapContactNow",
    "TrapContactSoon", "TrapContactLater", "RotatingHazard",
    "ExpandingRing", "TrapExpanding", "TimerSoon", "TimerMedium", "TimerLong",
}


def _safe_verdict_is_stale_risky(rule, tile_fluents) -> bool:
    """Decide whether a SAFE memory verdict could have gone stale.

    The old guard voided EVERY safe verdict whenever any dynamic object existed
    anywhere in the scene — discarding ~95% of correct safe reuse and forcing
    needless re-simulation.  A safe verdict is only stale-risky when the TILE
    BEING EVALUATED actually carries a moving/timed hazard whose phase could
    have changed since the rule was formed.  Two cases keep the verdict:

      1. No motion/timing fluent on the tile at all → the rule rests on static
         structure (or empty floor); phase staleness is impossible.
      2. The rule is phase-ANCHORED on a dormant condition (TrapInactive etc.)
         that is observed only when the hazard is > STEP_TICKS from activating,
         and the verdict is consumed one step later — the trap cannot reach its
         active phase inside that window, so a Wilson-licensed dormant-phase
         safe rule is as sound as the simulation it would replace.
    """
    tile_names = {f.name for f in tile_fluents}
    # the spore ring's lethal position is a pure function of its fast-growing
    # radius (≈1.2 tiles/step).  a per-tile safe snapshot can therefore be
    # outrun by the ring before the agent arrives, so a safe verdict on any
    # expanding-ring context must never shortcut the internal model — force a
    # fresh rollout that advances the actual ring geometry.
    if tile_names & {"ExpandingRing", "TrapExpanding"}:
        return True
    if not (tile_names & _MOTION_TIMING_FLUENTS):
        # case 1: no live motion/timing here
        return False
    rule_names = {f.name for f in rule.preconditions}
    if rule_names & _PHASE_SAFE_ANCHORS:
        # case 2: phase-anchored dormant rule
        return False
    return True


def _rule_label(rule: 'EECTemporalRule') -> str:
    """Compact single-line label for a rule, used in the side panel."""
    ev = ""
    if rule.event:
        ev = rule.event.name
        if rule.event.args:
            dmap = {(1,0):"R",(-1,0):"L",(0,-1):"U",(0,1):"D"}
            ev += "(" + (dmap.get(rule.event.args) or ",".join(str(a) for a in rule.event.args)) + ")"
    pre_parts = []
    for f in rule.preconditions:
        if f.args:
            pre_parts.append(f"{f.name}({f.args[0]})")
        else:
            pre_parts.append(f.name)
    pre = "+".join(pre_parts) if pre_parts else "—"
    eff = rule.effect.name
    if rule.effect.args:
        eff += f"({rule.effect.args[0]})"
    arrow = "→" if rule.effect_type == "Initiates" else "⊘"
    if ev:
        return f"{ev} ∧ {pre} {arrow} {eff}"
    return f"{pre} {arrow} {eff}"


class ExpectationMemory:
    """Stores EECTemporalRule objects; implements paper's Algorithm 1 (form) and
    Algorithm 2 (delta-rule update + generalise + prune).

    Unified with EECReasoner: every rule (innate AND learned) lives here, so
    eqs. 2-4 apply uniformly — innate priors are revisable (Popperian), and the
    reasoner shares the same rule objects by reference.

    Indexing: rules are indexed (a) structurally for O(1) de-duplication in
    form(), and (b) by (effect_type, effect.name) so outcome queries scan only
    Damaged/Safe rules instead of the whole rule base.
    """

    # base learning rate (modulated by evidence weight)
    K              = 0.18
    # prune when c(e) < τ_prune  (eq. 4)
    TAU_PRUNE      = 0.08
    # generalise at τ_generalise confirmations (eq. 5)
    TAU_GENERALISE = 2
    # ── evidence-quality weighting (refinement 1 & 2) ────────────────────────
    # the delta-rule step is k·w, where w ∈ (0,1] reflects how informative the
    # triggering observation is.  this keeps eqs. 2-3 intact (k is the paper's
    # adjustable rate) while letting confidence converge to a quality-weighted
    # reliability rather than a raw count.
    # third-person (observed) evidence vs first-person
    VICARIOUS_WEIGHT = 0.5
    # floor so a weak match still moves confidence a little
    MIN_EVIDENCE_W   = 0.25
    # share of parent confirmations a generalised rule keeps
    GENERALISE_INHERIT = 0.5
    # staleness half-life (game ticks).  under reloc_on_reentry the hazard map
    # is non-stationary, so a learned rule's effective confidence decays toward
    # zero as it goes unobserved: c_eff(e, t) = c(e) · 0.5^((t − t_obs)/t½).
    # innate rules are exempt (embodiment constraints don't go stale).
    STALENESS_HALF_LIFE = 1800

    def __init__(self):
        self.rules: list = []
        # id(rule) for o(1) membership tests
        self._ids:  set  = set()
        # structural key → rule (o(1) _find)
        self._index: dict = {}
        # (effect_type, effect.name) → [rules]
        self._by_effect: dict = {}
        # simulation runs that produced a new result
        self.sims_run             = 0
        # evaluate() calls answered by memory
        self.sims_skipped         = 0
        # mid-transit sweep detections (not endpoint)
        self.transit_hits         = 0
        # times simulation/feedback was converted to eec
        self.expectation_forms    = 0
        # candidate eec rules proposed before de-duplication
        self.rule_attempts        = 0
        # total rules ever added (all origins)
        self.expectations_created = 0
        # rules from generalisation + popperian surprise
        self.rules_derived        = 0
        # danger rules confirmed by observing other entities
        self.vicarious_confirms   = 0
        # injected by peagent after construction
        self._eec_reasoner        = None
        # unique (t, label, confidence, source)
        self.reused_log: deque    = deque(maxlen=10)
        # learned causal-relevance model — replaces hand-written precondition
        # whitelists.  shared by simulation formation, real feedback, and
        # vicarious observation so all evidence streams feed one causal model.
        self.causal               = CausalLedger()
        self.calibration          = SensorCalibration()
        # fluents screened out of rules by δp
        self.preconds_dropped     = 0
        # verdicts from graded (non-exact) matches
        self.partial_reuses       = 0
        # ── reuse-failure diagnostics (why is the internal model still running?) ─
        # query_outcome: no rule matched at all
        self.diag_no_candidate    = 0
        # matched but failed wilson reliability gate
        self.diag_gate_blocked    = 0
        # matched, passed gate, but c_eff ≤ threshold
        self.diag_thresh_blocked  = 0
        # query_outcome returned a verdict
        self.diag_answered        = 0
        # safe verdict discarded by staleness guard
        self.diag_safe_voided     = 0
        # danger verdict discarded (no motion context)
        self.diag_danger_voided   = 0
        # per-aspect/entity expectations formed
        self.factored_rules       = 0
        # children from violation-driven refinement
        self.specialisations      = 0

    # ── structural key / index maintenance ────────────────────────────────────
    @staticmethod
    def _rule_key(event, preconditions, effect_type, effect, delay):
        return (event,
                tuple(sorted(preconditions, key=lambda f: (f.name, f.args))),
                effect_type, effect, delay)

    def _register(self, rule: EECTemporalRule):
        self.rules.append(rule)
        self._ids.add(id(rule))
        self._index[self._rule_key(rule.event, rule.preconditions,
                                   rule.effect_type, rule.effect, rule.delay)] = rule
        self._by_effect.setdefault((rule.effect_type, rule.effect.name),
                                   []).append(rule)

    def _unregister(self, rule: EECTemporalRule):
        self._ids.discard(id(rule))
        self._index.pop(self._rule_key(rule.event, rule.preconditions,
                                       rule.effect_type, rule.effect, rule.delay),
                        None)
        bucket = self._by_effect.get((rule.effect_type, rule.effect.name))
        if bucket is not None and rule in bucket:
            bucket.remove(rule)
        if rule in self.rules:
            self.rules.remove(rule)
        self._remove_rule_from_reasoner(rule)

    # ── staleness-weighted confidence (read-only; never mutates c(e)) ────────
    def effective_confidence(self, rule: EECTemporalRule, t: int | None = None) -> float:
        if t is None or rule.origin == "innate":
            return rule.confidence
        age = max(0, t - rule.last_observed_time)
        if age <= 0:
            return rule.confidence
        return rule.confidence * (0.5 ** (age / self.STALENESS_HALF_LIFE))

    # ── innate priors (revisable embodiment constraints) ─────────────────────
    def ensure_innate(self, innate_rules: list):
        """Adopt innate rules into memory if not already present.

        Memory persists across game runs, so an innate rule that has already
        been revised by experience keeps its updated confidence — form() finds
        the structural duplicate and the fresh prior object is discarded.
        """
        for r in innate_rules:
            self.form(r)

    def log_reuse(self, rule: 'EECTemporalRule', source: str, t: int):
        """Record a unique reuse event for display in the side panel.

        Common rules such as Clear -> Safe can fire every tick.  Keep only the
        latest row for each displayed expectation so the panel shows variety
        instead of ten copies of the same rule.
        """
        label = _rule_label(rule)
        conf  = self.effective_confidence(rule, t)
        self.reused_log = deque(
            (row for row in self.reused_log
             if not (len(row) >= 2 and row[1] == label)),
            maxlen=self.reused_log.maxlen)
        self.reused_log.appendleft((t, label, conf, source))

    def sync_to_reasoner(self, eec_reasoner: 'EECReasoner'):
        """Link to EECReasoner and push all stored rules into it (used on re-start)."""
        self._eec_reasoner = eec_reasoner
        for rule in self.rules:
            eec_reasoner.add_rule_if_new(rule)

    def _sync_rule_to_reasoner(self, rule: EECTemporalRule):
        """Keep the formal EEC reasoner aligned with the mutable memory rule."""
        if self._eec_reasoner is not None:
            self._eec_reasoner.add_rule_if_new(rule)

    # confidence thresholds the formal reasoner is sensitive to (rule inclusion
    # at 0.08, inertia veto at holds_persist_thresh = 0.35).  a confidence
    # update only affects predictions if it crosses one of these.
    _REASONER_THRESHOLDS = (0.08, 0.35)

    def _note_threshold_crossing(self, c_before: float, c_after: float):
        """Flag the reasoner cache dirty iff confidence crossed a reasoner
        threshold (so the per-tick clear can be skipped when nothing changed)."""
        if c_before == c_after:
            return
        lo, hi = (c_before, c_after) if c_before < c_after else (c_after, c_before)
        for thr in self._REASONER_THRESHOLDS:
            if lo < thr <= hi:
                if self._eec_reasoner is not None:
                    self._eec_reasoner.mark_cache_dirty()
                return

    def _remove_rule_from_reasoner(self, rule: EECTemporalRule):
        """Remove a pruned/revised expectation from the formal EEC reasoner."""
        if self._eec_reasoner is not None:
            self._eec_reasoner.remove_rule(rule)

    # ── rule identity (structural equality ignoring learned stats) ────────────
    def _find(self, event, preconditions, effect_type, effect, delay=1):
        return self._index.get(
            self._rule_key(event, preconditions, effect_type, effect, delay))

    # ── algorithm 1 (paper §iii-e) ────────────────────────────────────────────
    def form(self, rule: EECTemporalRule) -> EECTemporalRule:
        """Store rule if no structurally identical one exists; return stored rule.
        Also registers the rule with EECReasoner for temporal chaining.
        """
        self.rule_attempts += 1
        existing = self._find(rule.event, rule.preconditions,
                              rule.effect_type, rule.effect, rule.delay)
        if existing is not None:
            return existing
        self._register(rule)
        self.expectations_created += 1
        self._sync_rule_to_reasoner(rule)
        return rule

    # ── query ─────────────────────────────────────────────────────────────────
    def _matches(self, rule: EECTemporalRule, fluents: set, event: Event) -> bool:
        """True if rule fires given current fluents + event context."""
        if rule.event is not None:
            if rule.event.name != event.name:
                return False
            if rule.event.args and rule.event.args != event.args:
                return False
        for f in rule.preconditions:
            if f.args:
                if f not in fluents: return False
            else:
                if not any(fl.name == f.name for fl in fluents): return False
        return True

    # ── graded matching (causal-relevance weighted) ───────────────────────────
    # per absent, causally-undetermined precond
    PARTIAL_UNKNOWN_PENALTY = 0.6

    # ── asymmetric evidence gates for replacing simulation ───────────────────
    # memory must never be less safe than the internal model it silences.
    # the two error costs are wildly asymmetric: a false danger verdict wastes
    # a detour or a redundant simulation; a false safe verdict walks the agent
    # into a trap.  so the wilson reliability lower bound a rule must prove
    # before it may answer instead of simulating depends on its polarity:
    # danger_lcb = 0.42  → ≈2 clean confirmations (vicarious ones count).
    # diagnosis showed the dominant reuse blocker was danger rules stuck at
    # exactly 2 clean confirmations (wilson lcb 0.425), one short of the old
    # 0.50 gate.  admitting them is efficiency-only and safe: a danger
    # verdict makes the agent avoid or simulate a tile, so an over-eager
    # danger rule costs a wasted detour or redundant sim — never a trap.
    # 1 confirmation (lcb 0.27) is still correctly blocked as noise.
    # safe_lcb   = 0.80  → ≈11 clean confirmations; unchanged — a false safe
    # verdict walks the agent into a hazard, so the
    # safety-critical gate keeps its full burden of proof.
    # below the gate a rule is still advisory (it informs route risk and the
    # reasoner) — it just cannot suppress the simulation that would test it.
    DANGER_LCB = 0.42
    SAFE_LCB   = 0.80

    def match_strength(self, rule: EECTemporalRule, fluents: set,
                       event: Event, degrees: dict | None = None,
                       fluent_names: set | None = None) -> tuple:
        """Return (strength ∈ [0,1], n_satisfied) for graded rule matching.

        Strict matching (_matches) requires the WHOLE precondition set to
        recur verbatim, so context-heavy rules almost never fire again in a
        non-stationary world.  Graded matching weighs each precondition by
        its learned causal relevance to the rule's effect (CausalLedger ΔP):

          • satisfied                  → full weight
          • absent + ledger-IRRELEVANT → ignored: the fluent was incidental
                                          context, its absence changes nothing
          • absent + ledger-RELEVANT   → strength 0: a causal condition of the
                                          expectation does not hold here
          • absent + UNDETERMINED      → danger/status rules tolerate it at a
                                          penalty (cautious over-prediction);
                                          Safe rules fail (never assume safety
                                          on unverified conditions)

        This lets one expectation transfer across states that differ only in
        causally idle context (room theme, unrelated statuses, …) while still
        refusing to fire when a genuine cause is missing.  EEC reading: the
        rule Happens(a,t) ∧ ⋀ᵢ HoldsAt(fᵢ,t) → Initiates(e) is evaluated with
        the fᵢ partitioned by learned causal status rather than treated as an
        opaque conjunction.

        Perf: `fluent_names` (the set of unparameterised fluent names present)
        may be supplied by the caller so the per-precondition membership test
        is O(1) instead of a linear scan of `fluents`; on the hot reuse path
        query_outcome computes it once per call rather than once per rule.
        """
        if rule.event is not None:
            if rule.event.name != event.name:
                return 0.0, 0
            if rule.event.args and rule.event.args != event.args:
                return 0.0, 0
        if fluent_names is None:
            fluent_names = {fl.name for fl in fluents}
        is_safe = (rule.effect.name == 'Safe')
        target  = 'Damaged' if is_safe else rule.effect.name
        strength, n_sat = 1.0, 0
        for f in rule.preconditions:
            if f.args:
                sat = f in fluents
            else:
                sat = f.name in fluent_names
            if sat:
                n_sat += 1
                continue
            rel = self.causal.relevance(f, target)
            if rel is False:
                # incidental context — ignore
                continue
            if rel is True or is_safe:
                # missing causal condition
                return 0.0, 0
            strength *= self.PARTIAL_UNKNOWN_PENALTY
        if n_sat == 0:
            # nothing in common with reality
            return 0.0, 0
        # ── fuzzy activation (t-norm over learned membership degrees) ─────
        # danger-side rules only: a satisfied sensor precondition contributes
        # its learned danger degree (sensorcalibration), so 'hightemperature'
        # at 55 °c activates a burn/damaged expectation more weakly than at
        # 80 °c.  safe rules are never degree-scaled — fuzziness may only
        # weaken danger votes (pushing the agent back to simulation), never
        # strengthen the case for safety.
        if degrees and not is_safe:
            for f in rule.preconditions:
                d = degrees.get(f.name)
                if d is not None and f.name in fluent_names:
                    strength *= d
        return strength, n_sat

    def _eligible(self, rule: EECTemporalRule, require_tested: bool) -> bool:
        """Gate for memory-first simulation skipping.

        A rule may suppress re-simulation only if it has survived contact with
        reality at least once (confirmations ≥ 1) or is an innate embodiment
        prior.  Freshly simulated rules (C_INIT = 0.5, confirmations = 0) stay
        advisory: they inform decisions but do not silence the Internal Model.
        Derived (generalised) rules inherit tested status from their ≥2-times
        confirmed parent and carry confirmations = 1 at creation.
        """
        if not require_tested:
            return True
        return rule.origin == "innate" or rule.confirmations >= 1

    def query_outcome(self, tile_fluents: set, event: Event, threshold: float,
                      t: int | None = None, require_tested: bool = False,
                      degrees: dict | None = None):
        """Return (is_dangerous, rule) if memory has a confident prediction, else (None, None).

        Checks Initiates(Damaged) and Initiates(Safe) rules from the EEC memory.
        HoldsAt rules (inertia) are excluded — they represent persistence, not outcomes.

        Matching is GRADED (match_strength): a rule applies to states that are
        not identical to the one it was formed in, provided every causally
        relevant precondition holds; absent-but-irrelevant context is ignored
        and absent-but-undetermined conditions discount the rule's confidence.
        The effective vote of a rule is therefore

            C_eff(e, t) × strength(e, state)

        i.e. staleness-weighted confidence further weighted by causal fit.

        When both danger and safe rules apply, the rule with MORE SATISFIED
        preconditions wins (more verified discriminating conditions).  Weighted
        confidence breaks ties within the same specificity level; danger breaks
        confidence ties as a safety margin.  This single contest adjudicates
        innate vs learned vs factored aspect rules: a 1-aspect danger rule
        (HighTemperature → Damaged) is beaten by a learned, phase-specific
        TrapInactive ∧ MovingHazard ∧ … → Safe rule, so the agent can learn to
        exploit the safe windows of cycling traps.
        """
        best_danger: 'EECTemporalRule | None' = None
        best_safe:   'EECTemporalRule | None' = None
        best_danger_c = best_safe_c = 0.0
        best_danger_n = best_safe_n = -1
        best_danger_s = best_safe_s = 1.0
        _matched_any = _gate_blocked = _thresh_blocked = False
        # o(1) membership on hot path
        fluent_names = {fl.name for fl in tile_fluents}
        candidates = (self._by_effect.get(("Initiates", "Damaged"), ()),
                      self._by_effect.get(("Initiates", "Safe"), ()))
        for bucket in candidates:
            for r in bucket:
                # immediate (t+1) contest only: a damaged rule with a learned
                # delay ≥ 2 predicts harm several steps ahead, not on the
                # arriving step (improvement a).  those belong to the chain
                # reasoner (chained_danger), which schedules effects at
                # t+delay; honouring them here would make the agent treat a
                # safe-now tile as immediately lethal.  safe rules are
                # unaffected (safe is an instantaneous arrival verdict).
                if r.effect.name == "Damaged" and r.delay >= 2:
                    continue
                if not self._eligible(r, require_tested):
                    continue
                strength, n = self.match_strength(r, tile_fluents, event,
                                                  degrees=degrees,
                                                  fluent_names=fluent_names)
                if strength <= 0.0:
                    continue
                _matched_any = True
                if require_tested and r.origin != "innate":
                    # statistical floor for silencing the internal model:
                    # the rule's demonstrated reliability must beat the gate
                    # for its polarity (see danger_lcb / safe_lcb above).
                    gate = (self.SAFE_LCB if r.effect.name == "Safe"
                            else self.DANGER_LCB)
                    if r.reliability_lcb() < gate:
                        _gate_blocked = True
                        continue
                c_eff = self.effective_confidence(r, t) * strength
                if c_eff <= threshold:
                    _thresh_blocked = True
                    continue
                if r.effect.name == "Damaged":
                    if (best_danger is None
                            or n > best_danger_n
                            or (n == best_danger_n and c_eff > best_danger_c)):
                        best_danger, best_danger_c = r, c_eff
                        best_danger_n, best_danger_s = n, strength
                else:
                    if (best_safe is None
                            or n > best_safe_n
                            or (n == best_safe_n and c_eff > best_safe_c)):
                        best_safe, best_safe_c = r, c_eff
                        best_safe_n, best_safe_s = n, strength

        chosen = polarity = None
        if best_danger is not None and best_safe is not None:
            if best_safe_n > best_danger_n:
                # safe rule more specific
                chosen, polarity = best_safe, False
            elif best_danger_n > best_safe_n:
                chosen, polarity = best_danger, True
            elif best_safe_c > best_danger_c:
                chosen, polarity = best_safe, False
            else:
                # danger breaks ties
                chosen, polarity = best_danger, True
        elif best_danger is not None:
            chosen, polarity = best_danger, True
        elif best_safe is not None:
            chosen, polarity = best_safe, False

        if chosen is None:
            if not _matched_any:
                self.diag_no_candidate += 1
            elif _gate_blocked and not _thresh_blocked:
                self.diag_gate_blocked += 1
            elif _thresh_blocked:
                self.diag_thresh_blocked += 1
            else:
                self.diag_no_candidate += 1
            return None, None
        self.diag_answered += 1
        if (polarity and best_danger_s < 1.0) or (not polarity and best_safe_s < 1.0):
            # answered from a non-identical state
            self.partial_reuses += 1
        return polarity, chosen

    # ── vicarious confirmation (falsification by observation) ────────────────
    def vicarious_confirm(self, tile_fluents: set, event: Event, t: int = 0) -> int:
        """Confirm matching Initiates(Damaged) rules from an OBSERVED collision.

        When another entity (a roaming enemy) is seen overlapping an active
        hazard, the agent treats it as evidence for its danger expectations
        about that context — Popperian testing without self-experiment.  This
        addresses the structural asymmetry that the controller avoids predicted
        danger, so danger rules are otherwise only ever tested via surprises.

        Direction-specific rules (Event("Move", (dx,dy))) are skipped: the
        observation carries no information about the agent's approach direction.
        Returns the number of rules confirmed.
        """
        n = 0
        for r in list(self._by_effect.get(("Initiates", "Damaged"), ())):
            if r.delay != 1:
                continue
            if r.event is not None and r.event.args:
                # direction-specific — not testable from observation
                continue
            if not self._matches(r, tile_fluents, event):
                continue
            self.update(r, True, t, context=tile_fluents,
                        weight=self.VICARIOUS_WEIGHT)
            n += 1
        self.vicarious_confirms += n
        return n

    def vicarious_confirm_safe(self, tile_fluents: set, event: Event,
                               t: int = 0) -> int:
        """Confirm matching Initiates(Safe) rules from an observed NON-event.

        The mirror image of vicarious_confirm: an enemy seen crossing a
        DORMANT hazard unharmed is a genuine test of the dormant-phase Safe
        expectations (… ∧ TrapInactive → Safe).  These rules are structurally
        even harder to test first-hand than danger rules — the controller
        rarely routes the agent over trap tiles at all — yet they need ~11
        clean confirmations to clear SAFE_LCB.  Watching other actors supplies
        that evidence without risking the agent's own body.
        """
        n = 0
        for r in list(self._by_effect.get(("Initiates", "Safe"), ())):
            if r.delay != 1:
                continue
            if r.event is not None and r.event.args:
                continue
            if not self._matches(r, tile_fluents, event):
                continue
            self.update(r, True, t, context=tile_fluents,
                        weight=self.VICARIOUS_WEIGHT)
            n += 1
        self.vicarious_confirms += n
        return n

    # ── algorithm 2 — generalisation (eq. 5) ─────────────────────────────────
    def _generalise_rule(self, r: EECTemporalRule):
        """Generalise a confirmed rule to a broader semantic category (paper §III-G eq. 5).

        The paper describes generalisation via ontology-based semantic clustering:
        'if an agent determines that stepping in either oil or water makes the surface
        slippery, it could generalise this expectation' to StepOnLiquid → Slippery.

        Here, the agent's ontology maps specific sensor fluents to broader categories:
          HighTemperature ∨ LowTemperature  → ThermalHazard  (both cause body harm)
          Constricting ∨ Unstable           → MechanicalHazard
          Toxic ∨ Corrupting                → ChemicalHazard
          HeavyImpact ∨ MovingHazard        → KineticHazard

        This mirrors the paper's liquid generalisation: rather than tracking each
        specific sensor property separately, the agent clusters them by harm type.
        We then store generalised rules with their semantic category fluent replacing
        the original specific sensors, at 80% of the original confidence.

        Additionally, we produce a room-level generalisation (room-type prior) for
        safe rules only — a 'Damaged' generalisation across the whole room would
        block navigation through safe corridors.
        """
        # ── semantic ontology: sensor fluent → broader category ───────────────
        SENSOR_CATEGORIES = {
            'HighTemperature': 'ThermalHazard',
            'LowTemperature':  'ThermalHazard',
            'Toxic':           'ChemicalHazard',
            'Corrupting':      'ChemicalHazard',
            'HeavyImpact':     'KineticHazard',
            'MovingHazard':    'KineticHazard',
            'DynamicHazard':   'KineticHazard',
            'CollisionPath':   'KineticHazard',
            'Constricting':    'MechanicalHazard',
            'Unstable':        'MechanicalHazard',
        }

        room_f     = next((f for f in r.preconditions if f.name == "Room"), None)
        activity_f = next((f for f in r.preconditions
                           if f.name in ("TrapActive", "TrapImminent", "TrapInactive")),
                          None)

        before = self.expectations_created

        # ── causal-ledger generalisation: drop demonstrably-irrelevant ────────
        # preconditions.  unlike screen() (which keeps undetermined fluents as
        # bold conjectures), generalisation demands positive evidence: only
        # fluents whose δp for this effect is established as relevant survive.
        # this is eq. 5 driven by the learned causal model — the agent
        # discovers which holdsat(f, t) conditions actually do causal work.
        target_eff = ('Damaged' if r.effect.name == 'Safe' else r.effect.name)
        causal_core = tuple(sorted(
            (f for f in r.preconditions
             if self.causal.relevance(f, target_eff) is True),
            key=lambda f: (f.name, f.args)))
        # refinement 5: a generalised rule is supported by all of the parent's
        # confirmations, not one.  transfer a discounted, capped share so the
        # abstraction inherits the standing it has actually earned and need not
        # re-clear the wilson gate from scratch.  only confirmations transfer —
        # never violations (a category rule should not inherit blame for an
        # instance-specific failure).
        inherit = max(2, min(self.TAU_GENERALISE * 3,
                             int(round(r.confirmations * self.GENERALISE_INHERIT)) + 1))
        if causal_core and causal_core != r.preconditions:
            self.preconds_dropped += len(r.preconditions) - len(causal_core)
            g = self.form(EECTemporalRule(
                event=Event("Move"),
                preconditions=causal_core,
                effect_type=r.effect_type, effect=r.effect,
                delay=r.delay,
                confidence=r.confidence * 0.85,
                confirmations=1,
                origin="derived"))
            if g.confirmations <= 1 and g.violations == 0:
                g.confirmations = inherit

        # ── category-level generalisation (main paper example) ────────────────
        # find all sensor-category mappings present in this rule's preconditions
        seen_categories = {}
        for f in r.preconditions:
            cat = SENSOR_CATEGORIES.get(f.name)
            if cat:
                seen_categories.setdefault(cat, []).append(f)

        for cat_name, specific_fluents in seen_categories.items():
            cat_fluent = Fluent(cat_name)
            # build generalised precondition: replace the specific sensors with
            # the category fluent; keep room and activity context.
            gen_pre_parts = [cat_fluent]
            if room_f:
                gen_pre_parts.append(room_f)
            if activity_f:
                gen_pre_parts.append(activity_f)
            gen_pre = tuple(sorted(gen_pre_parts, key=lambda f: (f.name, f.args)))
            g = self.form(EECTemporalRule(
                event=Event("Move"),
                preconditions=gen_pre,
                effect_type=r.effect_type, effect=r.effect,
                delay=r.delay,
                confidence=r.confidence * 0.80,
                confirmations=1,
                origin="derived"))
            if g.confirmations <= 1 and g.violations == 0:
                # refinement 5: inherit parent evidence
                g.confirmations = inherit

        # ── room-level prior: safe rules only (damage rule would block corridors) ──
        if room_f and r.effect.name != "Damaged":
            pre = (room_f, activity_f) if activity_f else (room_f,)
            self.form(EECTemporalRule(
                event=Event("Move"), preconditions=pre,
                effect_type=r.effect_type, effect=r.effect,
                delay=r.delay, confidence=r.confidence * 0.65,
                confirmations=1, origin="derived"))

        self.rules_derived += self.expectations_created - before

    def update(self, rule: EECTemporalRule, confirmed: bool, t: int = 0,
               context: set | None = None, weight: float = 1.0):
        """Algorithm 2: delta-rule update, generalisation, pruning, specialisation.

        Implements paper eqs. 2-5:
          Confirmed:   C(e) ← C(e) + (k·w) × (1 − C(e))   [eq. 2 — asymptotic to 1]
          Violated:    C(e) ← C(e) − (k·w) × C(e)          [eq. 3 — asymptotic to 0]
          Prune:       remove e if C(e) < τ_prune          [eq. 4]
          Generalise:  if confirm(e) ≥ τ_generalise         [eq. 5]

        `weight` ∈ (0,1] (Refinement 1 & 2) scales the learning step by how
        informative the triggering observation is: an exact-match first-person
        outcome moves confidence fully (w=1); a partial/fuzzy match or a
        third-person (vicarious) observation moves it proportionally less.
        This is still the paper's delta rule — k modulated by evidence quality
        — and makes confidence (hence the Wilson gate) reflect quality-weighted
        reliability rather than a raw count.

        High-confidence expectations deteriorate slowly under contradictions
        (eq. 3) and strengthen rapidly under confirmations (eq. 2), providing
        persistence of well-established beliefs while remaining responsive to
        repeated contradictions.

        `context` (the fluent set that held when the outcome was observed)
        feeds two refinement mechanisms that let rules settle at the RIGHT
        level of specificity instead of dying at the extremes:
          • confirming contexts are buffered on the rule (≤ 6), and
          • a violation of a previously-working rule triggers
            _specialise_on_violation — discrimination learning that conjectures
            WHICH condition separates the contexts where the rule held from
            the one where it failed.

        Innate rules are updated by eqs. 2-3 like any other expectation (they
        are revisable, Popperian priors) but are exempt from pruning — an
        embodiment constraint can lose authority through violations without
        vanishing from the agent's theory of the world.

        Only the updated rule can have crossed τ_prune, so pruning checks just
        that rule rather than rescanning the whole rule base.
        """
        if id(rule) not in self._ids:
            return
        rule.last_observed_time = t
        c_before = rule.confidence
        k_eff = self.K * max(self.MIN_EVIDENCE_W, min(1.0, weight))
        if confirmed:
            rule.confirmations += 1
            # eq. 2
            rule.confidence    += k_eff * (1 - rule.confidence)
            if context is not None:
                rule.confirm_ctx.append(frozenset(context))
                if len(rule.confirm_ctx) > 6:
                    rule.confirm_ctx.pop(0)
            if rule.confirmations >= self.TAU_GENERALISE and not rule.generalised:
                rule.generalised = True
                # eq. 5
                self._generalise_rule(rule)
        else:
            rule.violations += 1
            # eq. 3
            rule.confidence -= k_eff * rule.confidence
            if context is not None and rule.confirmations >= 2:
                self._specialise_on_violation(rule, context, t)
        # perf: the formal reasoner reads confidence only through two
        # thresholds (rule-inclusion 0.08 and holds_persist_thresh 0.35), so
        # its prediction cache only needs invalidating when this update pushed
        # the rule's confidence across one of them.  continuous drift that
        # stays on one side of both thresholds cannot change any prediction,
        # so we flag a crossing and let the per-tick clear become conditional.
        self._note_threshold_crossing(c_before, rule.confidence)
        if rule.confidence < self.TAU_PRUNE and rule.origin != "innate":
            # eq. 4
            self._unregister(rule)
        else:
            self._sync_rule_to_reasoner(rule)

    # ── violation-driven specialisation (discrimination learning) ────────────
    def _specialise_on_violation(self, rule: EECTemporalRule,
                                 viol_ctx: set, t: int):
        """Refine a rule that USUALLY works but just failed.

        This is the mechanism that lets expectations settle between the two
        bad extremes.  A rule too SPECIFIC never matches again; a rule too
        BROAD eventually meets a context where its prediction is wrong.  When
        that happens, eq. 3 alone would only bleed confidence — discarding
        the regularity along with the exception.  Instead, the violation is
        treated as INFORMATION: compare the buffered contexts where the rule's
        prediction held against the context where it failed, and conjecture
        the discriminating condition (Drescher-style marginal attribution /
        general-to-specific refinement):

          • a fluent present in EVERY confirming context but absent now
            → child rule: preconditions ∪ {f} → same effect
              ("the expectation actually depends on f")
          • a fluent present now but in NO confirming context
            → child rule: preconditions ∪ {f} → OPPOSITE outcome
              ("f is the exception condition", Damaged ↔ Safe only)

        Children are conjectures: they start at C_INIT with zero
        confirmations, so they cannot replace simulation until the
        Algorithm-2 sweep / vicarious observation has tested them — and they
        compete in query_outcome's specificity contest, where a tested child
        (more satisfied preconditions) beats its broader parent precisely in
        the contexts that refuted it.  Note the contrast with the
        CausalLedger: ΔP measures MARGINAL relevance and cannot see
        interaction effects; specialisation captures exactly those
        conditional dependencies (e.g. MovingHazard harms only ∧ TrapActive).
        """
        if rule.effect_type != "Initiates" or not rule.confirm_ctx:
            return
        _SKIP = {'Clear', 'ClearAhead', 'Safe', 'Damaged', 'NoStatus'}
        common = frozenset.intersection(*rule.confirm_ctx)
        union  = frozenset.union(*rule.confirm_ctx)
        viol   = set(viol_ctx)
        pre    = set(rule.preconditions)
        key    = lambda f: (f.name, f.args)

        # condition the effect on what the working contexts shared:
        pos = sorted((f for f in (common - viol)
                      if f.name not in _SKIP and f not in pre), key=key)[:2]
        for f in pos:
            child = self.form(EECTemporalRule(
                event=rule.event,
                preconditions=tuple(sorted(pre | {f}, key=key)),
                effect_type="Initiates", effect=rule.effect,
                delay=rule.delay, confidence=C_INIT,
                last_observed_time=t, origin="derived"))
            # the violating observation is itself a positive instance of this
            # child's parent effect, but here f was absent (f ∈ common−viol), so
            # the child correctly did not fire — it is not evidence for this
            # child.  leave it as an untested conjecture (refinement 4 applies
            # only to the exception children below, which did hold).
            self.specialisations += 1

        # conjecture the exception condition (outcome rules only):
        if rule.effect.name in ("Damaged", "Safe"):
            opp = Fluent("Safe" if rule.effect.name == "Damaged" else "Damaged")
            neg = sorted((f for f in (viol - union)
                          if f.name not in _SKIP and f not in pre), key=key)[:2]
            for f in neg:
                child = self.form(EECTemporalRule(
                    event=rule.event,
                    preconditions=tuple(sorted(pre | {f}, key=key)),
                    effect_type="Initiates", effect=opp,
                    delay=rule.delay, confidence=C_INIT,
                    last_observed_time=t, origin="derived"))
                # refinement 4: the violating context is a positive instance of
                # this exception child — its extra precondition f held now, and
                # the opposite outcome (opp) is exactly what occurred.  seed the
                # motivating evidence so the child can enter the specificity
                # contest one step sooner instead of discarding the very
                # observation that justified conjecturing it.  only credit a
                # freshly created child (confirmations == 0) to avoid
                # double-counting when the same exception recurs.
                if child.confirmations == 0 and child.violations == 0:
                    self.update(child, True, t, context=viol_ctx)
                self.specialisations += 1

    @property
    def count(self):
        return len(self.rules)

    @property
    def danger_count(self):
        return sum(1 for r in self.rules
                   if r.effect == Fluent("Damaged") and r.effect_type == "Initiates")

    @property
    def holds_count(self):
        """Number of HoldsAt (inertia) rules in memory."""
        return sum(1 for r in self.rules if r.effect_type == "HoldsAt")


class ConsequenceEvaluator:
    """Paper §III-D: Evaluates proposed actions via Internal Model + Expectation Memory.

    Cleanly separated from the Robot Controller (PEAgent.choose_action).
    Per-action flow (Algorithm 1):
      1. Query memory — if confident danger EECTemporalRule matches, skip simulation
      2. Run Internal Model (_sim_step) to predict consequence
      3. Form EECTemporalRule expectations from simulation; register with EECReasoner
      4. Check EECReasoner for chained multi-step danger (inertia + chaining)
      5. Return (danger, rule) to the Controller
    """
    def __init__(self, grid: list, room_of: dict,
                 memory: 'ExpectationMemory', danger_thresh: float,
                 eec_reasoner: 'EECReasoner' = None):
        self.grid          = grid
        self.room_of       = room_of
        self.memory        = memory
        self.danger_thresh = danger_thresh
        self.eec_reasoner  = eec_reasoner
        # ablation flags (set by peagent per mode — feedback #2 baselines):
        # false ⇒ never query/store expectations
        self.use_memory    = True
        # false ⇒ never run the internal model
        self.use_sim       = True

    # ── §iii-c internal model ─────────────────────────────────────────────────
    def _sim_step(self, dx: int, dy: int, from_x: int, from_y: int,
                  obs: dict) -> dict | None:
        """Predict the consequence of (dx,dy) without physical commitment.

        The Internal Model embeds the WORLD DYNAMICS (Winfield: the internal
        model contains a simulation of the world).  It therefore owns the
        mapping from hazards to bodily consequences — the same dynamics the
        real environment applies on contact.  Crucially, the EEC Expectation
        Formation module downstream never consults these dynamics directly:
        it only PERCEIVES the simulated outcome via 'outcome_fluents' and
        forms rules from the observed state difference (Algorithm 1).
        """
        tx, ty = from_x+dx, from_y+dy
        if not (0 <= tx < COLS and 0 <= ty < ROWS) or self.grid[ty][tx] == 1:
            return None
        kind  = obs['trap_map'].get((tx, ty))
        enemy = (tx, ty) in obs['enemy_tiles']
        danger = self.predict_physical_harm(kind, enemy, obs, tx, ty)

        # world dynamics: what the simulated body exhibits at t+1.  this is
        # the simulation's observable output — the formation module diffs it
        # against the pre-state; it does not know where it came from.
        outcome_fluents: set = set()
        if danger:
            outcome_fluents.add(Fluent("Damaged"))
            eff = TDEFS.get(kind, {}).get('eff') if kind else None
            if eff:
                outcome_fluents.add(Fluent(eff.capitalize()))
        return {'tx':tx, 'ty':ty, 'danger': danger,
                'trap_kind': kind, 'enemy_near': enemy,
                'outcome_fluents': outcome_fluents}

    def predict_physical_harm(self, kind: str, enemy: bool,
                              obs: dict, tx: int, ty: int) -> bool:
        """Predict whether moving to (tx, ty) will cause physical harm.

        Checks sensor readings against agent thresholds, and for moving traps
        uses dtrap_activity timing to determine whether the hazard will actually
        be in its dangerous phase when the agent arrives.
        """
        if enemy:
            return True
        if kind is None:
            return False

        p = TRAP_SENSORS.get(kind, {})
        if not p:
            # unrecognised kind — assume harmful
            return True

        temp = p.get('temp', 20)
        tox  = p.get('tox',  0.0)
        imp  = p.get('imp',  0)
        mov  = p.get('mov',  False)

        temp_harm = temp > AGENT_MAX_TEMP or temp < AGENT_MIN_TEMP
        tox_harm  = tox  > AGENT_MAX_TOXICITY
        imp_harm  = imp  > AGENT_MAX_IMPACT
        # status-effect hazards that don't exceed physical thresholds but still harm
        secondary = p.get('con', False) or p.get('unst', False) or p.get('cor', False)

        if not (temp_harm or tox_harm or imp_harm or secondary):
            # all sensor readings within agent's tolerance
            return False

        if not mov:
            # static hazard — permanently harmful
            return True

        # moving hazard: only harmful if this tile's owning instance is active
        # at arrival time.  same-kind traps can be in different phases.
        is_active, ticks_to_active = _dtrap_activity_for_tile(kind, obs, tx, ty)
        # peagent.step_ticks
        ticks_to_arrive            = 10

        return is_active or ticks_to_active <= ticks_to_arrive

    # ── §iii-e: tile fluents — sensor-based, no trap-kind names ──────────────
    def _get_tile_fluents(self, dx: int, dy: int, tx: int, ty: int,
                          obs: dict) -> tuple:
        """Return (tile_fluents: set[Fluent], event: Event) for a candidate move.

        Fluents describe PHYSICAL PROPERTIES the agent senses, not game
        object identities.  Sensor readings (temperature, toxicity, impact…)
        come from tile_sensor_fluents(); the agent never stores the kind name.
        """
        kind    = obs['trap_map'].get((tx, ty))
        enemy   = (tx, ty) in obs['enemy_tiles']
        rm      = self.room_of.get((tx, ty))
        rtype   = rm.rtype if rm else None
        fluents: set = set()
        tracked = list(obs.get('dtraps', [])) + list(obs.get('_sim_dtraps', []))

        contact_ticks = []
        contact_kinds = []
        for dt in tracked:
            if not TRAP_SENSORS.get(dt.kind, {}).get('mov', False):
                continue
            ticks = _dtrap_ticks_to_hit(dt, tx, ty, max_ticks=30)
            if ticks is None:
                continue
            contact_ticks.append(ticks)
            contact_kinds.append(dt.kind)
            fluents.update(_dynamic_motion_fluents(dt))
        if contact_ticks:
            soonest = min(contact_ticks)
            if soonest == 0:
                fluents.add(Fluent("TrapContactNow"))
            elif soonest <= 10:
                fluents.add(Fluent("TrapContactSoon"))
            else:
                fluents.add(Fluent("TrapContactLater"))
            if kind is None and soonest <= 10:
                kind = contact_kinds[contact_ticks.index(soonest)]
            # for quantitative delay (improvement a)
            self._last_contact_ticks = soonest
        else:
            self._last_contact_ticks = None

        # physical sensor readings
        in_kinetic = (tx, ty) in obs.get('kinetic_tiles', set())
        fluents.update(tile_sensor_fluents(kind, in_kinetic or bool(contact_ticks)))
        if kind:
            if TRAP_SENSORS.get(kind, {}).get('mov', False):
                fluents.add(Fluent("DynamicHazard"))
            else:
                fluents.add(Fluent("StaticHazard"))

        # trap activity state — lets the eec distinguish safe windows from dangerous ones
        # for traps that cycle between active and inactive phases (ceiling_crusher, etc.)
        if kind and TRAP_SENSORS.get(kind, {}).get('mov', False):
            is_active, ticks_to_active = _dtrap_activity_for_tile(
                kind, obs, tx, ty)
            if is_active:
                fluents.add(Fluent("TrapActive"))
            # step_ticks — will fire before we arrive
            elif ticks_to_active <= 10:
                fluents.add(Fluent("TrapImminent"))
            else:
                fluents.add(Fluent("TrapInactive"))

        if rtype:
            fluents.add(Fluent("Room", (rtype,)))
        if enemy:
            fluents.add(Fluent("EnemyNearby"))
        if not kind and not enemy:
            fluents.add(Fluent("Clear"))
        if self._predicts_dynamic_collision(tx, ty, obs) or any(t <= 10 for t in contact_ticks):
            fluents.add(Fluent("PredictedCollision"))

        # player's current physiological state
        statuses = obs.get('player_statuses', {})
        if statuses:
            for s in statuses:
                fluents.add(Fluent(s.capitalize()))
        else:
            fluents.add(Fluent("NoStatus"))

        return fluents, Event("Move", (dx, dy))

    def _predicts_dynamic_collision(self, tx: int, ty: int, obs: dict) -> bool:
        """Vision-style prediction: will a tracked object occupy this tile soon?"""
        if (tx, ty) in obs.get('enemy_tiles', set()):
            return True
        if (tx, ty) in obs.get('kinetic_tiles', set()):
            return True
        tracked = list(obs.get('dtraps', [])) + list(obs.get('_sim_dtraps', []))
        for dt in tracked:
            if not TRAP_SENSORS.get(dt.kind, {}).get('mov', False):
                continue
            active, ticks = _dtrap_phase(dt)
            if active or ticks <= 10:
                tmp = {}
                _map_dtrap_tiles(dt, tmp)
                if (tx, ty) in tmp:
                    return True
        return False

    # ── §iii-e eec expectation formation (algorithm 1) ───────────────────────
    def _form_expectations(self, dx: int, dy: int, sim: dict, obs: dict,
                           t: int = 0) -> EECTemporalRule:
        """Form EEC rules from simulated action outcome — Algorithm 1.

        Implements the paper's pseudocode faithfully:
          For action a in simulation S:
            Cond ← {Happens(a, t)} ∪ CollectPrecond(s, t)
            For each fluent f in F:
              if f changed to true  → Initiates(a, f, t+1)
              if f changed to false → Terminates(a, f, t+1)
              else                  → HoldsAt(f, t+1)   [inertia — stored if relevant]
            Store exp_rule(Cond, effect) if not already in memory

        Preconditions (CollectPrecond) are physical sensor fluents the agent
        observes BEFORE the action — never the trap kind name.  This ensures
        learned rules are embodied (sensor-based) and generalisable.
        """
        self.memory.expectation_forms += 1

        # ── step 1: observe world state s(t) at target tile ──────────────
        # before_fluents = holdsat(f, t) for all f perceived at target tile
        before_fluents, event = self._get_tile_fluents(dx, dy,
                                                       sim['tx'], sim['ty'], obs)

        # ── step 2: perceive s(t+1) from the internal model's output ─────
        # inertia axiom: after_fluents inherits everything from before by
        # default; the simulated outcome fluents are then observed on top.
        # formation never consults world-dynamics tables (tdefs) — the only
        # access to consequences is perception of the simulation result.
        # inertia: holdsat(f, t) → holdsat(f, t+1)
        after_fluents = set(before_fluents)
        outcome_fluents = set(sim.get('outcome_fluents', set()))
        if sim['danger'] and not any(f.name == "Damaged" for f in outcome_fluents):
            # harmful rollouts must expose damaged to algorithm 1.
            outcome_fluents.add(Fluent("Damaged"))
        after_fluents |= outcome_fluents

        if sim['danger']:
            if any(f.name not in ('Damaged',) and f.name != 'NoStatus'
                   for f in outcome_fluents):
                after_fluents.discard(Fluent("NoStatus"))
        else:
            after_fluents.add(Fluent("Safe"))
            # threat dissolves on safe move
            after_fluents.discard(Fluent("EnemyNearby"))

        # ── causal ledger: log this simulated outcome ─────────────────────
        # every simulation is an observation feeding δp(fluent, effect); the
        # same ledger also receives real-world and vicarious observations.
        observed_effect_names = ({f.name for f in outcome_fluents}
                                 if sim['danger'] else {'Safe'})
        self.memory.causal.record(before_fluents, observed_effect_names)
        # continuous-channel evidence for the learned membership curves.
        self.memory.calibration.record(sim.get('trap_kind'), sim['danger'])

        # ── step 3: state difference  (algorithm 1 lines 7-14) ───────────
        # f changed to true
        initiated  = after_fluents - before_fluents
        # f changed to false
        terminated = before_fluents - after_fluents
        # unchanged fluents: before ∩ after — these become holdsat (inertia) rules.
        # we only store holdsat rules for the primary observable properties
        # (trap sensors, room, activity state) to avoid combinatorial explosion.
        _HOLDS_INTERESTING = {'HazardPresent', 'HighTemperature', 'LowTemperature',
                              'Toxic', 'HeavyImpact', 'MovingHazard', 'Constricting',
                              'Unstable', 'Corrupting', 'TrapActive', 'TrapInactive',
                              'TrapImminent', 'EnemyNearby', 'DynamicHazard',
                              'StaticHazard', 'PredictedCollision', 'Room',
                              'TrapContactNow', 'TrapContactSoon', 'TrapContactLater',
                              'RotatingHazard', 'ExpandingRing', 'TrapExpanding',
                              'TimerSoon', 'TimerMedium', 'TimerLong'}
        unchanged = {f for f in before_fluents & after_fluents
                     if f.name in _HOLDS_INTERESTING}

        # ── step 4: collectprecond — full context vs causally screened ────
        # full variant (algorithm 1 verbatim): every observed pre-state fluent
        # except derived/output fluents that are effects, never causes.
        _SKIP_PRE = {'Clear', 'ClearAhead', 'Safe', 'Damaged', 'NoStatus'}
        full_precond   = tuple(sorted(
            (f for f in before_fluents if f.name not in _SKIP_PRE),
            key=lambda f: (f.name, f.args)))
        if not full_precond:
            full_precond = (Fluent("Clear"),)

        primary = None
        _PHASE = ('TrapActive', 'TrapImminent', 'TrapInactive',
                  'TrapContactNow', 'TrapContactSoon', 'TrapContactLater',
                  'TrapExpanding', 'TimerSoon', 'TimerMedium', 'TimerLong')

        # ── quantitative delay (improvement a) ────────────────────────────
        # the eec rule's `delay` field (initiates(effect, t+delay)) was always
        # 1.  but for a moving hazard the agent has observed exactly how many
        # ticks until contact (_last_contact_ticks); quantise that to
        # controller steps so the harm expectation records when, not just
        # whether.  the chain reasoner already schedules effects at t+delay,
        # so a learned delay immediately sharpens multi-step timelines.  only
        # the damaged effect carries a learned delay; non-temporal effects and
        # static hazards keep delay=1 (harm on the arriving step).
        step = PEAgent.STEP_TICKS
        ct = getattr(self, '_last_contact_ticks', None)
        dmg_delay = 1
        if ct is not None and ct > 0:
            dmg_delay = max(1, min(3, 1 + round(ct / step)))

        def _eff_delay(fl):
            return dmg_delay if fl.name == 'Damaged' else 1

        # ── initiates rules ───────────────────────────────────────────────
        for fluent in sorted(initiated, key=lambda f: f.name):
            if fluent.name in ('ClearAhead',):
                continue
            r = self.memory.form(EECTemporalRule(
                event=event, preconditions=full_precond,
                effect_type="Initiates", effect=fluent,
                delay=_eff_delay(fluent), last_observed_time=t))
            if fluent.name == 'Damaged':
                primary = r
            # causally screened, direction-agnostic variant: preconditions
            # restricted to fluents the ledger deems (or has not yet refuted
            # as) causally relevant to this effect.  replaces the former
            # hand-written sensor whitelist with learned δp screening.
            causal_precond = self.memory.causal.screen(
                (f for f in before_fluents if f.name not in _SKIP_PRE),
                fluent.name)
            if not causal_precond:
                causal_precond = (Fluent("Clear"),)
            if causal_precond != full_precond:
                self.memory.preconds_dropped += (len(full_precond)
                                                 - len(causal_precond))
                self.memory.form(EECTemporalRule(
                    event=Event("Move"), preconditions=causal_precond,
                    effect_type="Initiates", effect=fluent,
                    delay=_eff_delay(fluent), last_observed_time=t))

            # ── factored aspect expectations (per-property / per-entity) ──
            # a monolithic full_precond rule recurs only when the entire
            # context recurs.  here the same outcome is additionally
            # decomposed into multiple small expectations about how each
            # observed hazard property / actor aspect behaves:
            # holdsat(aspect, t) ∧ happens(move, t) → initiates(e, t+1)
            # and, for cycling entities, the aspect paired with the trap's
            # phase fluent (the entity-level behavioural expectation
            # "this hazard harms while active").  singleton conjectures that
            # are wrong (e.g. room(forest) → damaged) match often, get swept
            # by algorithm 2 often, accumulate violations, and are pruned —
            # conjecture and refutation doing the variable selection.
            before_factored = self.memory.expectations_created
            aspects = [f for f in before_fluents
                       if f.name not in _SKIP_PRE
                       and f.name not in _PHASE
                       and self.memory.causal.relevance(f, fluent.name)
                       is not False]
            phases = [f for f in before_fluents if f.name in _PHASE]
            for af in aspects:
                self.memory.form(EECTemporalRule(
                    event=Event("Move"), preconditions=(af,),
                    effect_type="Initiates", effect=fluent,
                    delay=_eff_delay(fluent), last_observed_time=t))
                for phase in phases:
                    pair = tuple(sorted((af, phase),
                                        key=lambda f: (f.name, f.args)))
                    self.memory.form(EECTemporalRule(
                        event=Event("Move"), preconditions=pair,
                        effect_type="Initiates", effect=fluent,
                        delay=_eff_delay(fluent), last_observed_time=t))
            self.memory.factored_rules += (self.memory.expectations_created
                                           - before_factored)

        # ── terminates rules (algorithm 1 line 10-11) ────────────────────
        _SKIP_TERM = {'HazardPresent', 'ClearAhead'}
        for fluent in sorted(terminated, key=lambda f: f.name):
            if fluent.name in _SKIP_TERM:
                continue
            self.memory.form(EECTemporalRule(
                event=event, preconditions=full_precond,
                effect_type="Terminates", effect=fluent,
                delay=1, last_observed_time=t))

        # ── holdsat rules (algorithm 1 line 12-13) — eec inertia axiom ───
        # for fluents that did not change: holdsat(f, t) → holdsat(f, t+1).
        # these encode the agent's expectation that certain properties persist.
        # stored only for hazard-relevant sensor properties to stay tractable.
        for fluent in sorted(unchanged, key=lambda f: f.name):
            self.memory.form(EECTemporalRule(
                event=event, preconditions=(fluent,),
                effect_type="HoldsAt", effect=fluent,
                delay=1,
                confidence=C_INIT,
                last_observed_time=t))

        # ── fallback: no-damage move → initiates(safe) ───────────────────
        if primary is None:
            primary = self.memory.form(EECTemporalRule(
                event=event, preconditions=full_precond,
                effect_type="Initiates", effect=Fluent("Safe"),
                delay=1, last_observed_time=t))
            # screened variant: condition the safe rule only on fluents the
            # ledger considers relevant to the damaged/safe outcome.
            safe_precond = self.memory.causal.screen(
                (f for f in before_fluents if f.name not in _SKIP_PRE), 'Safe')
            if not safe_precond:
                safe_precond = (Fluent("Clear"),)
            if safe_precond != full_precond:
                self.memory.preconds_dropped += (len(full_precond)
                                                 - len(safe_precond))
                self.memory.form(EECTemporalRule(
                    event=event, preconditions=safe_precond,
                    effect_type="Initiates", effect=Fluent("Safe"),
                    delay=1, last_observed_time=t))

            # ── factored entity-level safe expectations ───────────────────
            # "this hazard is harmless while dormant": pair each hazard
            # property with the observed dormant phase.  these are the
            # behavioural expectations that let the agent exploit the safe
            # windows of cycling traps in any room, not just the one where
            # the window was first simulated.  no singleton safe rules are
            # formed — safety is never asserted from one context fluent
            # alone (a room(x) → safe conjecture could mask a hazard).
            dormant = next((f for f in before_fluents
                            if f.name == 'TrapInactive'), None)
            if dormant is not None:
                before_factored = self.memory.expectations_created
                for af in before_fluents:
                    if af.name in _SKIP_PRE or af.name in _PHASE:
                        continue
                    pair = tuple(sorted((af, dormant),
                                        key=lambda f: (f.name, f.args)))
                    self.memory.form(EECTemporalRule(
                        event=Event("Move"), preconditions=pair,
                        effect_type="Initiates", effect=Fluent("Safe"),
                        delay=1, last_observed_time=t))
                self.memory.factored_rules += (
                    self.memory.expectations_created - before_factored)

        return primary

    # ── §iii-d core evaluation (algorithm 1 single step) ─────────────────────
    def evaluate(self, dx: int, dy: int, obs: dict) -> tuple:
        """Evaluate one candidate step.

        Returns (danger: bool|None, rule: EECTemporalRule|None).
        Returns (None, None) if blocked by a wall.

        Verdict pipeline:
          1. ExpectationMemory.query_outcome — single contest over ALL rules
             (innate + learned + derived), specificity-first, staleness-weighted,
             and gated so only reality-tested rules may suppress simulation.
          2. EECReasoner.chained_danger — multi-step (t ≥ 2) threats only;
             a chained threat can upgrade a 'safe' direct verdict.
          3. Internal Model simulation + EEC Expectation Formation when memory
             has no confident answer.
        """
        tx, ty = obs['ptx']+dx, obs['pty']+dy
        if not (0 <= tx < COLS and 0 <= ty < ROWS) or self.grid[ty][tx] == 1:
            return None, None

        tile_fluents, event = self._get_tile_fluents(dx, dy, tx, ty, obs)
        t = obs.get('sim_time', 0)
        dynamic_scene = bool(obs.get('dtraps') or obs.get('enemies') or
                             obs.get('_sim_dtraps') or obs.get('_sim_enemies'))

        # ── memory-first: skip simulation when we have a confident, tested prior ──
        has_moving_or_timing = any(
            f.name in ("MovingHazard", "DynamicHazard", "TrapActive",
                       "TrapImminent", "TrapInactive", "PredictedCollision",
                       "CollisionPath")
            for f in tile_fluents
        )

        degrees = self.memory.calibration.degrees_for(
            obs['trap_map'].get((tx, ty)))
        if self.use_memory:
            is_dangerous, prior_rule = self.memory.query_outcome(
                tile_fluents, event, self.danger_thresh, t=t,
                require_tested=True, degrees=degrees)
        else:
            # sim_only / avoidant ablations
            is_dangerous, prior_rule = None, None

        # safe memories are usually too stale for moving/timed hazards — the
        # trap phase may have changed since the rule was formed.  exception:
        # a safe rule explicitly conditioned on holdsat(trapinactive, t) is
        # phase-anchored, not phase-blind.  trapinactive is only perceived
        # when the hazard is > 10 ticks from activating, and the verdict is
        # consumed one step later — the trap cannot reach its active phase
        # in that window, so a wilson-licensed dormant-phase safe rule is as
        # sound as the simulation it replaces.  this is what finally lets
        # the agent reuse its learned safe windows of cycling traps.
        if (is_dangerous is False and prior_rule is not None
                and (has_moving_or_timing or dynamic_scene)
                and _safe_verdict_is_stale_risky(prior_rule, tile_fluents)):
            self.memory.diag_safe_voided += 1
            is_dangerous, prior_rule = None, None
        if (dynamic_scene and is_dangerous is True and prior_rule is not None and
                not _rule_has_specific_motion_context(prior_rule)):
            self.memory.diag_danger_voided += 1
            is_dangerous, prior_rule = None, None

        if is_dangerous is not None:
            # a 'safe' direct verdict can still be upgraded by a chained threat
            if (is_dangerous is False and self.eec_reasoner is not None and
                    self.eec_reasoner.chained_danger(tile_fluents, event)):
                chain_rule = EECTemporalRule(
                    event=Event("Move"),
                    preconditions=(Fluent("ChainThreat"),),
                    effect_type="Initiates", effect=Fluent("Damaged"),
                    delay=1, confidence=0.6)
                self.memory.sims_skipped += 1
                return True, chain_rule
            if prior_rule is not None:
                self.memory.log_reuse(prior_rule, "mem", t)
            self.memory.sims_skipped += 1
            return is_dangerous, prior_rule

        # ── no confident prior — run internal model and form expectation ────────
        if not self.use_sim:
            # no internal model available for this mode: cannot simulate, so an
            # unknown tile is treated as provisionally safe.  the agent then
            # learns only from real-world feedback (step 8).
            return False, None
        self.memory.sims_run += 1
        sim = self._sim_step(dx, dy, obs['ptx'], obs['pty'], obs)
        if sim is None:
            return None, None
        rule   = (self._form_expectations(dx, dy, sim, obs, t)
                  if self.use_memory else None)
        danger = sim['danger']

        # check for chained eec danger when direct simulation finds tile safe
        if not danger and self.eec_reasoner is not None:
            if self.eec_reasoner.chained_danger(tile_fluents, event):
                chain_rule = EECTemporalRule(
                    event=Event("Move"),
                    preconditions=(Fluent("ChainThreat"),),
                    effect_type="Initiates", effect=Fluent("Damaged"),
                    delay=1, confidence=0.6)
                return True, chain_rule
        return danger, rule


def build_innate_rules() -> list:
    """Innate EEC rules — interoceptive embodiment ONLY by default.

    With INNATE_WORLD_PRIORS = False (default), the agent is born knowing
    nothing about the ENVIRONMENT's causal structure.  HighTemperature → Burn,
    HazardPresent → Damaged, EnemyNearby → Damaged and every other
    sensor→outcome link must be learned — via internal simulation
    (Algorithm 1), real-world surprises (Algorithm 2), and vicarious
    observation — with preconditions screened for causal relevance by the
    CausalLedger.  Because evaluate() falls back to the Internal Model
    whenever memory has no confident tested rule, the agent remains safe
    while these expectations are still unlearned: it simply simulates.

    What remains innate is knowledge of the agent's OWN BODY (interoception):
    how its statuses interact and decay.  An agent can plausibly be built
    knowing its body's dynamics without knowing anything about the world —
    the Popperian distinction between embodiment and environment.

    All rules, innate included, stay revisable via eqs. 2-3.
    """
    rules: list = []

    def innate(**kw):
        rules.append(EECTemporalRule(origin="innate", **kw))

    # ═══ interoceptive embodiment (always innate) ═════════════════════════
    # ── immobilising status → slowed (body dynamics) ──────────────────────
    for src in ("Snare", "Freeze"):
        innate(event=None,
               preconditions=(Fluent(src),),
               effect_type="Initiates", effect=Fluent("Slowed"),
               delay=1, confidence=0.85)
    # ── dot effects → damaged after delay (body dynamics) ─────────────────
    for dot in ("Burn", "Poison", "Curse"):
        innate(event=None,
               preconditions=(Fluent(dot),),
               effect_type="Initiates", effect=Fluent("Damaged"),
               delay=2, confidence=0.75)
    # ── status decay on clear tile (body dynamics) ────────────────────────
    for brief in ("Stun", "Slowed", "Slow"):
        innate(event=Event("Move"), preconditions=(Fluent(brief), Fluent("ClearAhead")),
               effect_type="Terminates", effect=Fluent(brief),
               delay=2, confidence=0.85)
    for immob in ("Snare", "Freeze"):
        innate(event=Event("Move"), preconditions=(Fluent(immob), Fluent("ClearAhead")),
               effect_type="Terminates", effect=Fluent(immob),
               delay=3, confidence=0.80)
    for dot in ("Burn", "Poison", "Curse"):
        innate(event=Event("Move"), preconditions=(Fluent(dot), Fluent("ClearAhead")),
               effect_type="Terminates", effect=Fluent(dot),
               delay=3, confidence=0.75)

    if not INNATE_WORLD_PRIORS:
        return rules

    # ═══ hand-written world priors (ablation only — learned otherwise) ════
    # ── sensor property → status effect (thermal, chemical, mechanical) ──
    for sensor, eff in [
            ("HighTemperature", "Burn"),
            ("LowTemperature",  "Freeze"),
            ("Toxic",           "Poison"),
            ("Constricting",    "Snare"),
            ("Corrupting",      "Curse"),
            ("Unstable",        "Slow")]:
        innate(event=Event("Move"),
               preconditions=(Fluent(sensor),),
               effect_type="Initiates", effect=Fluent(eff),
               delay=1, confidence=0.90)
        innate(event=Event("Move", ("?agent", "?tile")),
               preconditions=(Fluent(sensor, ("?tile",)),),
               effect_type="Initiates", effect=Fluent(eff, ("?agent",)),
               delay=1, confidence=0.90)
    # ── heavy/moving impact → stun (collision needed for moving objects) ─
    innate(event=Event("Move"),
           preconditions=(Fluent("HeavyImpact"),),
           effect_type="Initiates", effect=Fluent("Stun"),
           delay=1, confidence=0.85)
    innate(event=Event("Move"),
           preconditions=(Fluent("MovingHazard"), Fluent("CollisionPath")),
           effect_type="Initiates", effect=Fluent("Stun"),
           delay=1, confidence=0.90)
    # ── any sensed hazard → damaged (weak catch-all prior; revisable) ─────
    innate(event=Event("Move"),
           preconditions=(Fluent("HazardPresent"),),
           effect_type="Initiates", effect=Fluent("Damaged"),
           delay=1, confidence=0.85)
    innate(event=Event("Move", ("?agent", "?tile")),
           preconditions=(Fluent("HazardPresent", ("?tile",)),),
           effect_type="Initiates", effect=Fluent("Damaged", ("?agent",)),
           delay=1, confidence=0.85)
    # ── enemy contact → damaged ───────────────────────────────────────────
    innate(event=Event("Move"),
           preconditions=(Fluent("EnemyNearby"),),
           effect_type="Initiates", effect=Fluent("Damaged"),
           delay=1, confidence=0.65)
    # ── impaired movement + enemy → damaged (chained) ────────────────────
    for status in ("Slowed", "Snare", "Stun", "Curse"):
        innate(event=None,
               preconditions=(Fluent(status), Fluent("EnemyNearby")),
               effect_type="Initiates", effect=Fluent("Damaged"),
               delay=1, confidence=0.80)
    # ── any status + enemy → damaged ─────────────────────────────────────
    for status in ("Burn", "Freeze", "Snare", "Slow", "Curse", "Poison", "Stun"):
        innate(event=None,
               preconditions=(Fluent(status), Fluent("EnemyNearby")),
               effect_type="Initiates", effect=Fluent("Damaged"),
               delay=1, confidence=0.80)
    return rules


# =============================================================================
# eecreasoner — formal temporal reasoner with fluent inertia
#
# implements event calculus semantics from the paper (§iii-b):
# happens(e, t) ∧ holdsat(f₁..fₙ, t) → initiates(g, t+delay)
# fluents persist by inertia unless explicitly terminated.
#
# enables chained multi-step predictions, e.g.:
# move(east,t) ∧ holdsat(trapahead(beartrap),t)
# → initiates(snare, t+1)
# → initiates(slowed, t+2)     [snare→slowed rule]
# → initiates(damaged, t+3)    [slowed∧enemynearby rule]
# =============================================================================
class EECReasoner:
    """Formal Event Calculus reasoner used alongside ExpectationMemory.

    EECReasoner handles chained temporal reasoning while ExpectationMemory
    owns ALL rules (innate and learned) and their confidence dynamics.  The
    reasoner holds references to the same rule objects, pushed in via
    ExpectationMemory.sync_to_reasoner(); confidence updates therefore
    propagate automatically, and there is a single revisable rule base.
    """

    CHAIN_DANGER_HORIZON = 3
    # below this, a holdsat rule vetoes inertia
    HOLDS_PERSIST_THRESH = 0.35

    def __init__(self):
        self.rules: list = []
        self.chain_dangers_detected = 0
        # (frozenset fluents, event, horizon) → timeline
        self._cache: dict = {}
        # fluent name → best holdsat-rule confidence
        self._holds_conf: dict = {}
        self._holds_dirty = True
        # set when a confidence threshold is crossed
        self._cache_dirty = False

    def mark_cache_dirty(self):
        """Signal that a confidence update crossed a reasoner threshold, so the
        prediction cache must be rebuilt on the next per-tick checkpoint."""
        self._cache_dirty = True

    def clear_cache_if_dirty(self):
        """Per-tick checkpoint: only rebuild the cache when a threshold-crossing
        confidence update (or a structural rule change) has invalidated it.
        Continuous confidence drift that stayed on one side of every reasoner
        threshold leaves predictions unchanged, so the cache survives — turning
        most per-tick clears into no-ops on the hot reuse path."""
        if self._cache_dirty:
            self._cache.clear()
            self._holds_dirty = True
            self._cache_dirty = False

    def clear_cache(self):
        """Invalidate prediction cache (call once per agent tick — confidences
        may have moved — and on any rule-base change)."""
        self._cache.clear()
        self._holds_dirty = True



    def add_rule_if_new(self, rule: EECTemporalRule):
        """Register a rule object with the reasoner (no duplicates).

        Memory and reasoner now share the SAME rule objects, so confidence
        updates propagate by reference — no field copying needed.  A structural
        duplicate held as a different object (stale from an earlier sync) is
        replaced by the memory's object.
        """
        for i, r in enumerate(self.rules):
            if r is rule:
                self.mark_cache_dirty()
                return
            if (r.event == rule.event and
                    set(r.preconditions) == set(rule.preconditions) and
                    r.effect_type == rule.effect_type and
                    r.effect == rule.effect and
                    r.delay == rule.delay):
                self.rules[i] = rule
                self.mark_cache_dirty()
                return
        self.rules.append(rule)
        self.mark_cache_dirty()

    def remove_rule(self, rule: EECTemporalRule):
        """Remove a structurally matching rule from the EEC reasoner."""
        before = len(self.rules)
        self.rules = [r for r in self.rules if not (
            r.event == rule.event and
            set(r.preconditions) == set(rule.preconditions) and
            r.effect_type == rule.effect_type and
            r.effect == rule.effect and
            r.delay == rule.delay)]
        if len(self.rules) != before:
            self.mark_cache_dirty()

    @staticmethod
    def holds_at(fluent: Fluent, t: int, timeline: dict) -> bool:
        """HoldsAt(fluent, t): True if fluent is in the timeline at time t.
        Supports both exact (with args) and name-only (no args) queries.
        """
        bucket = timeline.get(t, set())
        if fluent.args:
            return fluent in bucket
        return any(f.name == fluent.name for f in bucket)

    def explain(self, tile: tuple, obs: dict, horizon: int = 3,
                player_statuses: dict = None) -> tuple:
        """Return causal proof trace for why moving to *tile* is dangerous.

        Built on the same build_fact_base() engine used for prediction, so the
        explanation can never diverge from the inference that produced the
        decision (Winfield's interpretability principle).

        Returns (trace, timeline) where trace is a list of
        (t_from, t_to, rule) tuples:
          HoldsAt(rule.preconditions, t_from) → rule.effect_type(rule.effect, t_to)
        """
        fluents  = self.get_tile_fluents(tile, obs, player_statuses)
        fb       = self.build_fact_base(set(fluents), Event("Move"), horizon)
        timeline = {t: set(fb.fluents_at(t)) for t in range(horizon + 1)}
        trace    = [(t_from, t_to, rule) for (t_from, t_to, _etype, rule) in fb.trace]
        return trace, timeline

    def _rule_matches(self, rule: EECTemporalRule,
                      fluents: set, events: list) -> bool:
        """Return True if the rule's event + all precondition fluents are satisfied."""
        return bool(self._rule_substitutions(rule, fluents, events))

    def _rule_substitutions(self, rule: EECTemporalRule,
                            fluents: set, events: list) -> list:
        """Return substitutions satisfying the rule's event and HoldsAt conditions."""
        substs = [dict()]
        if rule.event is not None:
            next_substs = []
            for event in events:
                if event.name != rule.event.name:
                    continue
                if not rule.event.args:
                    next_substs.extend(substs)
                    continue
                for subst in substs:
                    out = _unify_atom(rule.event, event, subst)
                    if out is not None:
                        next_substs.append(out)
            substs = next_substs
            if not substs:
                return []
        for f in rule.preconditions:
            next_substs = []
            for fluent in fluents:
                if fluent.name != f.name:
                    continue
                if not f.args:
                    next_substs.extend(substs)
                    continue
                for subst in substs:
                    out = _unify_atom(f, fluent, subst)
                    if out is not None:
                        next_substs.append(out)
            substs = next_substs
            if not substs:
                return []
        return substs

    def build_fact_base(self, current_fluents: set, candidate_event: Event,
                        horizon: int = 3,
                        extra_happens: dict | None = None) -> EECFactBase:
        """Derive a formal EEC timeline from Happens/HoldsAt facts and rules.

        EC axioms (paper §III-B), with two refinements:
          • Effects landing beyond the horizon are DROPPED, not clamped —
            clamping pulled e.g. a delay-2 DoT into the horizon and produced
            Damaged predictions earlier than the rules state.
          • LEARNED PERSISTENCE: blanket inertia is moderated by the HoldsAt
            rules formed per Algorithm 1 line 13.  A fluent carries forward by
            default, but if the agent has learned (through violations) that a
            property does NOT persist — its HoldsAt rule's confidence has been
            driven below HOLDS_PERSIST_THRESH — the fluent is dropped instead
            of inherited.  This is how the agent can learn that e.g. TrapActive
            does not persist, opening up the safe windows of cycling traps.
        """
        fb = EECFactBase()
        for fluent in current_fluents:
            fb.add_holds(fluent, 0)
        fb.add_happens(candidate_event, 0)
        if extra_happens:
            for t, events in extra_happens.items():
                for event in events:
                    fb.add_happens(event, t)

        for t in range(horizon):
            fluents_t = fb.fluents_at(t)
            events_t = list(fb.events_at(t))
            for rule in self.rules:
                if rule.confidence < 0.08:
                    continue
                target_t = t + max(1, rule.delay)
                if target_t > horizon:
                    # effect lands beyond the horizon — drop, don't clamp
                    continue
                substitutions = self._rule_substitutions(rule, fluents_t, events_t)
                for subst in substitutions:
                    effect = _instantiate_atom(rule.effect, subst)
                    event = _instantiate_atom(rule.event, subst)
                    if rule.effect_type == "Initiates":
                        fb.add_initiates(event, effect, t, target_t, rule)
                    elif rule.effect_type == "Terminates":
                        fb.add_terminates(event, effect, t, target_t, rule)
                    elif rule.effect_type == "HoldsAt":
                        # persistence assertion — only if still believed.
                        # a holdsat rule below holds_persist_thresh has been
                        # falsified as a persistence claim and must not
                        # re-assert the fluent it failed to keep.
                        if rule.confidence >= self.HOLDS_PERSIST_THRESH:
                            fb.add_initiates(event, effect, t, target_t, rule)

            next_fluents = set()
            for fluent in fluents_t:
                if fluent.name in ("Damaged", "Safe"):
                    # outcome markers are instantaneous, not state —
                    continue
                               # carrying them forward would let a direct t+1
                               # verdict masquerade as a multi-step chain
                if fb.clipped(fluent, t, t + 1):
                    continue
                hc = self._holds_confidence(fluent.name)
                if hc is not None and hc < self.HOLDS_PERSIST_THRESH:
                    # learned non-persistence vetoes inertia
                    continue
                next_fluents.add(fluent)
            for fluent in fb.terminates.get(t + 1, set()):
                next_fluents.discard(fluent)
            for fluent in fb.initiates.get(t + 1, set()):
                next_fluents.add(fluent)
            fb.holds[t + 1] = next_fluents
        return fb

    def _holds_confidence(self, name: str) -> float | None:
        """Best confidence among learned HoldsAt(f) → HoldsAt(f) persistence
        rules for fluent *name*; None if no such rule exists (default inertia).
        Max across directional variants: persistence is believed if ANY
        variant remains confident.  Rebuilt lazily when the rule base changes.
        """
        if self._holds_dirty:
            self._holds_conf = {}
            for r in self.rules:
                if (r.effect_type == "HoldsAt"
                        and len(r.preconditions) == 1
                        and r.preconditions[0].name == r.effect.name):
                    prev = self._holds_conf.get(r.effect.name)
                    if prev is None or r.confidence > prev:
                        self._holds_conf[r.effect.name] = r.confidence
            self._holds_dirty = False
        return self._holds_conf.get(name)

    def query_holds_at(self, fluent: Fluent, current_fluents: set,
                       candidate_event: Event, t: int,
                       extra_happens: dict | None = None) -> bool:
        fb = self.build_fact_base(current_fluents, candidate_event, t, extra_happens)
        return fb.holds_at(fluent, t)

    def predict(self, current_fluents: set, candidate_event: Event,
                horizon: int = 3) -> dict:
        """Return a formal EEC HoldsAt timeline for t=0..horizon."""
        fb = self.build_fact_base(current_fluents, candidate_event, horizon)
        return {t: set(fb.fluents_at(t)) for t in range(horizon + 1)}

    def predict_cached(self, current_fluents: set, candidate_event: Event,
                       horizon: int = 3) -> dict:
        """predict() with memoisation keyed on (fluents, event, horizon).

        During route evaluation the same (fluent-set, event) contexts recur
        many times per tick; caching makes the formal chain check far cheaper
        than the simulation it complements.  The cache is invalidated on any
        rule-base change and once per agent tick (confidences move under
        feedback), via clear_cache().
        """
        key = (frozenset(current_fluents), candidate_event, horizon)
        hit = self._cache.get(key)
        if hit is not None:
            return hit
        timeline = self.predict(current_fluents, candidate_event, horizon)
        if len(self._cache) > 512:
            self._cache.clear()
        self._cache[key] = timeline
        return timeline

    def chained_danger(self, current_fluents: set, candidate_event: Event,
                       horizon: int = CHAIN_DANGER_HORIZON) -> bool:
        """True if chained EEC inference predicts Damaged at t ≥ 2.

        Direct t+1 outcomes are adjudicated by ExpectationMemory.query_outcome
        (specificity contest between danger and safe rules); the reasoner's
        unique contribution is MULTI-STEP chains — e.g. Snare(t+1) →
        Slowed(t+2) → Damaged(t+3) — so only t ≥ 2 predictions count here.
        This stops the innate single-step priors from silently overriding more
        specific learned verdicts.
        """
        timeline = self.predict_cached(current_fluents, candidate_event, horizon)
        damaged = Fluent("Damaged")
        # find the earliest t>=2 at which damaged is predicted.
        hit_t = None
        for t in range(2, horizon + 1):
            if any(f.name == "Damaged" for f in timeline.get(t, ())):
                hit_t = t
                break
        if hit_t is None:
            return False
        # reliability gate: only veto if the predicted damaged is supported by a
        # reality-tested rule (innate or >=1 confirmation).  a chain that
        # reaches damaged solely through unconfirmed conjectures (e.g. a learned
        # enemynearby/chainthreat -> damaged rule with confirmations == 0, whose
        # wilson lcb is 0.0) must not hard-veto the only path forward — that is
        # the freeze that kept the agent out of rooms.  rebuild the fact base
        # (the cache stores only the timeline, not provenance) to inspect which
        # rules produced the prediction.
        fb = self.build_fact_base(current_fluents, candidate_event, horizon)
        if fb.initiated_by_tested_rule(damaged, hit_t):
            self.chain_dangers_detected += 1
            return True
        # untested conjecture only — defer to simulation / direct verdict.
        return False

    def get_tile_fluents(self, tile: tuple, obs: dict,
                         player_statuses: dict = None) -> set:
        """Derive the initial fluent set for a candidate move to *tile*."""
        tx, ty = tile
        fluents: set = set()
        trap_kind = obs['trap_map'].get((tx, ty))
        in_kinetic = (tx, ty) in obs.get('kinetic_tiles', set())
        fluents.update(tile_sensor_fluents(trap_kind, in_kinetic))
        if trap_kind:
            if TRAP_SENSORS.get(trap_kind, {}).get('mov', False):
                fluents.add(Fluent("DynamicHazard"))
            else:
                fluents.add(Fluent("StaticHazard"))
        if not trap_kind:
            fluents.add(Fluent("ClearAhead"))
        # enemynearby: enemy is on or directly adjacent to this tile
        if (tx, ty) in obs.get('enemy_tiles', set()):
            fluents.add(Fluent("EnemyNearby"))
        if (tx, ty) in obs.get('kinetic_tiles', set()) or (tx, ty) in obs.get('enemy_tiles', set()):
            fluents.add(Fluent("PredictedCollision"))
        # player's active status effects persist into the next step
        if player_statuses:
            for eff in player_statuses:
                fluents.add(Fluent(eff.capitalize()))
        else:
            fluents.add(Fluent("NoStatus"))
        # room type fluent for room-level priors
        rm = obs.get('room_of', {}).get((tx, ty))
        if rm is not None and hasattr(rm, 'rtype'):
            fluents.add(Fluent("Room", (rm.rtype,)))
        return fluents

    def chain_danger(self, tile: tuple, obs: dict,
                     horizon: int = CHAIN_DANGER_HORIZON,
                     player_statuses: dict = None) -> bool:
        """Tile-level wrapper around chained_danger().

        Called when direct evaluation finds no immediate danger, to catch
        indirect multi-step threats like:
          Snare(t+1) → Slowed(t+2) → Damaged(t+3)
          Burn(t+1)  → Damaged(t+3)   [DoT, delay 2]
        """
        fluents = self.get_tile_fluents(tile, obs, player_statuses)
        return self.chained_danger(fluents, Event("Move"), horizon)


STRAP_KINDS = {k for v in RTYPES.values() for k in v["straps"]}


class DynamicsModel:
    """Learned EEC dynamics expectations — laws about HOW things move and work.

    Supervisor feedback: outcome expectations of the form
        Move ∧ HazardPresent → Initiates(Damaged)
    are almost tautological — of course stepping on a trap hurts.  The richer
    Popperian move is to form expectations about the BEHAVIOUR of the world's
    objects (the way the paper's chess agent learned movement deltas), and to
    NAVIGATE by deduction from those laws rather than by point-wise damage
    rules.

    Representation.  Each tracked dynamic entity is observed every world tick
    as a state s(t) = (occupied tiles, active?).  The model conjectures the
    strongest available behavioural law: a PERIOD P such that

        ∀t:  s(t) = s(t − P)            (P = 1 ⇒ "this thing never changes")

    which, in EEC terms, is the rule

        Happens(Tick, t) ∧ HoldsAt(Phase(k, p), t)
            → Initiates(Phase(k, (p+1) mod P), t+1),
        HoldsAt(Phase(k, p), t) → HoldsAt(Occupies(k, Tiles_p), t)
                                  ∧ HoldsAt(Active(k) ↔ p ∈ A, t)

    stored in ExpectationMemory as a single reified law (effect fluent
    OccupancyLaw(kind, P)) so it participates in eqs. 2-4: every subsequent
    tick the law's prediction s(t−P) is compared against the observed s(t) —
    a confirmation or a Popperian refutation.  The maze deliberately injects
    stochastic jitter into trap ACTIVATION cycles, so laws over jittered
    hazards keep getting refuted, never reach a reliable Wilson bound, and are
    correctly never used to guarantee anything — while purely kinematic
    hazards (sweepers, fire bars, boulders, pendulums) are deterministic,
    learnable, and DO license guarantees.

    Navigation guarantee.  window_state(tile, k₀, k₁) deduces, from every
    reliability-licensed law, whether `tile` will be harmfully occupied at any
    t+k, k ∈ [k₀, k₁].  Three-valued verdict:
        'danger' — some licensed law entails harmful occupancy in the window;
        'free'   — every tracked entity near the tile is licensed-lawful and
                   none occupies it anywhere in the window;
        None     — an unmodelled / unlicensed mover could reach the tile, or
                   a law predicts occupancy in a non-harmful phase: no
                   guarantee either way, fall back to the Internal Model.
    """
    # ticks of state history kept per entity
    HIST           = 240
    # p = 1 ⇒ stationary law
    MIN_PERIOD     = 1
    # observed full repetitions before conjecturing p
    MIN_REPEATS    = 2
    # min observations before any conjecture
    WARMUP         = 24
    # wilson bound a law needs to license guarantees
    GUARANTEE_LCB  = 0.80

    def __init__(self, memory: 'ExpectationMemory'):
        self.memory  = memory
        # id(entity) → record
        self.inst: dict = {}
        # planning steps answered by deduction from laws
        self.answers = 0

    # ── perception: one snapshot per world tick ─────────────────────────────
    @staticmethod
    def _snapshot(dt) -> tuple:
        tmp: dict = {}
        _map_dtrap_tiles(dt, tmp)
        active, _ = _dtrap_phase(dt)
        return (frozenset(t for t, k in tmp.items() if k == dt.kind),
                bool(active))

    def observe(self, tick: int, dtraps: list):
        seen = set()
        for dt in dtraps:
            key = id(dt)
            seen.add(key)
            rec = self.inst.setdefault(key, dict(
                kind=dt.kind, hist=deque(maxlen=self.HIST),
                period=None, rule=None))
            state = self._snapshot(dt)
            h = rec['hist']
            # ── test the standing law (popperian: predict, then check) ──────
            if rec['period'] and len(h) >= rec['period']:
                predicted = h[-rec['period']][1]
                rule = rec['rule']
                if rule is not None:
                    self.memory.update(rule, predicted == state, tick)
                    if rule.confidence < self.memory.TAU_PRUNE * 2:
                        # law refuted (e.g. jittered activation) — retract and
                        # let a better conjecture form from fresh evidence.
                        rec['period'], rec['rule'] = None, None
            h.append((tick, state))
            # ── conjecture a new law ────────────────────────────────────────
            if rec['period'] is None and len(h) >= self.WARMUP:
                p = self._detect_period([s for _, s in h])
                if p:
                    rec['period'] = p
                    rec['rule']   = self.memory.form(EECTemporalRule(
                        event=Event("Tick"),
                        preconditions=(Fluent("Periodic", (dt.kind, p)),),
                        effect_type="HoldsAt",
                        effect=Fluent("OccupancyLaw", (dt.kind, p)),
                        delay=1, confidence=C_INIT, origin="learned",
                        last_observed_time=tick))
        # entities that vanished (world reset) — drop stale tracks
        for key in [k for k in self.inst if k not in seen]:
            del self.inst[key]

    def _detect_period(self, seq: list) -> int | None:
        """Smallest P with s(t) = s(t−P) over ≥ MIN_REPEATS·P recent samples."""
        n = len(seq)
        max_p = (n - 1) // (self.MIN_REPEATS + 1)
        for p in range(self.MIN_PERIOD, max_p + 1):
            span = min(n - p, p * self.MIN_REPEATS + 1)
            if all(seq[-i] == seq[-i - p] for i in range(1, span + 1)):
                # a constant law (p=1) must really be constant, not a trap
                # merely resting between activations: require the whole
                # history to agree before conjecturing immobility.
                if p == 1 and len(set(seq)) != 1:
                    continue
                return p
        return None

    # ── deduction: entailed occupancy over a future window ──────────────────
    def _licensed(self, rec) -> bool:
        r = rec.get('rule')
        return (rec.get('period') is not None and r is not None
                and r.reliability_lcb() >= self.GUARANTEE_LCB)

    def window_state(self, tile: tuple, k_from: int, k_to: int) -> tuple:
        """(verdict, confidence, rule) for `tile` over world ticks now+[k_from, k_to]."""
        verdict_free_conf = 1.0
        free_rule = None
        uncertain = False
        for rec in self.inst.values():
            h = rec['hist']
            if not h:
                continue
            # region this entity has been seen to occupy, and distance to tile
            reach = set().union(*(s[0] for _, s in h)) if h else set()
            if reach:
                dmin = min(abs(tx - tile[0]) + abs(ty - tile[1])
                           for tx, ty in reach)
            else:
                dmin = 99
            near_hard = tile in reach or dmin <= 1
            if not self._licensed(rec):
                # an unlawful (or not-yet-lawful) mover: its observed reach may
                # be incomplete, so treat a generous neighbourhood as unsafe to
                # guarantee.  falls back to the internal model.
                if dmin <= 6:
                    uncertain = True
                continue
            if not near_hard:
                # licensed law, full extent observed, tile untouched
                continue
            p    = rec['period']
            # one full period ending now
            base = [s for _, s in list(h)[-p:]]
            rule = rec['rule']
            occupied_inactive = False
            for k in range(k_from, k_to + 1):
                tiles, active = base[(k % p) - 1]
                if tile in tiles:
                    if active:
                        return ('danger', rule.reliability_lcb(), rule)
                    occupied_inactive = True
            if occupied_inactive:
                # present but dormant: no guarantee
                uncertain = True
            else:
                verdict_free_conf = min(verdict_free_conf,
                                        rule.reliability_lcb())
                free_rule = free_rule or rule
        if uncertain:
            return (None, 0.0, None)
        return ('free', verdict_free_conf, free_rule)

    @property
    def law_count(self) -> int:
        return sum(1 for r in self.inst.values() if r.get('period'))


class PEAgent:
    """Autonomous maze-navigation agent using Popperian Expectations.

    Navigates from START to EXIT by:
      • Building EEC expectations from internal simulations of each candidate move
      • Skipping re-simulation when a high-confidence expectation already exists
      • Confirming / violating stored expectations from real-world outcomes
    """
    # l r u d
    DIRS            = [(-1,0),(1,0),(0,-1),(0,1)]
    # game ticks between agent decisions
    STEP_TICKS      = 10
    # ── tunable forward-simulation parameters (exposed for benchmarking) ─────
    # rollout depth for goal-route / detour risk check
    GOAL_HORIZON     = 5
    # rollout depth for periodic committed-route recheck
    COMMIT_HORIZON   = 3
    # lookahead while deciding whether standing still is safe
    EVAC_HORIZON     = 3
    # max consecutive ticks holding for a safe window
    WAIT_MAX         = 40
    # consecutive step-6 waits before forcing a risky move
    DEADLOCK_MAX     = 3
    # max cumulative ticks a staged crossing may stay armed
    CROSSING_AGE_CAP = 60
                              # without advancing before it is abandoned (livelock cap)
    # tiles: confinement region around the anchor
    REGION_RADIUS    = 3
    # absolute ticks confined to a region before the
    REGION_CAP       = 120
                              # forced-progress deadlock valve engages
    # tiles to commit a forced goal-ward push (through threat)
    FORCE_PUSH_TILES = 4
    # ── net-progress watchdog tuning ──────────────────────────────────────────
    # ticks with no net goal-distance improvement before
    STAGNATION_CAP   = 90
                              # the authoritative livelock breaker engages
    # base tiles of forced goal-ward route to commit
    STAGNATION_PUSH_TILES = 8
                              # (escalates with repeated breaks)
    # consecutive window-execution failures before forcing the move
    WINDOW_FAIL_MAX  = 2
    # agent-step lookahead in _find_earliest_safe_window
    WINDOW_MAX_STEPS = 16
    # max steps to commit to a window before re-planning
    WINDOW_RELIABLE_STEPS = 4
                              # (≈ shortest jittered trap dwell; beyond this the
                              # forecast is unreliable due to per-cycle rng)
    # only high-confidence rules block simulation
    DANGER_THRESH   = 0.28
    # per-visit penalty — each revisit costs half a danger step
    REVISIT_PENALTY = 2.5
    # steps at same tile before forcing bfs rebuild
    STUCK_LIMIT     = 12

    # ── asynchronous deliberation (supervisor feedback #1) ────────────────────
    # the world always moves at world speed.  deliberation — internal-model
    # rollouts — happens inside the agent, concurrently with the world, and
    # never slows or pauses it.  the agent's internal processor completes
    # sim_budget_per_tick rollout steps per world tick, so a plan that needed
    # n rollout steps becomes available ⌈n / sim_budget_per_tick⌉ ticks after
    # it was requested; until then the agent continues its current behaviour
    # (committed motion, or holding position under reflex monitoring).
    # • the internal model is "fed the time it has": rollouts are anchored
    # at the world state expected when the plan will be adopted (clones
    # advanced by the estimated latency), not the state when planning
    # was requested.
    # • expectation-memory answers complete within the same tick — this is
    # the paper's §vi efficiency benefit realised in world time: a warm
    # memory keeps the agent moving while a memoryless agent's plans lag
    # behind a world that will not wait for them.
    # • innate reflexes (_reflex_threat) are system-1: they can pre-empt a
    # pending plan instantly when the ground underfoot turns deadly.
    WORLD_ASYNC_DELIBERATION = True
    # rollout steps the agent computes per world tick
    SIM_BUDGET_PER_TICK      = 5
    # anytime cutoff: max ticks before a plan is adopted
    MAX_PLAN_LATENCY         = 12

    def __init__(self, player, grid, end, room_of=None, memory=None,
                 mode: str = "popperian", trace_sink: list | None = None):
        self.player  = player
        self.grid    = grid
        self.end     = end
        self.room_of = room_of or {}
        self.memory  = memory if memory is not None else ExpectationMemory()
        # ── agent ablation mode (supervisor feedback #2 — baseline agents) ──
        # popperian   — full architecture (memory + internal simulation)
        # sim_only    — simulates every decision, never stores/reuses memory
        # avoidant    — innate hazard-distance heuristic, no pe machinery
        self.mode       = mode
        self.use_memory = mode in ("popperian",)
        self.use_sim    = mode in ("popperian", "sim_only")
        # ── asynchronous-deliberation state (supervisor feedback #1) ────────
        # (route, commit) awaiting adoption
        self._pending_plan     = None
        # world ticks until the plan is adopted
        self._pending_ticks    = 0
        # ema of rollout steps per planning call
        self._lead_ema         = 0.0
        # set by choose_action when full planning ran
        self._planned          = False
        # cumulative plan-latency ticks
        self.think_ticks_total = 0
        # per-decision trace (feedback #4)
        self.trace_sink        = trace_sink
        # ── learned dynamics expectations (supervisor feedback: "how things
        # work", not just "where i get hurt") ──────────────────────────────
        self.use_dynamics = mode in ("popperian",)
        self.dynamics     = DynamicsModel(self.memory)
        self.eec_reasoner = EECReasoner()
        # formal simulation time t (incremented each step)
        self.sim_time     = 0
        # single revisable rule base: innate embodiment priors are adopted into
        # memory (no-op if a persisted memory already holds revised versions),
        # then all rules — innate and learned — are pushed into the reasoner.
        self.memory.ensure_innate(build_innate_rules())
        self.memory.sync_to_reasoner(self.eec_reasoner)
        self.ce = ConsequenceEvaluator(grid, self.room_of, self.memory,
                                       self.DANGER_THRESH, self.eec_reasoner)
        self.ce.use_memory = self.use_memory
        self.ce.use_sim    = self.use_sim
        self._path:  list = []
        self._tick         = 0
        # rule acted on last step
        self._last_rule: EECTemporalRule | None = None
        # obs snapshot for surprise
        self._last_obs:  dict | None            = None
        # pre-move fluent context (algorithm 2)
        self._last_fluents: set | None = None
        # happens(a, t) of the pending move
        self._last_event: Event | None = None
        # id(enemy) → tile, for vicarious obs
        self._enemy_last_tiles: dict   = {}
        # ── persistent static-hazard memory ─────────────────────────────────
        # static traps never move, so a tile observed to hold one stays lethal
        # for the whole run.  remembering discovered static-trap tiles closes
        # the gap where the forward-cone perception forgot a trap behind the
        # agent and routed it back onto a known-lethal tile.  this is exactly a
        # retained falsified expectation ("entering this tile → damaged"): the
        # agent must still discover each trap once (fog of war preserved), but
        # never forgets one.  maps (tx, ty) → kind.
        self._known_static_traps: dict = {}
        # room the remembered traps belong to
        self._static_mem_room = None
        # diagnostic: details of the last predictable death
        self._last_postmortem = None
        # optional list collecting all postmortems
        self._pm_sink = None
        # ticks to suppress re-committing after a transit abort
        self._transit_abort_hold = 0
        self._took_damage  = False
        self._was_dead     = False
        self._visit_counts: dict = {}
        self._stuck_ticks  = 0
        # consecutive ticks holding for a safe window
        self._wait_streak  = 0
        self._last_pos     = None
        # recent distinct tiles (for a<->b oscillation detection)
        self._tile_history: list = []
        # recent chosen first-step dirs (stationary flip detection)
        self._dir_history:  list = []
        # ticks remaining in an oscillation-breaking hold
        self._osc_hold     = 0
        # consecutive confinement holds (livelock guard)
        self._confine_holds = 0
        # best (closest) distance-to-exit achieved so far
        self._best_goal_dist = None
        # centre tile of the region the agent is confined to
        self._region_anchor = None
        # absolute ticks spent confined near the anchor
        self._region_ticks  = 0
        # ── net-progress watchdog (authoritative livelock breaker) ────────────
        # gated only on net distance-to-exit, not on a local anchor or tile
        # change, so slow drifting orbits (which reset every other timer by
        # nudging out of the previous anchor's radius) cannot defeat it.  when
        # the agent fails to beat its best-ever goal distance for stagnation_cap
        # ticks, it commits a hard directional lock along a fresh goal-ward
        # route and forces it through the local region, escalating on repeats.
        # ticks since best goal distance improved
        self._stagnation_ticks  = 0
        # consecutive watchdog escapes (escalation)
        self._stagnation_breaks = 0
        # current force-push came from the net-progress
        self._watchdog_push     = False
                                        # watchdog → follower uses a relaxed (short-
                                        # horizon) enemy-intercept test so it will
                                        # actually traverse a parallel corridor past
                                        # a merely-nearby wanderer instead of vetoing
                                        # every tile a wanderer might drift near.
        # committed forced-progress detour route (deadlock valve)
        self._force_push_route = []
        # ticks remaining in a forced push
        self._force_push_ticks = 0
        # suppress immediate re-push after bounce escape
        self._force_push_cooldown = 0
        self._keys = {K_UP:False, K_DOWN:False, K_LEFT:False, K_RIGHT:False,
                      K_w:False,  K_s:False,    K_a:False,    K_d:False}
        # committed route; re-evaluated before replanning
        self.current_route      = []
        # steps remaining before replanning
        self.route_commit_steps = 0
        # finish one-tile escape from a swept body point
        self._hazard_evac_ticks = 0
        # last valid (dx,dy) returned by choose_action
        self.last_action        = None
        # deliberate look direction (turn head toward goal
        self._gaze_heading      = None
                                       # while stationary); overrides last_action for fov
        # consecutive ticks spent turning gaze (anti-spin cap)
        self._gaze_hold_count   = 0
        # consecutive ticks choose_action returned none
        self.same_tile_ticks    = 0
        # temporal window: direction to move when window opens
        self._window_action     = None
        # temporal window: agent steps remaining before acting
        self._window_wait       = 0
        # consecutive window-execution failures (forces a move)
        self._window_fail       = 0
        # direction of the most recently failed window
        self._window_fail_dir   = None
        # staged multi-tile crossing through a rotating hazard
        self._crossing_route    = []
        # ticks to hold before retrying the staged crossing
        self._crossing_wait     = 0
        # cumulative ticks this crossing has been armed (livelock cap)
        self._crossing_age      = 0
        # first step of the current sim-chosen room-entry plan
        self._entry_lock_dir    = None
        # hysteresis survives short staging/replan gaps
        self._entry_lock_ticks  = 0
        # renderer: next safe action the agent currently perceives
        self._debug_safe_action = None
        # renderer: perceived route/commitment being followed
        self._debug_planned_route = []
        # consecutive step-6 waits with no progress (multi-trap freeze)
        self._deadlock_count    = 0
        # committed-retreat countdown (set when cornered/stuck)
        self._escape_ticks      = 0
        # direction of the committed retreat
        self._escape_dir        = None
        # all dtraps in current room (updated each step)
        self._room_dtraps: list = []
        # all enemies in current room (updated each step)
        self._room_enemies: list = []

    # ── 2. object tracker-localiser ───────────────────────────────────────────
    def observe(self, straps, dtraps, enemies, hazard_pulse=None) -> dict:
        """Scan hazards and enemies within the agent's forward field of view.

        Perception is directional (see VISION_* config): the agent sees a
        forward cone along its heading plus peripheral tiles to each side, and
        is blind behind.  Anything outside the FOV is simply absent from the
        returned snapshot — the agent cannot reason about, or form expectations
        from, what it cannot see.  Only the *live objects* lists ('dtraps',
        'enemies') are filtered to the visible subset, so forward simulation
        also rolls forward only what the agent has actually perceived.
        """
        px, py = self.player.x, self.player.y
        ptx, pty = self.player.tx, self.player.ty
        # heading drives the vision cone.  while moving, the agent looks the way
        # it travels (last_action).  while deliberating/waiting at a tile, it can
        # deliberately turn its head toward its goal (_gaze_heading) — a real
        # navigator stops and looks down the corridor it wants to enter rather
        # than staring at the wall behind the direction it last stepped.  the
        # gaze is set one tick earlier by choose_action, so turning costs a tick
        # of perception latency (honest: you turn, then you see).
        heading = self._gaze_heading or _heading_from(self.last_action)

        def visible_tile(tx, ty):
            if not VISION_ENABLED:
                return math.hypot(tx - px, ty - py) <= FOG_REVEAL_DIST
            return _in_fov(tx - ptx, ty - pty, heading)

        def dtrap_visible(dt):
            if not VISION_ENABLED:
                return math.hypot(dt.ox - px, dt.oy - py) <= FOG_REVEAL_DIST + 4
            tmp: dict = {}
            _map_dtrap_tiles(dt, tmp)
            # seen if any occupied tile or its origin falls in the fov.
            if _in_fov(int(round(dt.ox)) - ptx, int(round(dt.oy)) - pty, heading):
                return True
            return any(visible_tile(tx, ty) for (tx, ty) in tmp)

        trap_map: dict = {}
        # static traps can be re-randomised on room re-entry (reloc_on_reentry),
        # so remembered positions are only valid until the agent leaves a room.
        # detect a room change and forget the traps of the room just left; the
        # agent will rediscover them (possibly relocated) on its next visit.
        # within a room the memory persists, which is exactly the case the
        # "never walk back onto a seen static trap" invariant needs.
        here_room_obj = self.room_of.get((ptx, pty))
        if here_room_obj is not getattr(self, "_static_mem_room", here_room_obj):
            left = self._static_mem_room
            self._known_static_traps = {
                pos: k for pos, k in self._known_static_traps.items()
                if self.room_of.get(pos) is not left}
        self._static_mem_room = here_room_obj
        for t in straps:
            if visible_tile(t.tx, t.ty):
                trap_map[(t.tx, t.ty)] = t.kind
                # remember this static trap until the agent leaves the room.
                self._known_static_traps[(t.tx, t.ty)] = t.kind
        # recall discovered static traps even when now outside the vision cone.
        for (tx, ty), kind in self._known_static_traps.items():
            trap_map.setdefault((tx, ty), kind)

        visible_dtraps = [dt for dt in dtraps if dtrap_visible(dt)]
        for dt in visible_dtraps:
            # only the tiles of a visible dynamic trap that are themselves in
            # view are mapped — the agent sees the part of a long hazard that
            # is in front of it, not the segment trailing behind.
            tmp: dict = {}
            _map_dtrap_tiles(dt, tmp)
            for (tx, ty), kind in tmp.items():
                if visible_tile(tx, ty):
                    trap_map[(tx, ty)] = kind

        visible_enemies = [e for e in enemies
                           if visible_tile(int(e.x), int(e.y))]
        enemy_tiles: set = _enemy_tiles_from_list(visible_enemies)

        # kinetic_tiles: visible tiles occupied by moving (dynamic) traps —
        # used for collisionpath fluent in tile_sensor_fluents()
        kinetic_tiles: set = set()
        for dt in visible_dtraps:
            if TRAP_SENSORS.get(dt.kind, {}).get('mov', False):
                kinetic_tiles.update(
                    tile for tile, kind in trap_map.items() if kind == dt.kind)

        # dtrap_activity: kind → (is_active, ticks_until_active) for visible traps.
        # when multiple traps of the same kind exist, keep the most threatening one.
        dtrap_activity: dict = {}
        dtrap_activity_by_tile: dict = {}
        for dt in visible_dtraps:
            active, ticks = _dtrap_phase(dt)
            prev_active, prev_ticks = dtrap_activity.get(dt.kind, (False, 9999))
            if active or ticks < prev_ticks:
                dtrap_activity[dt.kind] = (active, ticks)
            tmp: dict = {}
            _map_dtrap_tiles(dt, tmp)
            for tile, tk in tmp.items():
                if tk != dt.kind or not visible_tile(tile[0], tile[1]):
                    continue
                prev = dtrap_activity_by_tile.get(tile)
                if prev is None or active or ticks < prev[2]:
                    dtrap_activity_by_tile[tile] = (dt.kind, active, ticks)

        return {'trap_map': trap_map, 'enemy_tiles': enemy_tiles,
                'kinetic_tiles': kinetic_tiles,
                'dtrap_activity': dtrap_activity,
                'dtrap_activity_by_tile': dtrap_activity_by_tile,
                'dtraps': visible_dtraps,  # visible live objects for simulation
                'enemies': visible_enemies,  # visible live objects for simulation
                'px': self.player.x, 'py': self.player.y,
                'ptx': self.player.tx, 'pty': self.player.ty,
                'heading': heading,
                'player_statuses': dict(self.player.statuses),
                'pulse_spd_mod': self.player.pulse_spd_mod,
                'hazard_pulse_active': bool(getattr(hazard_pulse, 'active', False)),
                'hazard_pulse_kind': getattr(hazard_pulse, 'kind', None),
                'room_of': self.room_of}

    # ── 3+5. internal model and eec formation → see consequenceevaluator ────────

    # ── 1. robot controller ────────────────────────────────────────────────────
    def _valid_step(self, action, ptx: int, pty: int) -> bool:
        """True only for one-tile cardinal moves into walkable grid cells."""
        if action not in self.DIRS:
            return False
        dx, dy = action
        tx, ty = ptx + dx, pty + dy
        return (0 <= tx < COLS and 0 <= ty < ROWS and self.grid[ty][tx] == 0)

    def _has_dynamic_threats(self, obs: dict) -> bool:
        """True when a snapshot contains hazards whose future position matters."""
        return bool(obs.get('dtraps') or obs.get('enemies') or
                    obs.get('_sim_dtraps') or obs.get('_sim_enemies') or
                    getattr(self, '_room_dtraps', None) or
                    getattr(self, '_room_enemies', None))

    def _one_step_danger(self, action, obs) -> tuple:
        """Evaluate an adjacent move, using forward simulation for moving threats."""
        dx, dy = action
        tx, ty = obs['ptx'] + dx, obs['pty'] + dy
        # hard static-hazard constraint: a known stationary trap is never a
        # valid destination, independent of any moving-threat reasoning.
        if self._tile_has_known_static_trap((tx, ty), obs):
            return True, None
        if self._has_dynamic_threats(obs):
            sim = self._make_sim_state(obs)
            self.memory.sims_run += 1
            sim = self._simulate_tick(sim, dx, dy)
            arrived = sim.get('_arrived', True)
            eval_dx, eval_dy = (dx, dy) if arrived else (0, 0)
            danger, rule = self.ce.evaluate(eval_dx, eval_dy, sim)
            # note: '_arrived' only reports whether the simulated body reached
            # the target tile's centre within one step_ticks window.  when the
            # body starts off-centre (e.g. mid-transit while the agent is
            # oscillating), a single step legitimately falls short of the centre
            # even though the move is completely safe.  treating "did not arrive"
            # as lethal therefore created a self-reinforcing trap: bouncing keeps
            # the body off-centre → every candidate move looks like a failed
            # arrival → flagged lethal → the agent keeps bouncing and never
            # finishes a maze.  danger is determined only by an actual predicted
            # outcome (danger) or a real mid-transit collision (_transit_hit);
            # non-arrival is a timing fact, not a hazard.
            hit = bool(danger or sim.get('_transit_hit'))
            # fixed-point straddle guard is only a hold verdict.  for a real
            # move, _simulate_tick already starts from the body's current
            # sub-tile position and samples the moving transit.  reusing the
            # fixed-point sweep for moving actions made every escape step look
            # lethal when the current point was about to be swept, trapping the
            # agent in the arc it was trying to leave.
            if not hit and dx == 0 and dy == 0 and self._straddle_sweep_hits(obs):
                hit = True
            return hit, rule
        danger, rule = self.ce.evaluate(dx, dy, obs)
        return bool(danger), rule

    def _straddle_sweep_hits(self, obs, ticks: int | None = None) -> bool:
        """True if any modelled hazard sweeps through the body's ACTUAL current
        sub-tile position over the next *ticks* game ticks (default STEP_TICKS),
        holding the body in place.

        This complements the tile-centre move projection in _simulate_tick: it
        catches a fast rotating/sweeping hazard arriving at the precise point
        the body currently occupies (e.g. while stalled against the hazard or
        straddling a tile boundary), which a fresh full-step projection from the
        tile centre can miss because its transit window is misaligned with the
        body's real remaining motion.

        Held-position (not velocity-projected): projecting the body forward made
        the guard abort too eagerly, leaving the agent dithering NEAR the hazard
        and raising exposure — at a fixed decision granularity, over-vetoing
        backfires.  Checking the body's real fixed point is the stable operating
        point.
        """
        px = obs.get('px'); py = obs.get('py')
        if px is None or py is None:
            return False
        sim = self._make_sim_state(obs)
        dtraps = sim.get('_sim_dtraps', [])
        enemies = sim.get('_sim_enemies', [])
        if not dtraps and not enemies:
            return False
        stub = _SimPlayer(px, py)
        stub.pulse_spd_mod = sim.get('pulse_spd_mod', 1.0)
        horizon = self.STEP_TICKS if ticks is None else ticks
        for _ in range(horizon):
            for dt in dtraps:
                _sim_update_dtrap(dt, stub)
            for e in enemies:
                _sim_update_enemy(e)
            for dt in dtraps:
                if _dtrap_hits_point(dt, px, py):
                    return True
            for e in enemies:
                if _enemy_hits_point(e, px, py):
                    return True
        return False

    # hold-safety lookahead (game ticks).  a held body does not advance, so a
    # long horizon here does not raise exposure the way it would for a moving
    # body — it simply lets the agent see a slowly-approaching rotating arm in
    # time to step off its real sub-tile position (which may sit at a tile edge
    # inside the arm's arc even while the tile centre looks safe).  sized to a
    # little over the slowest fire-bar/beam half-sweep across a tile.
    HOLD_SWEEP_TICKS = 60

    def _hold_position_swept(self, obs) -> bool:
        """True if standing at the body's CURRENT real position will be swept by
        a rotating/sweeping hazard within HOLD_SWEEP_TICKS.

        Tile-centre hold checks (_route_risk on (ptx,pty)) miss this: the body
        can be parked at a tile EDGE that lies in a rotating arm's path while the
        tile CENTRE the planner evaluates stays clear.  Evaluating the real
        sub-tile point closes that gap — the direct cause of the spinning-flame
        deaths where the agent stalled off-centre and was ground into.

        Cost guard: the long horizon is only needed for slow rotating/sweeping
        arms (fire_bar / ice_beam) whose lethal arc approaches over many ticks.
        Skip the expensive sweep entirely unless such a hazard is near the body,
        so ordinary holds stay cheap and the frame budget is preserved."""
        cache = getattr(self, '_decision_cache', None)
        cache_key = None
        if cache is not None:
            cache_key = (obs.get('sim_time'), obs.get('ptx'), obs.get('pty'),
                         round(obs.get('px', obs.get('ptx', 0)), 2),
                         round(obs.get('py', obs.get('pty', 0)), 2))
            sweep_cache = cache.setdefault('hold_swept', {})
            if cache_key in sweep_cache:
                return sweep_cache[cache_key]
        if not self._rotating_hazard_near(obs):
            if cache is not None:
                cache['hold_swept'][cache_key] = False
            return False
        result = self._straddle_sweep_hits(obs, ticks=self.HOLD_SWEEP_TICKS)
        if cache is not None:
            cache['hold_swept'][cache_key] = result
        return result

    def _current_tile_has_near_threat(self, obs, eta_ticks: int | None = None) -> bool:
        """Cheap prefilter for expensive hold-route simulations."""
        tile = (obs['ptx'], obs['pty'])
        if tile in obs.get('trap_map', {}) or tile in obs.get('enemy_tiles', set()):
            return True
        eta = self.EVAC_HORIZON * self.STEP_TICKS if eta_ticks is None else eta_ticks
        return self._enemy_threatens_at(tile, eta)

    def _body_enemy_contact_soon(self, obs, ticks: int | None = None) -> bool:
        """True if any currently known enemy will touch the body's real point.

        Tile-centre enemy checks miss the failure mode where the agent is
        physically parked near an edge or corner and a roaming enemy's circular
        body overlaps that exact sub-tile position before the tile centre looks
        occupied.  This mirrors the real update order: the player holds/moves,
        enemies advance on their current deterministic leg, then collision is
        tested against the real body position.
        """
        px = obs.get('px'); py = obs.get('py')
        if px is None or py is None:
            return False
        horizon = self.STEP_TICKS if ticks is None else ticks
        source_enemies = list(getattr(self, '_room_enemies',
                                      obs.get('enemies', [])))
        cache_key = (
            horizon, obs.get('sim_time'),
            round(px, 2), round(py, 2),
            tuple((round(e.x, 2), round(e.y, 2),
                   round(getattr(e, 'spd', getattr(e, 'base_spd', 0.0)), 3),
                   getattr(e, 'waypoint', None), getattr(e, 'wait', 0))
                  for e in source_enemies)
        )
        cached = getattr(self, '_body_enemy_contact_cache', None)
        if cached is not None and cached[0] == cache_key:
            return cached[1]

        enemies = [_clone_enemy(e) for e in source_enemies]
        if not enemies:
            self._body_enemy_contact_cache = (cache_key, False)
            return False
        for e in enemies:
            if _enemy_hits_point(e, px, py, margin=PLAYER_HIT_RADIUS + 0.08):
                self._body_enemy_contact_cache = (cache_key, True)
                return True
        for _ in range(horizon):
            for e in enemies:
                _sim_update_enemy(e)
                if _enemy_hits_point(e, px, py, margin=PLAYER_HIT_RADIUS + 0.08):
                    self._body_enemy_contact_cache = (cache_key, True)
                    return True
        self._body_enemy_contact_cache = (cache_key, False)
        return False

    def _body_dtrap_contact_soon(self, obs, ticks: int | None = None) -> bool:
        """True if a known dynamic trap will touch the body's real point."""
        px = obs.get('px'); py = obs.get('py')
        if px is None or py is None:
            return False
        horizon = self.STEP_TICKS if ticks is None else ticks
        source_dtraps = list(getattr(self, '_room_dtraps',
                                     obs.get('dtraps', [])))
        cache_key = (
            horizon, obs.get('sim_time'),
            round(px, 2), round(py, 2),
            tuple((dt.kind,
                   round(getattr(dt, 'ox', 0.0), 2),
                   round(getattr(dt, 'oy', 0.0), 2),
                   round(getattr(dt, 'px', getattr(dt, 'ox', 0.0)), 2),
                   round(getattr(dt, 'py', getattr(dt, 'oy', 0.0)), 2),
                   round(getattr(dt, 'vx', 0.0), 3),
                   round(getattr(dt, 'vy', 0.0), 3),
                   getattr(dt, 'active', None),
                   getattr(dt, 'state', None),
                   getattr(dt, 'timer', None))
                  for dt in source_dtraps)
        )
        cached = getattr(self, '_body_dtrap_contact_cache', None)
        if cached is not None and cached[0] == cache_key:
            return cached[1]

        dtraps = [_clone_dtrap(dt) for dt in source_dtraps]
        if not dtraps:
            self._body_dtrap_contact_cache = (cache_key, False)
            return False
        stub = _SimPlayer(px, py)
        stub.pulse_spd_mod = obs.get('pulse_spd_mod', 1.0)
        for dt in dtraps:
            if _dtrap_hits_point(dt, px, py):
                self._body_dtrap_contact_cache = (cache_key, True)
                return True
        for _ in range(horizon):
            for dt in dtraps:
                _sim_update_dtrap(dt, stub)
            for dt in dtraps:
                if _dtrap_hits_point(dt, px, py):
                    self._body_dtrap_contact_cache = (cache_key, True)
                    return True
        self._body_dtrap_contact_cache = (cache_key, False)
        return False

    def _dtrap_clearance_at_point(self, x: float, y: float, obs,
                                  ticks: int | None = None) -> float:
        """Minimum continuous body clearance from rolling boulders."""
        horizon = self.STEP_TICKS if ticks is None else ticks
        dtraps = []
        for dt in getattr(self, '_room_dtraps', obs.get('dtraps', [])):
            if dt.kind != "rolling_boulder":
                continue
            speed = math.hypot(getattr(dt, "vx", 0.0), getattr(dt, "vy", 0.0))
            radius = getattr(dt, "radius", 0.6) + PLAYER_HIT_RADIUS
            reach = speed * horizon + radius + 1.5
            if math.hypot(dt.px - x, dt.py - y) <= reach:
                dtraps.append(_clone_dtrap(dt))
        if not dtraps:
            return 99.0
        stub = _SimPlayer(x, y)
        stub.pulse_spd_mod = obs.get('pulse_spd_mod', 1.0)
        best = 99.0
        for tick in range(horizon + 1):
            for dt in dtraps:
                radius = getattr(dt, "radius", 0.6) + PLAYER_HIT_RADIUS
                best = min(best, math.hypot(dt.px - x, dt.py - y) - radius)
            if tick < horizon:
                for dt in dtraps:
                    _sim_update_dtrap(dt, stub)
        return best

    def _enemy_clearance_at_point(self, x: float, y: float, obs,
                                  ticks: int | None = None) -> float:
        """Minimum body clearance from known enemies at a fixed point."""
        horizon = self.STEP_TICKS if ticks is None else ticks
        enemies = [_clone_enemy(e) for e in getattr(self, '_room_enemies',
                                                    obs.get('enemies', []))]
        if not enemies:
            return 99.0
        best = 99.0
        for _ in range(horizon + 1):
            for e in enemies:
                radius = getattr(e, "RADIUS", 0.45) + PLAYER_HIT_RADIUS
                best = min(best, math.hypot(e.x - x, e.y - y) - radius)
            if _ < horizon:
                for e in enemies:
                    _sim_update_enemy(e)
        return best

    # deterministic continuously-sweeping hazards whose lethal geometry moves
    # predictably but can approach a fixed point over many ticks (longer than a
    # single step_ticks lookahead).  the hold-position sweep + variable commit
    # cadence protect against all of these.  random-phase or player-seeking
    # movers are deliberately excluded — their future is not exactly knowable,
    # so a death to them is not a sim bug and over-guarding only raises exposure.
    _SLOW_ARM_KINDS = frozenset({
        "fire_bar", "ice_beam",  # rotating arms (pivot geometry)
        "lava_tide", "ice_sweeper",  # linear room-sweeps (deterministic)
        "pendulum_axe",  # swinging arc (deterministic)
    })

    # kinds whose geometry isn't cleanly bounded by an origin radius (they sweep
    # across the whole room); treat them as "near" whenever present in the room,
    # since their swept band can reach the body from across the room.
    _ROOMWIDE_SWEEP_KINDS = frozenset({
        "lava_tide", "ice_sweeper",
    })

    def _rotating_hazard_near(self, obs, reach: int = 4) -> bool:
        """Cheap proximity test: is a slow deterministic sweeping hazard close
        enough to the body that its swept geometry could reach the body's tile
        within the hold horizon?  Origin-radius bound for pivot hazards
        (fire_bar/ice_beam/pendulum), and present-in-room for room-wide sweeps
        whose band crosses the whole room.  Robust to per-kind attribute
        differences."""
        px = obs.get('px'); py = obs.get('py')
        if px is None or py is None:
            return False
        bx, by = int(round(px)), int(round(py))
        room = self.room_of.get((bx, by))
        for dt in getattr(self, '_room_dtraps', obs.get('dtraps', [])):
            if dt.kind not in self._SLOW_ARM_KINDS:
                continue
            if dt.kind in self._ROOMWIDE_SWEEP_KINDS:
                # reaches across the room — count as near if it shares the room.
                dtile = (int(round(getattr(dt, 'ox', bx))),
                         int(round(getattr(dt, 'oy', by))))
                if room is None or self.room_of.get(dtile) is room:
                    return True
                continue
            # pivot hazards: bound by origin distance + arm/beam length.
            ox = getattr(dt, 'ox', None); oy = getattr(dt, 'oy', None)
            span = (getattr(dt, 'arm_len', None)
                    or getattr(dt, 'beam_len', None) or 3.5) + reach
            if ox is not None and abs(ox - bx) <= span and abs(oy - by) <= span:
                return True
        return False

    # ── static-hazard absolute constraint ────────────────────────────────────
    # a static trap never moves, so once perceived its tile is known for the
    # rest of the room visit (persistent static memory).  "never die to a static
    # hazard" is therefore enforceable as a hard constraint — such a tile is
    # simply not steppable — rather than a risk score that goal-pull or a
    # deadlock valve could override.  this is the agent retaining a falsified
    # expectation ("entering this tile → damaged") as an inviolable rule.
    def _tile_has_known_static_trap(self, tile, obs=None) -> bool:
        """True if *tile* carries a static trap the agent has perceived.

        Note: cracked_ice is excluded — it is a static *kind* but its effect is
        to break the floor over repeated contact, not an instant-kill on entry;
        treating it as unsteppable would wall off legitimate ice routes.  Every
        other static kind in this sim deals lethal contact damage, so entering a
        known one is never acceptable.
        """
        known = getattr(self, "_known_static_traps", {})
        k = known.get(tile)
        if k is not None and k != "cracked_ice":
            return True
        # also honour anything currently perceived as a static-trap tile, even
        # before it has been folded into persistent memory this tick.
        if obs is not None:
            tk = obs.get('trap_map', {}).get(tile)
            if tk in STRAP_KINDS and tk != "cracked_ice":
                return True
        return False

    def _body_in_known_static_trap(self, obs) -> bool:
        """True if the body's CURRENT sub-tile position lies within lethal
        contact range of any known static trap (catches a body that has crossed
        the contact radius mid-transit before reaching the tile centre)."""
        px = self.player.x
        py = self.player.y
        known = getattr(self, "_known_static_traps", {})
        for (tx, ty), k in known.items():
            if k == "cracked_ice":
                continue
            # statictrap.check_hit fires at dist < 0.55; veto a touch earlier so
            # the abort has a tick to act before the lethal threshold.
            if abs(tx - px) < 0.62 and abs(ty - py) < 0.62:
                if (tx - px) ** 2 + (ty - py) ** 2 < 0.62 ** 2:
                    return True
        return False

    def _transit_guard(self, obs):
        """Mid-transit re-decision (Winfield consequence-engine, continuous).

        The world moves every tick but moves commit over STEP_TICKS; a fast
        rotating/sweeping hazard can therefore sweep into a tile the body is
        already crossing, after the boundary decision cleared it.  Faithful to
        the architecture's concurrent internal model, the agent re-evaluates the
        in-flight move EVERY tick and aborts it the instant continuing turns
        lethal — rather than being locked in until the next tile centre.

        Returns an (action, rule) override when the current motion must change,
        or None when continuing the held action is still safe.  Abort options,
        in order of preference:
          1. Reverse toward the source tile centre if that retreat is safe.
          2. Hold position (None action) if standing is safer than advancing.
          3. As a last resort, return None and let the planner re-decide.
        """
        la = self.last_action
        if la is None or la not in self.DIRS:
            return None
        ptx, pty = obs['ptx'], obs['pty']
        tgt = (ptx + la[0], pty + la[1])

        # hard static constraint: never continue into a known static trap, and
        # bail out immediately if the body is already touching one.
        entering_static = self._tile_has_known_static_trap(tgt, obs)
        body_on_static = self._body_in_known_static_trap(obs)

        # dynamic danger of continuing the in-flight move this tick.
        dyn_danger = False
        if not entering_static and not body_on_static:
            dyn_danger, _ = self._one_step_danger(la, obs)
        if not (entering_static or body_on_static or dyn_danger):
            # continuing is safe — no override
            return None

        # the move is unsafe to continue.  try to retreat toward the tile the
        # body came from (its centre was safe a moment ago).
        rev = (-la[0], -la[1])
        if self._valid_step(rev, ptx, pty):
            rev_tgt = (ptx + rev[0], pty + rev[1])
            # don't reverse into a known static trap or a freshly-lethal tile.
            if not self._tile_has_known_static_trap(rev_tgt, obs):
                rev_danger, rrule = self._one_step_danger(rev, obs)
                if not rev_danger:
                    # brief abort cooldown: after reversing, don't let the very
                    # next tick re-commit forward into the same hazard (which
                    # produced a reverse/advance 2-tick limit cycle).  the hold
                    # lets the sweeping hazard pass before re-planning.
                    self._transit_abort_hold = self.STEP_TICKS
                    self.last_action = rev
                    return rev, rrule
        # can't safely reverse — hold position and let the next tick / planner
        # find a way out rather than walking into the hazard.
        self._transit_abort_hold = self.STEP_TICKS
        self._clear_motion_plan()
        self.last_action = None
        return None

    def _current_tile_will_be_unsafe(self, obs) -> bool:
        """Predict whether staying on the current tile is about to become unsafe."""
        cache = getattr(self, '_decision_cache', None)
        cache_key = None
        if cache is not None:
            cache_key = (obs.get('sim_time'), obs.get('ptx'), obs.get('pty'),
                         round(obs.get('px', obs.get('ptx', 0)), 2),
                         round(obs.get('py', obs.get('pty', 0)), 2))
            current_cache = cache.setdefault('current_unsafe', {})
            if cache_key in current_cache:
                return current_cache[cache_key]
        # real sub-tile body position: catches a rotating arm sweeping the tile
        # edge the body is parked on even when the tile centre stays clear.
        if self._hold_position_swept(obs):
            if cache is not None:
                cache['current_unsafe'][cache_key] = True
            return True
        if self._body_enemy_contact_soon(obs, ticks=self.STEP_TICKS):
            if cache is not None:
                cache['current_unsafe'][cache_key] = True
            return True
        if self._body_dtrap_contact_soon(obs, ticks=self.STEP_TICKS):
            if cache is not None:
                cache['current_unsafe'][cache_key] = True
            return True
        if not self._has_dynamic_threats(obs):
            if cache is not None:
                cache['current_unsafe'][cache_key] = False
            return False
        if not self._current_tile_has_near_threat(obs):
            if cache is not None:
                cache['current_unsafe'][cache_key] = False
            return False
        hold_route = [(obs['ptx'], obs['pty'])] * self.EVAC_HORIZON
        risk, _ = self._route_risk(hold_route, obs, horizon=self.EVAC_HORIZON)
        result = risk > 0
        if cache is not None:
            cache['current_unsafe'][cache_key] = result
        return result

    def _wait_is_safe(self, obs) -> bool:
        """True when holding position is safe over the near evacuation horizon."""
        cache = getattr(self, '_decision_cache', None)
        cache_key = None
        if cache is not None:
            cache_key = (obs.get('sim_time'), obs.get('ptx'), obs.get('pty'),
                         round(obs.get('px', obs.get('ptx', 0)), 2),
                         round(obs.get('py', obs.get('pty', 0)), 2))
            wait_cache = cache.setdefault('wait_safe', {})
            if cache_key in wait_cache:
                return wait_cache[cache_key]
        if self._hold_position_swept(obs):
            if cache is not None:
                cache['wait_safe'][cache_key] = False
            return False
        if self._body_enemy_contact_soon(obs, ticks=self.STEP_TICKS):
            if cache is not None:
                cache['wait_safe'][cache_key] = False
            return False
        if self._body_dtrap_contact_soon(obs, ticks=self.STEP_TICKS):
            if cache is not None:
                cache['wait_safe'][cache_key] = False
            return False
        if self._has_dynamic_threats(obs):
            if not self._current_tile_has_near_threat(obs):
                if cache is not None:
                    cache['wait_safe'][cache_key] = True
                return True
            hold_route = [(obs['ptx'], obs['pty'])] * self.EVAC_HORIZON
            risk, _ = self._route_risk(hold_route, obs, horizon=self.EVAC_HORIZON)
            result = risk == 0
            if cache is not None:
                cache['wait_safe'][cache_key] = result
            return result
        danger, _ = self.ce.evaluate(0, 0, obs)
        result = not danger
        if cache is not None:
            cache['wait_safe'][cache_key] = result
        return result

    def _evacuate_current_tile(self, obs):
        """Pick an adjacent tile to escape a soon-to-be-swept current tile."""
        ptx, pty = obs['ptx'], obs['pty']
        ex, ey = self.end
        # when a rotating arm (fire_bar/ice_beam/pendulum) is what makes the
        # current tile unsafe, the escape must leave the arm's reach annulus —
        # not merely step to whichever momentarily-clear neighbour sits closest
        # to the goal.  goal pull at a spinner edge selects a tile still inside
        # the swept radius, the agent drifts back, and the arm closes every exit
        # while it oscillates (the spinning-flame death).  detect the near arm
        # and make escaping the reach the dominant objective; verify the escape
        # tile survives the full sweep horizon, not just evac_horizon; and keep
        # goal distance only as a final tiebreak among equally-clear tiles.
        arm_near = self._rotating_hazard_near(obs)
        here_clear = self._rotator_clearance(ptx, pty) if arm_near else 99.0
        best = None
        best_rule = None
        for dx, dy in self.DIRS:
            tx, ty = ptx + dx, pty + dy
            if not self._valid_step((dx, dy), ptx, pty):
                continue

            immediate_danger, rule = self._one_step_danger((dx, dy), obs)
            hold_route = [(tx, ty)] * self.EVAC_HORIZON
            future_risk, future_rule = self._route_risk(
                hold_route, obs, horizon=self.EVAC_HORIZON)
            dtrap_clearance = self._dtrap_clearance_at_point(
                tx, ty, obs, ticks=self.EVAC_HORIZON * self.STEP_TICKS)
            dtrap_body_risk = dtrap_clearance < 0.10
            enemy_clearance = self._enemy_clearance_at_point(
                tx, ty, obs, ticks=self.EVAC_HORIZON * self.STEP_TICKS)
            enemy_body_risk = enemy_clearance < 0.10
            visits = self._visit_counts.get((tx, ty), 0)
            goal_dist = abs(tx - ex) + abs(ty - ey)

            if arm_near:
                # clearance of the destination from the nearest spinner arm
                # (negative ⇒ inside reach).  verify the tile also survives the
                # whole sweep, so we don't escape into the arc's far side.
                arm_clr = self._rotator_clearance(tx, ty)
                swept_full = self._tile_swept_within(
                    tx, ty, obs, ticks=self.HOLD_SWEEP_TICKS)
                # primary objective: get out of the reach annulus and stay out;
                # only then consider risk/visits/goal.  bucketing arm_clr into
                # "outside reach" first prevents a marginally-closer-to-goal but
                # still-inside-reach tile from winning.
                outside_reach = 0 if arm_clr > 0.0 else 1
                improves = 0 if arm_clr >= here_clear else 1
                score = ((1 if immediate_danger else 0),
                         1 if swept_full else 0,
                         outside_reach,
                         improves,
                         -round(arm_clr, 2),
                         future_risk,
                         1 if dtrap_body_risk else 0,
                         1 if enemy_body_risk else 0,
                         visits,
                         goal_dist)
            else:
                score = ((1 if immediate_danger else 0),
                         future_risk,
                         1 if dtrap_body_risk else 0,
                         -dtrap_clearance,
                         1 if enemy_body_risk else 0,
                         -enemy_clearance,
                         visits,
                         goal_dist)
            if best is None or score < best[0]:
                best = (score, (dx, dy))
                best_rule = rule or future_rule

        if best is None:
            return None
        return best[1], best_rule

    def _tile_swept_within(self, tx: int, ty: int, obs, ticks: int) -> bool:
        """True if a rotating/sweeping arm reaches tile-centre (tx,ty) within
        *ticks* game ticks — the moving-escape analogue of the hold sweep check,
        so an evacuation target is verified clear for the whole arm pass, not
        just the one-step horizon."""
        if not self._rotating_hazard_near(obs):
            return False
        sim = self._make_sim_state(obs)
        dtraps = [dt for dt in sim.get('_sim_dtraps', [])
                  if dt.kind in self._SLOW_ARM_KINDS]
        if not dtraps:
            return False
        cx, cy = float(tx), float(ty)
        for _ in range(max(1, ticks)):
            for dt in dtraps:
                _sim_update_dtrap(dt, None)
                if _dtrap_hits_point(dt, cx, cy):
                    return True
        return False

    def _sweep_evasion_step(self, obs):
        """Geometric evasion for room-wide horizontal sweeps (lava_tide,
        ice_sweeper).

        These hazards are a vertical lethal band that oscillates left<->right
        across the WHOLE room, so there is no permanently safe tile — the agent
        must stay on the side the wave has just left and time its crossing for
        when the band is far away or receding.  Generic tile routing mishandles
        this because every tile is periodically lethal; the band simply moves
        through them.

        Strategy: simulate the wave forward and, for the current tile and each
        adjacent tile, compute the MINIMUM horizontal clearance from the lethal
        band over a lookahead horizon.  If standing still will be swept, step to
        the neighbour that stays clear longest — which naturally retreats behind
        the advancing wave and holds there until it recedes, then allows the
        crossing.  Returns (action, rule) or None when no sweep evasion applies.
        """
        ptx, pty = obs['ptx'], obs['pty']

        def _band(dt):
            # returns (center_x, half_width) of the lethal vertical band, or none.
            if dt.kind == 'lava_tide':
                return getattr(dt, 'tide_x', None), getattr(dt, 'tide_w', 2.0) * 0.7
            if dt.kind == 'ice_sweeper':
                return getattr(dt, 'sweep_x', None), PLAYER_HIT_RADIUS + 0.18
            return None, None

        def _in_room_y(dt, y):
            rm = getattr(dt, 'room', None)
            if rm is None:
                return True
            return rm.y + 1 <= y <= rm.y + rm.h - 2

        sweeps = []
        for dt in getattr(self, '_room_dtraps', []):
            if dt.kind not in ('lava_tide', 'ice_sweeper'):
                continue
            cx, _ = _band(dt)
            if cx is None:
                continue
            # only react to a sweep that shares the agent's room band.
            if _in_room_y(dt, float(pty)):
                sweeps.append(dt)
        if not sweeps:
            return None

        horizon = max(self.EVAC_HORIZON * self.STEP_TICKS, 80)
        # safety pad beyond the lethal half-width so the agent keeps a margin.
        PAD = 0.50

        def ticks_until_hit(tile):
            """Ticks until any lethal band first reaches *tile* (capped at
            horizon+1 = 'stays safe').  Standing here is survivable for at least
            this many ticks."""
            x, y = float(tile[0]), float(tile[1])
            soonest = horizon + 1
            for src in sweeps:
                if not _in_room_y(src, y):
                    continue
                dt = _clone_dtrap(src)
                stub = _SimPlayer(x, y)
                for tick in range(horizon + 1):
                    if tick > 0:
                        _sim_update_dtrap(dt, stub)
                    cx, half = _band(dt)
                    if cx is None:
                        continue
                    if abs(x - cx) <= (half + PAD):
                        soonest = min(soonest, tick)
                        break
            return soonest

        cur_tile = (ptx, pty)
        cur_safe_ticks = ticks_until_hit(cur_tile)
        # comfortable margin: if the band won't reach the current tile for a
        # good while, no evasion needed — let normal planning proceed.
        # ~2 decision steps of breathing room
        SAFE_TICKS = 2 * self.STEP_TICKS
        if cur_safe_ticks > SAFE_TICKS:
            return None

        ex, ey = self.end
        best = None
        for dx, dy in self.DIRS:
            tx, ty = ptx + dx, pty + dy
            if not self._valid_step((dx, dy), ptx, pty):
                continue
            if self._tile_has_known_static_trap((tx, ty), obs):
                continue
            danger, rule = self._one_step_danger((dx, dy), obs)
            if danger:
                continue
            safe_ticks = ticks_until_hit((tx, ty))
            visits = self._visit_counts.get((tx, ty), 0)
            goal_dist = abs(tx - ex) + abs(ty - ey)
            # maximise survivable time on the destination, then fewer revisits,
            # then goal progress.  moving to a longer-safe tile naturally steps
            # away from the advancing band (the side it has just left).
            score = (-safe_ticks, visits, goal_dist)
            if best is None or score < best[0]:
                best = (score, (dx, dy), rule, safe_ticks)

        # move if a neighbour buys more survivable time than staying put.
        if best is not None and best[3] > cur_safe_ticks:
            return best[1], best[2]
        # no neighbour is safer.  hold only if the current tile is survivable
        # for now (band not imminently here); the agent rides out the sweep and
        # re-evaluates next tick as the band recedes.  if the current tile is
        # about to be hit and nothing is better, still take the best available
        # move (least-bad) rather than standing in the fire.
        if cur_safe_ticks > self.STEP_TICKS:
            return ('HOLD', None)
        if best is not None:
            return best[1], best[2]
        return None

    def _spore_blast_zone(self, obs) -> set:
        """Tiles inside the reach of any spore burst that is expanding or about
        to fire.  Routing avoids this disc during the countdown so the agent
        never gets parked at a mid-radius tile the expanding front will sweep
        (which, since the ring grows ~as fast as the agent moves, is an
        un-outrunnable position).  Returns a set of (tx, ty)."""
        zone: set = set()
        for dt in getattr(self, '_room_dtraps', []):
            if dt.kind != 'spore_burst':
                continue
            state = getattr(dt, 'state', '')
            timer = getattr(dt, 'timer', 999)
            reach = getattr(dt, 'max_r', 3.0) + SPORE_RING_HIT_HALF_WIDTH
            # react to a burst that is expanding or will fire before the agent
            # could clear the disc.  the ring grows about as fast as the agent
            # moves, so crossing a disc of radius `reach` takes on the order of
            # 2*reach controller steps (~step_ticks world ticks each).  if the
            # vent will erupt within that crossing time, entering the disc now
            # means being inside it when the front sweeps out — fatal.  a fixed
            # 25-tick window missed slow-cycling vents the agent walked into
            # during a long 'wait', which then expanded through it.
            cross_ticks = int(2.0 * reach * getattr(self, 'STEP_TICKS', 6)) + 30
            if not (state == 'expanding' or timer <= cross_ticks):
                continue
            ox = getattr(dt, 'ox', None); oy = getattr(dt, 'oy', None)
            if ox is None:
                continue
            r = int(math.ceil(reach))
            ox_t, oy_t = int(round(ox)), int(round(oy))
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if dx * dx + dy * dy <= reach * reach:
                        zone.add((ox_t + dx, oy_t + dy))
        return zone

    def _spore_escape_step(self, obs):
        """Geometric escape for the expanding spore ring.

        The ring fires from a fixed origin and its radius advances ~1.2 tiles
        per controller step, sweeping outward (then retracting).  The ONLY
        durably safe place is outside the ring's maximum reach — any tile the
        ring's radius will pass through is lethal at the moment the expanding
        front arrives there.  The earlier version only dodged the annulus once
        it was already expanding; if the agent was loitering NEAR the origin
        during the pre-fire 'wait' countdown, the ring then expanded through it
        faster than a one-tile dodge could escape.

        Fix: react during the 'wait' countdown too, and when close to a soon-to-
        fire (or expanding) burst, drive the agent AWAY from the origin — toward
        the tile that maximises clearance from the ring band over the horizon,
        with distance-from-origin as the tie-breaker so it actively flees the
        blast centre rather than picking a marginally-better adjacent tile that
        the ring will still sweep.
        """
        ptx, pty = obs['ptx'], obs['pty']
        here_room = self.room_of.get((ptx, pty))
        spores = [dt for dt in getattr(self, '_room_dtraps', [])
                  if dt.kind == 'spore_burst'
                  and (dt.room is here_room
                       or math.hypot(dt.ox - ptx, dt.oy - pty) <= 10)
                  and (getattr(dt, 'state', '') == 'expanding'
                       or getattr(dt, 'timer', 999) <= 35)]
        if not spores:
            return None

        horizon = max(self.EVAC_HORIZON * self.STEP_TICKS, 45)

        def clearance_at(tile):
            """Min clearance from any ring band over the horizon, simulating each
            burst forward (so a 'wait' burst that FIRES within the horizon is
            accounted for, not just one already expanding)."""
            x, y = tile
            worst = 99.0
            for src in spores:
                dt = _clone_dtrap(src)
                stub = _SimPlayer(x, y)
                for tick in range(horizon + 1):
                    if tick > 0:
                        _sim_update_dtrap(dt, stub)
                    # once expanding, the lethal band is at radius burst_r.
                    if dt.state == 'expanding' and dt.burst_r > 0.3:
                        d = math.hypot(dt.ox - x, dt.oy - y)
                        worst = min(worst, abs(d - dt.burst_r)
                                    - SPORE_RING_HIT_HALF_WIDTH)
            return worst

        # distance from the nearest soon-to-fire origin: the agent should be
        # outside the ring's max reach when it fires, so fleeing the origin is
        # the durable escape during the countdown.
        def origin_dist(tile):
            x, y = tile
            return min(math.hypot(src.ox - x, src.oy - y) for src in spores)

        cur_tile = (ptx, pty)
        cur_clear = clearance_at(cur_tile)
        cur_odist = origin_dist(cur_tile)
        # max ring reach across the active bursts (tiles).
        max_reach = max(getattr(src, 'max_r', 4.0) for src in spores)
        # if the current tile stays clear of the band for the whole horizon,
        # nothing to do (it is either well inside, well outside, or in a gap the
        # ring won't reach while we're here).
        if cur_clear > 0.75:
            return None

        ex, ey = self.end
        best = None
        for dx, dy in self.DIRS:
            tx, ty = ptx + dx, pty + dy
            if not self._valid_step((dx, dy), ptx, pty):
                continue
            if self._tile_has_known_static_trap((tx, ty), obs):
                continue
            danger, rule = self._one_step_danger((dx, dy), obs)
            if danger:
                continue
            clear = clearance_at((tx, ty))
            odist = origin_dist((tx, ty))
            visits = self._visit_counts.get((tx, ty), 0)
            goal_dist = abs(tx - ex) + abs(ty - ey)
            # maximise band clearance over the whole expansion.  this naturally
            # avoids the lethal shell at radius==burst_r and prefers tiles that
            # are either comfortably inside the ring's eventual radius or beyond
            # its max reach — never parked exactly on the expanding front.
            score = (-clear, visits, goal_dist)
            if best is None or score < best[0]:
                best = (score, (dx, dy), rule, clear, odist)

        if best is not None and best[3] > cur_clear + 1e-6:
            return best[1], best[2]

        # no outward/clear neighbour helps.  the ring front expands ~as fast as
        # the agent moves, so it cannot be outrun radially: fleeing outward just
        # gets caught on the max-radius shell.  if the agent is inside the ring's
        # reach and in the front's path, the safe play is to dive inward — get
        # to a distance the expanding front has already passed (the safe ring
        # interior, e.g. the origin tile itself) rather than standing where the
        # front will arrive.
        if cur_odist <= max_reach + 0.75:
            inward = None
            for dx, dy in self.DIRS:
                tx, ty = ptx + dx, pty + dy
                if not self._valid_step((dx, dy), ptx, pty):
                    continue
                if self._tile_has_known_static_trap((tx, ty), obs):
                    continue
                odist = origin_dist((tx, ty))
                # only consider tiles strictly closer to origin (diving inward).
                if odist >= cur_odist:
                    continue
                # the normal one-step danger flag marks the spore tile dangerous,
                # but inside the ring is exactly where we want to be — so don't
                # filter on it here.  instead require the destination to be safe
                # for the whole expansion at the body's real arrival (clearance),
                # i.e. the front never lands on it once we're there.
                clear = clearance_at((tx, ty))
                # prefer deepest-inside (closest to origin), then best clearance.
                score = (odist, -clear)
                if inward is None or score < inward[0]:
                    inward = (score, (dx, dy), None, clear)
            # dive inward only if the chosen inner tile stays clear of the front
            # (it is genuinely in the safe interior), not merely closer.
            if inward is not None and inward[3] > -0.2:
                return inward[1], inward[2]

        # fall back: take the least-bad clearance step if the current tile is
        # actually unsafe; otherwise hold.
        if cur_clear < 0.0 and best is not None:
            return best[1], best[2]
        return None

    def _clear_motion_plan(self, clear_last: bool = False):
        self.current_route = []
        self.route_commit_steps = 0
        self._hazard_evac_ticks = 0
        self._crossing_route = []
        self._crossing_wait = 0
        if clear_last:
            self._entry_lock_dir = None
            self._entry_lock_ticks = 0
        if clear_last:
            self.last_action = None
            self.same_tile_ticks = 0

    def _near_tile_center(self, tile: tuple, eps: float = 0.22) -> bool:
        tx, ty = tile
        return abs(self.player.x - tx) <= eps and abs(self.player.y - ty) <= eps

    def _route_commit_ticks(self, route: list, max_tiles: int = 1) -> int:
        """Keep a route alive long enough to actually cross tile boundaries."""
        tiles = max(1, min(len(route) if route else 1, max_tiles))
        return tiles * self.STEP_TICKS + 2

    def _escape_move(self, obs):
        """Cornered-retreat: choose an adjacent tile that moves AWAY from the
        nearest threat (enemy or moving hazard) and toward open space.

        Every other branch in choose_action pulls toward the GOAL; when the
        goal direction is blocked by a converging enemy the agent has no way to
        retreat and is overtaken in place.  This is the missing 'flee' — it
        ignores the goal entirely and maximises clearance from the nearest
        threat among tiles that are not immediately lethal, breaking out of the
        corner so normal planning can resume from safer ground.

        Returns (dx, dy) or None if no adjacent floor tile exists.
        """
        ptx, pty = obs['ptx'], obs['pty']
        px, py = self.player.x, self.player.y

        # nearest threat position (enemy first, then any positioned moving trap).
        threats = []
        for e in getattr(self, '_room_enemies', []):
            threats.append((math.hypot(e.x - px, e.y - py), e.x, e.y))
        for dt in getattr(self, '_room_dtraps', []):
            if not TRAP_SENSORS.get(dt.kind, {}).get('mov', False):
                continue
            hx = getattr(dt, "px", None)
            hy = getattr(dt, "py", None)
            if hx is None:
                continue
            if hy is None:
                hy = py
            threats.append((math.hypot(hx - px, hy - py), hx, hy))
        threats.sort()
        if threats:
            _, thx, thy = threats[0]
        else:
            thx, thy = px, py

        best = None
        for dx, dy in self.DIRS:
            tx, ty = ptx + dx, pty + dy
            if self._blocked_for_planning(tx, ty):
                continue
            lethal, _ = self._one_step_danger((dx, dy), obs)
            # clearance from the nearest threat after the move
            clr = math.hypot(tx - thx, ty - thy)
            visits = self._visit_counts.get((tx, ty), 0)
            # non-lethal tiles dominate; among them, maximise threat clearance
            # and prefer less-visited tiles (avoid pacing the same two tiles).
            score = (0 if lethal else 1000) + clr * 3.0 - visits * 0.4
            if best is None or score > best[0]:
                best = (score, (dx, dy))
        return best[1] if best else None

    def _least_bad_goal_step(self, obs):
        """Pick the adjacent step that best advances toward the exit while
        minimising immediate risk — the move the forced-progress valve commits
        when a perfectly-safe path does not exist.  Prefers, in order:
        non-lethal over lethal; greater reduction in distance-to-exit; greater
        clearance from the nearest enemy; less-visited tiles.  Returns a valid
        step if any adjacent floor tile exists, so the agent is never stuck for
        lack of a choice."""
        ptx, pty = obs['ptx'], obs['pty']
        ex, ey = self.end
        px, py = self.player.x, self.player.y
        nearest = None
        for e in getattr(self, '_room_enemies', []):
            dd = math.hypot(e.x - px, e.y - py)
            if nearest is None or dd < nearest[0]:
                nearest = (dd, e.x, e.y)
        best = None
        for dx, dy in self.DIRS:
            tx, ty = ptx + dx, pty + dy
            if self._blocked_for_planning(tx, ty):
                continue
            lethal, _ = self._one_step_danger((dx, dy), obs)
            d_goal = abs(tx - ex) + abs(ty - ey)
            clr = math.hypot(tx - nearest[1], ty - nearest[2]) if nearest else 99.0
            visits = self._visit_counts.get((tx, ty), 0)
            score = ((1 if not lethal else 0) * 100000
                     - d_goal * 100
                     + clr * 8.0
                     - visits * 1.5)
            if best is None or score > best[0]:
                best = (score, (dx, dy))
        return best[1] if best else None

    def _enemy_threatens_at(self, tile, eta_ticks, window=11):
        """Probabilistic enemy forecast over the high-confidence horizon.

        Even though a roaming enemy chooses its NEXT waypoint at random, its
        CURRENT leg is deterministic: it walks a straight line toward a known
        waypoint at ~base_spd.  This predicts the enemy position tick by tick
        along that leg and reports whether it comes within collision distance of
        `tile` during the window the agent would occupy it
        ([eta-window, eta+window]).  Prediction stops at the waypoint, beyond
        which the direction is random (low confidence) — so it never commits to
        a guessed future, only to what is actually determined.  This lets the
        planner refuse a step that walks into an enemy's predictable path even
        though the destination tile is clear at this instant (a 1-step safety
        check is structurally blind to a 2-tile-distant interception).
        """
        tx, ty = tile
        COLLIDE = 1.0
        lo = max(0, eta_ticks - window)
        hi = eta_ticks + window
        for e in getattr(self, '_room_enemies', []):
            ex, ey = e.x, e.y
            wait = getattr(e, 'wait', 0)
            spd = getattr(e, 'spd', getattr(e, 'base_spd', 0.06))
            wx, wy = e.waypoint
            dx, dy = wx - ex, wy - ey
            dist = math.hypot(dx, dy)
            ux, uy = (dx / dist, dy / dist) if dist > 1e-6 else (0.0, 0.0)
            for t in range(0, hi + 1):
                if t < wait:
                    # still paused
                    cx, cy = ex, ey
                else:
                    travelled = (t - wait) * spd
                    if travelled >= dist:
                        # reached waypoint
                        break
                    cx, cy = ex + ux * travelled, ey + uy * travelled
                if t >= lo and math.hypot(cx - tx, cy - ty) < COLLIDE:
                    return True
        return False

    def _form_rollout_expectation(self, obs, traj):
        """EEC Expectation Creation from a multi-ply rollout (diagram: Internal
        Model → Consequence Engine → EEC Creation/Update).

        A rollout that ends in death is a Popperian Expectation: the agent has
        learned, by internal simulation alone, that committing its goal-seeking
        policy from here leads to harm.  We anchor the expectation on the FIRST
        step of the predicted-fatal trajectory (the actionable decision), so the
        rule — once confirmed/strengthened by the update machinery — can later be
        REUSED to veto that step without re-running the whole rollout.
        """
        if not traj.get('died') or len(traj.get('path', [])) < 2:
            return None
        x0, y0 = traj['path'][0]
        x1, y1 = traj['path'][1]
        dx = int(round(x1 - x0)); dy = int(round(y1 - y0))
        if (dx, dy) not in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            return None
        tx, ty = obs['ptx'] + dx, obs['pty'] + dy
        kind = traj.get('death_kind')
        outcome_fluents = {Fluent("Damaged")}
        eff = TDEFS.get(kind, {}).get('eff') if kind else None
        if eff:
            outcome_fluents.add(Fluent(eff.capitalize()))
        sim = {'tx': tx, 'ty': ty, 'danger': True,
               'trap_kind': kind, 'enemy_near': (kind == 'enemy'),
               'outcome_fluents': outcome_fluents,
               'rollout_ply': traj.get('death_ply', -1)}
        try:
            rule = self.ce._form_expectations(dx, dy, sim, obs,
                                              obs.get('sim_time', 0))
            if rule is not None:
                self.memory.update(rule, True, obs.get('sim_time', 0))
            return rule
        except Exception:
            return None

    def _sim_timed_crossing(self, obs, max_wait=120):
        """Find a TIMED step through a deterministic mover using the internal sim.

        General replacement for hazard-specific dash logic: for the agent's
        intended next move(s), roll the World Model forward tick by tick and find
        the earliest future tick W at which taking that step survives the full
        crossing AND the destination tile stays safe for a short settle window.
        Works for ANY deterministic hazard (rolling boulder, ice sweeper, lava
        tide, rotating arms) because it simulates the real dynamics rather than
        encoding each trap's geometry.

        Returns (wait_ticks, action) for the best (soonest, most goal-ward)
        timed crossing, or None if no safe window exists within max_wait.
        """
        ptx, pty = obs['ptx'], obs['pty']
        gx, gy = self.end
        cands = []
        for d in self.DIRS:
            if not self._valid_step(d, ptx, pty):
                continue
            ntx, nty = ptx + d[0], pty + d[1]
            goal_gain = (abs(ptx - gx) + abs(pty - gy)) - (abs(ntx - gx) + abs(nty - gy))
            cands.append((goal_gain, d))
        cands.sort(key=lambda c: -c[0])
        if not cands:
            return None
        # ticks the destination must stay safe
        SETTLE = 4
        # (wait, -goal_gain, action)
        best = None
        base = self._build_internal_world(obs)
        for goal_gain, d in cands:
            for wait in range(0, max_wait + 1):
                w = base.fork()
                safe_wait = True
                for _ in range(wait):
                    w.step_world()
                    if w._body_lethal_here() is not None:
                        safe_wait = False
                        break
                if not safe_wait:
                    # waiting longer only worse for this dir
                    break
                cw = w.fork()
                if cw.apply_action(*d) is not None:
                    # crossing not safe at this wait; try later
                    continue
                ok = True
                for _ in range(SETTLE):
                    cw.step_world()
                    if cw._body_lethal_here() is not None:
                        ok = False
                        break
                if ok:
                    cand = (wait, -goal_gain, d)
                    if best is None or cand < best:
                        best = cand
                    # earliest wait for this dir found
                    break
        if best is None:
            return None
        return best[0], best[2]

    def _sim_screen_actions(self, obs, plies=None):
        """Internal Model → Consequence Evaluator → safe actions (Fig. 1 flow).

        This is the architecture's core loop made literal for action SELECTION,
        not just veto.  For each candidate first move the agent could make, the
        Internal Model forks the World Model, drives the Robot Model with that
        move followed by the agent's own goal-seeking controller policy for a
        few plies, and the Consequence Evaluator (the world's real check_hit
        lethality, run inside the rollout) judges whether the trajectory
        survives.  Only the moves whose simulated futures are safe are returned
        to the Robot Controller, ranked by how much they progress toward goal.

        Returns: (safe_actions, verdicts) where
          safe_actions = [ (dx,dy), ... ] ordered best-goal-progress first,
          verdicts     = { (dx,dy): {'died':bool,'death_kind':str|None,
                                     'death_ply':int,'goal_gain':int} }
        An empty safe_actions list means every simulated option led to harm —
        the caller then falls back to least-bad handling.
        """
        if plies is None:
            plies = self.GOAL_HORIZON
        ptx, pty = obs['ptx'], obs['pty']
        gx, gy = self.end
        # the agent's planned route, so the post-first-step controller policy
        # inside each rollout continues toward the goal the same way it really
        # would (otherwise a screened action's future wouldn't match reality).
        route = None
        try:
            full = self._dijkstra_route(ptx, pty, obs, penalize=frozenset())
            if full:
                route = list(full)
        except Exception:
            route = None
        base_world = self._build_internal_world(obs)
        cur_goal_d = abs(ptx - gx) + abs(pty - gy)
        verdicts = {}
        safe = []
        for (dx, dy) in self.DIRS:
            if not self._valid_step((dx, dy), ptx, pty):
                continue
            w = base_world.fork()
            # ply 0: the candidate move itself.
            kind0 = w.apply_action(dx, dy)
            died = kind0 is not None
            death_kind = kind0
            death_ply = 0 if died else -1
            # remaining plies: let the agent's controller policy carry on toward
            # the goal, exactly as the real rc would after taking this step.
            if not died:
                traj = w.rollout(
                    lambda ww: self._internal_controller_policy(ww, route=route),
                    plies - 1, branch=False, record=False)
                if traj['died']:
                    died = True
                    death_kind = traj['death_kind']
                    death_ply = traj['death_ply'] + 1
            ntx, nty = ptx + dx, pty + dy
            goal_gain = cur_goal_d - (abs(ntx - gx) + abs(nty - gy))
            verdicts[(dx, dy)] = {'died': died, 'death_kind': death_kind,
                                  'death_ply': death_ply, 'goal_gain': goal_gain}
            if not died:
                safe.append((dx, dy))
        # rank safe moves by goal progress (then stable by direction order).
        safe.sort(key=lambda a: -verdicts[a]['goal_gain'])
        # stash for the imagination panel / diagnostics.
        self._last_screen = {'origin': (ptx, pty), 'verdicts': verdicts,
                             'safe': list(safe)}
        return safe, verdicts

    def _internal_controller_policy(self, world, route=None):
        """A copy of the Robot Controller's CORE action logic, callable INSIDE
        the internal world (the diagram's nested Robot Controller box).

        Faithful behaviour: the real controller follows a Dijkstra route toward
        the goal and only deviates to avoid imminent harm.  So when given the
        agent's actual planned `route`, the internal controller FOLLOWS it tile
        by tile — making the imagined trajectory match what the agent will truly
        do and travel the FULL path ahead, instead of a shallow greedy wander
        that oscillates at walls and stays near the start (which read as the
        panel merely 'reflecting now').  It deviates greedily only when the next
        route tile is imminently lethal in the imagined world.
        """
        bx, by = world.body.x, world.body.y
        btx, bty = int(round(bx)), int(round(by))
        gx, gy = self.end

        def step_toward(tx, ty):
            ddx = (tx > btx) - (tx < btx)
            ddy = (ty > bty) - (ty < bty)
            # prefer the axis with the larger remaining gap; one-step moves only.
            if abs(tx - btx) >= abs(ty - bty) and ddx != 0:
                return (ddx, 0)
            if ddy != 0:
                return (0, ddy)
            if ddx != 0:
                return (ddx, 0)
            return None

        # 1) follow the supplied route: find the route tile nearest the body,
        # then target the next tile after it.  (scanning from the route start
        # for the first differing tile made the body match an earlier tile and
        # step backwards, oscillating in place — the shallow-rollout bug.)
        if route:
            best_i = 0
            best_d = 1e9
            for i, (rx, ry) in enumerate(route):
                d = abs(rx - btx) + abs(ry - bty)
                if d < best_d:
                    best_d = d; best_i = i
            # target the next tile beyond the nearest one we've reached.
            nxt = None
            for j in range(best_i + 1, len(route)):
                if route[j] != (btx, bty):
                    nxt = route[j]; break
            if nxt is not None:
                mv = step_toward(*nxt)
                if mv is not None:
                    ntx, nty = btx + mv[0], bty + mv[1]
                    if 0 <= ntx < COLS and 0 <= nty < ROWS and world.grid[nty][ntx] != 1:
                        probe = world.fork()
                        if probe.apply_action(*mv) is None:
                            return mv

        # 2) greedy goal-seeking fallback (no route, route exhausted, or route
        # step blocked/lethal): pick the safe goal-closing step.
        cands = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ntx, nty = btx + dx, bty + dy
            if not (0 <= ntx < COLS and 0 <= nty < ROWS):
                continue
            if world.grid[nty][ntx] == 1:
                continue
            ndist = abs(ntx - gx) + abs(nty - gy)
            cands.append((ndist, dx, dy))
        if not cands:
            return None
        cands.sort()
        for _, dx, dy in cands:
            probe = world.fork()
            if probe.apply_action(dx, dy) is None:
                return (dx, dy)
        return (cands[0][1], cands[0][2])

    def _learned_timing_kinds(self) -> set:
        """Trap KINDS whose activation period the agent has learned reliably
        (a DynamicsModel law that passes the Wilson guarantee bound).  The
        countdown for these is knowledge gained from EXPERIENCE; for other
        kinds (jittered/stochastic activation) the agent has no licensed period
        and the panel marks the countdown as an unverified estimate.
        """
        kinds = set()
        try:
            for rec in self.dynamics.inst.values():
                if self.dynamics._licensed(rec):
                    kinds.add(rec.get('kind'))
        except Exception:
            pass
        return kinds

    def _build_internal_world(self, obs):
        """Assemble the Internal Model's World Model from current perception
        (OTL output): grid + ALL currently-perceived dynamic traps + roaming
        enemies + body.

        Sourcing fix: previously only `_room_dtraps` (the strict current room)
        fed the internal world, so traps in an adjacent room the agent was about
        to enter — exactly the ones it most needs to imagine — were missing from
        the simulation.  We now take the union of everything the agent can SEE
        (obs['dtraps'] / obs['enemies'], the fog-respecting visible set) with the
        current room's objects, de-duplicated by identity, so the imagined world
        contains every hazard the agent is actually perceiving.
        """
        seen_d = list(obs.get('dtraps', []))
        room_d = list(getattr(self, '_room_dtraps', []) or [])
        dtraps = list({id(d): d for d in (seen_d + room_d)}.values())
        seen_e = list(obs.get('enemies', []))
        room_e = list(getattr(self, '_room_enemies', []) or [])
        enemies = list({id(e): e for e in (seen_e + room_e)}.values())
        return InternalWorldModel.from_observation(
            self.grid,
            obs['ptx'], obs['pty'],
            dtraps, enemies,
            statuses=obs.get('statuses', {}),
            t=obs.get('sim_time', 0),
            # start at tile centre: the rollout
            px=obs['ptx'], py=obs['pty'])
        # reasons about future tiles, so a clean tile-aligned start makes route
        # following exact (the agent's live sub-tile offset would otherwise
        # make every imagined position land mid-tile and confuse tile rounding).

    def _internal_model_rollout(self, obs, plies=None, for_display=False,
                                record=None):
        """Run the full nested Internal Model: a copy of the Robot Controller
        drives the Robot Model through the World Model for several plies,
        returning the Consequence-Engine trajectory verdict.

        This is the diagram's recursive simulation loop — used to look BEYOND
        the next tile so multi-step traps (whose danger is not visible one step
        out) are foreseen, matching the chess proof-of-concept's 3-ply lookahead.

        for_display: when True, the recorded frames are stashed on the agent for
        the imagination panel.  The decision-path rollout (short horizon, run
        every tick a commit is considered) passes for_display=False so it never
        clobbers the panel's deeper, slower-refreshing visualisation trace —
        previously both wrote `_imagination`, so the panel flickered between a
        20-ply display rollout and a 5-ply decision rollout every tick.
        """
        if plies is None:
            plies = self.GOAL_HORIZON
        if record is None:
            record = for_display
        world = self._build_internal_world(obs)
        # give the internal robot controller the agent's actual planned route so
        # the imagined trajectory follows the real path toward the goal (and so
        # travels the full distance ahead), matching what the agent will do.
        route = None
        try:
            full = self._dijkstra_route(obs['ptx'], obs['pty'], obs,
                                        penalize=frozenset())
            if full:
                route = list(full)
        except Exception:
            route = None
        policy = (lambda w: self._internal_controller_policy(w, route=route))
        traj = world.rollout(policy, plies, record=record)
        if for_display:
            # 'gen' identifies this display rollout; the panel only resets its
            # animation when gen changes, and the refresh logic bumps it on a
            # slow timer so each rollout plays through smoothly to completion.
            self._imagination = {
                'frames': traj.get('frames', []),
                'died': traj['died'],
                'death_ply': traj['death_ply'],
                'death_frame': traj.get('death_frame', -1),
                'death_kind': traj['death_kind'],
                'origin': (obs['ptx'], obs['pty']),
                'sim_time': obs.get('sim_time', 0),
                'gen': getattr(self, '_imag_gen_counter', 0),
                'learned_kinds': self._learned_timing_kinds(),
            }
        return traj

    def _gate_reflex(self, proposal, obs, *, allow_when_hold_lethal=False,
                     hold_is_lethal=False):
        """Route a reflex's PROPOSED action through the Consequence Evaluator.

        Architecture compliance (paper §III-A, Fig. 1 loop): the Robot
        Controller "is only fed safe actions as determined by the simulation
        engine."  The fast hazard reflexes (sweep / spore / spinner / transit)
        are Internal-Model components — specialised forward simulators that
        PROPOSE an escape action — but they must NOT approve their own output.
        Every proposal is gated here by ConsequenceEvaluator.evaluate, which is
        the single safe/unsafe arbiter for the whole agent.  The evaluator
        always wins: if its forward simulation disagrees with the reflex, the
        proposal is dropped and control falls through to the next planner.

        Because evaluate() runs the memory-first query and EEC expectation
        formation internally, gating here ALSO makes every reflex decision form
        and reuse a stored expectation — so a recurring hazard is answered from
        memory next time instead of being recomputed reflexively (the paper's
        core reuse contribution, now covering the reflex-handled cases too).

        `proposal` is the (action, rule) a reflex would have returned, where
        action is a (dx, dy) step, 'HOLD', or None.  Returns the gated
        (action, rule) to commit, or None to let the caller fall through.

        allow_when_hold_lethal: when True, and the current tile is judged lethal
        to remain on, an evaluator veto of the escape does NOT strand the agent
        — the reflex's timed escape is taken as the least-bad simulated option
        (recorded 'reflex_forced').  This is NOT the evaluator losing: it is the
        defined behaviour when every option is unsafe, where the least-bad must
        still be chosen.  hold_is_lethal lets the proposing reflex assert that
        holding is fatal from its OWN (finer, sub-tile, hazard-specific) forward
        model, used when that model is more accurate than the evaluator's
        tile-granular hold check — e.g. the spore reflex only proposes a move
        once its ring-clearance sim shows the current tile will be swept.
        """
        if proposal is None:
            return None
        action, rule = proposal
        # hold / none are "do not move" proposals: staying put is only approved
        # if the evaluator agrees the current tile is safe to occupy.
        if action in ('HOLD', None):
            hold_danger, hold_rule = self.ce.evaluate(0, 0, obs)
            if not hold_danger:
                self._last_decider = 'reflex_hold'
                return proposal
            return None
        dx, dy = action
        danger, crule = self.ce.evaluate(dx, dy, obs)
        # also verify the proposal with the internal world model, which steps the
        # hazards forward during the crossing.  the geometric evaluator only
        # checks the destination's current danger state, so it passes a step that
        # a slow mover (rolling boulder) rolls into mid-transit — the dominant
        # "predictable" death.  the sim catches that, and the sim's verdict can
        # only add safety (veto a move the evaluator missed), never remove it.
        if not danger and self.use_sim and self._has_dynamic_threats(obs):
            try:
                world = self._build_internal_world(obs)
                if world.fork().apply_action(dx, dy) is not None:
                    # sim foresees a collision en route
                    danger = True
                    self._form_rollout_expectation(
                        obs, {'died': True, 'death_kind': 'mover', 'death_ply': 0,
                              'path': [(obs['ptx'], obs['pty']),
                                       (obs['ptx'] + dx, obs['pty'] + dy)]})
            except Exception:
                pass
        if danger:
            # evaluator vetoes the reflex's escape — drop it, fall through.
            if allow_when_hold_lethal:
                hold_lethal = hold_is_lethal
                if not hold_lethal:
                    hold_danger, _ = self.ce.evaluate(0, 0, obs)
                    hold_lethal = bool(hold_danger)
                if hold_lethal:
                    # both moving and holding are lethal; the reflex's timed
                    # escape is the least-bad simulated option.  recorded as
                    # not-evaluator-certified for transparency in the decision
                    # log / csv.
                    self._last_decider = 'reflex_forced'
                    return action, (crule or rule)
            return None
        # evaluator certifies the reflex's proposal safe → commit it.
        self._last_decider = 'reflex_gated'
        return action, (crule or rule)

    def choose_action(self, obs):
        ptx, pty = obs['ptx'], obs['pty']
        # set true only when full deliberative planning runs
        self._planned = False
        # which layer chose this tick's committed action
        self._last_decider = None
        self._decision_cache = {
            'route_risk': {},
            'wait_safe': {},
            'current_unsafe': {},
            'hold_swept': {},
        }

        # ── baseline mode (feedback #2): innate avoidance heuristic only ────
        if self.mode == "avoidant":
            return self._avoidant_action(obs)

        # ── ultimate anti-freeze watchdog ──────────────────────────────────
        # hard guarantee that the agent can never stall forever.  a rare config
        # (e.g. standing where a spinner's conservative swept-disc footprint
        # marks every adjacent tile lethal, with no enemy to trigger the swarm
        # valve) could make every safety screen reject every move and the normal
        # deadlock valves find no certified-safe escape — so the agent waits
        # every tick indefinitely (the observed multi-hour freeze).  this valve
        # tracks ticks since the last actual tile change and, past a hard cap,
        # forces forward motion: first try a phase-timed spinner dash, then the
        # least-bad goal-ward move, committing it for several tiles so it breaks
        # clear.  standing still until the run ends is strictly worse than
        # accepting bounded, simulated-least-bad risk to escape.
        cur_tile = (ptx, pty)
        # track recent distinct tiles to detect both a hard single-tile stall and
        # an a<->b (or small-cycle) oscillation, which the old single-tile test
        # missed: an agent wedged against a wall ping-ponging between two tiles
        # changes tile every tick, so _freeze_ticks never grew — yet it makes no
        # real progress and a slow hazard (rolling boulder) can roll into it.
        hist = getattr(self, '_freeze_tile_hist', None)
        if hist is None:
            hist = self._freeze_tile_hist = []
        hist.append(cur_tile)
        if len(hist) > 16:
            hist.pop(0)
        # "confined" = the last many ticks only visited <=2 distinct tiles.
        confined = len(hist) >= 12 and len(set(hist[-12:])) <= 2
        if cur_tile != getattr(self, '_freeze_last_tile', None) and not confined:
            self._freeze_last_tile = cur_tile
            self._freeze_ticks = 0
        else:
            self._freeze_ticks = getattr(self, '_freeze_ticks', 0) + 1
        # a hard single-tile stall can wait the full cap, but a confined
        # oscillation needs a much faster break-out: the agent is making no
        # progress and a slow hazard can close in within a couple of tiles, so
        # force an escape after only a few tiles' worth of ping-ponging.
        FREEZE_CAP = (3 * self.STEP_TICKS if confined
                      else 40 * self.STEP_TICKS)
        if self._freeze_ticks >= FREEZE_CAP:
            # 0) if the agent is oscillating but holding still is simulated-safe,
            # just hold: the deterministic mover (patrolling boulder/sweeper)
            # will roll away on its own, and the lethal behaviour was the
            # oscillation itself keeping the agent at the hazard's reach-edge
            # until it got clipped.  stop moving; wait it out.  we verify the
            # hold stays safe for a meaningful window so we don't hold into a
            # mover that is actually approaching this tile.
            if confined:
                hold_world = self._build_internal_world(obs)
                hw = hold_world.fork()
                hold_safe = True
                HOLD_LOOKAHEAD = 24
                for _ in range(HOLD_LOOKAHEAD):
                    hw.step_world()
                    if hw._body_lethal_here() is not None:
                        hold_safe = False
                        break
                if hold_safe:
                    # suppress the reflex-driven oscillation for a few ticks and
                    # hold position; re-evaluate after the mover has advanced.
                    self._clear_motion_plan(clear_last=True)
                    self.route_commit_steps = 0
                    self._hazard_evac_ticks = 0
                    self._window_action = None
                    self._freeze_ticks = max(0, self._freeze_ticks - 6)
                    self._last_decider = 'wait_out_mover'
                    return None, None
            # 1) prefer a phase-timed dash through a swept hazard if one exists.
            # _spinner_escape_dash returns (wait_ticks, dash_route, first).
            try:
                dash = self._spinner_escape_dash(obs)
            except Exception:
                dash = None
            if dash is not None:
                wait_ticks, dash_route, first = dash
                if wait_ticks <= 0 and dash_route and first is not None:
                    self._freeze_ticks = 0
                    self.current_route = list(dash_route)
                    self.route_commit_steps = self._route_commit_ticks(
                        self.current_route, max_tiles=len(self.current_route))
                    self._entry_lock_dir = first
                    self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                 len(self.current_route) * self.STEP_TICKS)
                    self.last_action = first
                    return first, None
            # 2) prefer a sim-timed crossing: wait for the deterministic mover
            # (boulder/sweeper/lava/arm) to clear the corridor, then step.
            # this threads the hazard instead of fleeing or oscillating, and
            # is the architecturally correct use of the internal model — the
            # sim finds the safe time window rather than hand-coded geometry.
            timed = self._sim_timed_crossing(obs)
            if timed is not None:
                wait_t, act = timed
                if wait_t <= 0:
                    self._freeze_ticks = 0
                    self._freeze_tile_hist = []
                    self.last_action = act
                    self.current_route = [(ptx + act[0], pty + act[1])]
                    self.route_commit_steps = self._route_commit_ticks(
                        self.current_route, max_tiles=1)
                    self._entry_lock_dir = act
                    self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                 2 * self.STEP_TICKS)
                    return act, None
                else:
                    # hold in place this tick; the window opens shortly.  keep
                    # the freeze counter from re-firing every tick while waiting.
                    self._freeze_ticks = 0
                    self._window_action = act
                    self._window_wait = wait_t
                    return None, None
            # 3) no safe timed window — fall back to a hazard-aware escape that
            # at least moves away from the nearest mover.
            gx, gy = self.end
            haz = []
            for dt in obs.get('dtraps', []):
                hx = getattr(dt, 'px', getattr(dt, 'ox', None))
                hy = getattr(dt, 'py', getattr(dt, 'oy', None))
                if hx is not None:
                    haz.append((hx, hy))
            for e in obs.get('enemies', []):
                haz.append((e.x, e.y))
            world = self._build_internal_world(obs)
            scored = []
            for d in self.DIRS:
                if not self._valid_step(d, ptx, pty):
                    continue
                ntx, nty = ptx + d[0], pty + d[1]
                probe = world.fork()
                lethal = probe.apply_action(*d) is not None
                hd = min((math.hypot(ntx - hx, nty - hy) for hx, hy in haz),
                         default=99.0)
                nd = abs(ntx - gx) + abs(nty - gy)
                vis = self._visit_counts.get((ntx, nty), 0)
                scored.append(((0 if not lethal else 1, -hd, nd, vis), d))
            scored.sort(key=lambda s: s[0])
            act = scored[0][1] if scored else None
            if act is None:
                act = self._least_bad_goal_step(obs)
            if act is not None and act != 'HOLD':
                self._freeze_ticks = 0
                self._freeze_tile_hist = []
                self.last_action = act
                self.current_route = [(ptx + act[0], pty + act[1])]
                self.route_commit_steps = self._route_commit_ticks(
                    self.current_route, max_tiles=1)
                self._entry_lock_dir = act
                self._entry_lock_ticks = max(self._entry_lock_ticks,
                                             3 * self.STEP_TICKS)
                # penalise the pocket so post-escape routing doesn't curl back.
                for ddx in range(-2, 3):
                    for ddy in range(-2, 3):
                        tkey = (ptx + ddx, pty + ddy)
                        self._visit_counts[tkey] = self._visit_counts.get(tkey, 0) + 4
                return act, None

        # ── per-step commitment re-screen ──────────────────────────────────
        # the sim-driven selection screens candidate moves at decision points,
        # but once a multi-tile route is committed the agent used to follow it
        # without re-checking — so a slow mover (e.g. a rolling boulder at ~0.07
        # tiles/tick) could drift into the committed path between screens and
        # kill the agent, even though the internal model could have foreseen it.
        # (benchmark showed rolling_boulder as the dominant "predictable" death.)
        # before honouring any committed-route shortcut below, re-simulate the
        # immediate next committed step against the current world; if it is now
        # fatal, drop the commitment so the full sim-screened decision re-runs
        # this tick and picks a safe alternative.
        if (self.use_sim and self._has_dynamic_threats(obs)
                and self.current_route and self.route_commit_steps > 0):
            nxt_step = self._first_step(self.current_route, ptx, pty)
            if nxt_step is not None and self._valid_step(nxt_step, ptx, pty):
                world = self._build_internal_world(obs)
                probe = world.fork()
                kind = probe.apply_action(*nxt_step)
                if kind is not None:
                    # committed next step is now lethal in simulation — a hazard
                    # moved in.  abort the commitment and form an expectation so
                    # the agent both avoids it now and remembers it.
                    self._form_rollout_expectation(
                        obs, {'died': True, 'death_kind': kind, 'death_ply': 0,
                              'path': [(ptx, pty),
                                       (ptx + nxt_step[0], pty + nxt_step[1])]})
                    self._clear_motion_plan(clear_last=True)
                    self.route_commit_steps = 0
                    self._hazard_evac_ticks = 0
                    self._window_action = None


        # forward across what it can currently perceive, then re-imagines when it
        # reaches the edge of that window — i.e. when it has advanced about a
        # vision-window's length from where the last rollout started (new terrain
        # has rolled into view) or when its gaze direction flips (the cone now
        # points elsewhere, revealing different surroundings).  this replaces the
        # arbitrary fixed timer: the panel updates exactly when the agent's view
        # of the world has meaningfully changed, which is when a fresh prediction
        # is actually warranted.
        if (self.use_sim and getattr(self, '_visualise_imagination', False)
                and self._has_dynamic_threats(obs)):
            cur_tile = (obs['ptx'], obs['pty'])
            cur_head = obs.get('heading') or _heading_from(self.last_action)
            origin   = getattr(self, '_imag_origin_tile', None)
            last_head = getattr(self, '_imag_head', None)
            # distance travelled (tiles) since the current imagination began.
            if origin is None:
                rolled_over = True
            else:
                moved = abs(cur_tile[0] - origin[0]) + abs(cur_tile[1] - origin[1])
                rolled_over = moved >= VISION_FORWARD
            gaze_changed = False
            if (last_head is not None and cur_head is not None
                    and cur_head != last_head):
                # only a substantial turn (≥90°, i.e. the cone now points at
                # genuinely different terrain) warrants re-imagining; minor
                # heading wobble from corrective steps does not meaningfully
                # change what the agent sees, so it should not reset the panel.
                dot = cur_head[0] * last_head[0] + cur_head[1] * last_head[1]
                gaze_changed = (dot <= 0)
            self._imag_since = getattr(self, '_imag_since', 999) + 1
            if ((rolled_over or gaze_changed or not getattr(self, '_imagination', None))
                    and self._imag_since >= 24):
                # minimum ~0.4 s between refreshes: even when the agent rapidly
                # re-orients near a hazard, the panel won't thrash — it lets the
                # current window-prediction settle before computing the next.
                try:
                    self._imag_gen_counter = getattr(self, '_imag_gen_counter', 0) + 1
                    horizon = max(VISION_FORWARD + 2, self.GOAL_HORIZON)
                    self._internal_model_rollout(
                        obs, plies=horizon, for_display=True)
                    self._imag_origin_tile = cur_tile
                    self._imag_head = cur_head
                    self._imag_since = 0
                except Exception:
                    pass

        # ── mid-transit re-decision (continuous consequence engine) ─────────
        # the body moves every tick but moves commit over step_ticks.  before
        # any hold-shortcut can blindly continue the in-flight move, re-check it
        # against the current world: if a hazard has swept in (or the move is
        # heading into a known static trap), abort/redirect this tick instead of
        # being locked in until the next tile centre.  only engages while the
        # body is actually between tile centres and a held action exists.
        if (self.mode != "avoidant" and self.last_action is not None
                and not self._near_tile_center((ptx, pty), eps=0.20)):
            override = self._transit_guard(obs)
            if override is not None:
                # the transit guard re-simulates the in-flight move; its abort
                # proposal is still gated by the evaluator (sole arbiter).  the
                # hold-lethal valve applies because a hazard sweeping into the
                # body mid-transit can make both continuing and stopping unsafe.
                gated = self._gate_reflex(
                    override, obs, allow_when_hold_lethal=True)
                if gated is not None:
                    return gated
            # _transit_guard may have cleared last_action (chose to hold); if so
            # fall through to full planning rather than replaying a dropped move.

        # room-wide horizontal sweeps (lava_tide / ice_sweeper): retreat behind
        # the advancing wave and hold there, then cross once it recedes.  runs
        # before normal goal logic so the agent never strolls into the band.
        sweep_evade = self._sweep_evasion_step(obs)
        if sweep_evade is not None:
            action, swrule = sweep_evade
            # the sweep band oscillates across the whole room, so no tile is
            # permanently safe; holding can be lethal.  same valve as spore: if
            # the evaluator vetoes the retreat but holding is also fatal, the
            # reflex's behind-the-wave move is the least-bad option.
            gated = self._gate_reflex(
                ('HOLD', swrule) if action == 'HOLD' else (action, swrule), obs,
                allow_when_hold_lethal=True, hold_is_lethal=(action != 'HOLD'))
            if gated is not None:
                gact, grule = gated
                if gact in ('HOLD', None):
                    # deliberately wait on the safe side of the wave.
                    self._clear_motion_plan()
                    self.same_tile_ticks = 0
                    return None, None
                self._clear_motion_plan(clear_last=True)
                self._window_action = None
                self._window_wait = 0
                self.same_tile_ticks = 0
                self.last_action = gact
                self.current_route = [(ptx + gact[0], pty + gact[1])]
                self.route_commit_steps = self._route_commit_ticks(
                    self.current_route, max_tiles=1)
                return gact, grule
            # evaluator vetoed the sweep reflex → fall through to planning.

        spore_escape = self._spore_escape_step(obs)
        if spore_escape is not None:
            action, srule = spore_escape
            # inside/near an expanding ring there is no durably safe tile, so
            # holding can be lethal: if the evaluator vetoes every escape but
            # also judges holding fatal, the reflex's flee-the-origin move is the
            # least-bad simulated option and proceeds (recorded 'reflex_forced').
            gated = self._gate_reflex(
                (action, srule), obs, allow_when_hold_lethal=True,
                hold_is_lethal=True)
            if gated is not None:
                gact, grule = gated
                self._clear_motion_plan(clear_last=True)
                self._window_action = None
                self._window_wait = 0
                self.same_tile_ticks = 0
                self.last_action = gact
                self.current_route = [(ptx + gact[0], pty + gact[1])]
                self.route_commit_steps = self._route_commit_ticks(
                    self.current_route, max_tiles=1)
                return gact, grule
            # evaluator vetoed the spore reflex → fall through to planning.

        # hazard evacuation hysteresis: once a swept-body escape starts, finish
        # crossing the selected adjacent tile instead of re-planning on every
        # rounded-tile flicker and undoing the move.
        if getattr(self, '_hazard_evac_ticks', 0) > 0:
            while self.current_route and self.current_route[0] == (ptx, pty):
                self.current_route.pop(0)
            if self.current_route:
                action = self._first_step(self.current_route, ptx, pty)
                if action is not None and self._valid_step(action, ptx, pty):
                    self._hazard_evac_ticks -= 1
                    self.same_tile_ticks = 0
                    self.last_action = action
                    return action, self._last_rule
            self._hazard_evac_ticks = 0

        # if a predictable mover will sweep the tile we are standing on, leave
        # before normal goal/window logic can decide that waiting is acceptable.
        if self._current_tile_will_be_unsafe(obs):
            # cornered-by-rotating-arm case: when a fire_bar/ice_beam/pendulum
            # makes the current tile unsafe and no adjacent tile gives lasting
            # clearance from the arm's reach (the agent is boxed in a wall
            # pocket on the arm's edge), single-tile evacuation just ping-pongs
            # between two marginal tiles until the arm rotates in and kills it
            # (the spinning-flame death).  holding is unsafe, so the wait-gated
            # crossing/dash planners are all skipped — leaving only the
            # oscillating least-bad move.  instead, time the arm: roll it
            # forward and dash out the instant the chosen escape corridor is
            # clear for the whole crossing.  this runs even though holding is
            # unsafe, because waiting is exactly the lethal option here.
            spin_dash = self._spinner_escape_dash(obs)
            if spin_dash is not None:
                wait_ticks, dash_route, first = spin_dash
                self._clear_motion_plan(clear_last=True)
                self._window_action = None
                self._window_wait = 0
                self._window_fail = 0
                self._window_fail_dir = None
                if wait_ticks <= 0 and dash_route:
                    # gate the dash launch through the evaluator.  this branch
                    # only runs when the current tile is already unsafe, so the
                    # hold-lethal valve applies: if the evaluator vetoes the dash
                    # but also confirms holding is lethal, the timed dash is the
                    # least-bad simulated option and proceeds (recorded as
                    # 'reflex_forced'); otherwise the evaluator's veto stands.
                    gated = self._gate_reflex(
                        (first, None), obs, allow_when_hold_lethal=True)
                    if gated is not None:
                        gfirst, _grule = gated
                        self.current_route = list(dash_route)
                        self.route_commit_steps = self._route_commit_ticks(
                            self.current_route, max_tiles=len(self.current_route))
                        self._hazard_evac_ticks = self.route_commit_steps
                        self._entry_lock_dir = gfirst
                        self._entry_lock_ticks = max(
                            self._entry_lock_ticks,
                            len(self.current_route) * self.STEP_TICKS)
                        self.same_tile_ticks = 0
                        self.last_action = gfirst
                        return gfirst, None
                # window opens in a few ticks: a held body here is doomed, so we
                # cannot simply wait. take the single best clearance-improving
                # step now (the dash's first tile is verified clear at launch);
                # if even that is momentarily unsafe, fall through.
                if dash_route and first is not None and self._valid_step(first, ptx, pty):
                    dgr, _ = self._one_step_danger(first, obs)
                    if not dgr:
                        self.current_route = [dash_route[0]]
                        self.route_commit_steps = self._route_commit_ticks(
                            self.current_route, max_tiles=1)
                        self._hazard_evac_ticks = self.route_commit_steps
                        self.same_tile_ticks = 0
                        self.last_action = first
                        return first, None

            evac = self._evacuate_current_tile(obs)
            if evac is not None:
                action, erule = evac
                if action is not None and self._valid_step(action, ptx, pty):
                    danger, _ = self._one_step_danger(action, obs)
                    if not danger or not self._wait_is_safe(obs):
                        self._clear_motion_plan(clear_last=True)
                        self._window_action = None
                        self._window_wait = 0
                        self._window_fail = 0
                        self._window_fail_dir = None
                        self.same_tile_ticks = 0
                        self.last_action = action
                        self.current_route = [(ptx + action[0], pty + action[1])]
                        self.route_commit_steps = self._route_commit_ticks(
                            self.current_route, max_tiles=1)
                        self._hazard_evac_ticks = self.route_commit_steps
                        return action, erule

        # ══ net-progress watchdog (authoritative livelock breaker) ════════════
        # root-cause fix for the "never finishes a maze" stall.  the older
        # breakers below each track a local signal — a fixed-radius region
        # anchor, a tile-history a<->b pattern, a stuck-tick counter — and a
        # slow drifting orbit defeats all of them at once: every few ticks the
        # agent shuffles to an adjacent tile, which resets the region anchor,
        # keeps stuck_ticks near zero, and re-forms the bounce on a fresh tile
        # pair.  net distance-to-exit, however, does not improve.  this watchdog
        # is gated on exactly that one un-fakeable signal (maintained every tick
        # in step()).
        #
        # the dominant real cause of the stall (confirmed by tracing) is a
        # wandering enemy camped ~1-2 tiles along the only goal-ward direction:
        # the forward model correctly predicts that stepping toward the exit
        # walks into that enemy (a one-shot kill at hp=1), so every goal-ward
        # step is vetoed, and the agent diverts to a non-lethal but progress-
        # less side tile, re-forming the bounce.  the right response is not to
        # keep shuffling and not to ram the enemy — it is to hold at the launch
        # tile until the wanderer moves off the path (it always does; roaming
        # enemies re-pick waypoints), then proceed.  only when holding is itself
        # unsafe (a genuine corner) or the agent has waited far too long do we
        # accept bounded risk and force a move.
        if (self._stagnation_ticks >= self.STAGNATION_CAP
                and getattr(self, '_force_push_ticks', 0) == 0):
            ex0, ey0 = self.end
            # build an escape route that actively routes around the thing that
            # is blocking progress.  the dominant blocker is a wandering enemy
            # camped on the direct line to the exit; penalising the tiles it
            # currently occupies (and their neighbours) pushes dijkstra onto a
            # parallel corridor — exactly the detour the per-tick planner kept
            # failing to commit to because its first step flipped every tick.
            enemy_pen = set()
            for e in getattr(self, '_room_enemies', []):
                etx = int(math.floor(e.x)); ety = int(math.floor(e.y))
                # penalise a 5x5 block around each nearby enemy and its short
                # forward projection, so the escape route gives wanderers a wide
                # berth instead of skimming one tile away (which the body's
                # transit then collides with as the enemy drifts in).
                for ddx in range(-2, 3):
                    for ddy in range(-2, 3):
                        enemy_pen.add((etx + ddx, ety + ddy))
                # project the enemy a few tiles along its current heading.
                wp = getattr(e, 'waypoint', None)
                if wp is not None:
                    vx, vy = wp[0] - e.x, wp[1] - e.y
                    nrm = math.hypot(vx, vy)
                    if nrm > 1e-6:
                        for k in (1, 2, 3):
                            px_ = int(math.floor(e.x + vx / nrm * k))
                            py_ = int(math.floor(e.y + vy / nrm * k))
                            for ddx in (-1, 0, 1):
                                for ddy in (-1, 0, 1):
                                    enemy_pen.add((px_ + ddx, py_ + ddy))
            esc = (self._dijkstra_route(ptx, pty, obs, penalize=enemy_pen)
                   or self._dijkstra_route(ptx, pty, obs, penalize=frozenset()))

            # follow the route's first step.  hold (do not divert) when that
            # step is only transiently blocked and waiting here is safe; force
            # it through only when cornered.
            esc_first = esc_rule = None
            blocked_transient = False
            if esc:
                gd = (esc[0][0] - ptx, esc[0][1] - pty)
                if gd in self.DIRS and self._valid_step(gd, ptx, pty):
                    gtx, gty = esc[0]
                    lethal, esc_rule = self._one_step_danger(gd, obs)
                    if not lethal:
                        esc_first = gd
                    elif not self._tile_has_known_static_trap((gtx, gty), obs):
                        blocked_transient = True

            # transient block on the route's first tile: this is the wandering-
            # enemy-in-the-corridor case.  pure avoidance can't solve it (the
            # corridor is the only way through), so time a dash: find the
            # earliest future tick the next few route tiles are all enemy-clear.
            if (esc_first is None and blocked_transient
                    and self._wait_is_safe(obs)):
                dash = self._corridor_dash_plan(obs, esc)
                if dash is not None:
                    wait_ticks, dash_route = dash
                    if wait_ticks == 0 and dash_route:
                        # window is open now — commit the dash as a watchdog push
                        # so the follower threads the whole prefix uninterrupted.
                        self._stagnation_breaks = 0
                        self._force_push_route = list(dash_route)
                        self._force_push_ticks = (len(dash_route) + 3) * self.STEP_TICKS
                        self._force_push_cooldown = 0
                        self._watchdog_push = True
                        fd = (dash_route[0][0] - ptx, dash_route[0][1] - pty)
                        self._entry_lock_dir = fd
                        self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                     len(dash_route) * self.STEP_TICKS)
                        self._osc_hold = 0
                        self._confine_holds = 0
                        self._crossing_route = []
                        self._crossing_wait = 0
                        self._tile_history.clear()
                        self._dir_history.clear()
                        self._clear_motion_plan()
                        self.current_route = list(dash_route)
                        self.route_commit_steps = self._route_commit_ticks(
                            self.current_route, max_tiles=len(self.current_route))
                        self._stagnation_ticks = self.STAGNATION_CAP // 2
                        self.same_tile_ticks = 0
                        self.last_action = fd
                        return fd, None
                    # window opens soon — hold here until it does, keeping the
                    # goal heading locked so the launch is toward the exit.
                    self._osc_hold = 0
                    self._crossing_route = []
                    self._crossing_wait = 0
                    self._tile_history.clear()
                    self._dir_history.clear()
                    self._clear_motion_plan()
                    gd = (esc[0][0] - ptx, esc[0][1] - pty)
                    self._entry_lock_dir = gd
                    self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                 2 * self.STEP_TICKS)
                    # re-check every couple of ticks (don't re-arm the full cap).
                    self._stagnation_ticks = self.STAGNATION_CAP - 4
                    self.same_tile_ticks = 0
                    return None, None
                # no dash window within the horizon and we have not yet waited
                # through several full attempts → hold briefly anyway (the
                # wanderer may still drift off); after a few, fall through to the
                # bounded-risk escape below.
                if self._stagnation_breaks < 3:
                    self._stagnation_breaks += 1
                    self._clear_motion_plan()
                    gd = (esc[0][0] - ptx, esc[0][1] - pty)
                    self._entry_lock_dir = gd
                    self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                 2 * self.STEP_TICKS)
                    self._stagnation_ticks = self.STAGNATION_CAP - 6
                    self.same_tile_ticks = 0
                    return None, None

            # no safe route-first step (cornered or persistent camper): accept
            # bounded risk.  take the route's first step if it is not a certain
            # static-trap death; otherwise the non-lethal neighbour that makes
            # the most goal progress (not merely the least-visited one, which
            # could be straight backwards).
            if esc_first is None:
                gd = (esc[0][0] - ptx, esc[0][1] - pty) if esc else None
                if (gd in self.DIRS and self._valid_step(gd, ptx, pty)
                        and not self._tile_has_known_static_trap(
                            (ptx + gd[0], pty + gd[1]), obs)):
                    esc_first, esc_rule = gd, None
                else:
                    best = None
                    for d in self.DIRS:
                        if not self._valid_step(d, ptx, pty):
                            continue
                        ntx, nty = ptx + d[0], pty + d[1]
                        if self._tile_has_known_static_trap((ntx, nty), obs):
                            continue
                        lethal, r = self._one_step_danger(d, obs)
                        if lethal:
                            continue
                        nd = abs(ntx - ex0) + abs(nty - ey0)
                        vis = self._visit_counts.get((ntx, nty), 0)
                        # progress first, novelty as tiebreak
                        key = (nd, vis)
                        if best is None or key < best[0]:
                            best = (key, d, r)
                    if best is not None:
                        esc_first, esc_rule = best[1], best[2]
                        esc = [(ptx + esc_first[0], pty + esc_first[1])]

            if esc_first is not None:
                # commit and follow the full route (not a single direction), so
                # the agent threads the detour around the camper instead of
                # bouncing.  escalate length/penalty with repeated breaks.
                self._stagnation_breaks += 1
                push_len = self.STAGNATION_PUSH_TILES + 4 * (self._stagnation_breaks - 1)
                route_src = esc if esc else [(ptx + esc_first[0], pty + esc_first[1])]
                self._force_push_route = list(route_src[:push_len])
                self._force_push_ticks = (len(self._force_push_route) + 6) * self.STEP_TICKS
                self._force_push_cooldown = 0
                self._watchdog_push = True
                self._entry_lock_dir = esc_first
                self._entry_lock_ticks = max(self._entry_lock_ticks,
                                             3 * self.STEP_TICKS)
                # penalise the pocket the agent is escaping so post-escape
                # routing does not immediately curl back into it.
                rad = self.REGION_RADIUS + self._stagnation_breaks
                pen = 3 + self._stagnation_breaks
                for ddx in range(-rad, rad + 1):
                    for ddy in range(-rad, rad + 1):
                        t = (ptx + ddx, pty + ddy)
                        self._visit_counts[t] = self._visit_counts.get(t, 0) + pen
                self._osc_hold = 0
                self._confine_holds = 0
                self._crossing_route = []
                self._crossing_wait = 0
                self._crossing_age = 0
                self._tile_history.clear()
                self._dir_history.clear()
                self._clear_motion_plan()
                self.current_route = list(self._force_push_route)
                self.route_commit_steps = self._route_commit_ticks(
                    self.current_route, max_tiles=len(self.current_route))
                self._stagnation_ticks = self.STAGNATION_CAP // 2
                self.same_tile_ticks = 0
                self.last_action = esc_first
                return esc_first, esc_rule


        # ── forced-progress deadlock valve ────────────────────────────────────
        # the agent can be trapped in a small region by a swarm of roaming
        # enemies: every goal-ward step is momentarily threatened, so it commits
        # a 1-tile route, the enemy-interception veto aborts it, it re-commits,
        # aborts... forever, technically "moving" each tick so no other guard
        # fires.  when the absolute region-confinement timer (gated only on
        # position) exceeds the cap, we stop trying to find a perfectly-safe
        # path that does not exist and commit a full detour route toward the
        # exit, following it directly here — bypassing the per-tick enemy-
        # interception veto that was aborting every attempt — and sustaining it
        # for several tiles.  only a genuinely lethal (this-tick) hazard
        # interrupts.  accepting bounded risk to break a permanent deadlock
        # strictly dominates standing in the swarm until the run ends.  crucially
        # the route is a real dijkstra path, so it goes around the swarm when the
        # direct line is blocked, rather than ramming the goal-ward wall.
        if self._force_push_cooldown > 0:
            self._force_push_cooldown -= 1
        if self._force_push_ticks > 0:
            self._force_push_ticks -= 1
            # force-push bypasses the normal oscillation breaker below, so it
            # needs its own no-progress escape.  two failure modes showed up in
            # testing: holding forever because the next forced tile remains
            # lethal, and bouncing a<->b while technically changing tiles so
            # _stuck_ticks never rises.  in both cases, abort the forced route,
            # penalize the local loop, and let normal planning choose a detour.
            dh = [d for d in self._dir_history[-8:] if d is not None]
            dir_flip = (
                len(dh) >= 6
                and all(dh[i] == (-dh[i - 1][0], -dh[i - 1][1])
                        for i in range(1, len(dh)))
            )
            th = list(self._tile_history[-10:])
            tile_bounce = len(th) >= 6 and len(set(th)) <= 2
            force_stalled = getattr(self, '_stuck_ticks', 0) >= 6 * self.STEP_TICKS
            # a watchdog push manages its own re-firing, so give it a longer
            # leash than an ordinary force-push before the generic abort fires —
            # but it must still abort eventually, otherwise a push that keeps
            # bouncing a<->b against a lethal tile will ram the agent into a
            # seeking projectile (observed: mummy_wrap deaths).  ordinary pushes
            # abort immediately on a confirmed flip; watchdog pushes abort only
            # after a sustained stall.
            wd = getattr(self, '_watchdog_push', False)
            wd_stalled = getattr(self, '_stuck_ticks', 0) >= 10 * self.STEP_TICKS
            should_abort = (
                (not wd and (force_stalled or (dir_flip and tile_bounce)))
                or (wd and (wd_stalled or (dir_flip and tile_bounce)))
            )
            if should_abort:
                for t in list(self._force_push_route) + th + [(ptx, pty)]:
                    self._visit_counts[t] = self._visit_counts.get(t, 0) + 4
                self._force_push_ticks = 0
                self._force_push_route = []
                self._force_push_cooldown = self.REGION_CAP
                self._confine_holds = max(self._confine_holds, 2)
                self._watchdog_push = False

            # advance the push route past tiles already entered
            while self._force_push_route and self._force_push_route[0] == (ptx, pty):
                self._force_push_route.pop(0)
            if self._force_push_route:
                nx, ny = self._force_push_route[0]
                fd = (nx - ptx, ny - pty)
                if fd in self.DIRS and self._valid_step(fd, ptx, pty):
                    lethal, frule = self._one_step_danger(fd, obs)
                    if getattr(self, '_watchdog_push', False):
                        # watchdog escape: only veto on an imminent contact
                        # (this agent-step), not on a wanderer that might drift
                        # near over the next 30 ticks.  the long-horizon test
                        # vetoes every tile of a parallel corridor and is what
                        # kept the agent pinned one tile short of the exit path.
                        enemy_intercept = self._enemy_threatens_at((nx, ny),
                                                                   self.STEP_TICKS)
                    else:
                        enemy_intercept = (
                            self._enemy_threatens_at((nx, ny), self.STEP_TICKS)
                            or self._enemy_clearance_at_point(
                                nx, ny, obs,
                                ticks=self.EVAC_HORIZON * self.STEP_TICKS) < 0.10
                        )
                    if not lethal and not enemy_intercept:
                        self.same_tile_ticks = 0
                        self.last_action = fd
                        return fd, frule
                    # next route tile is blocked this tick.  hold here and wait
                    # for the window rather than sidestepping back the way we
                    # came — drifting back was what reset the push to its start.
                    if self._wait_is_safe(obs):
                        return None, None
                    # cannot safely wait and the next tile is genuinely lethal
                    # (a predicted dtrap/enemy collision, e.g. an incoming
                    # seeking mummy_wrap projectile): do not force a least-bad
                    # step that may ram the hazard.  abort the push and defer to
                    # the safe deliberative planner / evac logic below, which
                    # owns the accept-bounded-risk decision with full hazard
                    # awareness.
                    if lethal:
                        self._force_push_ticks = 0
                        self._force_push_route = []
                        self._watchdog_push = False
                        self._force_push_cooldown = self.STEP_TICKS
                        # fall through to normal planning (do not return here)
                    else:
                        # blocked only by an enemy-interception forecast (tile not
                        # lethal this tick): a least-bad sidestep is acceptable.
                        alt = self._least_bad_goal_step(obs)
                        if alt is not None and self._valid_step(alt, ptx, pty):
                            self.same_tile_ticks = 0
                            self.last_action = alt
                            return alt, None
                        return None, None
            # route exhausted
            self._force_push_ticks = 0
            self._force_push_route = []
            self._watchdog_push = False

        if (self._region_ticks >= self.REGION_CAP
                and self._force_push_ticks == 0
                and self._force_push_cooldown == 0):
            # engage: build a detour route to the exit that routes around the
            # swarm (enemy tiles carry +2 in dijkstra; heavily-visited bounce
            # tiles carry the accumulated visit penalty), and commit to it.
            push_route = self._dijkstra_route(ptx, pty, obs, penalize=frozenset())
            if push_route:
                # commit a generous prefix and a generous time budget: enough to
                # wait out a hazard cycle at a corridor pinch and traverse it.
                self._force_push_route = list(push_route[:self.FORCE_PUSH_TILES])
                self._force_push_ticks = (self.FORCE_PUSH_TILES + 6) * self.STEP_TICKS
                self._region_ticks = 0
                self._region_anchor = (ptx, pty)
                # heavily penalise the trapped region so the planner stops
                # routing back into it after the push.
                ax, ay = (ptx, pty)
                for ddx in range(-self.REGION_RADIUS, self.REGION_RADIUS + 1):
                    for ddy in range(-self.REGION_RADIUS, self.REGION_RADIUS + 1):
                        t = (ax + ddx, ay + ddy)
                        self._visit_counts[t] = self._visit_counts.get(t, 0) + 2
                self._clear_motion_plan()
                self._crossing_route = []
                self._crossing_wait = 0
                self._osc_hold = 0
                # follow the first step immediately if safe
                nx, ny = self._force_push_route[0]
                fd = (nx - ptx, ny - pty)
                if fd in self.DIRS and self._valid_step(fd, ptx, pty):
                    lethal, _ = self._one_step_danger(fd, obs)
                    enemy_intercept = (
                        self._enemy_threatens_at((nx, ny), self.STEP_TICKS)
                        or self._enemy_clearance_at_point(
                            nx, ny, obs,
                            ticks=self.EVAC_HORIZON * self.STEP_TICKS) < 0.10
                    )
                    if not lethal and not enemy_intercept:
                        self.same_tile_ticks = 0
                        self.last_action = fd
                        return fd, None
                    # first tile blocked — hold and let the push budget wait it out
                    if self._wait_is_safe(obs):
                        return None, None

        # safe-stall breaker: after force-push aborts or stale route waiting,
        # the controller can sit in a locally safe tile even though adjacent
        # safe tiles exist.  once the body has failed to change tile for several
        # decisions, take the least-visited safe neighbor to get fresh geometry
        # and avoid replaying the same blocked plan.
        if (getattr(self, '_stuck_ticks', 0) >= 3 * self.STEP_TICKS
                and self._force_push_ticks == 0
                and self._wait_is_safe(obs)
                and not self._current_tile_will_be_unsafe(obs)):
            cands = []
            ex0, ey0 = self.end
            for d in self.DIRS:
                if not self._valid_step(d, ptx, pty):
                    continue
                tx, ty = ptx + d[0], pty + d[1]
                if self._tile_has_known_static_trap((tx, ty), obs):
                    continue
                lethal, rule = self._one_step_danger(d, obs)
                if lethal:
                    continue
                visits = self._visit_counts.get((tx, ty), 0)
                goal_dist = abs(tx - ex0) + abs(ty - ey0)
                cands.append((visits, goal_dist, d, rule))
            if cands:
                cands.sort(key=lambda c: (c[0], c[1]))
                _, _, d, rule = cands[0]
                self._clear_motion_plan(clear_last=True)
                self._window_action = None
                self._window_wait = 0
                self._window_fail = 0
                self._window_fail_dir = None
                self.same_tile_ticks = 0
                self.last_action = d
                self._force_push_cooldown = max(self._force_push_cooldown,
                                                self.STEP_TICKS)
                return d, rule

        # ── oscillation breaker (inert unless a<->b bouncing is confirmed) ─────
        # at a hazard doorway the planner can flip between two adjacent tiles
        # (a->b->a->b...) for a long time without making progress, because the
        # cyclic hazard makes each side momentarily cheaper in turn.  this guard
        # does nothing in normal navigation; it only triggers once the recent
        # distinct-tile history is a clear two-tile bounce.  when triggered, and
        # only while holding position is safe, it holds at the current tile for a
        # short committed window so the hazard can clear and the agent can then
        # advance, instead of continuing to bounce.  if holding is unsafe it
        # stays inert and lets the normal logic run.
        if self._osc_hold > 0:
            self._osc_hold -= 1
            if self._wait_is_safe(obs):
                return None, None
            self._osc_hold = 0
        else:
            # (i) stationary heading-flip: the agent keeps deciding opposite
            # directions on consecutive ticks (l,r,l,r...) without ever moving a
            # tile, so _tile_history below never updates and never catches it.
            # if the recent chosen-direction history is dominated by two
            # opposite moves and the agent has not changed tile, the planner is
            # bouncing in place at a hazard-flanked doorway.  commit to a short
            # safe hold so the cycling hazard can clear and the (now hysteretic)
            # planner can pick one side and keep it.
            dh = [d for d in self._dir_history[-6:] if d is not None]
            th = list(self._tile_history[-6:])
            confined_flip = (len(th) >= 4 and len(set(th)) <= 2)
            stalled_flip = (getattr(self, '_stuck_ticks', 0) >= self.STEP_TICKS
                            or confined_flip
                            or self._force_push_ticks > 0)
            if len(dh) >= 4 and self._wait_is_safe(obs) and stalled_flip:
                from collections import Counter as _Cd
                dc = _Cd(dh)
                (d1, c1), *_rest = dc.most_common(1)
                opp = (-d1[0], -d1[1])
                flips = c1 + dc.get(opp, 0)
                if dc.get(opp, 0) >= 1 and flips >= 4 and flips >= len(dh) - 1:
                    # confirmed in-place heading flip.  hold, then let the
                    # hysteretic planner commit to one direction next.
                    self._osc_hold = 4 * self.STEP_TICKS
                    self._dir_history.clear()
                    self._tile_history.clear()
                    self._force_push_ticks = 0
                    self._force_push_route = []
                    self._force_push_cooldown = 3 * self.STEP_TICKS
                    # anchor the committed heading to the side closer to the
                    # exit so the post-hold launch is toward the goal.
                    ex0, ey0 = self.end
                    cand = [d for d in (d1, opp) if d in self.DIRS
                            and self._valid_step(d, ptx, pty)]
                    if cand:
                        self._entry_lock_dir = min(
                            cand,
                            key=lambda d: abs(ptx + d[0] - ex0) + abs(pty + d[1] - ey0))
                        self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                     5 * self.STEP_TICKS)
                    return None, None

            # (ii) tile-confinement detector (generalised a<->b bounce and
            # small-cluster orbit).  the agent is oscillating if, over a recent
            # window of moves, it keeps revisiting a small set of tiles and
            # makes no net progress toward the exit — whether that is a strict
            # 2-tile flip or a slow loop around a hazard-flanked doorway (4-6
            # tiles).  hysteresis alone turns a bounce into an orbit; this
            # catches the orbit too and converts it into a committed wait at the
            # best launch tile, which is the correct behaviour at a doorway
            # gated by a cycling hazard: hold, let the hazard clear, then cross.
            h = self._tile_history
            if len(h) >= 8 and self._wait_is_safe(obs):
                recent = h[-12:]
                uniq = set(recent)
                ex0, ey0 = self.end
                # net progress = did the agent's minimum distance-to-exit
                # actually improve across the window?  if the closest-to-exit
                # tile it reached early in the window is no nearer than where it
                # is now, it is confined, not advancing.  note: this must not be
                # gated on _stuck_ticks — an a<->b controller bounce moves every
                # tick (so stuck_ticks stays ~0) yet makes zero net progress;
                # gating on stuck_ticks would make this blind to exactly the
                # oscillation it exists to catch.
                d_now   = abs(ptx - ex0) + abs(pty - ey0)
                d_best  = min(abs(tx - ex0) + abs(ty - ey0) for tx, ty in recent)
                d_start = abs(recent[0][0] - ex0) + abs(recent[0][1] - ey0)
                # confined if the agent keeps revisiting a small tile set and
                # its closest approach to the exit over the window is no better
                # than where it started — i.e. the bounce is not secretly
                # making progress.
                confined = (len(uniq) <= 6
                            and len(recent) >= 8
                            and (d_best >= d_start - 1)  # no real net gain
                            and (ptx, pty) in uniq)
                if confined:
                    self._confine_holds += 1
                    ex0, ey0 = self.end
                    # best step toward the exit from here (the launch move).
                    best_dir = None; best_d = d_now
                    for d in self.DIRS:
                        if not self._valid_step(d, ptx, pty):
                            continue
                        nd = abs(ptx+d[0]-ex0) + abs(pty+d[1]-ey0)
                        if nd < best_d:
                            best_d, best_dir = nd, d
                    # ── livelock escape ──────────────────────────────────────
                    # if we have already held several times for this same
                    # confinement and still cannot make net progress, the
                    # blockage is not a briefly-cycling hazard — it is a
                    # persistent gate (a slow camped enemy, a static wall of
                    # hazard).  continuing to hold = frozen until the run ends.
                    # force one committed launch step toward the exit (the
                    # planner already judged it best), accepting bounded risk;
                    # moving strictly beats freezing.  if no exit-ward step
                    # exists, fall through to normal planning (detours/panic).
                    if self._confine_holds >= 2:
                        # the block is persistent (a cycling hazard would have
                        # opened in two holds).  escape it.  priority order:
                        # 1. a safe step toward the exit (best case).
                        # 2. a safe step that does not increase distance much
                        # and is least-visited — a detour around the block.
                        # 3. any safe step at all (even backtracking) — get
                        # off this tile so the planner re-derives from new
                        # ground.
                        # 4. nothing safe → fall through to planner/panic,
                        # which owns the accept-bounded-risk decision.
                        # this is the missing behaviour: at a persistently
                        # blocked doorway the agent must be willing to go around,
                        # not keep waiting for a gap that never comes.
                        cands = []
                        for d in self.DIRS:
                            if not self._valid_step(d, ptx, pty):
                                continue
                            tx2, ty2 = ptx + d[0], pty + d[1]
                            lethal, _ = self._one_step_danger(d, obs)
                            if lethal or self._enemy_threatens_at((tx2, ty2),
                                                                  self.STEP_TICKS):
                                continue
                            nd = abs(tx2 - ex0) + abs(ty2 - ey0)
                            visits = self._visit_counts.get((tx2, ty2), 0)
                            cands.append((nd, visits, d))
                        if cands:
                            # persistent confinement: the closest-to-exit tile
                            # is what keeps pulling the agent back into the
                            # bounce.  prioritise the least-visited safe tile
                            # (genuinely new ground) so the agent breaks out of
                            # the trapped region; tie-break by closeness to exit.
                            # escalating holds widen the search: after more
                            # failed escapes, weight novelty even harder.
                            cands.sort(key=lambda c: (c[1], c[0]))
                            esc_dir = cands[0][2]
                            self._confine_holds = 0
                            self._osc_hold = 0
                            self._crossing_route = []
                            self._crossing_wait = 0
                            self._crossing_age = 0
                            # lock the escape heading for a full tile-crossing
                            # plus margin so the planner cannot reverse it back
                            # toward the block on the very next tick — the
                            # reversal is what re-formed the a<->b bounce.
                            self._entry_lock_dir = esc_dir
                            self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                         2 * self.STEP_TICKS)
                            # penalise the tiles of the trapped region so the
                            # planner stops routing back through them for a
                            # while (dijkstra reads _visit_counts via the escape,
                            # and the bounce tiles now carry heavy visit counts).
                            for bt in uniq:
                                self._visit_counts[bt] = self._visit_counts.get(bt, 0) + 4
                            self.current_route = [(ptx + esc_dir[0],
                                                   pty + esc_dir[1])]
                            self.route_commit_steps = self._route_commit_ticks(
                                self.current_route, max_tiles=1)
                            self._tile_history.clear()
                            self.same_tile_ticks = 0
                            self.last_action = esc_dir
                            return esc_dir, None
                        # no safe escape step — clear the confinement state and
                        # let the full planner / panic logic handle it (it may
                        # accept bounded risk via the deadlock guard).
                        self._confine_holds = 0
                        self._tile_history.clear()
                        # fall through (do not return) to deliberative planning.
                    else:
                        # otherwise: hold at the best launch tile and lock heading.
                        target = min(uniq, key=lambda t: abs(t[0]-ex0)+abs(t[1]-ey0))
                        if best_dir is not None:
                            self._entry_lock_dir = best_dir
                            self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                         8 * self.STEP_TICKS)
                        if (ptx, pty) == target:
                            self._osc_hold = 6 * self.STEP_TICKS
                            self._tile_history.clear()
                            return None, None
                        tdir = (target[0]-ptx, target[1]-pty)
                        if tdir in self.DIRS and self._valid_step(tdir, ptx, pty):
                            dgr, drule = self._one_step_danger(tdir, obs)
                            if not dgr:
                                self._tile_history.clear()
                                self.last_action = tdir
                                return tdir, drule
                        self._osc_hold = 6 * self.STEP_TICKS
                        self._tile_history.clear()
                        return None, None

        # staged spinner crossing: if the next crossing step is momentarily
        # lethal but this staging tile is safe, hold the route instead of
        # discarding it and retreating. once a step starts, sustain it until
        # the tile boundary so per-tick timing drift cannot strand the agent.
        while self._crossing_route and self._crossing_route[0] == (ptx, pty):
            self._crossing_route.pop(0)
        if self._entry_lock_ticks > 0:
            self._entry_lock_ticks -= 1
        elif not self._crossing_route and self._crossing_wait <= 0:
            self._entry_lock_dir = None
        if self._crossing_route:
            # ── livelock cap ────────────────────────────────────────────────
            # a staged crossing whose first step stays lethal re-arms a 1-tick
            # wait every tick and holds forever (none of the wait-streak /
            # deadlock guards engage, because this block returns before them).
            # age the crossing each tick it is armed without the agent crossing
            # a tile boundary; once it exceeds the cap the predicted window is
            # not materialising (a persistently-camped hazard, or a forecast the
            # jittering trap timers keep invalidating), so abandon the crossing
            # entirely and fall through to full planning — which can detour or,
            # via the deadlock guard, force a least-bad move.  the age resets to
            # 0 whenever the agent actually advances along the crossing (handled
            # in step(), on a real tile change).
            self._crossing_age += 1
            if self._crossing_age > self.CROSSING_AGE_CAP:
                self._crossing_route = []
                self._crossing_wait = 0
                self._crossing_age = 0
                self._entry_lock_dir = None
                self._entry_lock_ticks = 0
                # do not return — fall through to the planner this very tick.
        if self._crossing_route:
            if self.last_action is not None and not self._near_tile_center((ptx, pty), eps=0.18):
                if self._valid_step(self.last_action, ptx, pty):
                    return self.last_action, None

            if self._crossing_wait > 0:
                self._crossing_wait -= 1
                staging = self._safe_staging_step_for_wait(obs, self._crossing_wait)
                if staging is not None:
                    action, rule = staging
                    self._entry_lock_ticks = max(self._entry_lock_ticks, 3 * self.STEP_TICKS)
                    self._crossing_route = []
                    self._crossing_wait = 0
                    self.current_route = [(ptx + action[0], pty + action[1])]
                    self.route_commit_steps = self._route_commit_ticks(self.current_route, max_tiles=1)
                    self.same_tile_ticks = 0
                    self.last_action = action
                    return action, rule
                if self._wait_is_safe(obs):
                    return None, None
                self._crossing_route = []
                self._crossing_wait = 0
            else:
                action = self._first_step(self._crossing_route, ptx, pty)
                if action is not None and self._valid_step(action, ptx, pty):
                    danger, rule = self._one_step_danger(action, obs)
                    if not danger:
                        self.same_tile_ticks = 0
                        self.last_action = action
                        return action, rule
                    refreshed, wait_steps = self._find_crossing_window(
                        self._crossing_route, obs,
                        max_steps=self.WINDOW_RELIABLE_STEPS)
                    if refreshed is not None and wait_steps > 0:
                        self._crossing_route = list(refreshed)
                        self._crossing_wait = wait_steps * self.STEP_TICKS
                        self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                     3 * self.STEP_TICKS)
                        return None, None
                    staging = self._safe_staging_step_for_wait(
                        obs, self.WINDOW_RELIABLE_STEPS * self.STEP_TICKS)
                    if staging is not None:
                        action, rule = staging
                        self._entry_lock_ticks = max(self._entry_lock_ticks,
                                                     3 * self.STEP_TICKS)
                        self._crossing_route = []
                        self._crossing_wait = 0
                        self.current_route = [(ptx + action[0], pty + action[1])]
                        self.route_commit_steps = self._route_commit_ticks(self.current_route, max_tiles=1)
                        self.same_tile_ticks = 0
                        self.last_action = action
                        return action, rule
                    if self._wait_is_safe(obs):
                        self._crossing_wait = 1
                        return None, None
                self._crossing_route = []
                self._crossing_wait = 0

        # ── temporal window countdown ─────────────────────────────────────────
        # when _find_earliest_safe_window committed us to waiting n steps for a
        # predicted safe gap, count down each tick and act when the timer hits 0.
        # if the current tile becomes unsafe before the window opens, abort the
        # wait and replan immediately — we cannot afford to stay.
        if self._window_wait > 0:
            self._window_wait -= 1
            if not self._wait_is_safe(obs):
                # current tile turned dangerous — abort and fall through to replan
                self._window_action = None
                self._window_wait   = 0
            elif self._window_wait > 0:
                # still counting down — hold position
                return None, None
            else:
                # timer just expired — attempt the window action now.
                action = self._window_action
                self._window_action = None
                if action is not None and self._valid_step(action, ptx, pty):
                    danger, rule = self._one_step_danger(action, obs)
                    if not danger:
                        # window opened as predicted — go, and clear the
                        # failure streak.
                        self._window_fail     = 0
                        self._window_fail_dir = None
                        self.same_tile_ticks  = 0
                        self.last_action      = action
                        return action, rule
                    # predicted gap did not materialise (trap jitter re-rolled
                    # the phase, or the moving-crossing transit differs from the
                    # stationary-dwell forecast).  blindly replanning here just
                    # re-predicts the same unreliable window next tick and waits
                    # again — the classic "waits and never goes" freeze.  count
                    # the failure; once the same direction has failed
                    # window_fail_max times in a row, force the move anyway: the
                    # planner already judged it the best available gap, and
                    # moving (risking one hit) strictly beats freezing until the
                    # run ends.
                    if action == self._window_fail_dir:
                        self._window_fail += 1
                    else:
                        self._window_fail     = 1
                        self._window_fail_dir = action
                    if self._window_fail >= self.WINDOW_FAIL_MAX:
                        self._window_fail     = 0
                        self._window_fail_dir = None
                        self.same_tile_ticks  = 0
                        self.last_action      = action
                        # brief commitment so we actually cross the boundary
                        # instead of re-deciding and reversing next tick.
                        self.current_route = [(ptx + action[0], pty + action[1])]
                        self.route_commit_steps = self._route_commit_ticks(self.current_route, max_tiles=1)
                        return action, rule
                # window didn't open as predicted — fall through to full replan



        # ── committed escape countdown ────────────────────────────────────────
        # a retreat the agent committed to when cornered (set below).  runs for
        # a few ticks without re-deciding so the agent actually crosses a tile
        # boundary instead of jittering in place — the jitter (re-deciding every
        # tick and reversing) was what kept it pinned while a threat closed in.
        # only the genuinely-lethal 1-step check can interrupt it.
        if self._escape_ticks > 0:
            self._escape_ticks -= 1
            edir = self._escape_dir
            if edir is not None and self._valid_step(edir, ptx, pty):
                lethal, _ = self._one_step_danger(edir, obs)
                if not lethal:
                    self.same_tile_ticks = 0
                    self.last_action = edir
                    return edir, None
                # this direction just became lethal — re-pick an escape now
                alt = self._escape_move(obs)
                if alt is not None and alt != edir and self._valid_step(alt, ptx, pty):
                    lethal2, _ = self._one_step_danger(alt, obs)
                    if not lethal2:
                        self._escape_dir = alt
                        self.last_action = alt
                        return alt, None
            # escape exhausted/blocked — fall through
            self._escape_ticks = 0

        # ── cornered-stuck trigger ────────────────────────────────────────────
        # the agent has not changed tile for a long time: goal-seeking is
        # blocked (an enemy/hazard sits on the only progress direction) and
        # waiting just lets the threat converge.  commit to a retreat away from
        # the nearest threat — overriding goal-seeking — and sustain it for
        # ~1 tile so the agent relocates to safer ground.  this is the missing
        # behaviour: every other branch pulls toward the goal, none retreats.
        if (self._escape_ticks == 0
                and getattr(self, '_stuck_ticks', 0) >= self.STEP_TICKS * 5):
            strategic = self._strategic_safe_step(obs)
            if strategic is not None:
                action, route, srule = strategic
                self._wait_streak = 0
                self._deadlock_count = 0
                self.current_route = route
                self.route_commit_steps = self._route_commit_ticks(route)
                self.same_tile_ticks = 0
                self.last_action = action
                return action, srule
            esc = self._escape_move(obs)
            if esc is not None and self._valid_step(esc, ptx, pty):
                self._escape_dir   = esc
                # sustain ~1 tile
                self._escape_ticks = self.STEP_TICKS
                self._wait_streak  = 0
                self._deadlock_count = 0
                self._clear_motion_plan()
                self.last_action = esc
                return esc, None


        # advance committed route past tiles the player has entered.
        while self.current_route and self.current_route[0] == (ptx, pty):
            self.current_route.pop(0)
        if self.current_route:
            nx, ny = self.current_route[0]
            if (abs(nx - ptx) + abs(ny - pty) != 1 or
                    not (0 <= nx < COLS and 0 <= ny < ROWS) or
                    self.grid[ny][nx] == 1):
                self._clear_motion_plan()

        # 0. commitment: if route still looks clear, keep following it.
        # per-tick lightweight check on the immediate next tile catches new
        # threats (e.g. a sweeper just entered the path) without waiting for
        # the periodic full re-check.  full _route_risk re-check still happens
        # every 2 ticks during the commitment window for deeper threats.
        if self.current_route and self.route_commit_steps > 0:
            self.route_commit_steps -= 1

            # variable commit cadence (decision granularity near fast hazards):
            # a committed move normally re-checks the full route every 2 ticks,
            # but near a slow rotating/sweeping arm the agent shortens its
            # effective commitment — re-evaluating every tick and also testing
            # its real sub-tile position — so it can abort an in-flight entry
            # before the arm sweeps in, instead of being locked to the coarse
            # step_ticks quantum through the sweep zone.
            near_fast_arm = self._rotating_hazard_near(obs)

            # ── a. per-tick immediate-tile check (cheap, runs every call) ──
            if self.current_route:
                nx, ny = self.current_route[0]
                ndx, ndy = nx - ptx, ny - pty
                # valid adjacent step
                if abs(ndx) + abs(ndy) == 1:
                    immediate_danger, _ = self._one_step_danger((ndx, ndy), obs)
                    # also veto if a roaming enemy is forecast to intercept the
                    # next tile as the agent enters it — the 1-step danger check
                    # alone misses a slow enemy converging on the committed path.
                    # suppressed during a loiter escape so a crossing the agent
                    # finally committed to isn't aborted on the first tick.
                    _stuck = getattr(self, "_stuck_ticks", 0)
                    enemy_block = (_stuck < self.STEP_TICKS * 7
                                   and self._enemy_threatens_at((nx, ny),
                                                                self.STEP_TICKS))
                    # near a rotating arm, also veto if the body's real position
                    # is about to be swept while still mid-entry.
                    arm_block = near_fast_arm and self._hold_position_swept(obs)
                    if immediate_danger or enemy_block or arm_block:
                        # the very next step has become dangerous — abort.
                        self.current_route = []
                        self.route_commit_steps = 0

            # ── b. full route re-check: every 2 ticks normally, every tick
            # when a fast rotating arm is near (shortened commitment). ──
            recheck_now = (self.route_commit_steps % 2 == 0) or near_fast_arm
            if self.current_route and recheck_now:
                risk, _ = self._route_risk(self.current_route, obs, horizon=self.COMMIT_HORIZON)
                if risk > 0:
                    self.current_route = []
                    self.route_commit_steps = 0

            if self.current_route:
                action = self._first_step(self.current_route, ptx, pty)
                if action is not None and self._valid_step(action, ptx, pty):
                    self.same_tile_ticks = 0
                    self.last_action = action
                    return action, self._last_rule
                self._clear_motion_plan()

        def _commit(route, rule):
            self.current_route = route
            # commit long enough to cross at least one tile; per-tick checks
            # below still interrupt if the immediate step becomes lethal.
            self.route_commit_steps = self._route_commit_ticks(route)
            action = self._first_step(route, ptx, pty)
            if action is None or not self._valid_step(action, ptx, pty):
                self._clear_motion_plan()
                return _fallback(*self._panic_move(obs))
            self.same_tile_ticks = 0
            self.last_action = action
            return action, rule

        def _fallback(action, rule):
            # if panic returned a real action, always use it — don't replay stale moves
            if action is not None and self._valid_step(action, ptx, pty):
                danger, _ = self._one_step_danger(action, obs)
                if danger:
                    strategic = self._strategic_safe_step(obs)
                    if strategic is not None:
                        _, route, srule = strategic
                        return _commit(route, srule)
                    self._clear_motion_plan(clear_last=True)
                    return None, None
                self.same_tile_ticks = 0
                self.last_action = action
                return action, rule
            # truly stuck: replay last known good direction briefly
            self.same_tile_ticks += 1
            if (self.same_tile_ticks < 3 and self.last_action is not None and
                    self._valid_step(self.last_action, ptx, pty)):
                danger, _ = self._one_step_danger(self.last_action, obs)
                if not danger:
                    return self.last_action, None
            # give up on last_action — clear it so we don't keep hammering a wall
            self.last_action = None
            self.same_tile_ticks = 0
            self._clear_motion_plan()
            return None, None

        # 1. primary goal route: always try to progress toward exit first
        # system-2 deliberation begins — charged in step()
        self._planned = True
        goal_route_full = self._dijkstra_route(ptx, pty, obs, penalize=frozenset())
        if not goal_route_full:
            return _fallback(*self._panic_move(obs))

        # ── turn to look toward the goal ──────────────────────────────────────
        # the vision cone follows the agent's heading.  if the goal route leaves
        # in a direction the agent is not currently facing (e.g. it last stepped
        # down but the exit is up), the up-corridor falls outside the fov, the
        # route gets truncated to a single tile, and the agent never perceives
        # the path it needs — it keeps re-looking the way it last moved and
        # flips back and forth.  fix: hold a deliberate gaze toward the goal
        # route's first step while the agent is stationary.  observe() uses this
        # on the next tick, so the agent physically turns its head (one tick of
        # latency) and then keeps facing up the corridor it intends to enter,
        # instead of snapping back to look the way it last travelled.  the gaze
        # is cleared only when the agent actually moves (see step(), where a real
        # tile change resets it), so heading follows travel during motion and
        # follows intent while waiting — no per-tick head-flip.
        if goal_route_full:
            gx, gy = goal_route_full[0]
            gdir = (gx - ptx, gy - pty)
            # if a room-entry direction is locked (set by the oscillation
            # breaker or a committed crossing) and is still a valid step, gaze
            # toward that rather than re-deriving from a route that may still be
            # jittering — the gaze is what rotates the fov, and a rotating fov
            # is half of the flicker feedback loop.  locking the gaze to the
            # committed heading breaks that loop.
            #
            # but only honour the lock when it does not point away from the goal
            # route.  a stale entry lock (e.g. set westward on room entry, then
            # never cleared because oscillating branches keep re-arming its
            # ticks) otherwise pins the gaze — and hence the fov and the dijkstra
            # hysteresis — opposite to the actual exit, so the agent stares and
            # steps back toward the hazard it just passed while the real route
            # runs the other way.
            #
            # a lock pointing away from the goal is only stale, however, when it
            # is not backing an active crossing/escape commitment (those
            # legitimately point away from the goal to clear a hazard first) and
            # the agent is actually stuck (no goal progress for a while).  clear
            # it only in that conjunction, so we break the stale-westward-stare
            # livelock without cancelling a valid hazard-escape dash that must
            # briefly head away from the exit.
            lock = self._entry_lock_dir
            if (lock in self.DIRS and gdir in self.DIRS
                    and (lock[0] * gdir[0] + lock[1] * gdir[1]) < 0
                    and not self._crossing_route
                    and self._crossing_wait <= 0
                    and getattr(self, '_hazard_evac_ticks', 0) <= 0
                    and getattr(self, '_stuck_ticks', 0) >= 4 * self.STEP_TICKS):
                self._entry_lock_dir = None
                self._entry_lock_ticks = 0
                lock = None
            if (lock in self.DIRS
                    and self._valid_step(lock, ptx, pty)):
                gdir = lock
            if gdir in self.DIRS:
                # settle the gaze on the goal direction and keep it there.
                turning = (self._gaze_heading != gdir)
                self._gaze_heading = gdir
                obs_heading = obs.get('heading')
                # if we just turned and this tick's perception still reflects the
                # old facing, hold one tick (turn in place) so the upcoming
                # decision is made from a snapshot that actually sees the goal
                # corridor — but only while holding is safe and not for more than
                # a couple ticks (anti-spin cap), else act on what we can see.
                goal_in_view_now = _in_fov(gdir[0] * 2, gdir[1] * 2,
                                           obs_heading or _heading_from(self.last_action))
                if (turning and not goal_in_view_now
                        and self._wait_is_safe(obs)
                        and self._gaze_hold_count < 2):
                    self._gaze_hold_count += 1
                    self.same_tile_ticks = 0
                    return None, None
                self._gaze_hold_count = 0

        # plan only as far as the agent can see.  the full dijkstra path fixes
        # the direction toward the exit, but committing to the unseen tail —
        # scored against hazard data the agent has no perception of — is what
        # makes the planned route flicker every tick without ever committing.
        # follow the visible prefix; re-plan the next segment as new tiles
        # enter the field of view.
        goal_route = self._truncate_to_vision(goal_route_full, obs)

        # 2. test short near-term horizon only
        risk, rule = self._route_risk(goal_route, obs, horizon=self.GOAL_HORIZON)
        # 2b. internal model drives selection (architecture fig. 1): rather than
        # merely vetoing the pre-chosen route, the internal model simulates
        # every candidate first move, the consequence evaluator judges each
        # trajectory, and only safe actions are fed to the robot controller.
        # - if the goal route's first step is simulated-safe, commit it.
        # - if it is simulated-fatal but another move is safe, redirect to
        # the safe move that best progresses toward the goal (the sim is
        # now finding the safe path, not just rejecting the unsafe one).
        # - if every move is simulated-fatal, fall through to the timed-
        # crossing / least-bad planners below.
        if self.use_sim and self._has_dynamic_threats(obs):
            goal_first = self._first_step(goal_route, ptx, pty) if goal_route else None
            safe_actions, verdicts = self._sim_screen_actions(
                obs, plies=self.GOAL_HORIZON)
            if goal_first is not None and goal_first in verdicts:
                if verdicts[goal_first]['died']:
                    # planned step is fatal in simulation.
                    self._form_rollout_expectation(
                        obs, {'died': True,
                              'death_kind': verdicts[goal_first]['death_kind'],
                              'death_ply': verdicts[goal_first]['death_ply'],
                              'path': [(ptx, pty),
                                       (ptx + goal_first[0], pty + goal_first[1])]})
                    # first choice: a sim-timed crossing — wait for the
                    # deterministic mover to clear, then take the step (keeps the
                    # agent on its route and threads the hazard, instead of
                    # sidestepping into a possibly-worse pocket).  runs before the
                    # agent can get cornered, which is why it resolves the
                    # boulder/sweeper/lava "predictable" deaths at the source.
                    timed = self._sim_timed_crossing(obs)
                    if timed is not None:
                        wait_t, tact = timed
                        if wait_t <= 0:
                            self._clear_motion_plan(clear_last=True)
                            self.same_tile_ticks = 0
                            self.last_action = tact
                            self.current_route = [(ptx + tact[0], pty + tact[1])]
                            self.route_commit_steps = self._route_commit_ticks(
                                self.current_route, max_tiles=1)
                            self._wait_streak = 0
                            return tact, None
                        # window opens shortly — hold safely until then.
                        self._window_action = tact
                        self._window_wait = wait_t
                        self._wait_streak = 0
                        return None, None
                    if safe_actions:
                        # no timed window on the route; redirect to the best
                        # simulated-safe move toward goal.
                        best = safe_actions[0]
                        self._clear_motion_plan(clear_last=True)
                        self.same_tile_ticks = 0
                        self.last_action = best
                        self.current_route = [(ptx + best[0], pty + best[1])]
                        self.route_commit_steps = self._route_commit_ticks(
                            self.current_route, max_tiles=1)
                        self._wait_streak = 0
                        return best, None
                    # no safe move at all → let least-bad machinery handle it.
                    risk = max(risk, 1)
                # else: goal step is simulated-safe → fall through to commit it.
            elif goal_first is None and not safe_actions:
                risk = max(risk, 1)
        # 3. goal route is survivable — take it directly
        if risk == 0:
            self._wait_streak  = 0
            # clear multi-trap freeze counter on safe progress
            self._deadlock_count = 0
            return _commit(goal_route, rule)

        # timed moving-trap crossing: a moving hazard can make the next tile
        # or a near-future route tile lethal only at certain phases. greedy
        # one-tile advances enter the swept zone, abort, retreat, and repeat.
        # instead, find the whole contested segment, wait at the safe edge for
        # a verified full-route window, then keep the crossing armed.
        open_obs = dict(obs)
        moving_kinds = {dt.kind for dt in getattr(self, '_room_dtraps', [])
                        if TRAP_SENSORS.get(dt.kind, {}).get('mov', False)}
        open_obs['trap_map'] = {tile: kind for tile, kind in obs.get('trap_map', {}).items()
                                if kind not in moving_kinds}
        direct_route = self._dijkstra_route(ptx, pty, open_obs, penalize=frozenset())
        open_route = direct_route or goal_route
        entry_routes = [open_route, goal_route]
        entry_routes.extend(self._candidate_routes(ptx, pty, k=6, obs=open_obs))
        timed_entry = self._best_timed_entry_plan(obs, entry_routes)
        if timed_entry is not None:
            crossing_route, wait_steps, first = timed_entry
            if list(crossing_route) != self._crossing_route:
                # genuinely new crossing → fresh budget
                self._crossing_age = 0
            self._crossing_route = list(crossing_route)
            self._crossing_wait = wait_steps * self.STEP_TICKS
            self._entry_lock_dir = first
            self._entry_lock_ticks = max(self._entry_lock_ticks, 4 * self.STEP_TICKS)
            self.current_route = []
            self.route_commit_steps = 0
            self._wait_streak = 0
            if self._crossing_wait > 0:
                return None, None
            action = self._first_step(self._crossing_route, ptx, pty)
            if action is not None and self._valid_step(action, ptx, pty):
                danger, crule = self._one_step_danger(action, obs)
                if not danger:
                    self.same_tile_ticks = 0
                    self.last_action = action
                    return action, crule

        crossing_seed = (self._timed_dynamic_crossing_route(obs, open_route)
                         or self._rotating_crossing_route(obs, open_route))
        if (not crossing_seed and self._has_dynamic_threats(obs)
                and self._wait_is_safe(obs)):
            # doorway timing: if the chosen route is blocked only because a
            # mover is currently crossing it, ask the internal model for the
            # next window where this same route segment is clear.  previously
            # the controller dropped into the generic wait branch below, which
            # clears the plan and replans every tick; at room entrances that
            # makes the selected option flicker instead of committing to the
            # simulated opening.
            # keep this short: room interiors often contain several movers, so
            # demanding a full 5-tile room prefix to be clear can fail even
            # when the doorway itself has a perfectly good timed opening.
            doorway_len = min(len(open_route), 3)
            if doorway_len >= 1:
                crossing_seed = open_route[:doorway_len]
        if crossing_seed and self._wait_is_safe(obs):
            crossing_route, wait_steps = self._find_crossing_window(crossing_seed, obs)
            if crossing_route is not None:
                if list(crossing_route) != self._crossing_route:
                    # genuinely new crossing → fresh budget
                    self._crossing_age = 0
                self._crossing_route = list(crossing_route)
                self._crossing_wait = wait_steps * self.STEP_TICKS
                self._entry_lock_dir = self._first_step(self._crossing_route, ptx, pty)
                self._entry_lock_ticks = max(self._entry_lock_ticks, 4 * self.STEP_TICKS)
                self.current_route = []
                self.route_commit_steps = 0
                self._wait_streak = 0
                if self._crossing_wait > 0:
                    return None, None
                action = self._first_step(self._crossing_route, ptx, pty)
                if action is not None and self._valid_step(action, ptx, pty):
                    danger, crule = self._one_step_danger(action, obs)
                    if not danger:
                        self.same_tile_ticks = 0
                        self.last_action = action
                        return action, crule

        # 3a. greedy single-step progress (the real fix for "frozen in front of
        # a moving trap").  the horizon=5 risk above is essentially always
        # >0 when a moving trap cycles anywhere near the 5-tile path: the
        # 50-game-tick rollout catches the trap in the path at some step,
        # so step 3 can never commit.  the agent then falls into step 3b's
        # blind 40-tick wait — during which the safe window to advance one
        # tile opens and closes undetected, because nothing re-checks
        # single-step safety until step 5 (panic), which only runs after
        # the wait expires.  the agent stands on a safe tile watching gaps
        # open and close in front of it, unable to take them.
        #
        # fix: re-check only the immediate next step toward the goal
        # (horizon=1, the exact sub-pixel transit check _one_step_danger
        # uses).  if advancing one tile toward the exit is safe this tick,
        # take it and re-evaluate next tick — threading the gap the instant
        # it opens instead of demanding the whole route be clear at once.
        # the horizon=5 check still governs route choice (step 4 won't pick
        # a detour that dead-ends into a trap); this only governs the
        # wait-vs-advance decision on an already-chosen good route.
        near_risk, near_rule = self._route_risk(goal_route, obs, horizon=1)
        if near_risk == 0:
            # per-tile enemy interception forecast.  the 1-step risk check above
            # is blind to a roaming enemy converging on the path from 1-2 tiles
            # away, so we forecast each candidate tile against the enemy's
            # deterministic current leg.  but we veto per-tile, not all-or-
            # nothing: if only the second tile is threatened we still commit the
            # (safe) first tile, so the agent keeps approaching a room one safe
            # tile at a time instead of refusing to move because a tile further
            # in is momentarily contested.  loiter escape: if the agent has been
            # stuck on this tile for a while (an enemy permanently patrolling a
            # doorway), relax the veto and attempt the crossing — making slow
            # risky progress beats timing out in the hallway forever.
            stuck = getattr(self, "_stuck_ticks", 0)
            loiter_escape = stuck >= self.STEP_TICKS * 7
            eta0 = self.STEP_TICKS
            first_blocked = (not loiter_escape) and self._enemy_threatens_at(
                goal_route[0], eta0)
            if not first_blocked:
                # normal greedy commit follows a 2-tile prefix.  during a loiter
                # escape, probe only one tile at a time: the agent is forcing a
                # contested crossing, so it should re-evaluate after every step
                # rather than commit two tiles blind.
                prefix = goal_route[:1]
                if (len(goal_route) > 1 and not loiter_escape
                        and not self._enemy_threatens_at(goal_route[1], 2 * eta0)):
                    prefix = goal_route[:2]
                self._wait_streak    = 0
                self._deadlock_count = 0
                return _commit(prefix, near_rule)

        # safe progress detours before waiting. a safe tile is only useful if
        # it helps solve the maze; if the direct route is temporarily blocked,
        # first look for a zero-risk route that still advances toward the exit.
        detours  = self._candidate_routes(ptx, pty, k=8, obs=obs)
        labelled = []
        for route in detours:
            r, rr     = self._route_risk(route, obs, horizon=self.GOAL_HORIZON)
            progress  = self._goal_progress_score(route)
            labelled.append((r, progress, len(route), route, rr))

        viable = [x for x in labelled if x[0] == 0]
        if viable:
            _, _, _, route, rule = min(viable, key=lambda x: (x[1], x[2]))
            self._wait_streak = 0
            self._deadlock_count = 0
            return _commit(route, rule)
            # else: even the immediate step walks into an enemy → wait below

        # 3b. goal route blocked by a dynamic obstacle — wait for a safe window.
        # "some stalling is fine, but it should wait for a safe window then
        # go."  when the only thing blocking the goal route is a moving
        # hazard / roaming enemy (a transient block that will clear) and
        # holding position is itself safe, hold — and keep re-testing every
        # tick.  reached only when even the immediate step toward the goal
        # is blocked (step 3a already takes any safe single step); the
        # instant that immediate step clears, step 3a advances next tick.
        # this avoids both retreating (which loses sight of the blockage)
        # and pushing through (which is fatal).  a bounded streak prevents
        # waiting forever on a block that never clears (e.g. a static
        # hazard or a persistently camped enemy): after _wait_max held
        # ticks we fall through to detour search instead.
        # if longer-horizon route risk is uncertain, still take a single
        # verified-safe step that reduces distance to the exit. this keeps the
        # agent entering rooms and making measurable progress instead of
        # waiting purely because all multi-step futures contain some risk.
        strategic = self._strategic_safe_step(obs)
        if strategic is not None:
            _, route, srule = strategic
            self._wait_streak = 0
            self._deadlock_count = 0
            return _commit(route, srule)

        ex, ey = self.end
        cur_goal_dist = abs(ptx - ex) + abs(pty - ey)
        best_step = None
        for dx_s, dy_s in self.DIRS:
            tx_s, ty_s = ptx + dx_s, pty + dy_s
            if not self._valid_step((dx_s, dy_s), ptx, pty):
                continue
            if self._enemy_threatens_at((tx_s, ty_s), self.STEP_TICKS):
                continue
            danger_s, rule_s = self._one_step_danger((dx_s, dy_s), obs)
            if danger_s:
                continue
            goal_dist = abs(tx_s - ex) + abs(ty_s - ey)
            if goal_dist >= cur_goal_dist:
                continue
            visits = self._visit_counts.get((tx_s, ty_s), 0)
            score = (goal_dist, visits)
            if best_step is None or score < best_step[0]:
                best_step = (score, (dx_s, dy_s), rule_s)
        if best_step is not None:
            self._wait_streak = 0
            self._deadlock_count = 0
            self.current_route = [(ptx + best_step[1][0], pty + best_step[1][1])]
            self.route_commit_steps = self._route_commit_ticks(self.current_route, max_tiles=1)
            self.same_tile_ticks = 0
            self.last_action = best_step[1]
            return best_step[1], best_step[2]

        doorway_stage = self._doorway_staging_step(obs)
        if doorway_stage is not None:
            action, route, drule = doorway_stage
            self._wait_streak = 0
            self._deadlock_count = 0
            self.current_route = route
            self.route_commit_steps = self._route_commit_ticks(route, max_tiles=1)
            self.same_tile_ticks = 0
            self.last_action = action
            return action, drule

        # doorway enemy timing: if the route into the room is blocked by a
        # roaming enemy's current deterministic leg, do not wait for the broad
        # deadlock watchdog.  simulate the enemy forward to the next random
        # waypoint choice and launch the shortest verified dash as soon as that
        # leg opens a gap.
        if goal_route and self._wait_is_safe(obs):
            first_enemy_block = self._enemy_threatens_at(
                goal_route[0], self.STEP_TICKS)
            if first_enemy_block:
                dash = self._corridor_dash_plan(
                    obs, goal_route, max_wait=80, dash_tiles=3)
                if dash is not None:
                    wait_ticks, dash_route = dash
                    if wait_ticks == 0 and dash_route:
                        self._wait_streak = 0
                        self._deadlock_count = 0
                        self._clear_motion_plan()
                        self.current_route = list(dash_route)
                        self.route_commit_steps = self._route_commit_ticks(
                            self.current_route, max_tiles=len(self.current_route))
                        action = self._first_step(self.current_route, ptx, pty)
                        if action is not None:
                            self._entry_lock_dir = action
                            self._entry_lock_ticks = max(
                                self._entry_lock_ticks,
                                len(self.current_route) * self.STEP_TICKS)
                            self.same_tile_ticks = 0
                            self.last_action = action
                            return action, None
                    if wait_ticks > 0 and dash_route:
                        self._wait_streak = 0
                        self._deadlock_count = 0
                        self._clear_motion_plan()
                        self._crossing_route = list(dash_route)
                        self._crossing_wait = wait_ticks
                        self._crossing_age = 0
                        first = self._first_step(self._crossing_route, ptx, pty)
                        if first is not None:
                            self._entry_lock_dir = first
                            self._entry_lock_ticks = max(
                                self._entry_lock_ticks,
                                len(self._crossing_route) * self.STEP_TICKS)
                        return None, None

        _WAIT_MAX = self.WAIT_MAX
        if (self._has_dynamic_threats(obs)
                and self._wait_streak < _WAIT_MAX
                and self._wait_is_safe(obs)):
            staging = self._safe_staging_step_for_wait(
                obs, min(_WAIT_MAX - self._wait_streak, self.WINDOW_RELIABLE_STEPS * self.STEP_TICKS))
            if staging is not None:
                action, srule = staging
                self._wait_streak = 0
                self._deadlock_count = 0
                self._entry_lock_ticks = max(self._entry_lock_ticks, 3 * self.STEP_TICKS)
                self._clear_motion_plan()
                self.current_route = [(ptx + action[0], pty + action[1])]
                self.route_commit_steps = self._route_commit_ticks(self.current_route, max_tiles=1)
                self.last_action = action
                return action, srule
            self._wait_streak += 1
            # hold position; re-decide next tick
            self._clear_motion_plan()
            return None, None
        # block did not clear in time (or waiting is unsafe / block is static):
        # proceed to detours / panic, and reset the streak so the next distinct
        # block gets its own full wait budget.
        self._wait_streak = 0

        # 4. goal route blocked near-term — search for detours
        detours  = self._candidate_routes(ptx, pty, k=6, obs=obs)
        labelled = []
        for route in detours:
            r, rr     = self._route_risk(route, obs, horizon=self.GOAL_HORIZON)
            progress  = self._goal_progress_score(route)
            labelled.append((r, progress, len(route), route, rr))

        viable = [x for x in labelled if x[0] == 0]
        if viable:
            _, _, _, route, rule = min(viable, key=lambda x: (x[0], x[1], x[2]))
            return _commit(route, rule)

        # 5. all multi-step routes look dangerous — try a safe immediate move.
        # the route-level risk might be overestimated due to false positives
        # downstream, but an adjacent tile that is safe right now is genuinely
        # the safest play.  panic prefers safe tiles (danger heavily penalised).
        panic_action, panic_rule = self._panic_move(obs)
        if panic_action is not None:
            # _panic_move returned a real action. clear hallway moves often
            # have no attached rule yet; do not treat "no rule" as "no move".
            # re-check the chosen tile's danger directly.
            dx_p, dy_p = panic_action
            danger_p, _ = self._one_step_danger((dx_p, dy_p), obs)
            if not danger_p:
                self.same_tile_ticks  = 0
                self.last_action      = panic_action
                # made progress
                self._deadlock_count  = 0
                # brief commitment so we don't immediately re-plan after one tick
                self.current_route = [(obs['ptx']+dx_p, obs['pty']+dy_p)]
                self.route_commit_steps = self._route_commit_ticks(self.current_route, max_tiles=1)
                return panic_action, panic_rule


        # 5.5. temporal window: every adjacent tile is currently dangerous due
        # to dynamic threats, but a safe gap may appear within a few agent steps
        # as the hazards move through their cycles.  simulate the world forward
        # (player stationary) to find which direction clears first and when.
        # store the result and hold position for exactly that many steps, then
        # execute the committed move.  this breaks the "stuck between two moving
        # threats" deadlock without the agent freezing indefinitely or accepting
        # guaranteed damage.
        if self._has_dynamic_threats(obs) and self._wait_is_safe(obs):
            window_dir, window_ticks = self._find_earliest_safe_window(obs)
            if window_dir is not None:
                self._window_action = window_dir
                # _window_wait is decremented once per game tick (every
                # choose_action call).  _find_earliest_safe_window returns
                # wait_step in agent steps (each = step_ticks game ticks),
                # so convert to the correct unit here.
                #
                # reliability cap: the dynamic traps re-roll their dwell timers
                # with stochastic jitter on every cycle (random.randint per
                # state transition), so a gap predicted more than ~one short
                # dwell ahead is forecasting an rng that will have moved by the
                # time we get there — that stale forecast was the root of the
                # "wait forever, the gap never matches" freeze.  commit to at
                # most window_reliable_steps of waiting, then re-plan against
                # fresh world state.  if the true window was further out we will
                # simply re-find it (now closer, and within the reliable
                # horizon); if it never converges, the window-failure counter
                # forces the move.
                committed_steps     = min(window_ticks, self.WINDOW_RELIABLE_STEPS)
                self._window_wait   = committed_steps * self.STEP_TICKS
                self._clear_motion_plan(clear_last=True)
                return None, None

        # 6. no safe move anywhere — commit to least-bad route to keep moving.
        # the agent accepts some risk rather than freezing (and possibly being
        # hit by a moving trap while standing still).
        #
        # multi-trap deadlock guard: when every route looks risky and waiting
        # is safe but no temporal window was found, we would return none,none,
        # _wait_streak resets to 0, step 3b starts 40 more ticks, and the
        # cycle repeats forever.  after _deadlock_max consecutive step-6 waits
        # we accept a potentially risky route — moving and risking damage is
        # strictly better than freezing until the run ends.
        _DEADLOCK_MAX = self.DEADLOCK_MAX
        if labelled:
            best = min(labelled, key=lambda x: (x[0], x[1], x[2]))
            _, _, _, route, rule = best
            if route:
                if self._wait_is_safe(obs) and self._deadlock_count < _DEADLOCK_MAX:
                    self._deadlock_count += 1
                    self._clear_motion_plan(clear_last=True)
                    return None, None
                self._deadlock_count = 0
                action = self._first_step(route, ptx, pty)
                if action is not None:
                    danger, _ = self._one_step_danger(action, obs)
                    if danger:
                        strategic = self._strategic_safe_step(obs)
                        if strategic is not None:
                            _, route2, srule = strategic
                            return _commit(route2, srule)
                        if self._wait_is_safe(obs):
                            self._clear_motion_plan(clear_last=True)
                            return None, None
                return _commit(route, rule)

        # 7. absolute last resort
        return _fallback(*self._panic_move(obs))

    def _goal_progress_score(self, route):
        """Manhattan distance from the 5th tile (or last) to exit — lower is closer."""
        if not route:
            return float('inf')
        ex, ey = self.end
        tx, ty = route[min(len(route) - 1, 4)]
        return abs(tx - ex) + abs(ty - ey)

    def _strategic_safe_step(self, obs):
        """Pick a safe adjacent step that leads toward a viable route.

        A correct bypass around a room hazard often starts sideways, so pure
        Manhattan progress rejects it and the agent jitters at the doorway.
        This evaluates every safe adjacent tile by the route it opens from
        there, with a small penalty for reversing the previous move.
        """
        ptx, pty = obs['ptx'], obs['pty']
        ex, ey = self.end
        cur_dist = abs(ptx - ex) + abs(pty - ey)
        reverse = None
        if self.last_action is not None:
            reverse = (-self.last_action[0], -self.last_action[1])

        best = None
        for dx, dy in self.DIRS:
            tx, ty = ptx + dx, pty + dy
            if not self._valid_step((dx, dy), ptx, pty):
                continue
            if self._enemy_threatens_at((tx, ty), self.STEP_TICKS):
                continue
            danger, rule = self._one_step_danger((dx, dy), obs)
            if danger:
                continue

            tail = self._dijkstra_route(tx, ty, obs, penalize={(ptx, pty)})
            if tail is None:
                tail = []
            route = [(tx, ty)] + tail
            probe = route[:max(1, min(3, len(route)))]
            risk, rr = self._route_risk(probe, obs, horizon=len(probe))
            if risk > 0:
                route = [(tx, ty)]

            end_tx, end_ty = route[min(len(route) - 1, 4)]
            future_dist = abs(end_tx - ex) + abs(end_ty - ey)
            first_dist = abs(tx - ex) + abs(ty - ey)
            visits = self._visit_counts.get((tx, ty), 0)
            rev_penalty = 2.5 if reverse == (dx, dy) else 0.0
            score = (future_dist,
                     0 if future_dist < cur_dist or first_dist <= cur_dist else 1,
                     len(route),
                     visits * 0.35 + rev_penalty)
            if best is None or score < best[0]:
                best = (score, (dx, dy), route, rr or rule)

        if best is None:
            return None
        return best[1], best[2], best[3]

    def _doorway_staging_step(self, obs):
        """Enter a room via a short simulated interior staging route.

        A doorway tile is often a bad place to *wait*: spore rings, sweeps, and
        roaming enemies can cross it again before the next full plan settles.
        The old helper therefore rejected valid room entries because it required
        the first tile inside the room to be a campsite.  Instead, simulate a
        short prefix that keeps moving to an interior staging point, then only
        require the final staging point to survive a brief replanning hold.
        """
        if not self._has_dynamic_threats(obs):
            return None
        ptx, pty = obs['ptx'], obs['pty']
        cur_room = self.room_of.get((ptx, pty))
        ex, ey = self.end
        base = self._make_sim_state(obs)
        best = None
        for dx, dy in self.DIRS:
            tx, ty = ptx + dx, pty + dy
            if not self._valid_step((dx, dy), ptx, pty):
                continue
            next_room = self.room_of.get((tx, ty))
            if next_room is None or next_room is cur_room:
                continue

            candidate_routes = []
            tail = self._dijkstra_route(tx, ty, obs, penalize={(ptx, pty)}) or []
            candidate_routes.append([(tx, ty)] + tail[:3])
            for alt in self._candidate_routes(tx, ty, k=4, obs=obs):
                candidate_routes.append([(tx, ty)] + alt[:3])

            seen = set()
            for route in candidate_routes:
                route = [t for t in route if t is not None]
                if not route or route[0] != (tx, ty):
                    continue
                key = tuple(route)
                if key in seen:
                    continue
                seen.add(key)

                # keep only a contiguous short prefix, and stop once the route
                # tries to leave the room we are entering.  this creates a real
                # room-entry commitment without blindly crossing the whole room.
                prefix = []
                cx, cy = ptx, pty
                for nx, ny in route[:4]:
                    if abs(nx - cx) + abs(ny - cy) != 1:
                        break
                    if self.room_of.get((nx, ny)) is not next_room:
                        break
                    prefix.append((nx, ny))
                    cx, cy = nx, ny
                if not prefix:
                    continue

                end_tx, end_ty = prefix[-1]
                hold_sim = self._sim_route_end_state(base, prefix)
                if hold_sim is None:
                    continue
                if not self._sim_hold_clear(hold_sim, self.STEP_TICKS):
                    continue

                future_dist = abs(end_tx - ex) + abs(end_ty - ey)
                visits = sum(self._visit_counts.get(t, 0) for t in prefix)
                clearance = min(self._rotator_clearance(x, y) for x, y in prefix)
                depth = len(prefix)
                score = (future_dist, -depth, visits * 0.25, -clearance)
                if best is None or score < best[0]:
                    first = (prefix[0][0] - ptx, prefix[0][1] - pty)
                    best = (score, first, prefix, None)

        if best is None:
            return None
        return best[1], best[2], best[3]

    def _blocked_for_planning(self, tx: int, ty: int) -> bool:
        """Effective obstacle test for ALL route generation and stepping.

        A tile is impassable for planning if it is a grid wall OR carries a
        known static trap.  Folding known static traps into the SAME hard
        obstacle test the planner uses for walls makes a static-trap death
        impossible by construction: no candidate route through one is ever
        generated, so no such move can ever be committed or executed — the body
        is never sent toward it in the first place.  This is stronger than a
        risk penalty (which goal-pull or a deadlock valve could outweigh): a
        wall is never "worth it", and now neither is a known static trap.
        """
        if not (0 <= tx < COLS and 0 <= ty < ROWS):
            return True
        if self.grid[ty][tx] == 1:
            return True
        return self._tile_has_known_static_trap((tx, ty))

    def _candidate_routes(self, sx, sy, k=6, obs=None) -> list:
        obs      = obs or self._last_obs or {}
        routes   = []
        penalize: set = set()
        for _ in range(k):
            route = self._dijkstra_route(sx, sy, obs, penalize=penalize)
            if route is None:
                break
            routes.append(route)
            for tx, ty in route:
                penalize.add((tx, ty))
        return routes

    def _dijkstra_route(self, sx, sy, obs, penalize: set = frozenset()) -> list | None:
        # hysteresis: bias the first step out of the start tile toward the
        # direction the agent is already committed to (its last action / the
        # heading of the route it is currently following).  without this, two
        # near-equal routes around a hazard-flanked doorway swap which one is
        # cheapest every tick as the moving trap cycles its +2 penalty on and
        # off, and the agent's chosen first step flips a->b->a forever while
        # never actually crossing a tile (so the tile-history oscillation
        # breaker never even sees it).  a small continuation bonus makes the
        # current heading "sticky": the agent only abandons it when an
        # alternative is genuinely, not marginally, better.
        ex, ey      = self.end
        trap_map    = obs.get('trap_map', {})
        enemy_tiles = obs.get('enemy_tiles', set())
        spore_zone  = self._spore_blast_zone(obs)
        prefer_dir  = self._committed_dir()
        # continuation bonus must be smaller than the smallest real cost signal
        # (a +1.5 penalty / +2 hazard) so it only decides genuine ties and
        # near-ties, never overrides a real safety penalty.
        CONT_BONUS  = 0.6
        dist_map    = {(sx, sy): 0.0}
        par         = {(sx, sy): None}
        # heap entries carry a deterministic tiebreak (dir index, then tile)
        # so equal-cost expansions are resolved identically every tick rather
        # than by nondeterministic heap/insertion order.
        heap        = [(0.0, 0, sx, sy)]
        while heap:
            cost, _tb, cx, cy = heapq.heappop(heap)
            if cost > dist_map.get((cx, cy), float('inf')):
                continue
            if (cx, cy) == (ex, ey):
                path, pos = [], (cx, cy)
                while pos != (sx, sy):
                    path.append(pos); pos = par[pos]
                return path[::-1]
            for di, (ddx, ddy) in enumerate(self.DIRS):
                nx, ny = cx+ddx, cy+ddy
                if self._blocked_for_planning(nx, ny):
                    continue
                step = 1.0
                # ── danger aversion (human-like routing) ────────────────────
                # a dynamic-hazard or enemy tile is a one-hit kill, not a minor
                # toll.  the old +2 meant the planner would thread a path
                # straight through a lethal zone whenever going around cost more
                # than two tiles — exactly the "riskier path a human wouldn't
                # take" behaviour.  a person treats a known hazard tile as
                # near-impassable and only crosses it when there is genuinely no
                # reasonable alternative.  we model that with a large penalty
                # (hazard_cost) that distance can almost never outweigh, while
                # still staying finite so the bounded-risk deadlock valves can
                # force a crossing when the maze truly leaves no other route.
                # cost of routing onto a lethal tile
                HAZARD_COST   = 18.0
                # cost of hugging the edge of a hazard
                ADJ_BUFFER    = 3.0
                on_hazard = ((nx, ny) in trap_map) or ((nx, ny) in enemy_tiles)
                if on_hazard:
                    step += HAZARD_COST
                else:
                    # keep a margin: tiles orthogonally adjacent to a hazard are
                    # costlier so the planner prefers a path that gives danger a
                    # wide berth rather than skimming its edge, where a moving
                    # trap's next tile or a one-tick forecast error is lethal.
                    for adx, ady in self.DIRS:
                        anb = (nx + adx, ny + ady)
                        if anb in trap_map or anb in enemy_tiles:
                            step += ADJ_BUFFER
                            break
                if (nx, ny) in penalize:    step += 1.5
                # inside an
                if (nx, ny) in spore_zone:  step += HAZARD_COST
                # expanding/imminent spore disc: the outward-sweeping ring will
                # pass through this tile, and it grows about as fast as the
                # agent moves, so a tile inside the disc is un-outrunnable once
                # the front arrives.  treat it like any other lethal tile, not
                # a +4 toll the goal-pull could outweigh.
                # mild revisit penalty: tiles the agent has bounced on many
                # times (a trapped oscillation region, marked by the confinement
                # escape) become slightly costlier, nudging the planner toward
                # unexplored ground instead of re-entering the bounce.  capped
                # so it never dominates a real hazard signal.
                vc = self._visit_counts.get((nx, ny), 0)
                if vc > 3:
                    step += min(2.0, 0.15 * (vc - 3))
                # apply the continuation bonus only on the very first step out
                # of the start tile, only when this step matches the committed
                # heading, and only when that heading is genuinely available.
                if ((cx, cy) == (sx, sy) and prefer_dir is not None
                        and (ddx, ddy) == prefer_dir):
                    step = max(0.05, step - CONT_BONUS)
                nc = cost + step
                if nc < dist_map.get((nx, ny), float('inf')):
                    dist_map[(nx, ny)] = nc
                    par[(nx, ny)]      = (cx, cy)
                    heapq.heappush(heap, (nc, di, nx, ny))
        return None

    def _committed_dir(self):
        """The direction the agent is currently committed to, if any — used as
        a hysteresis anchor so route planning doesn't flip-flop tick to tick.

        Prefers (in order): the locked room-entry direction, the first step of
        the live committed route, then the last action actually taken.  Returns
        None when the agent has no active commitment (a genuine fresh decision,
        where no bias should apply)."""
        if self._entry_lock_dir in self.DIRS:
            return self._entry_lock_dir
        if self.current_route:
            nx, ny = self.current_route[0]
            # derive direction from last known position when available.
            if self._last_pos is not None:
                d = (nx - self._last_pos[0], ny - self._last_pos[1])
                if d in self.DIRS:
                    return d
        if self.last_action in self.DIRS:
            return self.last_action
        return None

    def _truncate_to_vision(self, route: list, obs: dict) -> list:
        """Clip a planned route to the agent's current field of view.

        Dijkstra always plans all the way to the exit, but tiles beyond the
        forward vision cone are scored against hazard data the agent CANNOT
        see — those tiles are simply absent from obs['trap_map'], so they look
        falsely safe, and their shape changes every tick as the agent (and any
        partly-visible moving hazard) shifts.  Committing to that unseen tail
        is what produces the "flicker between full routes, never commit"
        oscillation: each tick re-derives a different far half and the renderer
        redraws it.

        The agent should commit only to the stretch it can actually verify.
        We keep the route's visible PREFIX (which still points toward the goal,
        since the full plan determines the first tiles' direction) and drop the
        rest.  The agent re-plans the next segment once it advances and new
        tiles enter view — planning exactly as far as it can see.

        The own tile is always visible; we always retain at least the first
        step so the agent never stalls purely from truncation.
        """
        if not route or not VISION_ENABLED:
            return route
        ptx = obs.get('ptx')
        pty = obs.get('pty')
        if ptx is None or pty is None:
            return route
        heading = obs.get('heading') or _heading_from(self.last_action)
        visible_prefix = []
        for (tx, ty) in route:
            if _in_fov(tx - ptx, ty - pty, heading):
                visible_prefix.append((tx, ty))
            else:
                break
        # always keep at least the immediate step: it is adjacent and its
        # safety is verified directly by _one_step_danger before any commit.
        if not visible_prefix:
            return route[:1]
        return visible_prefix

    @staticmethod
    def _has_fast_radius_hazard(sim: dict) -> bool:
        """True if the scene contains a hazard whose lethal geometry moves fast
        enough (≈≥1 tile per agent step) that a per-tile snapshot goes stale
        within one rollout step — currently the expanding spore ring."""
        for dt in sim.get('_sim_dtraps', []):
            if dt.kind == 'spore_burst':
                return True
        return False

    def _advance_sim_movers(self, sim: dict) -> None:
        """Advance cloned dynamic traps/enemies by one agent decision step."""
        stub = _SimPlayer(sim.get('px', sim['ptx']), sim.get('py', sim['pty']))
        stub.pulse_spd_mod = sim.get('pulse_spd_mod', 1.0)
        for _ in range(self.STEP_TICKS):
            for dt in sim.get('_sim_dtraps', []):
                _sim_update_dtrap(dt, stub)
            for e in sim.get('_sim_enemies', []):
                _sim_update_enemy(e)
        self._rebuild_sim_derived(sim)

    def _route_risk(self, route: list, obs, horizon: int = 5) -> tuple:
        """Score a route by simulating the world forward step-by-step.

        Implements the paper's §III-F memory-first principle:
          "Before a new simulation is run, it will reference the Expectation
           storage to determine whether any relevant expectations could be used
           instead of simulating."

        Each step:
          1. Query ExpectationMemory — if confident prediction exists, skip sim
          2. If no prior: advance traps/enemies by STEP_TICKS (Internal Model)
          3. Evaluate the target tile with the correct (dx,dy) offset
          4. If a trap swept through the target mid-transit, treat as danger
             and form an expectation from that simulated state (EEC Formation)
          5. Move the simulated player to the target tile
        """
        cache = getattr(self, '_decision_cache', None)
        cache_key = None
        if cache is not None:
            prefix = tuple(route[:horizon])
            cache_key = (prefix, horizon, obs.get('sim_time'),
                         obs.get('ptx'), obs.get('pty'),
                         round(obs.get('px', obs.get('ptx', 0)), 2),
                         round(obs.get('py', obs.get('pty', 0)), 2))
            route_cache = cache.setdefault('route_risk', {})
            if cache_key in route_cache:
                return route_cache[cache_key]
        sim        = self._make_sim_state(obs)
        risk       = 0
        worst_rule = None
        t          = obs.get('sim_time', 0)
        dynamic_scene = bool(sim.get('_sim_dtraps') or sim.get('_sim_enemies'))
        step_i     = -1

        for target in route[:horizon]:
            step_i += 1
            # advance formal simulation time per rollout step so expectations
            # formed during the rollout carry distinct happens(a, t) timestamps.
            t += 1
            sim['sim_time'] = t

            dx = target[0] - sim['ptx']
            dy = target[1] - sim['pty']
            tx, ty = sim['ptx'] + dx, sim['pty'] + dy

            # ── hard static-hazard constraint ────────────────────────────────
            # a known static trap never moves; routing onto it is never
            # acceptable regardless of goal pull.  treat it as maximal,
            # non-negotiable risk so no route through it is ever selected and
            # any committed route that includes it is dropped on re-check.
            if self._tile_has_known_static_trap((tx, ty)):
                risk += 1
                if worst_rule is None:
                    worst_rule = None
                break

            # ── dynamics-first: deduce safety from learned behaviour laws ────
            # before consulting outcome memory or the internal model, ask the
            # learned dynamics model whether this tile is entailed occupied or
            # free over the traversal window.  this is navigation by knowing
            # how things work: a reliability-licensed occupancy law makes the
            # verdict a guarantee, not a guess.
            if self.use_dynamics:
                k_from = sim.get('lead_ticks', 0) + step_i * self.STEP_TICKS + 1
                k_to   = k_from + self.STEP_TICKS - 1
                dv, dconf, dyn_rule = self.dynamics.window_state(
                    (tx, ty), k_from, k_to)
                if dv == 'danger':
                    self.memory.sims_skipped += 1
                    self.dynamics.answers += 1
                    if dyn_rule is not None:
                        self.memory.log_reuse(dyn_rule, "dyn", t)
                    risk += 1
                    if worst_rule is None:
                        worst_rule = dyn_rule
                    break
                if dv == 'free':
                    static_kind = sim['trap_map'].get((tx, ty))
                    enemy_near = any(
                        abs(ex - tx) + abs(ey - ty) <= 3 + k_to // 6
                        for (ex, ey) in sim.get('enemy_tiles', set()))
                    if static_kind is None and not enemy_near:
                        # a tile-occupancy law cannot prove the body's transit
                        # path is clear of thin/rotating geometry.  run the
                        # exact crossing sim, then skip only the heavier
                        # consequence/memory evaluation if no contact occurred.
                        self.memory.sims_run += 1
                        sim = self._simulate_tick(sim, dx, dy)
                        if sim.get('_transit_hit'):
                            risk += 1
                            if worst_rule is None:
                                worst_rule = dyn_rule
                            break
                        self.dynamics.answers += 1
                        if dyn_rule is not None:
                            self.memory.log_reuse(dyn_rule, "dyn", t)
                        sim['ptx'] = int(sim.get('px', sim['ptx']) + .5)
                        sim['pty'] = int(sim.get('py', sim['pty']) + .5)
                        if not sim.get('_arrived', True):
                            break
                        continue

            # ── memory-first (paper §iii-f step 6) ───────────────────────────
            # query memory before running the internal model simulation.
            # only reality-tested rules may answer (require_tested), and the
            # single specificity contest adjudicates innate vs learned rules.
            tile_fluents, event = self.ce._get_tile_fluents(dx, dy, tx, ty, sim)
            has_moving = any(f.name in ("MovingHazard", "DynamicHazard",
                                        "TrapActive", "TrapImminent",
                                        "TrapInactive", "PredictedCollision",
                                        "CollisionPath")
                             for f in tile_fluents)
            degrees = self.memory.calibration.degrees_for(
                sim.get('trap_map', {}).get((tx, ty))
                if isinstance(sim, dict) else None)
            if self.use_memory:
                is_dangerous, prior_rule = self.memory.query_outcome(
                    tile_fluents, event, self.ce.danger_thresh,
                    t=t, require_tested=True, degrees=degrees)
            else:
                # sim_only ablation
                is_dangerous, prior_rule = None, None
            # safe memory stale for moving traps — force fresh sim, unless
            # the rule is phase-anchored on trapinactive (see evaluate()).
            if (is_dangerous is False and prior_rule is not None
                    and (dynamic_scene or has_moving)
                    and _safe_verdict_is_stale_risky(prior_rule, tile_fluents)):
                self.memory.diag_safe_voided += 1
                is_dangerous, prior_rule = None, None
            if (dynamic_scene and is_dangerous is True and prior_rule is not None and
                    not _rule_has_specific_motion_context(prior_rule)):
                self.memory.diag_danger_voided += 1
                is_dangerous, prior_rule = None, None

            if is_dangerous is not None:
                # a chained multi-step threat upgrades a 'safe' direct verdict
                if is_dangerous is False and self.eec_reasoner.chained_danger(
                        tile_fluents, event):
                    is_dangerous, prior_rule = True, None
                # expectation memory answered this step — skip internal model
                if prior_rule is not None:
                    self.memory.log_reuse(prior_rule, "mem", t)
                self.memory.sims_skipped += 1
                if is_dangerous:
                    risk += 1
                    if worst_rule is None:
                        worst_rule = prior_rule
                    break
                sim['ptx'] += dx
                sim['pty'] += dy
                sim['px'] = sim['ptx']
                sim['py'] = sim['pty']
                # even when memory answered this step, advance the dynamic
                # objects if a fast-radius hazard is present (the expanding
                # spore ring moves ≈1.2 tiles/step), so it is in the right
                # place for the next step's evaluation.  other hazards move
                # slowly enough that the snapshot remains valid across a step,
                # so we skip this cost for them (keeps reuse high and fast).
                if dynamic_scene:
                    self._advance_sim_movers(sim)
                continue
            # ── no confident prior — run internal model (paper §iii-c) ───────
            if not self.use_sim:
                # no internal model for this mode — advance the lookahead
                # optimistically (treat the next tile as reachable and safe).
                sim['ptx'] += dx; sim['pty'] += dy
                sim['px'] = sim['ptx']; sim['py'] = sim['pty']
                continue
            self.memory.sims_run += 1
            sim    = self._simulate_tick(sim, dx, dy)
            arrived = sim.get('_arrived', True)
            eval_dx, eval_dy = (dx, dy) if arrived else (0, 0)
            danger, rule = self.ce.evaluate(eval_dx, eval_dy, sim)

            # transit hit: trap swept through target during the step_ticks window
            # even if it was gone by the snapshot endpoint.  form an expectation
            # from the world snapshot that best captures the ring's approach.
            if not danger and sim.get('_transit_hit'):
                danger = True
                self.memory.transit_hits += 1
                transit_kind = sim.get('_transit_kind')
                transit_enemy = sim.get('_transit_enemy', False)

                # for the expanding spore ring the endpoint sim has the ring at
                # a much larger radius than when the hit occurred (ring grows
                # ≈1.2 tiles/step), so _get_tile_fluents on the endpoint state
                # sees trapcontactlater or none rather than trapcontactsoon/now.
                # the formed rule then lacks contact timing — it becomes the
                # over-broad {expandingring, trapexpanding} → damaged pattern
                # that blocks all movement while the ring expands and only
                # accumulates violations once the ring is dormant.
                # fix: use the initial obs (ring at its planning-time position,
                # still approaching the target tile) so the formed rule correctly
                # captures trapcontactsoon/now as a required precondition.
                _use_initial_obs = (transit_kind == 'spore_burst')
                rule_obs = obs if _use_initial_obs else sim
                if transit_kind or transit_enemy:
                    rule_obs = dict(rule_obs)
                    rule_obs['trap_map'] = dict(rule_obs.get('trap_map', {}))
                    rule_obs['enemy_tiles'] = set(rule_obs.get('enemy_tiles', set()))
                    if transit_kind:
                        rule_obs['trap_map'][(tx, ty)] = transit_kind
                        rule_obs['kinetic_tiles'] = set(rule_obs.get('kinetic_tiles', set()))
                        rule_obs['kinetic_tiles'].add((tx, ty))
                    if transit_enemy:
                        rule_obs['enemy_tiles'].add((tx, ty))
                transit_sim = {
                    'tx': tx if arrived else sim['ptx'],
                    'ty': ty if arrived else sim['pty'],
                    'danger': True,
                    'trap_kind': transit_kind or sim['trap_map'].get((tx, ty)),
                    'enemy_near': transit_enemy or (tx, ty) in sim['enemy_tiles'],
                    'outcome_fluents': {Fluent("Damaged")},
                }
                rule = (self.ce._form_expectations(eval_dx, eval_dy,
                                                   transit_sim, rule_obs, t)
                        if self.use_memory else None)

            if danger:
                risk += 1
                if worst_rule is None:
                    worst_rule = rule
                break

            # player arrives at target tile after evaluation
            sim['ptx'] = int(sim.get('px', sim['ptx']) + .5)
            sim['pty'] = int(sim.get('py', sim['pty']) + .5)
            if not arrived:
                break

        result = (risk, worst_rule)
        if cache is not None:
            cache['route_risk'][cache_key] = result
        return result

    @staticmethod
    def _rebuild_sim_derived(sim: dict) -> None:
        """Recompute trap_map / enemy_tiles / kinetic_tiles / dtrap_activity
        from the CURRENT positions of the cloned dynamic objects."""
        dtrap_kinds = {dt.kind for dt in sim['_sim_dtraps']}
        new_trap_map = {tile: kind for tile, kind in sim['trap_map'].items()
                        if kind not in dtrap_kinds}
        for dt in sim['_sim_dtraps']:
            _map_dtrap_tiles(dt, new_trap_map)
        sim['trap_map'] = new_trap_map

        sim['enemy_tiles'] = _enemy_tiles_from_list(sim['_sim_enemies'])

        kinetic: set = set()
        kinetic_kinds = {dt.kind for dt in sim['_sim_dtraps']
                         if TRAP_SENSORS.get(dt.kind, {}).get('mov', False)}
        if kinetic_kinds:
            kinetic = {tile for tile, k in new_trap_map.items()
                       if k in kinetic_kinds}
        sim['kinetic_tiles'] = kinetic

        dtrap_activity: dict = {}
        dtrap_activity_by_tile: dict = {}
        for dt in sim['_sim_dtraps']:
            active, ticks = _dtrap_phase(dt)
            prev_a, prev_t = dtrap_activity.get(dt.kind, (False, 9999))
            if active or ticks < prev_t:
                dtrap_activity[dt.kind] = (active, ticks)
            tmp: dict = {}
            _map_dtrap_tiles(dt, tmp)
            for tile, tk in tmp.items():
                if tk != dt.kind:
                    continue
                prev = dtrap_activity_by_tile.get(tile)
                if prev is None or active or ticks < prev[2]:
                    dtrap_activity_by_tile[tile] = (dt.kind, active, ticks)
        sim['dtrap_activity'] = dtrap_activity
        sim['dtrap_activity_by_tile'] = dtrap_activity_by_tile

    def _lead_ticks(self) -> int:
        """Expected plan latency (world ticks) for the NEXT planning call —
        the time the Internal Model is told it has (feedback #1).  Estimated
        as ⌈EMA(rollout steps) / budget⌉; 0 when deliberation is synchronous."""
        if not self.WORLD_ASYNC_DELIBERATION:
            return 0
        est = -(-int(round(self._lead_ema)) // self.SIM_BUDGET_PER_TICK)
        return min(self.MAX_PLAN_LATENCY, max(0, est))

    def _make_sim_state(self, obs: dict) -> dict:
        """Clone the current world state for forward simulation.

        Dynamic traps and enemies are shallow-copied (sharing immutable
        room/grid references) so their update() methods can be called
        without affecting the real game objects.

        Latency anchoring (feedback #1): when deliberation costs world time,
        the chosen plan will only start EXECUTING ~_lead_ticks() from now.
        The clones are therefore advanced by that expected latency before the
        rollout begins, so predictions are made for the world the plan will
        actually meet — Winfield's internal model fed the time it has.
        """
        sim = {
            'ptx':            obs['ptx'],
            'pty':            obs['pty'],
            'px':             obs.get('px', obs['ptx']),
            'py':             obs.get('py', obs['pty']),
            'trap_map':       dict(obs.get('trap_map', {})),
            'enemy_tiles':    set(obs.get('enemy_tiles', set())),
            'kinetic_tiles':  set(obs.get('kinetic_tiles', set())),
            'dtrap_activity': dict(obs.get('dtrap_activity', {})),
            'dtrap_activity_by_tile': dict(obs.get('dtrap_activity_by_tile', {})),
            'player_statuses':dict(obs.get('player_statuses', {})),
            'pulse_spd_mod':  obs.get('pulse_spd_mod', 1.0),
            'hazard_pulse_active': obs.get('hazard_pulse_active', False),
            'hazard_pulse_kind': obs.get('hazard_pulse_kind', None),
            'room_of':        obs.get('room_of', {}),
            'sim_time':       obs.get('sim_time', 0),
            # use the full room lists captured in step() so the internal
            # model sees all threats regardless of the agent's current fov.
            # fov filtering stays in obs['dtraps'] / obs['enemies'] so the
            # perception-based expectation system is unaffected; only the
            # simulator gains visibility into traps behind the agent.
            '_sim_dtraps':    [_clone_dtrap(dt)
                               for dt in getattr(self, '_room_dtraps',
                                                  obs.get('dtraps', []))],
            '_sim_enemies':   [_clone_enemy(e)
                               for e  in getattr(self, '_room_enemies',
                                                  obs.get('enemies', []))],
        }
        # rebuild trap_map immediately from all sim dtraps so the very
        # first planning step sees invisible traps' tile positions too.
        # without this, step-0 memory/evaluation queries use the obs
        # trap_map (fov-limited) until _simulate_tick's rebuild fires.
        if sim['_sim_dtraps'] or sim['_sim_enemies']:
            self._rebuild_sim_derived(sim)
        lead = self._lead_ticks()
        if lead and (sim['_sim_dtraps'] or sim['_sim_enemies']):
            stub = _SimPlayer(sim['px'], sim['py'])
            stub.pulse_spd_mod = sim.get('pulse_spd_mod', 1.0)
            for _ in range(lead):
                for dt in sim['_sim_dtraps']:
                    _sim_update_dtrap(dt, stub)
                for e in sim['_sim_enemies']:
                    _sim_update_enemy(e)
            self._rebuild_sim_derived(sim)
        sim['lead_ticks'] = lead
        return sim

    def _simulate_tick(self, sim: dict, dx: int, dy: int) -> dict:
        """Advance the cloned world state by one agent step (STEP_TICKS game ticks).

        The player is NOT moved here — caller moves sim['ptx'/'pty'] after
        evaluating the target tile.  This keeps evaluate(dx,dy,sim) pointing
        at the correct tile (ptx+dx, pty+dy), not two steps ahead.

        Also samples 5 evenly-spaced sub-ticks to catch traps that sweep
        through the target tile mid-transit without being there at the endpoint.
        """
        # target tile (player not moved yet)
        tx, ty = sim['ptx'] + dx, sim['pty'] + dy
        stub   = _SimPlayer(sim.get('px', sim['ptx']), sim.get('py', sim['pty']))
        stub.pulse_spd_mod = sim.get('pulse_spd_mod', 1.0)

        # move the simulated body with the same speed/collision rules as the
        # real player. older rollouts interpolated all the way to the target in
        # exactly step_ticks frames, which was optimistic under slow/status
        # effects and when gravity-like traps displaced the body.
        start_x, start_y = sim.get('px', sim['ptx']), sim.get('py', sim['pty'])
        target_x, target_y = tx, ty
        pulse_mod = sim.get('pulse_spd_mod', 1.0)
        if sim.get('hazard_pulse_active') and sim.get('hazard_pulse_kind') == 'speed':
            pulse_mod = min(pulse_mod, 0.5)
        spd = _sim_player_speed(sim.get('player_statuses', {}), pulse_mod)
        move_dx = target_x - start_x
        move_dy = target_y - start_y

        # when dx=dy=0 the route target is the current tile — the intent is
        # "player holds position; do traps sweep through where they stand?"
        # allowing move_dx/dy to be non-zero here causes the body to drift
        # toward tile center and then overshoot by up to ~0.9 tiles in the
        # opposite direction over step_ticks ticks, registering false transit
        # hits for traps that were never actually in the player's path and
        # mispointing seeking traps at the wrong target position.
        # the real player holds perfectly still when no keys are pressed, so
        # the sim should do the same.
        if dx == 0 and dy == 0:
            move_dx = 0.0
            move_dy = 0.0

        transit_hit = False
        transit_kind = None
        transit_enemy = False

        for tick_i in range(self.STEP_TICKS):
            stub.x, stub.y = _sim_move_body(
                stub.x, stub.y, move_dx, move_dy, spd, self.grid)

            for dt in sim['_sim_dtraps']:
                _sim_update_dtrap(dt, stub)
            for e in sim['_sim_enemies']:
                _sim_update_enemy(e)

            # check whether the player's moving body intersects exact hazard
            # geometry.  this catches thin rotating fire bars/beams and enemies
            # crossing between rounded tile centers.
            if not transit_hit:
                for dt in sim['_sim_dtraps']:
                    if _dtrap_hits_point(dt, stub.x, stub.y):
                        transit_hit = True
                        transit_kind = dt.kind
                        break
                if not transit_hit:
                    for e in sim['_sim_enemies']:
                        if _enemy_hits_point(e, stub.x, stub.y):
                            transit_hit = True
                            transit_enemy = True
                            break

            # fall back to occupancy checks for broad area hazards that are
            # naturally represented as tiles or bands.
            if not transit_hit:
                tmp_map: dict = {}
                for dt in sim['_sim_dtraps']:
                    _map_dtrap_tiles(dt, tmp_map)
                tmp_enemies = _enemy_tiles_from_list(sim['_sim_enemies'])
                # tiles to check: the player's interpolated body tile plus the
                # source/target only while the body still overlaps them.  keeping
                # the source tile "occupied" for the whole step made every escape
                # from an incoming sweeper look dangerous, so the agent could
                # freeze in the path it was trying to leave.
                src_tile  = (sim['ptx'], sim['pty'])
                tgt_tile  = (tx, ty)
                stub_tile = (int(stub.x + 0.5), int(stub.y + 0.5))
                check_tiles = [stub_tile]
                if math.hypot(stub.x - start_x, stub.y - start_y) <= 0.40:
                    check_tiles.append(src_tile)
                if math.hypot(stub.x - target_x, stub.y - target_y) <= 0.40:
                    check_tiles.append(tgt_tile)
                for chk in check_tiles:
                    kind = tmp_map.get(chk)
                    if kind:
                        transit_hit = True
                        transit_kind = kind
                        break
                    if chk in tmp_enemies:
                        transit_hit = True
                        transit_enemy = True
                        break

        self._rebuild_sim_derived(sim)

        sim['player_statuses'] = {
            k: v - self.STEP_TICKS
            for k, v in sim.get('player_statuses', {}).items()
            if v > self.STEP_TICKS}

        # trap/enemy swept through target mid-transit
        sim['_transit_hit'] = transit_hit
        sim['_transit_kind'] = transit_kind
        sim['_transit_enemy'] = transit_enemy
        sim['px'] = stub.x
        sim['py'] = stub.y
        sim['_arrived'] = (int(stub.x + .5), int(stub.y + .5)) == (tx, ty)
        return sim

    def _first_step(self, route: list, ptx: int, pty: int):
        if not route:
            return None
        tx, ty = route[0]
        action = (tx - ptx, ty - pty)
        if action not in self.DIRS:
            return None
        return action

    def _reflex_threat(self, obs) -> bool:
        """Innate, zero-deliberation threat check on the CURRENT tile.

        Used to interrupt deliberation (feedback #1): standing still to think
        is only permitted while the ground underfoot, or the body point the
        player is actually occupying between tile centres, is not obviously
        about to kill the agent.
        """
        pt = (obs['ptx'], obs['pty'])
        if pt in obs.get('enemy_tiles', set()):
            return True
        if self._body_enemy_contact_soon(obs, ticks=self.STEP_TICKS):
            return True
        if self._body_dtrap_contact_soon(obs, ticks=self.STEP_TICKS):
            return True
        if pt in obs.get('kinetic_tiles', set()):
            return True
        kind = obs.get('trap_map', {}).get(pt)
        if kind:
            act = obs.get('dtrap_activity', {}).get(kind)
            if act is None:
                # static hazard underfoot
                return True
            active, ticks = act
            return active or ticks <= self.STEP_TICKS
        return False


    def _avoidant_action(self, obs):
        """Baseline agent (feedback #2): greedily maximise distance from all
        visible hazards with a mild drift toward the exit.  No simulation, no
        expectations — the maze analogue of the paper's Avoidant chess agent.
        """
        ptx, pty = obs['ptx'], obs['pty']
        hazards = set(obs.get('trap_map', {})) | set(obs.get('enemy_tiles', set()))
        ex, ey = self.end
        best = None
        for dx, dy in self.DIRS + [(0, 0)]:
            tx, ty = ptx + dx, pty + dy
            if self._blocked_for_planning(tx, ty):
                continue
            mind = (min(abs(tx-hx) + abs(ty-hy) for hx, hy in hazards)
                    if hazards else 99)
            score = (-mind
                     + (abs(tx-ex) + abs(ty-ey)) * 0.05
                     + self._visit_counts.get((tx, ty), 0) * 0.2)
            if best is None or score < best[0]:
                best = (score, (dx, dy))
        if best is None or best[1] == (0, 0):
            return None, None
        self.last_action = best[1]
        return best[1], None

    def _panic_move(self, obs):
        """Emergency move when all planned routes look dangerous.

        Picks the adjacent walkable tile with the lowest combined score.
        DANGER DOMINATES: any safe tile is preferred over any dangerous tile,
        regardless of goal distance — this is a one-hit-kill game.
        Tie-breakers: fewer revisits, then proximity to goal.
        """
        ptx, pty  = obs['ptx'], obs['pty']
        ex,  ey   = self.end
        best      = None
        best_rule = None
        for dx, dy in self.DIRS:
            tx, ty = ptx+dx, pty+dy
            if self._blocked_for_planning(tx, ty):
                continue
            danger, rule = self._one_step_danger((dx, dy), obs)
            visits    = self._visit_counts.get((tx, ty), 0)
            goal_dist = abs(tx - ex) + abs(ty - ey)
            # danger weight (1000) > any possible visit/distance contribution
            # so a safe tile always beats a dangerous one regardless of position.
            score = (1000 if danger else 0) + visits * 0.5 + goal_dist * 0.02
            if best is None or score < best[0]:
                best      = (score, dx, dy)
                best_rule = rule
        if best is None:
            return None, None
        return (best[1], best[2]), best_rule

    def _find_earliest_safe_window(self, obs, max_steps=None):
        """Simulate the world forward (player stationary) to find the soonest
        agent step at which an adjacent tile opens a TRANSIT-VERIFIED safe passage.

        Called when every immediate neighbour is blocked by a dynamic hazard.
        Instead of waiting blindly or forcing a guaranteed-damage move, the
        agent predicts WHEN a gap will appear and which direction it opens in,
        then commits to waiting exactly that many steps.

        max_steps=16 gives 160-game-tick lookahead — enough to find combined
        windows for two traps with periods up to ~80 ticks each.

        Each candidate is verified with _simulate_tick (sub-pixel transit check)
        so the predicted window is guaranteed to pass the _one_step_danger
        verification at countdown time.  The old tile-map-only check could
        disagree with the sub-pixel check, causing a repeated fail→replan cycle.

        Returns (direction, steps_to_wait) or (None, max_steps+1) if no window
        is found within the look-ahead horizon.
        """
        if max_steps is None:
            max_steps = self.WINDOW_MAX_STEPS
        if not self._has_dynamic_threats(obs):
            return None, max_steps + 1

        sim      = self._make_sim_state(obs)
        ex, ey   = self.end

        for wait_step in range(1, max_steps + 1):
            # advance dynamic traps and enemies by one agent step (step_ticks
            # game ticks); the simulated player does not move — they are waiting.
            if not self._advance_wait_step_safe(sim):
                return None, max_steps + 1

            # collect candidates that pass the coarse tile-map filter first
            # (cheap), then verify each with _simulate_tick (sub-pixel transit
            # check identical to _one_step_danger) so windows that will be
            # rejected at countdown time are never committed to.
            best_dir   = None
            best_score = float('inf')
            for dx, dy in self.DIRS:
                tx, ty = sim['ptx'] + dx, sim['pty'] + dy
                if self._blocked_for_planning(tx, ty):
                    continue
                # coarse filter: tile must not be in trap_map or enemy_tiles
                if ((tx, ty) in sim['trap_map']
                        or (tx, ty) in sim.get('enemy_tiles', set())):
                    continue
                # transit verification: clone the current sim and simulate the
                # actual crossing so sub-pixel traps that straddle the tile
                # boundary are correctly detected.  this matches exactly what
                # _one_step_danger will do when the countdown expires.
                sim_check = {k: v for k, v in sim.items()
                             if k not in ('_sim_dtraps', '_sim_enemies')}
                sim_check['_sim_dtraps']  = [_clone_dtrap(dt)
                                              for dt in sim['_sim_dtraps']]
                sim_check['_sim_enemies'] = [_clone_enemy(e)
                                             for e in sim['_sim_enemies']]
                checked = self._simulate_tick(sim_check, dx, dy)
                if checked.get('_transit_hit'):
                    # sub-pixel check says still blocked — skip
                    continue
                visits     = self._visit_counts.get((tx, ty), 0)
                goal_dist  = abs(tx - ex) + abs(ty - ey)
                score      = visits * 0.5 + goal_dist * 0.02
                if score < best_score:
                    best_score = score
                    best_dir   = (dx, dy)

            if best_dir is not None:
                return best_dir, wait_step

        return None, max_steps + 1


    # ── 7. expectation update (real-world feedback) ───────────────────────────
    def _clone_sim_for_check(self, sim: dict) -> dict:
        sim_check = {k: v for k, v in sim.items()
                     if k not in ('_sim_dtraps', '_sim_enemies')}
        sim_check['_sim_dtraps'] = [_clone_dtrap(dt)
                                    for dt in sim.get('_sim_dtraps', [])]
        sim_check['_sim_enemies'] = [_clone_enemy(e)
                                     for e in sim.get('_sim_enemies', [])]
        return sim_check

    def _advance_wait_step(self, sim: dict) -> None:
        stub = _SimPlayer(sim.get('px', sim['ptx']), sim.get('py', sim['pty']))
        stub.pulse_spd_mod = sim.get('pulse_spd_mod', 1.0)
        for _ in range(self.STEP_TICKS):
            for dt in sim['_sim_dtraps']:
                _sim_update_dtrap(dt, stub)
            for e in sim['_sim_enemies']:
                _sim_update_enemy(e)
        self._rebuild_sim_derived(sim)

    def _advance_wait_step_safe(self, sim: dict) -> bool:
        """Advance one stationary agent step and report whether the body lives."""
        stub = _SimPlayer(sim.get('px', sim['ptx']), sim.get('py', sim['pty']))
        stub.pulse_spd_mod = sim.get('pulse_spd_mod', 1.0)
        safe = True
        for _ in range(self.STEP_TICKS):
            for dt in sim['_sim_dtraps']:
                _sim_update_dtrap(dt, stub)
            for e in sim['_sim_enemies']:
                _sim_update_enemy(e)
            if safe:
                for dt in sim['_sim_dtraps']:
                    if _dtrap_hits_point(dt, stub.x, stub.y):
                        safe = False
                        break
                if safe:
                    for e in sim['_sim_enemies']:
                        if _enemy_hits_point(e, stub.x, stub.y):
                            safe = False
                            break
        self._rebuild_sim_derived(sim)
        return safe

    def _sim_route_clear(self, sim: dict, route: list) -> bool:
        sim = self._clone_sim_for_check(sim)
        for tx, ty in route:
            dx = tx - sim['ptx']
            dy = ty - sim['pty']
            if abs(dx) + abs(dy) != 1:
                return False
            sim = self._simulate_tick(sim, dx, dy)
            # non-arrival (body short of tile centre after one step) is a timing
            # artifact when starting off-centre, not a hazard — evaluate the
            # move itself and gate only on real danger / transit collision.
            danger, _ = self.ce.evaluate(dx, dy, sim)
            if danger or sim.get('_transit_hit'):
                return False
            sim['ptx'] = int(sim.get('px', sim['ptx']) + .5)
            sim['pty'] = int(sim.get('py', sim['pty']) + .5)
        return True

    def _sim_route_end_state(self, sim: dict, route: list) -> dict | None:
        """Return the simulated state after a clear route prefix, else None."""
        sim = self._clone_sim_for_check(sim)
        for tx, ty in route:
            dx = tx - sim['ptx']
            dy = ty - sim['pty']
            if abs(dx) + abs(dy) != 1:
                return None
            sim = self._simulate_tick(sim, dx, dy)
            danger, _ = self.ce.evaluate(dx, dy, sim)
            if danger or sim.get('_transit_hit'):
                return None
            sim['ptx'] = int(sim.get('px', sim['ptx']) + .5)
            sim['pty'] = int(sim.get('py', sim['pty']) + .5)
            if not sim.get('_arrived', True):
                return None
        return sim

    def _sim_hold_clear(self, sim: dict, ticks: int) -> bool:
        """Exact internal-model check for waiting on the current body point."""
        sim = self._clone_sim_for_check(sim)
        stub = _SimPlayer(sim.get('px', sim['ptx']), sim.get('py', sim['pty']))
        stub.pulse_spd_mod = sim.get('pulse_spd_mod', 1.0)
        for _ in range(max(0, ticks)):
            for dt in sim.get('_sim_dtraps', []):
                _sim_update_dtrap(dt, stub)
            for e in sim.get('_sim_enemies', []):
                _sim_update_enemy(e)
            for dt in sim.get('_sim_dtraps', []):
                if _dtrap_hits_point(dt, stub.x, stub.y):
                    return False
            for e in sim.get('_sim_enemies', []):
                if _enemy_hits_point(e, stub.x, stub.y):
                    return False
        return True

    def _rotator_clearance(self, tx: int, ty: int) -> float:
        """Positive when a tile is outside nearby spinner reach."""
        clear = 99.0
        for dt in getattr(self, '_room_dtraps', []):
            if dt.kind == 'fire_bar':
                reach = getattr(dt, 'arm_len', 2.0) + PLAYER_HIT_RADIUS + THIN_HAZARD_HALF_WIDTH
                clear = min(clear, math.hypot(tx - dt.ox, ty - dt.oy) - reach)
            elif dt.kind == 'ice_beam':
                reach = getattr(dt, 'beam_len', 2.0) + PLAYER_HIT_RADIUS + THIN_HAZARD_HALF_WIDTH
                clear = min(clear, math.hypot(tx - dt.ox, ty - dt.oy) - reach)
            elif dt.kind == 'pendulum_axe':
                reach = getattr(dt, 'arm_len', 2.0) + PLAYER_HIT_RADIUS + THIN_HAZARD_HALF_WIDTH
                clear = min(clear, math.hypot(tx - dt.pivot_x, ty - dt.pivot_y) - reach)
        return clear

    def _safe_staging_step_for_wait(self, obs: dict, wait_ticks: int):
        """Move out of a spinner's future sweep instead of waiting inside it.

        The crossing/window planner may correctly find that the doorway opens
        in a few ticks, but the *staging* tile itself can be inside a rotating
        hazard's reach.  Waiting there is only safe for the current instant,
        not for the planned wait.  Simulate the hold; if it fails, pick an
        adjacent tile whose move and remaining hold both survive.
        """
        if wait_ticks <= 0 or not self._has_dynamic_threats(obs):
            return None
        horizon = min(wait_ticks, self.WINDOW_RELIABLE_STEPS * self.STEP_TICKS)
        base = self._make_sim_state(obs)
        if self._sim_hold_clear(base, horizon):
            return None

        ptx, pty = obs['ptx'], obs['pty']
        ex, ey = self.end
        best = None
        for dx, dy in self.DIRS:
            tx, ty = ptx + dx, pty + dy
            if not self._valid_step((dx, dy), ptx, pty):
                continue
            sim_step = self._clone_sim_for_check(base)
            sim_step = self._simulate_tick(sim_step, dx, dy)
            danger, rule = self.ce.evaluate(dx, dy, sim_step)
            if danger or sim_step.get('_transit_hit'):
                continue
            sim_step['ptx'] = int(sim_step.get('px', sim_step['ptx']) + .5)
            sim_step['pty'] = int(sim_step.get('py', sim_step['pty']) + .5)
            remaining = max(0, horizon - self.STEP_TICKS)
            if not self._sim_hold_clear(sim_step, remaining):
                continue
            visits = self._visit_counts.get((tx, ty), 0)
            goal_dist = abs(tx - ex) + abs(ty - ey)
            clearance = self._rotator_clearance(tx, ty)
            score = (-clearance, goal_dist * 0.03, visits)
            if best is None or score < best[0]:
                best = (score, (dx, dy), rule)
        if best is None:
            return None
        return best[1], best[2]

    def _best_timed_entry_plan(self, obs: dict, routes: list):
        """Choose a room-entry route by simulating timing windows.

        Dijkstra's instantaneous cost can flicker at room mouths because moving
        hazards alter the visible map every tick.  For dynamic rooms, compare
        several route prefixes with the Internal Model and commit to the prefix
        whose future crossing window is best, rather than repeatedly adopting
        whichever route is cheapest in this single snapshot.
        """
        if not routes or not self._has_dynamic_threats(obs) or not self._wait_is_safe(obs):
            return None
        ex, ey = self.end
        best = None
        seen = set()
        for route in routes:
            if not route:
                continue
            seed = (self._timed_dynamic_crossing_route(obs, route)
                    or self._rotating_crossing_route(obs, route)
                    or route[:min(len(route), 3)])
            if not seed:
                continue
            seed = seed[:min(len(seed), 3)]
            key = tuple(seed)
            if key in seen:
                continue
            seen.add(key)
            crossing, wait_steps = self._find_crossing_window(seed, obs)
            if crossing is None:
                continue
            first = self._first_step(crossing, obs['ptx'], obs['pty'])
            if first is None or not self._valid_step(first, obs['ptx'], obs['pty']):
                continue
            end_tx, end_ty = crossing[-1]
            progress = abs(end_tx - ex) + abs(end_ty - ey)
            visits = sum(self._visit_counts.get(t, 0) for t in crossing)
            switch_penalty = 0.0
            if self._entry_lock_dir is not None and first != self._entry_lock_dir:
                # strong hysteresis while a room-entry decision is still live:
                # keep the sim-chosen doorway option until its own safe window
                # disappears. otherwise equally plausible paths can steal the
                # plan every tick as moving hazards alter instantaneous costs.
                switch_penalty = (self.WINDOW_MAX_STEPS + 2
                                  if self._entry_lock_ticks > 0 else 2.0)
            score = (wait_steps + switch_penalty, progress * 0.03, visits * 0.2, len(crossing))
            if best is None or score < best[0]:
                best = (score, list(crossing), wait_steps, first)
        if best is None:
            return None
        _, crossing, wait_steps, first = best
        return crossing, wait_steps, first

    def _rotating_crossing_route(self, obs, goal_route: list) -> list:
        """Return the short route needed to pass through a spinner's radius."""
        if not goal_route:
            return []
        rotators = [dt for dt in getattr(self, '_room_dtraps', [])
                    if dt.kind in ('fire_bar', 'ice_beam')]
        if not rotators:
            return []

        best = None
        best_dist = float('inf')
        scan = [(obs['ptx'], obs['pty'])] + goal_route[:6]
        for dt in rotators:
            reach = getattr(dt, 'arm_len', getattr(dt, 'beam_len', 2.0)) + 0.70
            for tx, ty in scan:
                dist = math.hypot(tx - dt.ox, ty - dt.oy)
                if dist <= reach and dist < best_dist:
                    best = (dt, reach)
                    best_dist = dist
        if best is None:
            return []

        dt, reach = best
        crossing = []
        entered = math.hypot(obs['ptx'] - dt.ox, obs['pty'] - dt.oy) <= reach
        for tx, ty in goal_route[:6]:
            dist = math.hypot(tx - dt.ox, ty - dt.oy)
            if dist <= reach:
                entered = True
            if entered:
                crossing.append((tx, ty))
                if dist > reach and len(crossing) >= 2:
                    break
        return crossing if len(crossing) >= 2 else []

    def _timed_dynamic_crossing_route(self, obs, goal_route: list) -> list:
        """Return a short route segment that needs timing through moving traps.

        Instead of treating moving hazards as only "occupied now", forecast the
        tiles they sweep over the next timing window. If the goal route enters
        that swept band soon, commit to the whole contested segment once a
        verified safe window opens.
        """
        if not goal_route or not self._has_dynamic_threats(obs):
            return []

        sim = self._make_sim_state(obs)
        swept_tiles: set = set()
        for _ in range(self.WINDOW_MAX_STEPS + 1):
            tmp: dict = {}
            for dt in sim.get('_sim_dtraps', []):
                if TRAP_SENSORS.get(dt.kind, {}).get('mov', False):
                    _map_dtrap_tiles(dt, tmp)
            swept_tiles.update(tmp)
            self._advance_wait_step(sim)

        if not swept_tiles:
            return []

        first = None
        last = None
        for i, tile in enumerate(goal_route[:self.GOAL_HORIZON + 2]):
            if tile in swept_tiles:
                if first is None:
                    first = i
                last = i

        if first is None or first > 2:
            return []

        # include the approach tile(s) and one exit tile after the swept band.
        # the exact simulator will reject this route if any step is unsafe for
        # the selected timing, so this can stay intentionally broad.
        end_i = min(len(goal_route), last + 2)
        route = goal_route[:end_i]
        return route if len(route) >= 2 else []

    def _spinner_escape_dash(self, obs: dict, max_wait: int = 80,
                             dash_tiles: int = 4):
        """Escape a rotating-arm corner by TIMING a dash out of the reach annulus.

        Engaged when the current tile is about to be swept by a fire_bar /
        ice_beam / pendulum AND holding is unsafe (so every wait-gated planner
        is skipped).  Unlike the enemy corridor dash, this does NOT require
        holding to be safe — waiting is the lethal option in a wall pocket on
        the arm's edge.  For each candidate escape corridor it rolls the arm
        forward and, at each launch tick, simulates the BODY ACTUALLY MOVING
        along the dash (not held), accepting the first launch where the whole
        crossing stays clear and the endpoint sits OUTSIDE the arm's reach.
        Returns (wait_ticks, dash_route, first_dir) or None.
        """
        if not self._rotating_hazard_near(obs):
            return None
        # restrict to pivot spinners (bounded reach annulus).  room-wide sweeps
        # (lava_tide / ice_sweeper) have no origin-radius clearance and are owned
        # by _sweep_evasion_step; _rotator_clearance returns +inf for them, which
        # would make this planner trim every dash to one tile and mis-escape.
        pivots = [dt for dt in getattr(self, '_room_dtraps', [])
                  if dt.kind in ('fire_bar', 'ice_beam', 'pendulum_axe')]
        if not pivots:
            return None
        ptx, pty = obs['ptx'], obs['pty']
        ex, ey = self.end
        base = self._make_sim_state(obs)

        # build candidate dash corridors: each cardinal direction extended as a
        # straight walkable run, plus the goal-ward dijkstra prefix.  a straight
        # run is the fastest way out of a circular reach annulus.
        candidates = []
        for dx, dy in self.DIRS:
            run = []
            cx, cy = ptx, pty
            for _ in range(dash_tiles):
                nx, ny = cx + dx, cy + dy
                if not self._valid_step((dx, dy), cx, cy):
                    break
                run.append((nx, ny))
                cx, cy = nx, ny
            if run:
                candidates.append(run)
        goal = self._dijkstra_route(ptx, pty, obs, penalize=frozenset())
        if goal:
            prefix = []
            cx, cy = ptx, pty
            for (nx, ny) in goal[:dash_tiles]:
                if abs(nx - cx) + abs(ny - cy) != 1:
                    break
                prefix.append((nx, ny))
                cx, cy = nx, ny
            if prefix:
                candidates.append(prefix)

        # trim each candidate so it ends just outside the arm's reach: that is
        # the whole objective — leave the annulus and stop, not barrel deeper.
        trimmed = []
        seen = set()
        for run in candidates:
            cut = []
            for (tx, ty) in run:
                cut.append((tx, ty))
                if self._rotator_clearance(tx, ty) > 0.30:
                    # reached safe ground — stop the dash here
                    break
            key = tuple(cut)
            if cut and key not in seen:
                seen.add(key)
                trimmed.append(cut)
        if not trimmed:
            return None

        # (cost_tuple, wait_ticks, dash_route, first_dir)
        best = None
        for dash in trimmed:
            end_clear = self._rotator_clearance(*dash[-1])
            # only consider corridors that actually reach (near-)clear ground;
            # a dash that ends still deep inside the reach is not an escape.
            if end_clear <= -0.50:
                continue
            for wait in range(0, max_wait + 1):
                cross = self._clone_sim_for_check(base)
                cross['ptx'], cross['pty'] = ptx, pty
                cross['px'], cross['py'] = float(ptx), float(pty)
                # advance the world `wait` ticks with the body held in place.
                stub = _SimPlayer(float(ptx), float(pty))
                stub.pulse_spd_mod = cross.get('pulse_spd_mod', 1.0)
                for _ in range(wait):
                    for dt in cross.get('_sim_dtraps', []):
                        _sim_update_dtrap(dt, stub)
                    for e in cross.get('_sim_enemies', []):
                        _sim_update_enemy(e)
                self._rebuild_sim_derived(cross)
                # now simulate the moving dash from this future world state.
                clear = True
                for (nx, ny) in dash:
                    d = (nx - cross['ptx'], ny - cross['pty'])
                    if d not in self.DIRS:
                        clear = False
                        break
                    cross = self._simulate_tick(cross, d[0], d[1])
                    if cross.get('_transit_hit') or not cross.get('_arrived', True):
                        clear = False
                        break
                    cross['ptx'] = int(cross.get('px', cross['ptx']) + .5)
                    cross['pty'] = int(cross.get('py', cross['pty']) + .5)
                if not clear:
                    continue
                first = (dash[0][0] - ptx, dash[0][1] - pty)
                goal_dist = abs(dash[-1][0] - ex) + abs(dash[-1][1] - ey)
                # prefer: launch soonest, end furthest outside reach, then
                # closest to the exit.  exposure (wait) dominates — every waited
                # tick is spent in a lethal pocket.
                cost = (wait, -round(end_clear, 2), goal_dist, len(dash))
                if best is None or cost < best[0]:
                    best = (cost, wait * self.STEP_TICKS, list(dash), first)
                # earliest viable launch for this corridor found
                break
        if best is None:
            return None
        _, wait_ticks, dash_route, first = best
        return wait_ticks, dash_route, first

    def _corridor_dash_plan(self, obs: dict, route: list,
                            max_wait: int = 80, dash_tiles: int = 3):
        """Find the earliest future moment to dash through an enemy-blocked
        corridor prefix, and return (wait_ticks, dash_route).

        The dominant terminal stall is a wandering enemy sitting in the only
        goal-ward corridor: every step toward the exit collides with it, so the
        agent bounces one tile short forever.  Pure avoidance cannot solve this
        because the corridor is the only way through — the agent must TIME a
        dash for when the wanderer has drifted clear, exactly as it already does
        for cycling traps.  This rolls the world forward tick by tick; at each
        future tick it asks "if I committed the next `dash_tiles` route tiles
        starting now, would my moving body stay clear of every enemy for the
        whole crossing?"  The first tick where that holds is the launch window.

        Returns None when the corridor never clears within `max_wait` ticks (the
        caller then falls back to its bounded-risk escape), or when holding here
        is not safe (a different guard owns that case).
        """
        if not route or not self._has_dynamic_threats(obs):
            return None
        if not self._wait_is_safe(obs):
            return None
        ptx, pty = obs['ptx'], obs['pty']
        # build the candidate dash: the route prefix that stays cardinally
        # adjacent and walkable.  stop at the first non-unit step.
        prefix = []
        cx, cy = ptx, pty
        for (nx, ny) in route:
            if abs(nx - cx) + abs(ny - cy) != 1:
                break
            d = (nx - cx, ny - cy)
            if d not in self.DIRS or not self._valid_step(d, cx, cy):
                break
            prefix.append((nx, ny))
            cx, cy = nx, ny
            if len(prefix) >= dash_tiles:
                break
        if not prefix:
            return None

        base = self._make_sim_state(obs)
        # advance a wait-stub each tick (body holds at the launch tile), then
        # test a full simulated crossing of the prefix from that future state.
        for wait in range(0, max_wait + 1):
            # snapshot the world `wait` ticks from now.
            probe = self._clone_sim_for_check(base)
            probe['ptx'], probe['pty'] = ptx, pty
            probe['px'], probe['py'] = float(ptx), float(pty)
            ok_hold = True
            for _ in range(wait):
                if not self._advance_wait_step_safe(probe):
                    ok_hold = False
                    break
            if not ok_hold:
                # cannot even hold this long → no point waiting further
                break
            # now simulate dashing the prefix from the waited state.
            cross = self._clone_sim_for_check(probe)
            cross['ptx'], cross['pty'] = ptx, pty
            cross['px'], cross['py'] = float(ptx), float(pty)
            clear = True
            for (nx, ny) in prefix:
                d = (nx - cross['ptx'], ny - cross['pty'])
                cross = self._simulate_tick(cross, d[0], d[1])
                if cross.get('_transit_hit') or not cross.get('_arrived', True):
                    clear = False
                    break
                cross['ptx'] = int(cross.get('px', cross['ptx']) + .5)
                cross['pty'] = int(cross.get('py', cross['pty']) + .5)
            if clear:
                return wait * self.STEP_TICKS, list(prefix)
        return None

    def _find_crossing_window(self, route: list, obs, max_steps=None) -> tuple:
        if max_steps is None:
            max_steps = self.WINDOW_MAX_STEPS
        if not route or not self._has_dynamic_threats(obs):
            return None, max_steps + 1

        sim = self._make_sim_state(obs)
        for wait_step in range(0, max_steps + 1):
            if wait_step > 0:
                if not self._advance_wait_step_safe(sim):
                    return None, max_steps + 1
            if self._sim_route_clear(sim, route):
                return route, wait_step
        return None, max_steps + 1

    def _observed_feedback_rule(self, obs: dict, took_damage: bool,
                                t: int = 0) -> EECTemporalRule:
        """Create an EEC rule from the real observed post-action outcome.

        confirmations=1: this rule comes directly from a real-world
        observation, so it is born reality-tested and may immediately
        participate in memory-first simulation skipping.
        """
        ptx, pty = obs['ptx'], obs['pty']
        kind = obs['trap_map'].get((ptx, pty))
        enemy_now = (ptx, pty) in obs['enemy_tiles']

        sensor_f = tile_sensor_fluents(
            kind, (ptx, pty) in obs.get('kinetic_tiles', set()))
        precond = [f for f in sensor_f if f.name != 'HazardPresent']
        if kind:
            if TRAP_SENSORS.get(kind, {}).get('mov', False):
                precond.append(Fluent("DynamicHazard"))
            else:
                precond.append(Fluent("StaticHazard"))

        if kind and TRAP_SENSORS.get(kind, {}).get('mov', False):
            active, ticks = obs.get('dtrap_activity', {}).get(kind, (True, 0))
            if active:
                precond.append(Fluent("TrapActive"))
            elif ticks <= self.STEP_TICKS:
                precond.append(Fluent("TrapImminent"))
            else:
                precond.append(Fluent("TrapInactive"))

        if enemy_now:
            precond.append(Fluent("EnemyNearby"))
        if ((ptx, pty) in obs.get('kinetic_tiles', set()) or
                (ptx, pty) in obs.get('enemy_tiles', set())):
            precond.append(Fluent("PredictedCollision"))

        rm = self.room_of.get((ptx, pty))
        if rm is not None:
            precond.append(Fluent("Room", (rm.rtype,)))

        if not precond:
            precond = [Fluent("HazardPresent") if took_damage else Fluent("Clear")]

        precond = tuple(sorted(set(precond), key=lambda f: (f.name, f.args)))
        # causal screening: drop fluents the ledger has refuted as irrelevant
        # to this outcome, so surprise rules are born causal, not correlational.
        screened = self.memory.causal.screen(
            precond, 'Damaged' if took_damage else 'Safe')
        if screened:
            if len(screened) < len(precond):
                self.memory.preconds_dropped += len(precond) - len(screened)
            precond = screened
        return EECTemporalRule(
            event=Event("Move"),
            preconditions=precond,
            effect_type="Initiates",
            effect=Fluent("Damaged" if took_damage else "Safe"),
            delay=1,
            confidence=C_INIT_SURPRISE,  # elevated prior — eq. 1 with popperian bias
            confirmations=1,
            last_observed_time=t)

    def _feedback_rule_from_precontext(self, pre_fluents: set,
                                       took_damage: bool,
                                       t: int = 0) -> EECTemporalRule:
        """Create a surprise rule from the exact context before the action."""
        _SKIP_PRE = {'ClearAhead', 'Safe', 'Damaged', 'NoStatus'}
        precond = tuple(sorted(
            (f for f in pre_fluents if f.name not in _SKIP_PRE),
            key=lambda f: (f.name, f.args)))
        if not precond:
            precond = (Fluent("HazardPresent") if took_damage else Fluent("Clear"),)
        screened = self.memory.causal.screen(
            precond, 'Damaged' if took_damage else 'Safe')
        if screened:
            if len(screened) < len(precond):
                self.memory.preconds_dropped += len(precond) - len(screened)
            precond = screened
        return EECTemporalRule(
            event=Event("Move"),
            preconditions=precond,
            effect_type="Initiates",
            effect=Fluent("Damaged" if took_damage else "Safe"),
            delay=1,
            confidence=C_INIT_SURPRISE,
            confirmations=1,
            last_observed_time=t)

    def _after_fluents(self, obs: dict | None, took_damage: bool) -> set:
        """Observed post-action state S(t+1) — what actually held on arrival."""
        out: set = set()
        if obs is not None:
            fl, _ = self.ce._get_tile_fluents(0, 0, obs['ptx'], obs['pty'], obs)
            out |= fl
        out.add(Fluent("Damaged") if took_damage else Fluent("Safe"))
        return out

    @staticmethod
    def _rule_confirmed(rule: EECTemporalRule, after: set,
                        took_damage: bool) -> bool | None:
        """Did the real-world outcome confirm this rule's predicted effect?

        Returns None when the effect is not verifiable from this observation.
        Name-level matching mirrors ExpectationMemory._matches for arg-less
        fluents.
        """
        name = rule.effect.name
        if rule.effect_type == "Initiates":
            if name == "Damaged":
                return took_damage
            if name == "Safe":
                return not took_damage
            return any(f.name == name for f in after)
        if rule.effect_type == "Terminates":
            return not any(f.name == name for f in after)
        if rule.effect_type == "HoldsAt":
            return any(f.name == name for f in after)
        return None

    def feedback(self, took_damage: bool, t: int = 0, current_obs: dict = None):
        """Compare the real outcome to stored expectations — paper Algorithm 2.

        Faithful to the paper's pseudocode: EVERY rule in memory whose
        conditions matched (currState + Happens(a, t)) at decision time is
        confirmed or violated against the observed outcome — not just the
        single rule the controller acted on.  This is what drives confidence
        dynamics (eqs. 2-3), pruning (eq. 4), and generalisation (eq. 5)
        across the whole rule base, including HoldsAt persistence rules and
        the revisable innate priors.

        Multi-step rules (delay ≠ 1) and variable-argument rules are skipped:
        a single t → t+1 observation cannot verify them.

        Surprise handling (Popperian falsification): when the acted-on
        expectation is disconfirmed — or damage arrives with no expectation at
        all — a new rule is formed from the observed context with an elevated
        prior (C_INIT_SURPRISE).
        """
        pre_fluents = self._last_fluents
        pre_event   = self._last_event
        acted_rule  = self._last_rule
        self._last_rule    = None
        self._last_obs     = None
        self._last_fluents = None
        self._last_event   = None

        # ── algorithm 2 sweep: update all rules that matched the pre-move state ──
        if pre_fluents is not None and pre_event is not None:
            after = self._after_fluents(current_obs, took_damage)
            # real-world evidence into the causal ledger (same model that
            # simulation evidence feeds — one unified causal picture).
            _status_names = {s.capitalize() for s in SDEFS}
            observed = ({f.name for f in after
                         if f.name in _status_names} | {'Damaged'}
                        if took_damage else {'Safe'})
            self.memory.causal.record(pre_fluents, observed)
            for rule in list(self.memory.rules):
                if rule.delay != 1:
                    # not verifiable from a one-step observation
                    continue
                if rule.event is not None and any(
                        _is_var(a) for a in rule.event.args):
                    # variable-argument demo rules — skip
                    continue
                if not self.memory._matches(rule, pre_fluents, pre_event):
                    continue
                confirmed = self._rule_confirmed(rule, after, took_damage)
                if confirmed is None:
                    continue
                self.memory.update(rule, confirmed, t, context=pre_fluents)
        elif acted_rule is not None:
            # no stored pre-move context — fall back to single-rule update
            expected_damage = (acted_rule.effect == Fluent("Damaged") and
                               acted_rule.effect_type == "Initiates")
            self.memory.update(acted_rule, expected_damage == took_damage, t)

        # ── popperian surprise: outcome contradicted the acted-on expectation ──
        if acted_rule is not None:
            expected_damage = (acted_rule.effect == Fluent("Damaged") and
                               acted_rule.effect_type == "Initiates")
            surprised = (expected_damage != took_damage)
        else:
            # damage with no expectation at all
            surprised = took_damage

        if surprised and current_obs is not None:
            before = self.memory.expectations_created
            self.memory.expectation_forms += 1
            if pre_fluents is not None:
                self.memory.form(self._feedback_rule_from_precontext(
                    pre_fluents, took_damage, t))
            else:
                self.memory.form(self._observed_feedback_rule(current_obs,
                                                              took_damage, t))
            self.memory.rules_derived += self.memory.expectations_created - before

    def _vicarious_confirm(self, obs: dict):
        """Falsification by observation (Popperian testing without self-experiment).

        The controller avoids predicted-dangerous tiles, so Initiates(Damaged)
        rules are structurally hard to test first-hand.  But the agent can
        watch OTHER entities: when a roaming enemy is observed entering a tile
        whose hazard is currently active, the matching danger expectations are
        vicariously confirmed via ExpectationMemory.vicarious_confirm().

        Only newly-entered tiles count (per-enemy tile tracking) so a loitering
        enemy doesn't spam confirmations every tick.
        """
        for e in obs.get('enemies', ()):
            et  = (int(e.x + 0.5), int(e.y + 0.5))
            eid = id(e)
            if self._enemy_last_tiles.get(eid) == et:
                # hasn't entered a new tile
                continue
            self._enemy_last_tiles[eid] = et
            kind = obs['trap_map'].get(et)
            if not kind:
                continue
            mov = TRAP_SENSORS.get(kind, {}).get('mov', False)
            if mov:
                active, ticks = obs.get('dtrap_activity', {}).get(kind, (True, 0))
                if not active:
                    # dormant: no collision — but the non-event is evidence.
                    # only clearly-dormant contacts count (ticks > 10, i.e.
                    # the trapinactive perceptual band); near-activation
                    # crossings are ambiguous and recorded as nothing.
                    if ticks > 10:
                        fl = set(tile_sensor_fluents(
                            kind, et in obs.get('kinetic_tiles', set())))
                        if fl:
                            fl.add(Fluent("DynamicHazard"))
                            fl.add(Fluent("TrapInactive"))
                            rm = self.room_of.get(et)
                            if rm is not None:
                                fl.add(Fluent("Room", (rm.rtype,)))
                            self.memory.causal.record(fl, {"Safe"})
                            self.memory.calibration.record(kind, False)
                            self.memory.vicarious_confirm_safe(
                                fl, Event("Move"), self.sim_time)
                    continue
            fl = set(tile_sensor_fluents(
                kind, et in obs.get('kinetic_tiles', set())))
            if not fl:
                continue
            fl.add(Fluent("DynamicHazard") if mov else Fluent("StaticHazard"))
            if mov:
                fl.add(Fluent("TrapActive"))
            rm = self.room_of.get(et)
            if rm is not None:
                fl.add(Fluent("Room", (rm.rtype,)))
            # vicarious causal evidence: another body in this fluent context
            # was damaged — that is an observation of initiates(damaged) and
            # feeds the same δp ledger as first-person and simulated outcomes.
            self.memory.causal.record(fl, {"Damaged"})
            self.memory.calibration.record(obs['trap_map'].get(et), True)
            self.memory.vicarious_confirm(fl, Event("Move"), self.sim_time)

    def step(self, straps, dtraps, enemies, hazard_pulse=None):
        # capture the full room lists so _make_sim_state can simulate all
        # threats — not just the ones currently inside the agent's fov.
        # traps behind the heading direction are invisible to observe() but
        # can still sweep through the agent's path; the internal model must
        # see them or transit-hit detection is completely blind to that half
        # of the room.
        self._room_dtraps  = list(dtraps)
        self._room_enemies = list(enemies)
        """Full Popperian Expectations functional loop — paper §IV.

        Maps to the paper's 8-step closed loop:
          1. OTL processes real-time sensor data → observe()
          2. Robot controller generates candidate actions → choose_action()
          3. Internal Model simulates each candidate → ConsequenceEvaluator._sim_step()
          4. Consequence Evaluator filters safe/unsafe actions → CE.evaluate()
          5. EEC Expectation Formation stores rules → CE._form_expectations()
          6. Expectation Memory stores rules + metadata → ExpectationMemory.form()
          7. Robot Controller executes chosen safe action → self._keys update
          8. Real-world feedback triggers expectation update → feedback()

        Note: steps 3-6 are bypassed when a high-confidence memory rule already
        covers the candidate action (memory-first principle, §III-F).
        """
        self._tick    += 1
        # advance formal simulation time t (happens(a, t))
        self.sim_time += 1
        # confidences may have moved since last tick (feedback, vicarious
        # updates), but the formal reasoner only reads confidence through two
        # thresholds — so we rebuild the cache only when an update actually
        # crossed one (or rules changed structurally), not every tick.
        self.eec_reasoner.clear_cache_if_dirty()

        # track first frame of player death (damage event)
        now_dead = self.player.dead
        if now_dead and not self._was_dead:
            self._took_damage = True
        self._was_dead = now_dead

        # ── step 1. otl: observe current environment ─────────────────────────
        obs = self.observe(straps, dtraps, enemies, hazard_pulse)
        obs['sim_time'] = self.sim_time
        pt  = (obs['ptx'], obs['pty'])
        moved = pt != self._last_pos

        if now_dead:
            if self._last_rule is not None or self._last_fluents is not None:
                self.feedback(True, self.sim_time, current_obs=obs)
            self._took_damage = False
            for k in self._keys: self._keys[k] = False
            return

        # ── vicarious testing: falsification by observation (popperian) ──────
        # watching a roaming enemy collide with an active hazard confirms the
        # matching danger expectations without self-experiment.
        self._vicarious_confirm(obs)

        # ── dynamics learning: observe how things move, every tick ───────────
        # behaviour laws (periodic occupancy) are conjectured from observation
        # and tested against each new tick — expectations about the world's
        # mechanics, not merely about where the agent gets hurt.
        if self.use_dynamics:
            self.dynamics.observe(self._tick, obs.get('dtraps', []))

        # ── step 8. feedback: compare real outcome to expectation ─────────────
        # only triggered when the player actually arrives at a new tile —
        # i.e. when a real-world consequence can be observed and compared.
        if moved:
            if self._last_rule is not None or self._last_fluents is not None:
                self.feedback(self._took_damage, self.sim_time, current_obs=obs)
            self._took_damage = False
            self._visit_counts[pt] = self._visit_counts.get(pt, 0) + 1
            self._stuck_ticks = 0
            # advanced a tile → crossing is making progress
            self._crossing_age = 0
            # net-progress bookkeeping (best goal distance, stagnation, and the
            # confinement-hold counter) is now maintained unconditionally below,
            # in the per-tick stagnation block, so it cannot be defeated by a
            # drifting orbit that resets local timers.  nothing to do here.
            # record distinct-tile history for a<->b oscillation detection.
            self._tile_history.append(pt)
            if len(self._tile_history) > 16:
                self._tile_history.pop(0)
            # the agent travelled a tile: heading should follow motion again.
            # clearing the deliberate goal-gaze lets observe() use last_action,
            # so the vision cone points the way the agent is actually going.
            self._gaze_heading = None
            self._gaze_hold_count = 0
        else:
            # count raw ticks without tile change; scale limit to match old behaviour
            self._stuck_ticks += 1
            if self._stuck_ticks >= self.STUCK_LIMIT * self.STEP_TICKS:
                self._path = []
                # force full replan
                self.current_route = []
                self.route_commit_steps = 0
                self._visit_counts[pt] = self._visit_counts.get(pt, 0) + 3
                self._stuck_ticks = 0

        # ── absolute-region confinement tracking (deadlock valve) ───────────
        # independently of why the agent is or isn't moving, track how long it
        # has stayed within a small radius of an anchor tile.  enemy-swarm
        # deadlocks (commit→threat→abort→commit forever) keep the agent inside a
        # tiny region while it technically "moves" every tick, so neither the
        # stuck-tick counter nor the wait-safety-gated confinement detector
        # catches them.  this timer is gated on nothing but position, so it
        # always fires.  when it crosses the cap, choose_action's forced-push
        # valve commits a goal-ward move and holds it through enemy threat.
        if self._region_anchor is None:
            self._region_anchor = pt
            self._region_ticks = 0
        else:
            ax, ay = self._region_anchor
            if abs(pt[0] - ax) + abs(pt[1] - ay) <= self.REGION_RADIUS:
                self._region_ticks += 1
            else:
                # left the region → genuine progress; reset anchor here.
                self._region_anchor = pt
                self._region_ticks = 0

        # ── net-progress stagnation tracking (authoritative livelock signal) ──
        # runs every tick regardless of movement.  the one signal that cannot be
        # faked by a drifting orbit or in-place flip is whether the agent's
        # closest-ever approach to the exit actually improves.  when it does,
        # the watchdog disarms; when it doesn't, the counter climbs until the
        # breaker in choose_action engages.  kept here (not in the `moved`
        # branch) so a fully frozen agent also accrues stagnation.
        ex_w, ey_w = self.end
        d_w = abs(pt[0] - ex_w) + abs(pt[1] - ey_w)
        if self._best_goal_dist is None:
            self._best_goal_dist = d_w
        if d_w < self._best_goal_dist:
            # real net progress toward the exit: disarm every livelock timer.
            self._best_goal_dist = d_w
            self._stagnation_ticks = 0
            self._stagnation_breaks = 0
            self._confine_holds = 0
        else:
            self._stagnation_ticks += 1

        self._last_pos = pt
        self._last_obs = obs
        if self._transit_abort_hold > 0:
            self._transit_abort_hold -= 1

        # ── asynchronous deliberation (feedback #1): world never waits ───────
        # a plan computed last decision is still being "thought" inside the
        # agent; the world keeps moving meanwhile.  when the latency elapses
        # the plan is adopted and executed through the normal commitment path.
        if self.WORLD_ASYNC_DELIBERATION and self._pending_ticks > 0:
            if self._reflex_threat(obs):
                # system-1 pre-emption: drop the pending plan, replan now.
                self._pending_plan, self._pending_ticks = None, 0
                self._clear_motion_plan(clear_last=True)
            else:
                self._pending_ticks -= 1
                if self._pending_ticks > 0:
                    # still deliberating: continue current behaviour (committed
                    # motion if any survives; otherwise hold under monitoring).
                    if not self.current_route:
                        self._debug_safe_action = None
                        if self._pending_plan and self._pending_plan[0]:
                            self._debug_planned_route = list(self._pending_plan[0])
                        else:
                            self._debug_planned_route = []
                        for k in self._keys:
                            self._keys[k] = False
                        return
                else:
                    # deliberation complete — adopt the plan if still anchored
                    # to where the agent actually is (the world moved on).
                    if self._pending_plan:
                        route, commit = self._pending_plan
                        self._pending_plan = None
                        while route and route[0] == pt:
                            route.pop(0)
                        if route:
                            nx, ny = route[0]
                            if abs(nx - pt[0]) + abs(ny - pt[1]) == 1:
                                self.current_route      = route
                                self.route_commit_steps = max(commit, 1)
                    # fall through: commitment path executes the adopted plan

        # ── steps 2-6: robot controller → internal model → eec → memory ──────
        # choose_action() orchestrates the full simulation/memory loop internally
        # via consequenceevaluator.  it returns the chosen safe action and the
        # eectemporalrule that justified it (for feedback in step 8 next tick).
        sims_before = self.memory.sims_run
        action, rule = self.choose_action(obs)
        sims_used = self.memory.sims_run - sims_before
        # record the direction the controller chose this tick (none when it held
        # position).  this lets the oscillation breaker detect a stationary
        # heading flip (deciding left, then right, then left... at a doorway
        # without ever crossing a tile) — invisible to the tile-based history,
        # which only updates when the agent actually moves between tiles.
        self._dir_history.append(action)
        if len(self._dir_history) > 8:
            self._dir_history.pop(0)
        self._debug_safe_action = action
        if self.current_route:
            self._debug_planned_route = list(self.current_route)
        elif self._crossing_route:
            self._debug_planned_route = list(self._crossing_route)
        elif self._pending_plan and self._pending_plan[0]:
            self._debug_planned_route = list(self._pending_plan[0])
        elif self._window_action is not None:
            self._debug_planned_route = [(obs['ptx'] + self._window_action[0],
                                          obs['pty'] + self._window_action[1])]
        elif action is not None:
            self._debug_planned_route = [(obs['ptx'] + action[0],
                                          obs['pty'] + action[1])]
        else:
            self._debug_planned_route = []

        # ── plan latency (feedback #1) ────────────────────────────────────────
        # full planning that consumed internal-model rollouts takes world time
        # to compute inside the agent: the freshly planned route is stashed and
        # adopted ⌈sims / budget⌉ ticks from now.  the world is never slowed —
        # it simply moves on while the agent thinks, which is why rollouts are
        # anchored at the expected adoption time (_lead_ticks).  memory- and
        # dynamics-answered planning (sims_used == 0) completes within the
        # tick — the paper's §vi efficiency benefit, realised in world time.
        # reflex emergencies are exempt: immediate danger acts immediately.
        if self.WORLD_ASYNC_DELIBERATION and self._planned:
            self._lead_ema = 0.7 * self._lead_ema + 0.3 * sims_used
            timed_wait_plan = bool(
                self._crossing_route or self._crossing_wait > 0 or
                self._window_action is not None or self._window_wait > 0)
            evacuation_now = self._current_tile_will_be_unsafe(obs)
            if (sims_used > 0 and not self._reflex_threat(obs)
                    and not evacuation_now and not timed_wait_plan):
                # the current tick's budget is spent on this plan first; only
                # the overflow defers adoption to future ticks.
                overflow = max(0, sims_used - self.SIM_BUDGET_PER_TICK)
                latency  = min(self.MAX_PLAN_LATENCY,
                               -(-overflow // self.SIM_BUDGET_PER_TICK))
                if latency > 0:
                    self._pending_plan  = (list(self.current_route),
                                           self.route_commit_steps)
                    self._pending_ticks = latency
                    self.think_ticks_total += latency
                    self._clear_motion_plan()
                    for k in self._keys:
                        self._keys[k] = False
                    self._last_rule = None
                    self._last_fluents = self._last_event = None
                    return

        # ── decision trace (feedback #4: how the agent solves the room) ──────
        if self.trace_sink is not None and action is not None:
            self.trace_sink.append(dict(
                tick=self._tick, mode=self.mode,
                tile=pt, action=action,
                source=("plan-mem" if (self._planned and sims_used == 0)
                        else "plan-sim" if self._planned else "commit"),
                sims_used=sims_used,
                plan_latency=self._pending_ticks,
                mem_rules=self.memory.count,
                rule=(_rule_label(rule) if rule is not None else "")))

        # emergency stop: eec flagged danger on the currently-held direction.
        if action is None:
            for k in self._keys:
                self._keys[k] = False
            self._last_rule = None
            self._last_fluents = self._last_event = None
            return

        if not self._valid_step(action, obs['ptx'], obs['pty']):
            self._clear_motion_plan(clear_last=True)
            for k in self._keys:
                self._keys[k] = False
            self._last_rule = None
            self._last_fluents = self._last_event = None
            return

        dx, dy = action

        # ── step 7. robot controller executes the chosen safe action ──────────
        current_dx = 0
        current_dy = 0
        if self._keys[K_LEFT]  or self._keys[K_a]: current_dx -= 1
        if self._keys[K_RIGHT] or self._keys[K_d]: current_dx += 1
        if self._keys[K_UP]    or self._keys[K_w]: current_dy -= 1
        if self._keys[K_DOWN]  or self._keys[K_s]: current_dy += 1

        # refresh keys every controller tick so centering corrections cannot go stale.
        should_update = True

        if should_update:
            for k in self._keys:
                self._keys[k] = False
            # stored for step 8 feedback next tick
            self._last_rule = rule
            # capture the pre-move context (currstate + happens(a, t)) so
            # feedback can sweep all matching rules per algorithm 2 — even
            # during route commitment, when no single acted-on rule exists.
            ttx, tty = obs['ptx'] + dx, obs['pty'] + dy
            if (0 <= ttx < COLS and 0 <= tty < ROWS
                    and self.grid[tty][ttx] != 1):
                self._last_fluents, self._last_event = \
                    self.ce._get_tile_fluents(dx, dy, ttx, tty, obs)
            else:
                self._last_fluents = self._last_event = None

            # continuous body vs tile planner: center on the hallway axis before
            # pushing forward. diagonal correction can keep a round body wedged
            # against corridor corners, so large offsets get correction-only keys.
            cx, cy = obs['ptx'], obs['pty']
            center_eps = 0.08
            hard_center_eps = 0.16
            center_only = False
            evacuating_current_tile = self._current_tile_will_be_unsafe(obs)
            enemy_body_evac = self._body_enemy_contact_soon(
                obs, ticks=self.STEP_TICKS)
            off_axis_stuck_evac = (
                evacuating_current_tile
                and getattr(self, '_stuck_ticks', 0) >= 2 * self.STEP_TICKS
                and ((dx != 0 and abs(self.player.y - cy) > center_eps)
                     or (dy != 0 and abs(self.player.x - cx) > center_eps))
            )
            hazard_commit = (
                (evacuating_current_tile and not enemy_body_evac
                 and not off_axis_stuck_evac)
                or bool(self._crossing_route)
                or self._crossing_wait > 0
                or self._entry_lock_ticks > 0
                or self._window_action is not None
                or (self._rotating_hazard_near(obs) and not off_axis_stuck_evac)
            )

            # ── wall-wedge override ───────────────────────────────────────────
            # a round body sitting off the perpendicular axis can be physically
            # blocked from a cardinal move by a wall corner on its leading edge
            # (e.g. body at y=35.5 trying to go left while (x-1, 35) is a wall):
            # the move probe collides, so the body never advances, yet the agent
            # keeps committing the (correct) cardinal move forever.  hazard_commit
            # normally suppresses axis-centering, which is exactly what lets this
            # wedge persist.  detect the wedge directly — the intended cardinal
            # move is wall-blocked and the body is off the perpendicular axis —
            # and force a centering correction toward the tile axis regardless of
            # hazard_commit, so the body slides clear of the corner and can then
            # proceed.  this is purely a wall-collision remedy; it never steers
            # into a hazard tile (the centering target is the body's own lane).
            wall_wedge = False
            if dx != 0 or dy != 0:
                pbx, pby = self.player.x, self.player.y
                _wr = PLAYER_WALL_RADIUS

                def _wall_blocks(px, py):
                    for ox, oy in ((_wr, 0), (-_wr, 0), (0, _wr), (0, -_wr)):
                        gx = int(px + ox + .5); gy = int(py + oy + .5)
                        if (0 <= gx < COLS and 0 <= gy < ROWS
                                and self.grid[gy][gx] == 1):
                            return True
                    return False

                # probe a small step along the intended direction.
                if _wall_blocks(pbx + dx * 0.30, pby + dy * 0.30):
                    if dx != 0 and abs(pby - cy) > center_eps:
                        wall_wedge = True
                        center_only = True
                        if pby > cy:
                            self._keys[K_UP] = True; self._keys[K_w] = True
                        else:
                            self._keys[K_DOWN] = True; self._keys[K_s] = True
                    elif dy != 0 and abs(pbx - cx) > center_eps:
                        wall_wedge = True
                        center_only = True
                        if pbx > cx:
                            self._keys[K_LEFT] = True; self._keys[K_a] = True
                        else:
                            self._keys[K_RIGHT] = True; self._keys[K_d] = True

            if not wall_wedge and dx != 0 and not hazard_commit:
                off_y = self.player.y - cy
                if (abs(off_y) > hard_center_eps and not evacuating_current_tile
                        or off_axis_stuck_evac):
                    center_only = True
                if off_y > center_eps:
                    self._keys[K_UP] = True; self._keys[K_w] = True
                elif off_y < -center_eps:
                    self._keys[K_DOWN] = True; self._keys[K_s] = True
            elif not wall_wedge and dy != 0 and not hazard_commit:
                off_x = self.player.x - cx
                if (abs(off_x) > hard_center_eps and not evacuating_current_tile
                        or off_axis_stuck_evac):
                    center_only = True
                if off_x > center_eps:
                    self._keys[K_LEFT] = True; self._keys[K_a] = True
                elif off_x < -center_eps:
                    self._keys[K_RIGHT] = True; self._keys[K_d] = True

            if not center_only:
                self._last_rule = rule
                ttx, tty = obs['ptx'] + dx, obs['pty'] + dy
                if (0 <= ttx < COLS and 0 <= tty < ROWS
                        and self.grid[tty][ttx] != 1):
                    self._last_fluents, self._last_event = \
                        self.ce._get_tile_fluents(dx, dy, ttx, tty, obs)
                else:
                    self._last_fluents = self._last_event = None
                if dx == -1: self._keys[K_LEFT]  = True; self._keys[K_a] = True
                elif dx == 1: self._keys[K_RIGHT] = True; self._keys[K_d] = True
                if dy == -1: self._keys[K_UP]    = True; self._keys[K_w] = True
                elif dy == 1: self._keys[K_DOWN]  = True; self._keys[K_s] = True
            else:
                self._last_rule = None
                self._last_fluents, self._last_event = \
                    self.ce._get_tile_fluents(0, 0, obs['ptx'], obs['pty'], obs)

            # final actuator-level veto.  axis-centering may add a correction
            # key to the planned cardinal move; if that correction points into
            # a currently lethal swept tile, drop it before the player physics
            # applies the keys.  then re-check the remaining cardinal key vector
            # so stale/pending intent cannot execute into a now-visible trap.
            kdx = (1 if (self._keys[K_RIGHT] or self._keys[K_d]) else 0) - \
                  (1 if (self._keys[K_LEFT] or self._keys[K_a]) else 0)
            kdy = (1 if (self._keys[K_DOWN] or self._keys[K_s]) else 0) - \
                  (1 if (self._keys[K_UP] or self._keys[K_w]) else 0)

            def _clear_x_keys():
                self._keys[K_LEFT] = self._keys[K_a] = False
                self._keys[K_RIGHT] = self._keys[K_d] = False

            def _clear_y_keys():
                self._keys[K_UP] = self._keys[K_w] = False
                self._keys[K_DOWN] = self._keys[K_s] = False

            if kdx and kdy:
                correction = (0, kdy) if dx != 0 else (kdx, 0)
                if self._valid_step(correction, obs['ptx'], obs['pty']):
                    corr_danger, _ = self._one_step_danger(correction, obs)
                    if corr_danger:
                        if correction[0]:
                            _clear_x_keys()
                        else:
                            _clear_y_keys()

            kdx = (1 if (self._keys[K_RIGHT] or self._keys[K_d]) else 0) - \
                  (1 if (self._keys[K_LEFT] or self._keys[K_a]) else 0)
            kdy = (1 if (self._keys[K_DOWN] or self._keys[K_s]) else 0) - \
                  (1 if (self._keys[K_UP] or self._keys[K_w]) else 0)
            if kdx and kdy:
                # a diagonal key vector can still remain if both the planned
                # move and the centering correction looked individually safe.
                # the real player moves diagonally in that case, so run the
                # same sub-tile transit simulation for the combined vector.
                exec_danger, _ = self._one_step_danger((kdx, kdy), obs)
                emergency_commit = (
                    (evacuating_current_tile
                     or getattr(self, '_hazard_evac_ticks', 0) > 0)
                    and not self._wait_is_safe(obs)
                )
                if exec_danger and not emergency_commit:
                    for k in self._keys:
                        self._keys[k] = False
                    self._clear_motion_plan(clear_last=True)
                    self._last_rule = None
                    self._last_fluents = self._last_event = None
            elif (kdx, kdy) in self.DIRS:
                exec_danger, _ = self._one_step_danger((kdx, kdy), obs)
                emergency_commit = (
                    (evacuating_current_tile
                     or getattr(self, '_hazard_evac_ticks', 0) > 0)
                    and not self._wait_is_safe(obs)
                )
                if exec_danger and not emergency_commit:
                    for k in self._keys:
                        self._keys[k] = False
                    self._clear_motion_plan(clear_last=True)
                    self._last_rule = None
                    self._last_fluents = self._last_event = None

    @property
    def keys(self):
        return self._keys


# =============================================================================
# astaragent — classic a* shortest-path baseline (supervisor feedback #2)
# -----------------------------------------------------------------------------
# a deliberately simple, recognisable baseline that contrasts with the
# popperian-expectations agent.  it carries none of the pe machinery — no
# expectation memory, no internal-model rollouts, no learned dynamics.  it
# does exactly what the name says:
#
# 1. run a* (binary heap + admissible manhattan heuristic) over the static
# wall-grid to find a shortest path from the current tile to the exit.
# 2. treat tiles currently occupied by a hazard (dynamic-trap or roaming
# enemy) as temporary obstacles, so the path is re-routed around live
# danger when a route around it exists, and replanned each decision as
# hazards move.  with astar_hazard_aware = false this reduces to a pure
# static-grid a* (an ablation that ignores moving hazards entirely).
# 3. follow the path one tile at a time, holding briefly if the only next
# tile is momentarily occupied by a hazard.
#
# because a* has no model of how hazards move (unlike pe's forward model), it
# cannot anticipate a trap that is clear now but will sweep into the next tile
# as the agent crosses — those collisions are the expected failure mode and
# are exactly what the comparison is meant to expose.
#
# the class satisfies the same controller contract the world expects of any
# agent: a `.keys` mapping read every world tick, and a `.step(straps, dtraps,
# enemies, hazard_pulse)` method called once per tick.  it also exposes the
# handful of attributes the benchmark harness reads off an agent
# (`think_ticks_total`, `dynamics.answers`) so run_single_trial treats it
# uniformly with the pe agent; a*'s search effort is reported through the
# shared sims_run counter (one count per node expanded).
# =============================================================================
# false ⇒ pure static-grid a* (ignores live hazards)
ASTAR_HAZARD_AWARE = True


class _NullDynamics:
    """Stand-in for PEAgent.dynamics so the harness's dynamics.answers read
    returns 0 for the A* agent without special-casing."""
    answers = 0


class AStarAgent:
    # l r u d (matches peagent)
    DIRS       = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # world ticks per decision (same cadence as peagent)
    STEP_TICKS = 10

    def __init__(self, player, grid, end, room_of=None, memory=None,
                 mode: str = "astar", trace_sink: list | None = None):
        self.player  = player
        self.grid    = grid
        self.end     = (int(round(end[0])), int(round(end[1])))
        self.room_of = room_of or {}
        self.mode    = mode
        # shared expectationmemory (for sims_run)
        self.memory  = memory
        self.trace_sink = trace_sink
        self._keys = {K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False,
                      K_w: False,  K_s: False,    K_a: False,    K_d: False}
        # ── harness-compatibility attributes ────────────────────────────────
        # the benchmark reads these off whatever agent is installed; provide
        # inert values so a* slots into run_single_trial with no special cases.
        self.think_ticks_total = 0
        self.dynamics          = _NullDynamics()
        self.use_memory = self.use_sim = self.use_dynamics = False
        # ── navigation state ────────────────────────────────────────────────
        # remaining tiles to the goal (start-exclusive)
        self._route: list = []
        self._tick        = 0
        self._last_pos    = (player.tx, player.ty)
        self._stuck_ticks = 0
        self._wait_ticks  = 0
        # persistent memory of static-trap tiles discovered (treated as walls).
        self._known_static: dict = {}
        self._known_static_room = self.room_of.get((player.tx, player.ty))

    # ── a* core ─────────────────────────────────────────────────────────────
    @staticmethod
    def _h(ax, ay, bx, by) -> int:
        """Manhattan distance — admissible & consistent for 4-connected grids
        with unit step cost, so A* returns a provably shortest path."""
        return abs(ax - bx) + abs(ay - by)

    def _astar(self, sx, sy, blocked: set) -> list | None:
        """Shortest path from (sx,sy) to self.end avoiding `blocked` tiles.

        Standard A*: a binary heap ordered by f = g + h, a g-score map, and
        parent links for reconstruction.  `blocked` holds grid walls implicitly
        (tested live) plus any extra obstacle tiles (known static traps, and —
        when hazard-aware — tiles a live hazard currently occupies).  Each node
        popped is counted as one unit of search work via the shared sims_run
        counter, mirroring how the PE agent's Internal-Model steps are counted.
        """
        gx, gy = self.end
        if not (0 <= gx < COLS and 0 <= gy < ROWS) or self.grid[gy][gx] == 1:
            return None
        start = (sx, sy)
        # heap entries: (f, g, tiebreak, x, y).  the tiebreak is a deterministic
        # monotonic counter so equal-f pops resolve identically every call
        # (no reliance on nondeterministic tuple comparison of coordinates).
        counter = 0
        open_heap = [(self._h(sx, sy, gx, gy), 0, counter, sx, sy)]
        g_score = {start: 0}
        parent  = {start: None}
        closed  = set()
        expanded = 0
        while open_heap:
            f, g, _tb, cx, cy = heapq.heappop(open_heap)
            if (cx, cy) in closed:
                continue
            closed.add((cx, cy))
            expanded += 1
            if (cx, cy) == (gx, gy):
                # reconstruct, excluding the start tile (the agent is on it).
                path, node = [], (cx, cy)
                while node != start:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                self._charge_search(expanded)
                return path
            for ddx, ddy in self.DIRS:
                nx, ny = cx + ddx, cy + ddy
                if not (0 <= nx < COLS and 0 <= ny < ROWS):
                    continue
                # grid wall
                if self.grid[ny][nx] == 1:
                    continue
                # static trap / live hazard
                if (nx, ny) in blocked:
                    continue
                ng = g + 1
                if ng < g_score.get((nx, ny), 1 << 30):
                    g_score[(nx, ny)] = ng
                    parent[(nx, ny)] = (cx, cy)
                    counter += 1
                    nf = ng + self._h(nx, ny, gx, gy)
                    heapq.heappush(open_heap, (nf, ng, counter, nx, ny))
        self._charge_search(expanded)
        # goal unreachable under the current obstacle set
        return None

    def _charge_search(self, nodes: int):
        """Account A* search effort against the shared sims_run counter so the
        comparison CSV's sim_steps column reflects A*'s computational work the
        same way it reflects the PE agent's Internal-Model evaluations."""
        if self.memory is not None:
            try:
                self.memory.sims_run += nodes
            except Exception:
                pass

    # ── perception of live hazards (tiles to avoid) ─────────────────────────
    def _hazard_tiles(self, dtraps, enemies) -> set:
        """Tiles currently occupied by a moving hazard, used as transient A*
        obstacles.  Mirrors the world's own tile-occupancy mapping so the agent
        avoids exactly the tiles that are lethal *this* tick (it has no model of
        where they go next — that is the whole point of the baseline)."""
        blocked: set = set()
        if not ASTAR_HAZARD_AWARE:
            return blocked
        for dt in dtraps:
            tmp: dict = {}
            _map_dtrap_tiles(dt, tmp)
            blocked.update(tmp.keys())
        blocked.update(_enemy_tiles_from_list(enemies))
        return blocked

    def _refresh_static_memory(self, straps):
        """Remember static-trap tiles (they are immovable within a room) and
        treat them as permanent walls for planning.  Forget a room's static
        traps when the agent leaves it, since RELOC_ON_REENTRY may move them."""
        ptx, pty = self.player.tx, self.player.ty
        here = self.room_of.get((ptx, pty))
        if here is not self._known_static_room:
            left = self._known_static_room
            self._known_static = {p: k for p, k in self._known_static.items()
                                  if self.room_of.get(p) is not left}
            self._known_static_room = here
        for t in straps:
            # the agent learns a static trap's tile once it is close enough to
            # perceive it (same neighbourhood the world uses to resolve a hit).
            if abs(t.tx - ptx) <= 6 and abs(t.ty - pty) <= 6:
                self._known_static[(t.tx, t.ty)] = t.kind

    # ── controller: convert "move toward next tile" into key presses ─────────
    def _press_toward(self, dx, dy):
        """Press the keys that move the round body toward the neighbouring tile
        (dx,dy).

        The body has a wall radius, so two corrections are needed for it to
        traverse tile-centred corridors without wedging:

          * Axis centering — before advancing ALONG a corridor, align onto the
            perpendicular lane centre, so the leading edge clears the tile it is
            entering.
          * Wall-wedge break — if the intended cardinal move is physically
            blocked by a wall corner AND the body is off the perpendicular axis,
            force a centering correction toward the lane even though centering
            would otherwise be skipped; otherwise the body presses into the
            corner forever (the livelock observed at corridor mouths).

        It never presses toward a non-target tile: corrections move only along
        the body's own current lane.
        """
        for k in self._keys:
            self._keys[k] = False
        # lane centre = current tile
        cx, cy = self.player.tx, self.player.ty
        bx, by = self.player.x, self.player.y
        eps = 0.06
        wr  = PLAYER_WALL_RADIUS

        def wall_blocks(px, py):
            for ox, oy in ((wr, 0), (-wr, 0), (0, wr), (0, -wr)):
                gx = int(px + ox + .5); gy = int(py + oy + .5)
                if 0 <= gx < COLS and 0 <= gy < ROWS and self.grid[gy][gx] == 1:
                    return True
            return False

        # would a small step in the intended direction collide with a wall?
        blocked_ahead = wall_blocks(bx + dx * 0.30, by + dy * 0.30)

        if dx != 0:
            # vertical offset from lane centre
            off = by - cy
            need_center = abs(off) > eps and (blocked_ahead or abs(off) > 0.10)
            if need_center:
                if off > 0: self._keys[K_UP]   = self._keys[K_w] = True
                else:       self._keys[K_DOWN] = self._keys[K_s] = True
                return
            if dx < 0: self._keys[K_LEFT]  = self._keys[K_a] = True
            else:      self._keys[K_RIGHT] = self._keys[K_d] = True
        elif dy != 0:
            off = bx - cx
            need_center = abs(off) > eps and (blocked_ahead or abs(off) > 0.10)
            if need_center:
                if off > 0: self._keys[K_LEFT]  = self._keys[K_a] = True
                else:       self._keys[K_RIGHT] = self._keys[K_d] = True
                return
            if dy < 0: self._keys[K_UP]   = self._keys[K_w] = True
            else:      self._keys[K_DOWN] = self._keys[K_s] = True

    def _hold(self):
        for k in self._keys:
            self._keys[k] = False

    # ── main per-tick entry point (controller contract) ─────────────────────
    def step(self, straps, dtraps, enemies, hazard_pulse=None):
        self._tick += 1
        if self.player.dead:
            self._hold()
            return

        ptx, pty = self.player.tx, self.player.ty
        moved = (ptx, pty) != self._last_pos
        if moved:
            self._stuck_ticks = 0
        else:
            self._stuck_ticks += 1
        self._last_pos = (ptx, pty)
        # drop any leading route tiles the body already stands on — every tick,
        # not only when the tile index changed.  the continuous body can settle
        # onto the next route tile (its tx,ty updates) while still centering on
        # that tile's axis, i.e. without registering as "moved" relative to the
        # previous decision; if the head were popped only on `moved`, the route
        # head would remain equal to the current tile and the step logic would
        # see a zero-length first move, mistake it for a desync, and replan the
        # identical route forever (a livelock observed at corridor centres).
        while self._route and self._route[0] == (ptx, pty):
            self._route.pop(0)

        # already at the goal: nothing to do.
        if (ptx, pty) == self.end:
            self._hold()
            return

        # decision policy: commit to a planned route and follow it, replanning
        # only when there is a reason to — the route is empty, the body is stuck,
        # or a live hazard now sits on a tile of the committed route ahead.
        # replanning every decision tick instead caused the chosen direction to
        # flip-flop at chokepoints: as a moving hazard cycles, the cheaper way
        # around it alternates left/right each plan, and the body oscillates at
        # the corridor mouth without ever crossing.  commit-until-invalid gives
        # the hysteresis a shortest-path follower needs in a dynamic field.
        haz = self._hazard_tiles(dtraps, enemies)
        route_blocked_ahead = any(tile in haz for tile in self._route[:4])
        need_replan = (not self._route
                       or self._stuck_ticks >= self.STEP_TICKS
                       or route_blocked_ahead)

        if need_replan:
            self._refresh_static_memory(straps)
            haz = self._hazard_tiles(dtraps, enemies)
            # permanent obstacles: known static traps (treated like walls).
            obstacles = haz | set(self._known_static.keys())
            route = self._astar(ptx, pty, obstacles)
            if route is None and ASTAR_HAZARD_AWARE:
                # no hazard-free path exists right now (a moving hazard is fully
                # blocking the only corridor).  fall back to a path that ignores
                # live hazards but still respects walls + known static traps, so
                # the agent keeps progressing toward the goal and waits out the
                # blockage at the chokepoint rather than freezing forever.
                route = self._astar(ptx, pty, set(self._known_static.keys()))
            if route:
                self._route = route
                # emit a lightweight per-decision trace entry so the harness's
                # `decisions` count (len(trace) delta) advances for a* too.
                if self.trace_sink is not None:
                    self.trace_sink.append({
                        't': self._tick, 'mode': self.mode,
                        'pos': (ptx, pty), 'next': route[0],
                        'route_len': len(route)})

        # execute one step along the current route.
        if not self._route:
            self._hold()
            return
        nxt = self._route[0]
        dx, dy = nxt[0] - ptx, nxt[1] - pty
        # if the immediate next tile is occupied by a live hazard this tick,
        # hold position for a moment (let the hazard pass) rather than stepping
        # into it — but cap the wait so a permanently-guarded tile eventually
        # forces a replan on the next decision tick.
        if ASTAR_HAZARD_AWARE and abs(dx) + abs(dy) == 1:
            live = self._hazard_tiles(dtraps, enemies)
            if nxt in live and self._wait_ticks < 3 * self.STEP_TICKS:
                self._wait_ticks += 1
                self._hold()
                return
        self._wait_ticks = 0
        if abs(dx) + abs(dy) != 1:
            # route desynced from body (e.g. pushed off-lane); drop it and let
            # the next decision tick replan from the true current tile.
            self._route = []
            self._hold()
            return
        self._press_toward(dx, dy)

    @property
    def keys(self):
        return self._keys


# =============================================================================
# randomagent — random-walk floor baseline (supervisor feedback #2)
# -----------------------------------------------------------------------------
# the simplest possible agent: it does not try to solve the maze at all.  at
# each decision point it picks a random walkable neighbouring tile and steps
# onto it, with no notion of the goal, no pathfinding, no hazard reasoning, and
# no memory.  it is the experimental floor — the "no strategy" reference every
# other agent (avoidant heuristic, a* search, pe) should beat.  reaching the
# exit is purely a matter of chance, so a win is a diffusion event, not a plan.
#
# design of the walk:
# • moves are chosen over the four cardinal neighbours that are not grid
# walls and not a known static-trap tile (so the body is not sent into a
# tile that is lethal-on-contact and immovable — even a random walker does
# not need to step onto a wall or a remembered floor spike to be a fair
# "random movement" baseline; those are treated like walls, exactly as the
# other agents treat them for stepping).
# • a pure uniform random walk wastes almost all its time undoing its last
# step (it backtracks with probability 1/deg every move), which makes it a
# pathologically slow and uninformative baseline.  we apply a mild
# anti-backtrack bias: the tile just came from is avoided when any other
# walkable neighbour exists, falling back to it only at dead ends.  this is
# still a memoryless random walk over the maze graph (it does not aim at
# the goal); it merely doesn't compulsively reverse.  set
# random_anti_backtrack = false for an unbiased uniform random walk.
# • live moving hazards are not avoided — a random agent has no model of
# them.  whether it walks into a sweeping trap is left entirely to chance,
# which is the point of the floor baseline.
#
# reproducibility: the walk is driven by a private random.random seeded
# deterministically from the world seed, so a given seed yields the same random
# trajectory on every run (consistent with the per-seed reproducibility of the
# nondeterministic hazards).  it does not touch the global rng stream, so it
# cannot perturb hazard generation or motion.
#
# like the other baselines it satisfies the controller contract (.keys /
# .step) and exposes the few attributes the benchmark harness reads off an
# agent, so run_single_trial treats it uniformly.
# =============================================================================
# false ⇒ unbiased uniform random walk
RANDOM_ANTI_BACKTRACK = True


class RandomAgent:
    # l r u d (matches peagent)
    DIRS       = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # world ticks per decision (same cadence as peagent)
    STEP_TICKS = 10

    def __init__(self, player, grid, end, room_of=None, memory=None,
                 mode: str = "random", trace_sink: list | None = None,
                 world_seed: int = 0):
        self.player  = player
        self.grid    = grid
        self.end     = (int(round(end[0])), int(round(end[1])))
        self.room_of = room_of or {}
        self.mode    = mode
        self.memory  = memory
        self.trace_sink = trace_sink
        self._keys = {K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False,
                      K_w: False,  K_s: False,    K_a: False,    K_d: False}
        # private deterministic rng: same seed ⇒ same random walk every run,
        # and independent of the global stream so hazard generation/motion is
        # untouched.  salted so it never coincides with a hazard's own stream.
        self._rng = random.Random(_stable_hash(world_seed, "random_walk"))
        # ── harness-compatibility attributes ────────────────────────────────
        self.think_ticks_total = 0
        self.dynamics          = _NullDynamics()
        self.use_memory = self.use_sim = self.use_dynamics = False
        # ── walk state ──────────────────────────────────────────────────────
        # tile currently stepping toward
        self._target: tuple | None = None
        # for anti-backtrack bias
        self._prev_tile = (player.tx, player.ty)
        self._tick        = 0
        self._last_pos    = (player.tx, player.ty)
        self._stuck_ticks = 0
        self._known_static: dict = {}
        self._known_static_room = self.room_of.get((player.tx, player.ty))

    # ── static-trap memory (treated as walls for stepping) ──────────────────
    def _refresh_static_memory(self, straps):
        ptx, pty = self.player.tx, self.player.ty
        here = self.room_of.get((ptx, pty))
        if here is not self._known_static_room:
            left = self._known_static_room
            self._known_static = {p: k for p, k in self._known_static.items()
                                  if self.room_of.get(p) is not left}
            self._known_static_room = here
        for t in straps:
            if abs(t.tx - ptx) <= 6 and abs(t.ty - pty) <= 6:
                self._known_static[(t.tx, t.ty)] = t.kind

    def _walkable(self, tx, ty) -> bool:
        if not (0 <= tx < COLS and 0 <= ty < ROWS):
            return False
        if self.grid[ty][tx] == 1:
            return False
        return (tx, ty) not in self._known_static

    def _pick_random_neighbour(self, ptx, pty) -> tuple | None:
        """Choose a random walkable cardinal neighbour, biased (by default)
        against immediately reversing onto the tile just left."""
        nbrs = [(ptx + dx, pty + dy) for dx, dy in self.DIRS
                if self._walkable(ptx + dx, pty + dy)]
        if not nbrs:
            return None
        if RANDOM_ANTI_BACKTRACK and len(nbrs) > 1 and self._prev_tile in nbrs:
            forward = [n for n in nbrs if n != self._prev_tile]
            if forward:
                nbrs = forward
        return self._rng.choice(nbrs)

    # ── movement controller (shared pattern with astaragent) ────────────────
    def _press_toward(self, dx, dy):
        """Press keys to move the round body toward neighbouring tile (dx,dy),
        centering on the perpendicular lane first and breaking wall-corner
        wedges, identical in spirit to AStarAgent._press_toward."""
        for k in self._keys:
            self._keys[k] = False
        cx, cy = self.player.tx, self.player.ty
        bx, by = self.player.x, self.player.y
        eps = 0.06
        wr  = PLAYER_WALL_RADIUS

        def wall_blocks(px, py):
            for ox, oy in ((wr, 0), (-wr, 0), (0, wr), (0, -wr)):
                gx = int(px + ox + .5); gy = int(py + oy + .5)
                if 0 <= gx < COLS and 0 <= gy < ROWS and self.grid[gy][gx] == 1:
                    return True
            return False

        blocked_ahead = wall_blocks(bx + dx * 0.30, by + dy * 0.30)
        if dx != 0:
            off = by - cy
            if abs(off) > eps and (blocked_ahead or abs(off) > 0.10):
                if off > 0: self._keys[K_UP]   = self._keys[K_w] = True
                else:       self._keys[K_DOWN] = self._keys[K_s] = True
                return
            if dx < 0: self._keys[K_LEFT]  = self._keys[K_a] = True
            else:      self._keys[K_RIGHT] = self._keys[K_d] = True
        elif dy != 0:
            off = bx - cx
            if abs(off) > eps and (blocked_ahead or abs(off) > 0.10):
                if off > 0: self._keys[K_LEFT]  = self._keys[K_a] = True
                else:       self._keys[K_RIGHT] = self._keys[K_d] = True
                return
            if dy < 0: self._keys[K_UP]   = self._keys[K_w] = True
            else:      self._keys[K_DOWN] = self._keys[K_s] = True

    def _hold(self):
        for k in self._keys:
            self._keys[k] = False

    # ── main per-tick entry point (controller contract) ─────────────────────
    def step(self, straps, dtraps, enemies, hazard_pulse=None):
        self._tick += 1
        if self.player.dead:
            self._hold()
            return

        ptx, pty = self.player.tx, self.player.ty
        moved = (ptx, pty) != self._last_pos
        if moved:
            self._stuck_ticks = 0
            # reaching the current target completes a step: remember where we
            # came from (for anti-backtrack) and clear the target so a new
            # random neighbour is chosen.
            if self._target is not None and (ptx, pty) == self._target:
                self._prev_tile = self._last_pos
                self._target = None
        else:
            self._stuck_ticks += 1
        self._last_pos = (ptx, pty)

        if (ptx, pty) == self.end:
            self._hold()
            return

        # choose a new random neighbour when we have no target, reached it, or
        # have been wedged against a wall for a while (re-roll so a blocked pick
        # cannot stall the walk forever).
        need_pick = (self._target is None
                     or self._stuck_ticks >= self.STEP_TICKS
                     or not self._walkable(*self._target))
        if need_pick:
            self._refresh_static_memory(straps)
            self._target = self._pick_random_neighbour(ptx, pty)
            self._stuck_ticks = 0
            if self.trace_sink is not None and self._target is not None:
                self.trace_sink.append({
                    't': self._tick, 'mode': self.mode,
                    'pos': (ptx, pty), 'next': self._target})

        # fully boxed in (shouldn't happen)
        if self._target is None:
            self._hold()
            return
        dx, dy = self._target[0] - ptx, self._target[1] - pty
        if abs(dx) + abs(dy) != 1:
            # desynced from the body (e.g. pushed off-tile); drop and re-pick.
            self._target = None
            self._hold()
            return
        self._press_toward(dx, dy)

    @property
    def keys(self):
        return self._keys


# === ported from mcts_baseline: monte-carlo tree search baseline agent ===
# drop-in compatible with peagent/astaragent/randomagent (.keys/.step contract,
# shares the run-level expectationmemory as a sims_run sink, uses the same
# forward-sim primitives).  selected via mode="mcts".
# ═══════════════════════════════════════════════════════════════════════════
# mcts baseline agent
# ═══════════════════════════════════════════════════════════════════════════
# a vanilla monte-carlo tree search navigator used as a learning-free baseline
# against the popperian-expectations agent.  it shares the same world (map,
# traps, enemies, fog-of-war perception) and the same forward-simulation
# primitives the pe agent's internal model uses (_clone_dtrap/_clone_enemy,
# _sim_update_*, _sim_move_body, _dtrap_hits_point, _enemy_hits_point), so the
# only thing that differs is the decision algorithm: there is no expectation
# memory, no eec rule base, no causal ledger, no learned dynamics — just uct
# search over primitive moves with random-rollout value estimates.
#
# interface is drop-in compatible with peagent:
# __init__(player, grid, end, room_of, memory, mode, trace_sink)
# .step(straps, dtraps, enemies, hazard_pulse)
# .keys      → pygame key-state dict consumed by player.update
# ═══════════════════════════════════════════════════════════════════════════

class _MCTSNode:
    """A node in the search tree.  `state` is a cloned sim dict (see
    MCTSAgent._clone_state); `untried` is the list of legal actions not yet
    expanded from this node."""
    __slots__ = ("parent", "action", "children", "untried",
                 "visits", "value", "state", "terminal", "reward")

    def __init__(self, state, parent, action, untried, terminal=False,
                 reward=0.0):
        self.parent   = parent
        # action taken from parent to reach here
        self.action   = action
        self.children = []
        # actions not yet expanded
        self.untried  = untried
        self.visits   = 0
        # cumulative reward
        self.value    = 0.0
        self.state    = state
        self.terminal = terminal
        # immediate reward stored at creation
        self.reward   = reward


class MCTSAgent:
    """Learning-free UCT baseline.

    Each decision (every STEP_TICKS world ticks) runs a fresh search from the
    current world state, picks the most-visited root action, and executes it as
    a single cardinal move via the same key-state interface the human/PE agent
    use.  No information is carried between decisions or between runs — every
    search starts from scratch.
    """

    # same actuation cadence and action set as peagent so the comparison is fair.
    # l r u d
    DIRS       = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # + hold/stay
    ACTIONS    = DIRS + [(0, 0)]
    # game ticks per agent decision (matches peagent)
    STEP_TICKS = 10

    # ── search budget ────────────────────────────────────────────────────────
    # mcts iterations per decision
    ITERATIONS    = 120
    # max agent-steps simulated in a rollout
    ROLLOUT_DEPTH = 10
    # exploration constant (≈ sqrt 2)
    UCT_C         = 1.4
    # per-step reward discount
    GAMMA         = 0.97

    # ── reward shaping ───────────────────────────────────────────────────────
    # terminal: walked into a hazard
    DEATH_REWARD = -1.0
    # terminal: reached the exit
    GOAL_REWARD  = +2.0
    # tiny per-step cost discourages dawdling
    STEP_COST    = -0.002
    # reward per tile of net progress toward the exit
    PROGRESS_W   = 0.04

    def __init__(self, player, grid, end, room_of=None, memory=None,
                 mode: str = "mcts", trace_sink: list | None = None):
        self.player   = player
        self.grid     = grid
        self.end      = end
        self.room_of  = room_of or {}
        self.mode     = mode
        self.trace_sink = trace_sink
        # peagent exposes a `memory` with a `sims_run`/`count` counter that the
        # game/hud reads; provide a compatible stand-in so rendering and the
        # benchmark summary keep working without special-casing the agent type.
        self.memory   = memory if memory is not None else ExpectationMemory()

        self._tick     = 0
        self.sim_time  = 0
        self.last_action = None
        self._keys = {K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False,
                      K_w: False,  K_s: False,    K_a: False,    K_d: False}

        # committed cardinal move: once a decision is made we hold those keys
        # for step_ticks ticks so the body actually traverses a whole tile,
        # exactly like the pe agent's route commitment.
        self._commit_action = None
        self._commit_ticks  = 0

        # persistent static-hazard memory (same fog-of-war fairness rule the pe
        # agent uses): a static trap, once seen, is remembered until the agent
        # leaves the room, so the planner never routes back onto a known lethal
        # tile it can no longer see.
        self._known_static_traps: dict = {}
        self._static_mem_room = None

        # diagnostics parity with peagent (read by game on death).
        self._last_obs = None
        self._pm_sink  = None
        self.think_ticks_total = 0

        # renderer-overlay parity (game._draw_agent_plan_overlay reads these).
        self._debug_safe_action   = None
        self._debug_planned_route = []
        self.current_route        = []
        self._crossing_route      = []
        self._pending_plan        = None
        self._window_action       = None

        # a tiny "dynamics" stand-in so game.new_game()'s
        # self._dyn_total += self.agent.dynamics.answers
        # accounting does not crash for the mcts agent.
        self.dynamics = _NullDynamics()

        # ── heuristic for the rollout policy and leaf evaluation ──────────────
        # this is still a standard mcts baseline: the action is chosen purely by
        # the tree (most-visited root child).  we only give the *default policy*
        # inside playouts and the *leaf evaluation* a domain heuristic, which is
        # textbook practice (strong mcts players bias playouts with heuristics).
        # the heuristic is the true shortest-path (geodesic) distance to the
        # goal, precomputed once per maze by a bfs over the wall grid — manhattan
        # distance is deceptive in a maze because the corridor out often leads
        # away from the goal first.  no expectation memory, no learned dynamics:
        # just an admissible distance field, the usual grid-mcts heuristic.
        self._goal_field = self._compute_goal_field()

    def _compute_goal_field(self) -> dict:
        """BFS distance (in tiles) from the goal tile to every reachable open
        tile over the wall grid.  Returns {(tx,ty): dist}; tiles with no path to
        the goal are absent."""
        gx, gy = int(round(self.end[0])), int(round(self.end[1]))
        field = {}
        if not (0 <= gx < COLS and 0 <= gy < ROWS) or self.grid[gy][gx] == 1:
            return field
        from collections import deque
        dq = deque([(gx, gy)])
        field[(gx, gy)] = 0
        while dq:
            cx, cy = dq.popleft()
            d = field[(cx, cy)] + 1
            for ddx, ddy in self.DIRS:
                nx, ny = cx + ddx, cy + ddy
                if not (0 <= nx < COLS and 0 <= ny < ROWS):
                    continue
                if self.grid[ny][nx] == 1 or (nx, ny) in field:
                    continue
                field[(nx, ny)] = d
                dq.append((nx, ny))
        return field

    def _goal_dist_tile(self, tx: int, ty: int) -> float:
        """Geodesic distance from (tx,ty) to the goal; Manhattan + large penalty
        for tiles with no path (so unreachable is always worse than reachable)."""
        d = self._goal_field.get((int(tx), int(ty)))
        if d is not None:
            return float(d)
        return 1000.0 + abs(tx - self.end[0]) + abs(ty - self.end[1])

    def _occupied_tiles(self, s) -> set:
        """Tiles currently covered by the state's tracked movers (enemies +
        dynamic-trap footprints), so the rollout policy can avoid stepping onto
        a known threat instead of marching into it."""
        occ = set()
        for e in s['enemies']:
            ex = getattr(e, 'x', None); ey = getattr(e, 'y', None)
            if ex is not None and ey is not None:
                occ.add((int(ex + 0.5), int(ey + 0.5)))
        for dt in s['dtraps']:
            try:
                tmp = {}
                _map_dtrap_tiles(dt, tmp)
                occ.update(tmp.keys())
            except Exception:
                ox = getattr(dt, 'ox', None); oy = getattr(dt, 'oy', None)
                if ox is not None and oy is not None:
                    occ.add((int(ox + 0.5), int(oy + 0.5)))
        return occ

    # ── property parity with peagent ─────────────────────────────────────────
    @property
    def keys(self):
        return self._keys

    # ── perception: identical fov / fog-of-war rules as peagent.observe ──────
    def observe(self, straps, dtraps, enemies, hazard_pulse=None) -> dict:
        px, py   = self.player.x, self.player.y
        ptx, pty = self.player.tx, self.player.ty
        heading  = _heading_from(self.last_action)

        def visible_tile(tx, ty):
            if not VISION_ENABLED:
                return math.hypot(tx - px, ty - py) <= FOG_REVEAL_DIST
            return _in_fov(tx - ptx, ty - pty, heading)

        def dtrap_visible(dt):
            if not VISION_ENABLED:
                return math.hypot(dt.ox - px, dt.oy - py) <= FOG_REVEAL_DIST + 4
            tmp: dict = {}
            _map_dtrap_tiles(dt, tmp)
            if _in_fov(int(round(dt.ox)) - ptx, int(round(dt.oy)) - pty, heading):
                return True
            return any(visible_tile(tx, ty) for (tx, ty) in tmp)

        trap_map: dict = {}
        here_room_obj = self.room_of.get((ptx, pty))
        if here_room_obj is not getattr(self, "_static_mem_room", here_room_obj):
            left = self._static_mem_room
            self._known_static_traps = {
                pos: k for pos, k in self._known_static_traps.items()
                if self.room_of.get(pos) is not left}
        self._static_mem_room = here_room_obj

        for t in straps:
            if visible_tile(t.tx, t.ty):
                trap_map[(t.tx, t.ty)] = t.kind
                self._known_static_traps[(t.tx, t.ty)] = t.kind
        for (tx, ty), kind in self._known_static_traps.items():
            trap_map.setdefault((tx, ty), kind)

        visible_dtraps = [dt for dt in dtraps if dtrap_visible(dt)]
        for dt in visible_dtraps:
            tmp: dict = {}
            _map_dtrap_tiles(dt, tmp)
            for (tx, ty), kind in tmp.items():
                if visible_tile(tx, ty):
                    trap_map[(tx, ty)] = kind

        visible_enemies = [e for e in enemies
                           if visible_tile(int(e.x), int(e.y))]
        enemy_tiles = _enemy_tiles_from_list(visible_enemies)

        return {'trap_map': trap_map, 'enemy_tiles': enemy_tiles,
                'dtraps': visible_dtraps, 'enemies': visible_enemies,
                'px': self.player.x, 'py': self.player.y,
                'ptx': ptx, 'pty': pty, 'heading': heading,
                'player_statuses': dict(self.player.statuses),
                'pulse_spd_mod': self.player.pulse_spd_mod,
                'hazard_pulse_active': bool(getattr(hazard_pulse, 'active', False)),
                'hazard_pulse_kind': getattr(hazard_pulse, 'kind', None),
                'room_of': self.room_of}

    # ── static obstacle test (walls + known static traps) ────────────────────
    def _blocked(self, tx: int, ty: int) -> bool:
        if not (0 <= tx < COLS and 0 <= ty < ROWS):
            return True
        if self.grid[ty][tx] == 1:
            return True
        return (tx, ty) in self._known_static_traps

    # ── simulation state used internally by the tree search ──────────────────
    # we keep our own compact clone of the world (player body + cloned movers)
    # and advance it one agent-step at a time, reusing the same module-level
    # mover-update and hit-test helpers the pe agent's internal model uses.
    def _clone_state_from_obs(self, obs, room_dtraps, room_enemies):
        return {
            'px': obs['px'], 'py': obs['py'],
            'ptx': obs['ptx'], 'pty': obs['pty'],
            'statuses': dict(obs.get('player_statuses', {})),
            'pulse_spd_mod': obs.get('pulse_spd_mod', 1.0),
            'hazard_pulse_active': obs.get('hazard_pulse_active', False),
            'hazard_pulse_kind': obs.get('hazard_pulse_kind', None),
            'dtraps':  [_clone_dtrap(dt) for dt in room_dtraps],
            'enemies': [_clone_enemy(e)  for e  in room_enemies],
        }

    def _clone_state(self, s):
        return {
            'px': s['px'], 'py': s['py'], 'ptx': s['ptx'], 'pty': s['pty'],
            'statuses': dict(s['statuses']),
            'pulse_spd_mod': s['pulse_spd_mod'],
            'hazard_pulse_active': s['hazard_pulse_active'],
            'hazard_pulse_kind': s['hazard_pulse_kind'],
            'dtraps':  [_clone_dtrap(dt) for dt in s['dtraps']],
            'enemies': [_clone_enemy(e)  for e  in s['enemies']],
        }

    def _legal_actions(self, s):
        ptx, pty = s['ptx'], s['pty']
        acts = [(0, 0)]
        for dx, dy in self.DIRS:
            if not self._blocked(ptx + dx, pty + dy):
                acts.append((dx, dy))
        return acts

    def _advance(self, s, dx, dy):
        """Advance the cloned world by one agent-step (STEP_TICKS game ticks),
        moving the body toward the target tile while the movers update.
        Returns (next_state, dead, reached_goal).  Mutates `s` in place; caller
        clones first if it needs the parent preserved."""
        tx, ty = s['ptx'] + dx, s['pty'] + dy
        stub = _SimPlayer(s['px'], s['py'])
        stub.pulse_spd_mod = s['pulse_spd_mod']

        pulse_mod = s['pulse_spd_mod']
        if s['hazard_pulse_active'] and s['hazard_pulse_kind'] == 'speed':
            pulse_mod = min(pulse_mod, 0.5)
        spd = _sim_player_speed(s['statuses'], pulse_mod)

        move_dx = (tx - s['px']) if (dx or dy) else 0.0
        move_dy = (ty - s['py']) if (dx or dy) else 0.0

        dead = False
        for _ in range(self.STEP_TICKS):
            stub.x, stub.y = _sim_move_body(stub.x, stub.y, move_dx, move_dy,
                                            spd, self.grid)
            for dt in s['dtraps']:
                _sim_update_dtrap(dt, stub)
            for e in s['enemies']:
                _sim_update_enemy(e)
            if not dead:
                for dt in s['dtraps']:
                    if _dtrap_hits_point(dt, stub.x, stub.y):
                        dead = True
                        break
            if not dead:
                for e in s['enemies']:
                    if _enemy_hits_point(e, stub.x, stub.y):
                        dead = True
                        break
            if dead:
                break

        s['px'], s['py'] = stub.x, stub.y
        s['ptx'], s['pty'] = int(stub.x + 0.5), int(stub.y + 0.5)
        s['statuses'] = {k: v - self.STEP_TICKS
                         for k, v in s['statuses'].items()
                         if v > self.STEP_TICKS}

        reached = (math.hypot(s['px'] - self.end[0],
                              s['py'] - self.end[1]) < 0.8)
        return s, dead, reached

    def _dist_to_goal(self, s):
        return abs(s['ptx'] - self.end[0]) + abs(s['pty'] - self.end[1])

    # ── uct machinery ────────────────────────────────────────────────────────
    def _uct_select(self, node):
        logN = math.log(node.visits + 1.0)
        best, best_score = None, -1e18
        for ch in node.children:
            exploit = ch.value / ch.visits if ch.visits else 0.0
            explore = self.UCT_C * math.sqrt(logN / (ch.visits + 1e-9))
            score = exploit + explore
            if score > best_score:
                best_score, best = score, ch
        return best

    def _expand(self, node):
        dx, dy = node.untried.pop(random.randrange(len(node.untried)))
        child_state = self._clone_state(node.state)
        child_state, dead, reached = self._advance(child_state, dx, dy)
        terminal = dead or reached
        reward = self.STEP_COST
        if dead:
            reward += self.DEATH_REWARD
        elif reached:
            reward += self.GOAL_REWARD
        untried = [] if terminal else self._legal_actions(child_state)
        child = _MCTSNode(child_state, node, (dx, dy), untried,
                          terminal=terminal, reward=reward)
        node.children.append(child)
        return child

    def _rollout(self, state):
        """Heuristic default policy with heuristic leaf evaluation.

        Standard MCTS practice: instead of a uniformly random playout (which on
        a maze this large almost never reaches the goal, so the search gets no
        signal), the default policy is biased toward the goal by the geodesic
        field and avoids tiles a tracked mover currently occupies.  If the
        playout neither reaches the goal nor dies within ROLLOUT_DEPTH, the leaf
        is EVALUATED heuristically by how close to the exit it got, rather than
        returning a flat zero.  The recommendation policy is unchanged — the
        action is still the most-visited root child — so this remains MCTS, not
        a hand-coded planner."""
        s = self._clone_state(state)
        total, discount = 0.0, 1.0
        d_best = self._goal_dist_tile(s['ptx'], s['pty'])
        dead = reached = False
        for _ in range(self.ROLLOUT_DEPTH):
            acts = self._legal_actions(s)
            if len(acts) > 1:
                # prefer to keep moving
                acts = [a for a in acts if a != (0, 0)]
            occupied = self._occupied_tiles(s)
            # ε-greedy on the geodesic heuristic: 75% pick the goal-ward move
            # (penalising a step onto an occupied tile so the playout routes
            # around threats), 25% explore at random among non-occupied moves.
            if random.random() < 0.75:
                best_a, best_h = None, 1e18
                for a in acts:
                    ntx, nty = s['ptx'] + a[0], s['pty'] + a[1]
                    h = self._goal_dist_tile(ntx, nty)
                    if (ntx, nty) in occupied:
                        h += 50.0
                    if h < best_h:
                        best_h, best_a = h, a
                a = best_a if best_a is not None else random.choice(acts)
            else:
                free = [a for a in acts
                        if (s['ptx'] + a[0], s['pty'] + a[1]) not in occupied]
                a = random.choice(free if free else acts)

            s, dead, reached = self._advance(s, a[0], a[1])
            r = self.STEP_COST
            if dead:
                r += self.DEATH_REWARD
            elif reached:
                r += self.GOAL_REWARD
            total += discount * r
            d_best = min(d_best, self._goal_dist_tile(s['ptx'], s['pty']))
            discount *= self.GAMMA
            if dead or reached:
                break

        # ── heuristic leaf evaluation (only if the playout was truncated) ─────
        # convert closest geodesic approach into a bounded bonus in roughly
        # [0, goal_reward): closer to the exit ⇒ higher estimated value.  this
        # gives the search a dense gradient toward the goal without a terminal
        # being reached, which is what lets goal-ward branches out-score
        # aimless ones near spawn.
        if not (dead or reached):
            field_max = self._goal_field_max()
            closeness = max(0.0, (field_max - d_best) / max(1.0, field_max))
            total += discount * self.GOAL_REWARD * closeness
        return total

    def _goal_field_max(self) -> float:
        m = getattr(self, "_gf_max", None)
        if m is None:
            m = max(self._goal_field.values()) if self._goal_field else 1.0
            self._gf_max = float(m)
        return self._gf_max

    def _backprop(self, node, value):
        # standard uct backup: accumulate the (discounted) return up the path so
        # each node's value/visits gives the mean return of simulations through
        # it.  the leaf's own immediate reward is folded in as we ascend.
        while node is not None:
            node.visits += 1
            node.value  += value
            value = node.reward + self.GAMMA * value
            node = node.parent

    def _search(self, root_state):
        # bracket the global rng once for the entire search.  every rollout
        # uses _sim_update_dtrap (no per-update save/restore), and the
        # rollout/expansion randomness draws from the same global stream, so we
        # snapshot here and restore at the end — the real world's maze/trap/
        # enemy sequence is left exactly as it was before deliberation.
        _rng_state = random.getstate()
        try:
            return self._search_inner(root_state)
        finally:
            random.setstate(_rng_state)

    def _search_inner(self, root_state):
        root = _MCTSNode(root_state, None, None,
                         self._legal_actions(root_state))
        if not root.untried and not root.children:
            return (0, 0)
        for _ in range(self.ITERATIONS):
            node = root
            # 1. selection
            while not node.untried and node.children and not node.terminal:
                node = self._uct_select(node)
            # 2. expansion
            if node.untried and not node.terminal:
                node = self._expand(node)
            # 3. simulation
            value = 0.0 if node.terminal else self._rollout(node.state)
            # 4. back-propagation
            self._backprop(node, value)
        # most-robust action: the root child with the highest visit count — the
        # standard uct recommendation policy.  no external heuristic overrides
        # the tree: the move the search actually preferred is the move taken,
        # win or lose.
        if not root.children:
            return (0, 0)
        best = max(root.children, key=lambda c: c.visits)
        return best.action

    # ── per-tick driver (called by game._step_world) ─────────────────────────
    def step(self, straps, dtraps, enemies, hazard_pulse=None):
        self._tick    += 1
        self.sim_time += 1
        self._room_dtraps  = list(dtraps)
        self._room_enemies = list(enemies)

        obs = self.observe(straps, dtraps, enemies, hazard_pulse)
        self._last_obs = obs

        if self.player.dead:
            for k in self._keys:
                self._keys[k] = False
            return

        # hold a committed cardinal move for a full step_ticks window so the
        # round body actually crosses the tile before re-deciding.
        if self._commit_ticks > 0 and self._commit_action is not None:
            self._commit_ticks -= 1
            self._apply_action(obs, self._commit_action)
            return

        # new decision: run a fresh search from the current world state.
        root_state = self._clone_state_from_obs(obs, self._room_dtraps,
                                                self._room_enemies)
        action = self._search(root_state)

        if action == (0, 0):
            # decided to hold position this window.
            self._commit_action = (0, 0)
            self._commit_ticks  = self.STEP_TICKS - 1
            for k in self._keys:
                self._keys[k] = False
            self._debug_safe_action   = (0, 0)
            self._debug_planned_route = []
            if self.trace_sink is not None:
                self.trace_sink.append(dict(
                    tick=self._tick, mode=self.mode,
                    tile=(obs['ptx'], obs['pty']), action=(0, 0),
                    source="mcts", sims_used=self.ITERATIONS,
                    plan_latency=0, mem_rules=0, rule=""))
            return

        self._commit_action = action
        self._commit_ticks  = self.STEP_TICKS - 1
        self.last_action    = action
        self._debug_safe_action   = action
        self._debug_planned_route = [(obs['ptx'] + action[0],
                                      obs['pty'] + action[1])]
        if self.trace_sink is not None:
            self.trace_sink.append(dict(
                tick=self._tick, mode=self.mode,
                tile=(obs['ptx'], obs['pty']), action=action,
                source="mcts", sims_used=self.ITERATIONS,
                plan_latency=0, mem_rules=0, rule=""))
        self._apply_action(obs, action)

    def _apply_action(self, obs, action):
        dx, dy = action
        for k in self._keys:
            self._keys[k] = False
        if action == (0, 0):
            return
        cx, cy = obs['ptx'], obs['pty']
        center_eps = 0.08
        # axis-centering so the round body slides down the corridor lane
        # instead of wedging on wall corners (same idea peagent uses).
        if dx != 0:
            off_y = self.player.y - cy
            if off_y > center_eps:
                self._keys[K_UP] = True; self._keys[K_w] = True
            elif off_y < -center_eps:
                self._keys[K_DOWN] = True; self._keys[K_s] = True
            if dx == -1:
                self._keys[K_LEFT] = True; self._keys[K_a] = True
            else:
                self._keys[K_RIGHT] = True; self._keys[K_d] = True
        elif dy != 0:
            off_x = self.player.x - cx
            if off_x > center_eps:
                self._keys[K_LEFT] = True; self._keys[K_a] = True
            elif off_x < -center_eps:
                self._keys[K_RIGHT] = True; self._keys[K_d] = True
            if dy == -1:
                self._keys[K_UP] = True; self._keys[K_w] = True
            else:
                self._keys[K_DOWN] = True; self._keys[K_s] = True


class Player:
    SPEED=0.10

    def __init__(self, tx, ty):
        self.x=float(tx); self.y=float(ty)
        self.tx=tx; self.ty=ty
        self.hp=1; self.max_hp=1
        self.statuses={}
        # no initial invincibility — agent must be vulnerable from frame 1 so
        # visible trap hits register immediately.  (was 180 ticks = 3 sec, which
        # caused traps to visibly trigger without damage on spawn.)
        self.dmg_flash=0; self.inv=0; self.dead=False
        self.death_kind=None; self.death_label=None; self.death_predictable=None
        self.move_t=0; self.facing=0.0
        self.msgs=[]
        # legacy (hazardpulse push removed)
        self.pulse_push = (0.0, 0.0)
        # from hazardpulse flux
        self.pulse_spd_mod = 1.0

    def take_damage(self, dmg, eff, lbl, col, kind=None):
        if self.inv>0: return
        self.hp=0; self.dead=True; self.dmg_flash=22; self.inv=45
        # death-cause attribution (diagnostic): record what killed the agent
        # and whether that hazard was fully predictable.  a predictable killer
        # means the forward model should have foreseen the collision.
        self.death_kind = kind
        self.death_label = lbl
        self.death_predictable = (hazard_is_predictable(kind)
                                  if kind is not None else None)
        if eff and eff in SDEFS and SDEFS[eff]["dur"]>0:
            self.statuses[eff]=SDEFS[eff]["dur"]
        self.push_msg(f"{lbl}!",col)

    def push_msg(self, txt, col):
        self.msgs.append([txt,col,150])

    def update(self, keys, grid):
        if self.dead: return
        if self.inv>0: self.inv-=1
        if self.dmg_flash>0: self.dmg_flash-=1
        slow=0.
        for eff in list(self.statuses):
            self.statuses[eff]-=1
            if self.statuses[eff]<=0: del self.statuses[eff]; continue
            sd=SDEFS[eff]; slow=max(slow,sd["slow"])
        spd=self.SPEED*(1-slow)*self.pulse_spd_mod
        mx=my=0.
        if keys[K_w] or keys[K_UP]:    my-=1.
        if keys[K_s] or keys[K_DOWN]:  my+=1.
        if keys[K_a] or keys[K_LEFT]:  mx-=1.
        if keys[K_d] or keys[K_RIGHT]: mx+=1.
        ml=math.hypot(mx,my)
        if ml>0: mx/=ml; my/=ml; self.facing=math.atan2(my,mx)
        if mx or my: self.move_t+=1
        # axis-separated collision
        m=PLAYER_WALL_RADIUS
        def blocked(x,y):
            for dx2,dy2 in [(m,0),(-m,0),(0,m),(0,-m)]:
                # player coordinates use integer tile centers (see tx=int(x+.5)).
                # use the same nearest-tile convention for collision probes; plain
                # int() floors left/up probes into adjacent wall tiles and wedges
                # the player in one-tile hallways.
                tx2=int(x+dx2+.5); ty2=int(y+dy2+.5)
                if 0<=tx2<COLS and 0<=ty2<ROWS and grid[ty2][tx2]==1: return True
            return False
        nx=self.x+mx*spd; ny=self.y+my*spd
        if not blocked(nx,self.y): self.x=nx
        if not blocked(self.x,ny): self.y=ny
        # apply shockwave push (from hazardpulse)
        ppx, ppy = self.pulse_push
        if ppx or ppy:
            npx = self.x + ppx; npy = self.y + ppy
            if not blocked(npx, self.y): self.x = npx
            if not blocked(self.x, npy): self.y = npy
        # consumed each frame
        self.pulse_push = (0.0, 0.0)
        self.tx=int(self.x+.5); self.ty=int(self.y+.5)
        self.msgs=[[t,c,n-1] for t,c,n in self.msgs if n>1]

    def draw(self, surf, cam_x, cam_y, ts, font_sm):
        sx=int((self.x-cam_x)*ts)
        sy=int((self.y-cam_y)*ts)
        if FORMAL_STYLE:
            r = int(ts * PLAYER_WALL_RADIUS)
            damaged = self.dmg_flash > 0 and self.dmg_flash % 4 < 2
            fill = (200, 60, 60) if damaged else FML["agent"]
            edge = (150, 30, 30) if damaged else FML["agent_ed"]
            # status effect: thin coloured ring (no glow/pulse)
            if self.statuses:
                first_eff = next(iter(self.statuses))
                sc = SDEFS[first_eff]["col"]
                pygame.draw.circle(surf, sc, (sx, sy), r + 3, 1)
            pygame.draw.circle(surf, fill, (sx, sy), r)
            pygame.draw.circle(surf, edge, (sx, sy), r, 1)
            # facing tick
            fa = self.facing
            pygame.draw.line(surf, (255,255,255), (sx, sy),
                             (sx + int(math.cos(fa)*r), sy + int(math.sin(fa)*r)), 2)
            f = _formal_font(9, bold=True)
            t = f.render("A", True, (255,255,255))
            surf.blit(t, (sx - t.get_width()//2, sy - t.get_height()//2 - 1))
            for i,(txt,tcol,timer) in enumerate(reversed(self.msgs[-3:])):
                ms = font_sm.render(txt, True, FML["ink"])
                ms.set_alpha(min(255, timer*3))
                surf.blit(ms, (sx - ms.get_width()//2, sy - r - 18 - i*14))
            return
        r=max(6,int(ts*PLAYER_WALL_RADIUS))
        fa=self.facing
        damaged=self.dmg_flash>0 and self.dmg_flash%4<2
        armor_col=(55,105,185) if not damaged else (200,40,40)
        skin_col=(230,185,140)
        t_ms=pygame.time.get_ticks()

        # ── ground shadow ────────────────────────────────────────────────────
        gs=asurf(r*2+6,r+4)
        pygame.draw.ellipse(gs,(0,0,0,55),(0,0,r*2+6,r+4))
        surf.blit(gs,(sx-r-3,sy-2))

        # ── status aura rings ────────────────────────────────────────────────
        for i,eff in enumerate(self.statuses):
            sc=SDEFS[eff]["col"]
            pulse=0.4+0.4*math.sin(t_ms*0.006+i*1.2)
            ar=r+6+i*4
            gs2=asurf(ar*2+2,ar*2+2)
            pygame.draw.circle(gs2,(*sc,int(70*pulse)),(ar+1,ar+1),ar,2)
            surf.blit(gs2,(sx-ar-1,sy-ar-1))

        # ── legs (walk animation) ────────────────────────────────────────────
        # -0.7 to +0.7
        walk=math.sin(self.move_t*0.35)*0.7
        leg_col=lerpc(armor_col,(0,0,0),0.4)
        # perpendicular to facing direction
        perp=(fa+math.pi/2)
        pw=int(math.cos(perp)*r*0.4); ph=int(math.sin(perp)*r*0.4)
        fw=int(math.cos(fa)*r*0.35);  fh=int(math.sin(fa)*r*0.35)
        # left leg
        llx=sx-pw+int(fw*walk*0.6); lly=sy-ph+int(fh*walk*0.6)
        pygame.draw.circle(surf,leg_col,(llx,lly+r//2),r//3+1)
        # right leg (opposite phase)
        rlx=sx+pw-int(fw*walk*0.6); rly=sy+ph-int(fh*walk*0.6)
        pygame.draw.circle(surf,leg_col,(rlx,rly+r//2),r//3+1)

        # ── body (main circle) ───────────────────────────────────────────────
        pygame.draw.circle(surf,lerpc(armor_col,(0,0,0),0.5),(sx,sy),r)
        pygame.draw.circle(surf,armor_col,(sx,sy),r-1)
        # chest highlight
        pygame.draw.circle(surf,lerpc(armor_col,WHITE,0.3),(sx-r//5,sy-r//5),r//3)

        # ── arms ────────────────────────────────────────────────────────────
        arm_col=lerpc(armor_col,(0,0,0),0.25)
        # opposite swing to legs
        alx=sx-pw+int(-fw*walk*0.8); aly=sy-ph+int(-fh*walk*0.8)
        arx=sx+pw-int(-fw*walk*0.8); ary=sy+ph-int(-fh*walk*0.8)
        pygame.draw.circle(surf,arm_col,(alx,aly),r//3)
        pygame.draw.circle(surf,arm_col,(arx,ary),r//3)

        # ── head ────────────────────────────────────────────────────────────
        hx=sx+int(math.cos(fa)*r*0.18); hy=sy+int(math.sin(fa)*r*0.18)
        hr=int(r*0.52)
        pygame.draw.circle(surf,lerpc(skin_col,(0,0,0),0.3),(hx,hy),hr)
        pygame.draw.circle(surf,skin_col,(hx,hy),hr-1)

        # eyes — two dots offset left and right of facing direction
        eye_dist=hr*0.38
        eye_fwd=hr*0.25
        ex1=hx+int(math.cos(fa)*eye_fwd)+int(math.cos(fa+math.pi/2)*eye_dist)
        ey1=hy+int(math.sin(fa)*eye_fwd)+int(math.sin(fa+math.pi/2)*eye_dist)
        ex2=hx+int(math.cos(fa)*eye_fwd)+int(math.cos(fa-math.pi/2)*eye_dist)
        ey2=hy+int(math.sin(fa)*eye_fwd)+int(math.sin(fa-math.pi/2)*eye_dist)
        pygame.draw.circle(surf,(20,18,30),(int(ex1),int(ey1)),max(1,hr//3))
        pygame.draw.circle(surf,(20,18,30),(int(ex2),int(ey2)),max(1,hr//3))
        # eye shine
        pygame.draw.circle(surf,WHITE,(int(ex1)-1,int(ey1)-1),max(1,hr//5))
        pygame.draw.circle(surf,WHITE,(int(ex2)-1,int(ey2)-1),max(1,hr//5))

        # ── floating combat messages ─────────────────────────────────────────
        for i,(txt,tcol,timer) in enumerate(reversed(self.msgs[-4:])):
            ms=font_sm.render(txt,True,tcol)
            ms.set_alpha(min(255,timer*3))
            surf.blit(ms,(sx-ms.get_width()//2,sy-r-22-i*15))


# =============================================================================
# game
# =============================================================================
class Game:
    def __init__(self, mode: str = "popperian", headless: bool = False,
                 max_ticks: int | None = None):
        # agent type (feedback #2 baselines)
        self.mode      = mode
        # benchmark mode: no rendering, no fps cap
        self.headless  = headless
        # total world ticks for headless runs
        self.max_ticks = max_ticks
        # ── per-world rng seed ───────────────────────────────────────────────
        # callers seed the global rng (random.seed(seed)) immediately before
        # constructing the game, so the maze itself is reproducible.  snapshot
        # that state now and derive a stable integer from it; new_game() re-reads
        # it and uses it to seed each nondeterministic hazard's private rng, so
        # nondeterministic-hazard motion is identical across agents on the same
        # seed, not just the static maze layout.
        self._world_seed = _stable_hash(random.getstate())
        pygame.init()
        self.screen=pygame.display.set_mode((W + SIDE_W + IMAG_W, WIN_H))
        pygame.display.set_caption("Room Maze -- PE Uncertainty Demo")
        self.clock=pygame.time.Clock()
        self.f_big=pygame.font.SysFont("consolas",30,bold=True)
        self.f_med=pygame.font.SysFont("consolas",17)
        self.f_sm =pygame.font.SysFont("consolas",13)
        self.tick=0
        # total ticks, not reset by new_game
        self._bench_tick = 0
        # deliberation ticks across all runs
        self._think_total = 0
        # dynamics-law planning answers across runs
        self._dyn_total   = 0
        # deaths (one-hit world) across all runs
        self._damage_total = 0
        # per-decision trace (feedback #4)
        self.trace = []
        self.agent_mode = False
        self.agent = None
        # wiped after every run (win or lose)
        self.agent_memory = ExpectationMemory()
        # set true when any run ends
        self._reset_memory_on_restart = False
        # ticks elapsed since win/dead in agent mode
        self._restart_timer = 0
        # runs where agent reached the exit
        self._completions   = 0
        # runs where agent died
        self._fails         = 0
        # death-cause diagnostics: a death to a fully predictable hazard means
        # the forward model failed to foresee a knowable collision (a bug),
        # whereas a death to a roamer/stochastic trap can be legitimate.
        self._deaths_predictable   = 0
        self._deaths_unpredictable = 0
        self._death_by_kind        = {}
        # ── live-session results csv ─────────────────────────────────────────
        # created the instant the program starts (not only under --compare), so
        # an interactive play/agent session always leaves a results file in the
        # user's downloads folder.  one row is appended + fsync'd as each run
        # finishes, so the file is always a complete, valid csv even if the
        # window is closed mid-session.  headless benchmark trials manage their
        # own csv via run_paired_benchmark and must not open this one.
        self._live_csv_fh = None
        self._live_csv_writer = None
        self._live_run_idx = 0
        if not self.headless:
            self._open_live_csv()
        self.new_game()

    def _open_live_csv(self):
        """Open (and header) the per-session results CSV in Downloads.

        Falls back to the current working directory when the Downloads path
        does not exist (e.g. a non-Windows machine), mirroring the --compare
        output-dir logic so behaviour is consistent across launch modes.
        """
        import csv as _csv, time as _time
        out_dir = r"C:/Users/kper2/Downloads"
        if not os.path.isdir(out_dir):
            out_dir = os.getcwd()
        fname = _time.strftime("maze_session_%Y%m%d_%H%M%S.csv")
        path = os.path.join(out_dir, fname)
        self._live_csv_fields = [
            "run", "mode", "outcome", "win", "death", "timeout",
            "ticks", "rules", "valid_rules",
            "deaths_predictable", "deaths_unpredictable",
            "death_kind", "death_predictable",
        ]
        try:
            self._live_csv_fh = open(path, "w", newline="", encoding="utf-8")
            self._live_csv_writer = _csv.DictWriter(
                self._live_csv_fh, fieldnames=self._live_csv_fields)
            self._live_csv_writer.writeheader()
            self._live_csv_fh.flush()
            self._live_csv_path = path
            print(f"[session CSV] writing results to {path}")
        except OSError as exc:
            # never let a file-permission problem stop the game from running.
            print(f"[session CSV] could not open results file: {exc}")
            self._live_csv_fh = None
            self._live_csv_writer = None

    def _write_live_csv_row(self, outcome: str):
        """Append one fsync'd row for a just-finished interactive run."""
        if self._live_csv_writer is None:
            return
        self._live_run_idx += 1
        mem = self.agent_memory
        try:
            valid_rules = sum(1 for r in mem.rules
                              if r.reliability_lcb() > 0.0)
        except Exception:
            valid_rules = 0
        row = {
            "run": self._live_run_idx,
            "mode": self.mode,
            "outcome": outcome,
            "win": int(outcome == "win"),
            "death": int(outcome == "death"),
            "timeout": int(outcome == "timeout"),
            "ticks": self.tick,
            "rules": mem.count,
            "valid_rules": valid_rules,
            "deaths_predictable": self._deaths_predictable,
            "deaths_unpredictable": self._deaths_unpredictable,
            "death_kind": (getattr(self.player, "death_kind", "")
                           if outcome == "death" else ""),
            "death_predictable": (getattr(self.player, "death_predictable", "")
                                  if outcome == "death" else ""),
        }
        try:
            self._live_csv_writer.writerow(row)
            self._live_csv_fh.flush()
            os.fsync(self._live_csv_fh.fileno())
        except (OSError, ValueError):
            pass

    def new_game(self):
        # snapshot the seed-pinned global rng state before world generation
        # consumes it, so the world seed tracks the maze being built on this
        # call (e.g. after pressing r for a fresh maze, or each benchmark seed).
        self._world_seed = _stable_hash(random.getstate())
        self.grid,self.rooms,self.floors,self.enemies=generate_world()
        self.room_of={}
        for room in self.rooms:
            for ry in range(room.y,room.y+room.h):
                for rx in range(room.x,room.x+room.w):
                    self.room_of[(rx,ry)]=room
        self.straps=[]; self.strap_map={}; self.dtraps=[]
        for room in self.rooms:
            for t in room.straps:
                self.straps.append(t); self.strap_map[(t.tx,t.ty)]=t
            for dt in room.dtraps:
                self.dtraps.append(dt)
        s,e=self.rooms[0],self.rooms[-1]; bd=0
        for i,r1 in enumerate(self.rooms):
            for r2 in self.rooms[i+1:]:
                d=abs(r1.cx-r2.cx)+abs(r1.cy-r2.cy)
                if d>bd: bd=d; s,e=r1,r2
        self.start=(s.cx,s.cy); self.end=(e.cx,e.cy)
        self.start_room=s
        self.end_room=e
        # variety guarantee: every non-start/end room that can physically hold a
        # trap gets at least one, so no room is left with only roaming enemies.
        # (a safety net for the rare room population misses, independent of why.)
        _safe = set()
        _safe |= safe_zone_tiles(self.start[0], self.start[1], START_SAFE_RADIUS)
        _safe |= safe_zone_tiles(self.end[0], self.end[1], EXIT_SAFE_RADIUS)
        for room in self.rooms:
            if room is s or room is e:
                continue
            if room.straps or room.dtraps:
                continue
            deep = [t for t in _room_deep_tiles(room, self.grid) if t not in _safe]
            if not deep:
                continue
            sp = RTYPES[room.rtype]["straps"]
            random.shuffle(deep)
            for tx, ty in deep:
                cand = [StaticTrap(tx, ty, random.choice(sp), room.rtype)]
                if _room_hazard_layout_passable(room, self.grid, cand, []):
                    room.straps = cand
                    self.straps.append(cand[0])
                    self.strap_map[(tx, ty)] = cand[0]
                    break
        # no enemies in spawn room
        s.enemies=[]
        self.enemies=[e2 for r in self.rooms for e2 in r.enemies]
        self.player=Player(*self.start)
        self.state="playing"; self.tick=0
        self._restart_timer  = 0
        # ensures each run is counted exactly once
        self._counted_outcome = False
        self.visited=set()
        self.particles=[]
        self.stats=dict(steps=0,damage_taken=0,traps_triggered=0)
        self.last_room=None
        self.dmg_overlay=0
        # the pulse gets its own deterministic rng seeded from this world's seed,
        # so its kind/duration/speed-mod sequence is fixed per seed and identical
        # across agents (independent of how any agent moves).
        self.hazard_pulse=HazardPulse(rng=random.Random(
            _stable_hash(self._world_seed, "pulse")))
        # ── reproducible nondeterministic hazards ────────────────────────────
        # world generation above (generate_world + the variety builders) ran on
        # the global, seed-pinned stream, so the static layout and each hazard's
        # private re-arm rng seed are already identical across agents.  every
        # nondeterministic hazard (homing/randomly-re-arming traps, roaming
        # enemies, the pulse) now carries its own rng, so its motion is a pure
        # function of the world seed — the tick on which it happens to draw
        # (which can depend on the player's path) never shifts another hazard's
        # sequence.  predictable hazards draw no rng during motion at all.
        # on-re-entry relocation reseeds the global rng per (room, visit#) so a
        # rebuilt room's layout is also identical across agents (see
        # _relocate_traps).
        # id(room) -> times relocated (for reseed)
        self._reloc_counts = {}
        # track which room the player was in last frame for re-entry detection
        self._prev_room=None
        # new agent with fresh nav state.  every run is independent: the
        # expectation memory and all learned dynamics laws are wiped at the
        # start of each run (win or lose), so the agent always starts from
        # scratch with only its innate embodiment priors.
        if self.agent is not None:
            self._think_total += self.agent.think_ticks_total
            self._dyn_total   += self.agent.dynamics.answers
        if self._reset_memory_on_restart:
            # forget everything
            self.agent_memory = ExpectationMemory()
            self._reset_memory_on_restart = False
        if self.mode == "astar":
            # a* baseline: a self-contained shortest-path agent with none of the
            # pe machinery.  it shares the same controller contract (.keys /
            # .step) and the run-level expectationmemory (used only as a sink for
            # the sims_run search-effort counter), so the benchmark harness
            # treats it uniformly with the pe agent.
            self.agent = AStarAgent(self.player, self.grid, self.end,
                                    room_of=self.room_of, memory=self.agent_memory,
                                    mode=self.mode, trace_sink=self.trace)
        elif self.mode == "random":
            # random-walk floor baseline: steps onto a random walkable neighbour
            # each decision, no goal/pathfinding/hazard reasoning.  its rng is
            # seeded from the world seed so the walk is reproducible per seed and
            # independent of the global (hazard) stream.
            self.agent = RandomAgent(self.player, self.grid, self.end,
                                     room_of=self.room_of, memory=self.agent_memory,
                                     mode=self.mode, trace_sink=self.trace,
                                     world_seed=self._world_seed)
        elif self.mode == "mcts":
            # mcts baseline: a learning-free uct navigator (no expectation memory,
            # no eec rules, no learned dynamics) sharing the same controller
            # contract and forward-sim primitives as the pe agent.  it uses the
            # run-level expectationmemory only as a sink for the sims_run counter
            # so the benchmark harness treats it uniformly.
            self.agent = MCTSAgent(self.player, self.grid, self.end,
                                   room_of=self.room_of, memory=self.agent_memory,
                                   mode=self.mode, trace_sink=self.trace)
        else:
            self.agent = PEAgent(self.player, self.grid, self.end,
                                 room_of=self.room_of, memory=self.agent_memory,
                                 mode=self.mode, trace_sink=self.trace)
        # drive the imagination panel only when there is a window to show it,
        # so headless benchmark runs pay none of its cost.
        self.agent._visualise_imagination = not self.headless
        # collect predictable-death post-mortems across all runs (diagnostic).
        if not hasattr(self, "_pm_all"):
            self._pm_all = []
        self.agent._pm_sink = self._pm_all


    def _geodesic_optimal_len(self) -> int:
        """Shortest wall-respecting path length (in tiles) from start to goal,
        via BFS over the grid.  Used as the denominator for path efficiency."""
        from collections import deque
        sx, sy = int(round(self.start[0])), int(round(self.start[1]))
        gx, gy = int(round(self.end[0])),   int(round(self.end[1]))
        if self.grid[sy][sx] == 1 or self.grid[gy][gx] == 1:
            return -1
        dq = deque([(sx, sy, 0)]); seen = {(sx, sy)}
        while dq:
            cx, cy, d = dq.popleft()
            if (cx, cy) == (gx, gy):
                return d
            for ddx, ddy in ((-1,0),(1,0),(0,-1),(0,1)):
                nx, ny = cx+ddx, cy+ddy
                if (0 <= nx < COLS and 0 <= ny < ROWS
                        and self.grid[ny][nx] != 1 and (nx, ny) not in seen):
                    seen.add((nx, ny)); dq.append((nx, ny, d+1))
        # goal unreachable (shouldn't happen for a valid maze)
        return -1

    def run_single_trial(self, max_ticks: int) -> dict:
        """Run ONE maze attempt headlessly (no auto-restart) and return a flat
        dict of per-run metrics for the comparison CSV.  The maze is whatever
        new_game() built for the current (seeded) world, so calling this after
        random.seed(S) + new_game() gives a reproducible, paired trial.

        Metrics captured per run:
          outcome        — 'win' | 'death' | 'timeout'
          ticks          — world ticks until outcome (or the cap)
          decisions      — number of agent decisions made
          path_tiles     — distinct-step path length the body actually walked
          optimal_tiles  — shortest wall-respecting start→goal distance
          path_ratio     — path_tiles / optimal_tiles (≥1; lower is straighter)
          sim_steps      — forward-simulation steps executed (search/IM cost)
          sims_run/skipped/reuse_pct — PE memory accounting (0 for MCTS)
          rules/valid_rules          — learned + reliability-passing (PE only)
          think_ticks    — deliberation ticks
          close_calls    — steps ending within 1 tile of a live mover
          death_kind / death_predictable — hazard attribution on death
        """
        self.agent_mode = True
        self._counted_outcome = False
        optimal = self._geodesic_optimal_len()

        # reset per-run accumulators.
        path_tiles = 0
        close_calls = 0
        decisions_before = len(self.trace)
        last_tile = (self.player.tx, self.player.ty)
        sims_run_0    = self.agent_memory.sims_run
        sims_skip_0   = self.agent_memory.sims_skipped
        # estimate forward-sim cost for mcts (no memory counter): iterations ×
        # rollout depth per decision is the dominant simulation work.
        is_mcts = (self.mode == "mcts")

        t = 0
        outcome = "timeout"
        while t < max_ticks:
            self._single_step()
            t += 1
            cur = (self.player.tx, self.player.ty)
            if cur != last_tile:
                path_tiles += 1
                last_tile = cur
            # close-call: a live mover sits on an adjacent tile this tick.
            if self._near_live_mover(cur):
                close_calls += 1
            if self.player.dead:
                outcome = "death"; break
            if math.hypot(self.player.x - self.end[0],
                          self.player.y - self.end[1]) < 0.8:
                outcome = "win"; break

        mem = self.agent_memory
        decisions = len(self.trace) - decisions_before
        sims_run  = mem.sims_run - sims_run_0
        sims_skip = mem.sims_skipped - sims_skip_0
        reuse_tot = sims_run + sims_skip
        if is_mcts and 'MCTSAgent' in globals():
            sim_steps = decisions * MCTSAgent.ITERATIONS * MCTSAgent.ROLLOUT_DEPTH
        else:
            # each pe sim is one internal-model evaluation
            sim_steps = sims_run
        try:
            valid_rules = sum(1 for r in mem.rules
                              if r.reliability_lcb() > 0.0)
        except Exception:
            valid_rules = 0
        think = (self.agent.think_ticks_total if self.agent else 0)

        return dict(
            mode=self.mode,
            outcome=outcome,
            win=int(outcome == "win"),
            death=int(outcome == "death"),
            timeout=int(outcome == "timeout"),
            ticks=t,
            decisions=decisions,
            path_tiles=path_tiles,
            optimal_tiles=optimal,
            path_ratio=(round(path_tiles / optimal, 3)
                        if optimal and optimal > 0 else -1),
            sim_steps=sim_steps,
            sims_run=sims_run,
            sims_skipped=sims_skip,
            reuse_pct=(round(100.0 * sims_skip / reuse_tot, 1)
                       if reuse_tot else 0.0),
            rules=mem.count,
            valid_rules=valid_rules,
            think_ticks=think,
            close_calls=close_calls,
            death_kind=(getattr(self.player, "death_kind", None)
                        if outcome == "death" else ""),
            death_predictable=("" if outcome != "death"
                               else getattr(self.player, "death_predictable", "")),
        )

    def _near_live_mover(self, tile) -> bool:
        """True if any roaming enemy or active dynamic-trap tile is within one
        tile (Chebyshev) of `tile` — a near-miss with a live hazard."""
        tx, ty = tile
        for e in self.enemies:
            ex = getattr(e, "x", None); ey = getattr(e, "y", None)
            if ex is None:
                continue
            if abs(int(ex + 0.5) - tx) <= 1 and abs(int(ey + 0.5) - ty) <= 1:
                return True
        for dt in self.dtraps:
            ox = getattr(dt, "ox", None); oy = getattr(dt, "oy", None)
            if ox is None:
                continue
            if abs(int(ox + 0.5) - tx) <= 1 and abs(int(oy + 0.5) - ty) <= 1:
                return True
        return False

    def _single_step(self):
        """One world tick for a single trial — like _step_world but with NO
        auto-restart and no outcome aggregation into cross-run counters."""
        self.tick += 1
        if self.state != "playing":
            return
        cur_room_now = self.cur_room()
        if RELOC_ON_REENTRY and cur_room_now is not None:
            if self._prev_room is not None and cur_room_now != self._prev_room:
                self._relocate_traps(cur_room_now)
        self._prev_room = cur_room_now
        self.agent.step(self.straps, self.dtraps, self.enemies, self.hazard_pulse)
        keys = self.agent.keys
        self.player.update(keys, self.grid)
        # hazards each carry their own rng (seeded per-seed at construction), so
        # nondeterministic-hazard motion is identical across agents on the same
        # seed regardless of how the agent moves.  no global-stream juggling
        # needed here.
        for tr in self.straps:
            tr.update()
        st = self.strap_map.get((self.player.tx, self.player.ty))
        if st:
            st.check_hit(self.player, self.floors)
        for dt in self.dtraps:
            dt.update(self.player); dt.check_hit(self.player)
        for e in self.enemies:
            e.update(self.player); e.check_hit(self.player)
        self.hazard_pulse.update(self.player, self.grid)
        if self.player.dead:
            self.state = "dead"
        elif math.hypot(self.player.x - self.end[0],
                        self.player.y - self.end[1]) < 0.8:
            self.state = "win"


    def _relocate_traps(self, room):
        """Deterministic, agent-independent wrapper around trap relocation.

        Relocation fires on room RE-ENTRY, and different agents re-enter a given
        room at different times.  Rebuilding the room's hazards draws from the
        global RNG (both for trap positions and to seed each new hazard's
        private RNG), so without care the "same" visit would yield a different
        layout per agent.  To make the non-stationary hazard map a pure function
        of (seed, room, visit#), temporarily reseed the GLOBAL RNG from a stable
        hash of those three for the duration of the rebuild, then restore it so
        the surrounding global stream (visuals, etc.) is undisturbed.  The k-th
        relocation of a room is therefore byte-identical across agents,
        regardless of WHEN it happens, while still differing visit-to-visit
        (the anti-memorisation intent is preserved).
        """
        rid = id(room)
        # stable per-room key: rooms keep identity across a run, but to be robust
        # to any reordering we mix in the room's grid geometry too.
        room_key = (getattr(room, "x", 0), getattr(room, "y", 0),
                    getattr(room, "w", 0), getattr(room, "h", 0),
                    getattr(room, "rtype", 0))
        visit = self._reloc_counts.get(rid, 0)
        self._reloc_counts[rid] = visit + 1
        sub_seed = _stable_hash(self._world_seed, "reloc", room_key, visit)
        saved = random.getstate()
        random.seed(sub_seed)
        try:
            self._relocate_traps_impl(room)
        finally:
            random.setstate(saved)

    def _relocate_traps_impl(self, room):
        """Randomise static trap positions in a room on re-entry.
        This prevents an RL agent from memorising the trap layout through
        repeated visits — the hazard map is non-stationary."""
        if room is self.start_room or room is self.end_room:
            room.straps = []
            room.dtraps = []
            if room is self.start_room:
                room.enemies = []
            self.straps = [t for t in self.straps if self.room_of.get((t.tx, t.ty)) is not room]
            self.dtraps = [dt for dt in self.dtraps if dt.room is not room]
            self.strap_map = {pos: t for pos, t in self.strap_map.items()
                              if self.room_of.get(pos) is not room}
            self.enemies = [e for r in self.rooms for e in r.enemies]
            return

        # remove old straps for this room from global lists
        self.straps = [t for t in self.straps if not (
            self.room_of.get((t.tx, t.ty)) is room)]
        self.dtraps = [dt for dt in self.dtraps if dt.room is not room]
        for k in [k2 for k2,v in self.strap_map.items() if v in room.straps]:
            del self.strap_map[k]
        room.straps = []
        room.dtraps = []

        # rebuild traps for this room (mirrors generate_world logic)
        deep_inn = [(x,y) for y in range(room.y+2, room.y+room.h-2)
                          for x in range(room.x+2, room.x+room.w-2)
                          if self.grid[y][x] == 0]
        if len(deep_inn) < 3:
            return
        safe = set()
        safe |= safe_zone_tiles(self.start[0], self.start[1], START_SAFE_RADIUS)
        safe |= safe_zone_tiles(self.end[0], self.end[1], EXIT_SAFE_RADIUS)
        populate_room_hazards(room, self.grid, safe)
        for t in room.straps:
            self.straps.append(t)
            self.strap_map[(t.tx, t.ty)] = t
        for dt in room.dtraps:
            self.dtraps.append(dt)

        # also refresh enemies in room — new positions, new timing
        room.enemies = [RoamingEnemy(room, self.grid) for _ in range(ENEMY_COUNT)]
        self.enemies = [e for r in self.rooms for e in r.enemies]
        return

    def cam(self):
        cam_x=self.player.x+0.5-W/(2*TS)
        cam_y=self.player.y+0.5-H/(2*TS)
        return cam_x,cam_y

    def cur_room(self):
        return self.room_of.get((self.player.tx,self.player.ty))

    def draw_world(self, cam_x, cam_y):
        if FORMAL_STYLE:
            return self._draw_world_formal(cam_x, cam_y)
        tx0=max(0,int(cam_x)-1); ty0=max(0,int(cam_y)-1)
        tx1=min(COLS,int(cam_x+W/TS)+2); ty1=min(ROWS,int(cam_y+H/TS)+2)

        for ty in range(ty0,ty1):
            for tx in range(tx0,tx1):
                sx=int((tx-0.5-cam_x)*TS); sy=int((ty-0.5-cam_y)*TS)
                rect=pygame.Rect(sx,sy,TS+1,TS+1)
                owner=self.room_of.get((tx,ty))
                th=THEMES[RTYPES[owner.rtype]["theme"]] if owner else THEMES["dungeon"]
                is_room_tile = owner is not None
                rtype = owner.rtype if owner else "dungeon"

                if self.grid[ty][tx]==1:
                    # wall base
                    pygame.draw.rect(self.screen,th["wall"],rect)
                    # top-left highlight (simulates top-down lighting)
                    pygame.draw.line(self.screen,th["wall_hi"],(sx,sy),(sx+TS,sy),2)
                    pygame.draw.line(self.screen,th["wall_hi"],(sx,sy),(sx,sy+TS),2)
                    # bottom-right shadow
                    dark=lerpc(th["wall"],(0,0,0),0.35)
                    pygame.draw.line(self.screen,dark,(sx,sy+TS),(sx+TS,sy+TS),1)
                    pygame.draw.line(self.screen,dark,(sx+TS,sy),(sx+TS,sy+TS),1)
                    # wall face: if open tile below, draw a darker step
                    if ty+1<ROWS and self.grid[ty+1][tx]==0:
                        face=lerpc(th["wall"],(0,0,0),0.5)
                        pygame.draw.rect(self.screen,face,pygame.Rect(sx,sy+TS-3,TS+1,4))
                else:
                    # floor base — corridors slightly darker than rooms
                    if is_room_tile:
                        fc=th["floor2"] if (tx+ty)%2==0 else th["floor"]
                    else:
                        # corridor — darker, neutral grey-tinted
                        fc=lerpc(th["floor"],(8,8,12),0.35) if (tx+ty)%2==0 else lerpc(th["floor"],(8,8,12),0.48)
                    pygame.draw.rect(self.screen,fc,rect)

                    # theme floor details on room tiles
                    if is_room_tile:
                        cx2=sx+TS//2; cy2=sy+TS//2
                        if rtype=="lava" and (tx*7+ty*13)%11==0:
                            # lava crack lines
                            pygame.draw.line(self.screen,th["detail"],(cx2-4,cy2),(cx2+3,cy2-3),1)
                            pygame.draw.line(self.screen,th["detail"],(cx2+3,cy2-3),(cx2+5,cy2+2),1)
                        elif rtype=="ice" and (tx+ty*3)%9==0:
                            # ice sparkle
                            pygame.draw.line(self.screen,lerpc(th["detail"],WHITE,0.6),(cx2-3,cy2),(cx2+3,cy2),1)
                            pygame.draw.line(self.screen,lerpc(th["detail"],WHITE,0.6),(cx2,cy2-3),(cx2,cy2+3),1)
                        elif rtype=="forest" and (tx*5+ty*7)%13==0:
                            # grass tufts
                            for gi in range(3):
                                gx=cx2-3+gi*3; gy=cy2+2
                                pygame.draw.line(self.screen,th["detail"],(gx,gy),(gx-1,gy-3),1)
                        elif rtype=="tomb" and (tx*3+ty*11)%15==0:
                            # stone tiles — small cross
                            pygame.draw.line(self.screen,th["detail"],(cx2-2,cy2),(cx2+2,cy2),1)
                            pygame.draw.line(self.screen,th["detail"],(cx2,cy2-2),(cx2,cy2+2),1)
                        elif rtype=="void" and (tx*11+ty*7)%17==0:
                            # void rune dot
                            pygame.draw.circle(self.screen,th["detail"],(cx2,cy2),1)
                        elif rtype=="dungeon" and (tx*3+ty*5)%19==0:
                            # dungeon cracks
                            pygame.draw.line(self.screen,th["detail"],(cx2-2,cy2-2),(cx2+1,cy2+2),1)

                    # room border accent — 1px accent line on room edge tiles
                    if is_room_tile:
                        on_edge=(tx==owner.x or tx==owner.x+owner.w-1 or
                                 ty==owner.y or ty==owner.y+owner.h-1)
                        if on_edge:
                            edge_col=lerpc(th["floor"],th["acc"],0.25)
                            pygame.draw.rect(self.screen,edge_col,rect,1)

        # room labels
        for room in self.rooms:
            lx=int((room.cx-cam_x)*TS)
            ly=int((room.cy-cam_y)*TS)
            if -80<lx<W+80 and -20<ly<H+20:
                th=THEMES[RTYPES[room.rtype]["theme"]]
                lbl=self.f_sm.render(RTYPES[room.rtype]["theme"].upper(),True,th["acc"])
                lbl.set_alpha(180)
                self.screen.blit(lbl,(lx-lbl.get_width()//2,ly-lbl.get_height()//2))

        # start / end portals
        for pos,col,lbl in [(self.start,(55,220,95),"START"),(self.end,(255,200,40),"EXIT")]:
            sx=int((pos[0]-cam_x)*TS)
            sy=int((pos[1]-cam_y)*TS)
            pulse=0.5+0.5*math.sin(self.tick*0.05)
            # pulsing glow ring
            for rr in (18,13,9):
                gs=asurf(rr*2+2,rr*2+2)
                pygame.draw.circle(gs,(*col,int(50*pulse)),(rr+1,rr+1),rr)
                self.screen.blit(gs,(sx-rr-1,sy-rr-1))
            # solid centre
            pygame.draw.circle(self.screen,lerpc(col,(0,0,0),0.3),(sx,sy),10)
            pygame.draw.circle(self.screen,col,(sx,sy),8)
            pygame.draw.circle(self.screen,lerpc(col,WHITE,0.5),(sx,sy),4)
            # label
            t=self.f_sm.render(lbl,True,col)
            self.screen.blit(t,(sx-t.get_width()//2,sy+11))

    def _draw_world_formal(self, cam_x, cam_y):
        """Flat, neutral, academic-figure rendering of the grid.

        Walls are solid grey, the interior is white with a faint tile grid,
        rooms get a thin outline and a small monospace type label.  No
        gradients, lighting, decorative tiles, or glow.
        """
        tx0 = max(0, int(cam_x) - 1); ty0 = max(0, int(cam_y) - 1)
        tx1 = min(COLS, int(cam_x + W / TS) + 2)
        ty1 = min(ROWS, int(cam_y + H / TS) + 2)

        for ty in range(ty0, ty1):
            for tx in range(tx0, tx1):
                sx = int((tx - 0.5 - cam_x) * TS); sy = int((ty - 0.5 - cam_y) * TS)
                rect = pygame.Rect(sx, sy, TS + 1, TS + 1)
                if self.grid[ty][tx] == 1:
                    pygame.draw.rect(self.screen, FML["wall"], rect)
                    pygame.draw.rect(self.screen, FML["wall_hi"], rect, 1)
                else:
                    owner = self.room_of.get((tx, ty))
                    if owner is not None:
                        fc = FML["floor2"] if (tx + ty) % 2 == 0 else FML["floor"]
                    else:
                        # corridors read as background
                        fc = FML["bg"]
                    pygame.draw.rect(self.screen, fc, rect)
                    # faint tile gridline (top + left only, avoids double-draw)
                    pygame.draw.line(self.screen, FML["grid"], (sx, sy), (sx + TS, sy))
                    pygame.draw.line(self.screen, FML["grid"], (sx, sy), (sx, sy + TS))

        # room outlines + labels
        for room in self.rooms:
            rx = int((room.x - 0.5 - cam_x) * TS)
            ry = int((room.y - 0.5 - cam_y) * TS)
            rw = room.w * TS
            rh = room.h * TS
            if rx + rw < -40 or rx > W + 40 or ry + rh < -40 or ry > H + 40:
                continue
            pygame.draw.rect(self.screen, FML["panel_ln"],
                             pygame.Rect(rx, ry, rw, rh), 1)
            lbl = self.f_sm.render(RTYPES[room.rtype]["theme"].upper(),
                                   True, FML["ink_soft"])
            self.screen.blit(lbl, (rx + 3, ry + 2))

        # start / exit markers — flat squares with labels, no glow
        for pos, col, lbl in [(self.start, FML["start"], "START"),
                              (self.end, FML["goal"], "EXIT")]:
            sx = int((pos[0] - 0.5 - cam_x) * TS)
            sy = int((pos[1] - 0.5 - cam_y) * TS)
            r = pygame.Rect(sx + 3, sy + 3, TS - 5, TS - 5)
            pygame.draw.rect(self.screen, col, r, 2)
            t = self.f_sm.render(lbl, True, col)
            self.screen.blit(t, (sx + TS // 2 - t.get_width() // 2, sy + TS + 1))

    def _update_particles(self):
        # spawn from all nearby rooms (not just current)
        px,py=self.player.x,self.player.y
        for room in self.rooms:
            if abs(room.cx-px)>20 or abs(room.cy-py)>20: continue
            rt=room.rtype
            def rp(margin=1):
                return (room.x+random.uniform(margin,room.w-margin),
                        room.y+random.uniform(margin,room.h-margin))
            if rt=="lava" and random.random()<0.18:
                x2,y2=rp()
                self.particles.append(dict(x=x2,y=y2,
                    vx=random.uniform(-0.01,0.01),vy=random.uniform(-0.05,-0.015),
                    life=random.randint(25,60),maxlife=60,
                    col=(255,random.randint(90,180),10),kind="ember",r=random.randint(2,4)))
            elif rt=="ice" and random.random()<0.14:
                x2,y2=rp()
                self.particles.append(dict(x=x2,y=y2,
                    vx=random.uniform(-0.018,0.018),vy=random.uniform(0.006,0.022),
                    life=random.randint(40,85),maxlife=85,
                    col=(random.randint(160,210),random.randint(220,255),255),kind="snow",r=random.randint(1,3)))
            elif rt=="forest" and random.random()<0.10:
                x2,y2=rp()
                self.particles.append(dict(x=x2,y=y2,
                    vx=random.uniform(-0.02,0.02),vy=random.uniform(-0.03,-0.006),
                    life=random.randint(45,90),maxlife=90,
                    col=(random.randint(50,130),random.randint(170,220),30),kind="leaf",r=2))
            elif rt=="void" and random.random()<0.09:
                x2,y2=rp()
                self.particles.append(dict(x=x2,y=y2,
                    vx=random.uniform(-0.01,0.01),vy=random.uniform(-0.015,0.015),
                    life=random.randint(60,130),maxlife=130,
                    col=(random.randint(130,210),10,random.randint(200,255)),kind="wisp",r=random.randint(2,4)))
            elif rt=="tomb" and random.random()<0.07:
                x2,y2=rp()
                self.particles.append(dict(x=x2,y=y2,
                    vx=random.uniform(-0.008,0.008),vy=random.uniform(-0.012,-0.003),
                    life=random.randint(50,100),maxlife=100,
                    col=(random.randint(140,180),random.randint(130,160),random.randint(100,140)),kind="dust",r=random.randint(2,5)))
            elif rt=="dungeon" and random.random()<0.06:
                x2,y2=rp()
                self.particles.append(dict(x=x2,y=y2,
                    vx=random.uniform(-0.005,0.005),vy=random.uniform(-0.008,-0.002),
                    life=random.randint(40,80),maxlife=80,
                    col=(random.randint(80,120),random.randint(70,100),random.randint(100,140)),kind="dust",r=random.randint(1,3)))
        # update
        alive=[]
        for p in self.particles:
            p['x']+=p['vx']; p['y']+=p['vy']; p['life']-=1
            if p['life']>0: alive.append(p)
        self.particles=alive[-120:]

    def _draw_vision_outline(self, cam_x, cam_y):
        """Trace a red outline around the agent's field of view.

        Uses the SAME _in_fov geometry the agent perceives with, so the outline
        is the true perimeter of what it can see: a forward cone (VISION_FORWARD
        deep, VISION_PERIPHERAL wide each side) with no vision behind.  The
        boundary is drawn as line segments along every edge between a visible
        tile and a non-visible neighbour.
        """
        ptx, pty = self.player.tx, self.player.ty
        heading = _heading_from(self.agent.last_action)
        RED = (220, 60, 60)

        reach = VISION_FORWARD + 1
        visible = set()
        for oy in range(-reach, reach + 1):
            for ox in range(-reach, reach + 1):
                if _in_fov(ox, oy, heading):
                    visible.add((ptx + ox, pty + oy))

        def s(tx, ty):
            return int((tx - cam_x) * TS), int((ty - cam_y) * TS)

        # each visible tile contributes the edges it shares with a non-visible
        # neighbour; together these trace the fov perimeter.
        edges = [((0, 0), (1, 0)),  # top    edge -> neighbour (0,-1)
                 ((0, 1), (1, 1)),  # bottom edge -> neighbour (0,+1)
                 ((0, 0), (0, 1)),  # left   edge -> neighbour (-1,0)
                 # right  edge -> neighbour (+1,0)
                 ((1, 0), (1, 1))]
        neigh = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for (tx, ty) in visible:
            sx, sy = s(tx, ty)
            for (nx, ny), ((ax, ay), (bx, by)) in zip(neigh, edges):
                if (tx + nx, ty + ny) not in visible:
                    pygame.draw.line(self.screen, RED,
                                     (sx + ax * TS, sy + ay * TS),
                                     (sx + bx * TS, sy + by * TS), 2)

    def _draw_agent_plan_overlay(self, cam_x, cam_y):
        if not (self.agent_mode and self.agent is not None):
            return
        agent = self.agent
        route = list(getattr(agent, '_debug_planned_route', []) or [])
        action = getattr(agent, '_debug_safe_action', None)
        ptx, pty = self.player.tx, self.player.ty

        if not route:
            if getattr(agent, '_crossing_route', None):
                route = list(agent._crossing_route)
            elif getattr(agent, 'current_route', None):
                route = list(agent.current_route)
            elif getattr(agent, '_pending_plan', None) and agent._pending_plan[0]:
                route = list(agent._pending_plan[0])
            elif getattr(agent, '_window_action', None) is not None:
                wx, wy = agent._window_action
                route = [(ptx + wx, pty + wy)]
            elif action in PEAgent.DIRS:
                route = [(ptx + action[0], pty + action[1])]

        if not route and action not in PEAgent.DIRS:
            return

        pending = bool(getattr(agent, '_window_wait', 0) > 0 or
                       getattr(agent, '_crossing_wait', 0) > 0 or
                       getattr(agent, '_pending_ticks', 0) > 0)
        col = (245, 190, 70) if pending else (65, 235, 135)
        shadow = (4, 8, 10)

        def pt(wx, wy):
            return int((wx - cam_x) * TS), int((wy - cam_y) * TS)

        path = [(self.player.x, self.player.y)] + route[:10]
        if len(path) >= 2:
            pts = [pt(x, y) for x, y in path]
            for tx, ty in route[:10]:
                sx, sy = pt(tx, ty)
                rect = pygame.Rect(sx - TS // 3, sy - TS // 3,
                                   (TS * 2) // 3, (TS * 2) // 3)
                tile = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
                tile.fill((*col, 44))
                self.screen.blit(tile, rect.topleft)
                pygame.draw.rect(self.screen, (*col, 150), rect, 1)
            if len(pts) > 1:
                pygame.draw.lines(self.screen, shadow, False, pts, 5)
                pygame.draw.lines(self.screen, col, False, pts, 3)

        if route:
            nx, ny = route[0]
            dx, dy = nx - ptx, ny - pty
        elif action in PEAgent.DIRS:
            dx, dy = action
        else:
            return
        if abs(dx) + abs(dy) != 1:
            return

        sx, sy = pt(self.player.x, self.player.y)
        ex = sx + dx * int(TS * 0.82)
        ey = sy + dy * int(TS * 0.82)
        pygame.draw.line(self.screen, shadow, (sx, sy), (ex, ey), 7)
        pygame.draw.line(self.screen, col, (sx, sy), (ex, ey), 4)
        perp = (-dy, dx)
        tip = (ex, ey)
        back = (ex - dx * 9, ey - dy * 9)
        head = [tip,
                (back[0] + perp[0] * 6, back[1] + perp[1] * 6),
                (back[0] - perp[0] * 6, back[1] - perp[1] * 6)]
        pygame.draw.polygon(self.screen, shadow,
                            [(x + 1, y + 1) for x, y in head])
        pygame.draw.polygon(self.screen, col, head)

    def _draw_particles(self, cam_x, cam_y):
        for p in self.particles:
            sx=int((p['x']-cam_x)*TS); sy=int((p['y']-cam_y)*TS)
            if not(-4<=sx<W+4 and -4<=sy<H+4): continue
            lr=p['life']/p['maxlife']
            r=max(1,p['r'])
            kind=p['kind']
            if kind=="snow":
                alpha=int(180*lr)
                gs=asurf(r*2+4,r*2+4)
                cx2=r+2; cy2=r+2
                pygame.draw.line(gs,(*p['col'],alpha),(0,cy2),(r*2+3,cy2),1)
                pygame.draw.line(gs,(*p['col'],alpha),(cx2,0),(cx2,r*2+3),1)
                pygame.draw.line(gs,(*p['col'],alpha//2),(cx2-r,cy2-r),(cx2+r,cy2+r),1)
                pygame.draw.line(gs,(*p['col'],alpha//2),(cx2+r,cy2-r),(cx2-r,cy2+r),1)
                self.screen.blit(gs,(sx-r-2,sy-r-2))
            elif kind=="ember":
                # bright core + fading tail
                alpha=int(240*lr*lr+60*lr)
                gs=asurf(r*2+2,r*2+2)
                pygame.draw.circle(gs,(*p['col'],min(255,alpha)),(r+1,r+1),r)
                if r>2:
                    bright=tuple(min(255,c+80) for c in p['col'])
                    pygame.draw.circle(gs,(*bright,min(255,int(alpha*0.7))),(r+1,r+1),r//2)
                self.screen.blit(gs,(sx-r-1,sy-r-1))
            elif kind=="wisp":
                alpha=int(160*lr)
                gs=asurf(r*2+2,r*2+2)
                pygame.draw.circle(gs,(*p['col'],alpha),(r+1,r+1),r)
                pygame.draw.circle(gs,(*tuple(min(255,c+100) for c in p['col']),int(alpha*0.5)),(r+1,r+1),max(1,r//2))
                self.screen.blit(gs,(sx-r-1,sy-r-1))
            elif kind=="dust":
                alpha=int(90*lr)
                gs=asurf(r*2+2,r*2+2)
                pygame.draw.circle(gs,(*p['col'],alpha),(r+1,r+1),r)
                self.screen.blit(gs,(sx-r-1,sy-r-1))
            elif kind=="leaf":
                alpha=int(200*lr)
                gs=asurf(r*2+4,r*2+4)
                ang=p.get('ang',0)+0.05; p['ang']=ang
                pts=[(r+2+int(r*math.cos(ang+i*math.pi*2/3)),
                      r+2+int(r*math.sin(ang+i*math.pi*2/3))) for i in range(3)]
                if len(pts)==3:
                    pygame.draw.polygon(gs,(*p['col'],alpha),pts)
                self.screen.blit(gs,(sx-r-2,sy-r-2))

    def draw_imagination_panel(self):
        """Far-right panel: a live view of the agent's INTERNAL MODEL — the
        forked world it simulates each decision.  It replays the most recent
        multi-ply rollout so you can watch how the agent PICTURES the traps
        moving and where its imagined body goes, including a foreseen death.

        This is the diagram's Internal Model made visible: imagined body (Robot
        Model) + imagined hazards (World Model), driven by the internal Robot
        Controller, judged ply-by-ply.
        """
        # starts after the expectations panel
        px = W + SIDE_W
        pw = IMAG_W
        ph = WIN_H
        # clip everything this panel draws to its own rectangle.  without this,
        # an imagined entity (enemy/hazard) whose world position falls outside
        # the mini-map's small viewport maps, via to_px, to a pixel left of the
        # panel — painting stray markers into the real game view (the reported
        # glitch).  the clip guarantees the panel can never draw outside itself.
        prev_clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(px, 0, pw, ph))
        try:
            self._draw_imagination_panel_body(px, pw, ph)
        finally:
            self.screen.set_clip(prev_clip)

    def _draw_imagination_panel_body(self, px, pw, ph):
        bg_c    = FML["panel_bg"] if FORMAL_STYLE else (10, 12, 20)
        ln_c    = FML["panel_ln"] if FORMAL_STYLE else (35, 32, 55)
        title_c = FML["ink"]      if FORMAL_STYLE else (120, 180, 240)
        pygame.draw.rect(self.screen, bg_c, pygame.Rect(px, 0, pw, ph))
        pygame.draw.line(self.screen, ln_c, (px, 0), (px, ph), 2)

        y = 10
        title = self.f_sm.render("INTERNAL MODEL — IMAGINATION", True, title_c)
        self.screen.blit(title, (px + 8, y)); y += 18
        sub = self.f_sm.render("vision-window sim · trap countdowns", True,
                               FML["ink_soft"] if FORMAL_STYLE else (110, 120, 150))
        self.screen.blit(sub, (px + 8, y)); y += 16

        if not (self.agent_mode and self.agent):
            hint = self.f_sm.render("[TAB] enable agent", True,
                                    FML["ink_soft"] if FORMAL_STYLE else (60, 70, 90))
            self.screen.blit(hint, (px + 8, y + 4))
            return

        imag = getattr(self.agent, "_imagination", None)
        if not imag or not imag.get('frames'):
            hint = self.f_sm.render("no active simulation", True,
                                    FML["ink_soft"] if FORMAL_STYLE else (60, 70, 90))
            self.screen.blit(hint, (px + 8, y + 4))
            return

        frames = imag['frames']
        n = len(frames)
        # playback advances one imagined frame per render frame — exactly how the
        # real world draws its traps (the real loop re-renders the live trap
        # state once per frame).  driving playback from a frame counter instead
        # of wall-clock get_ticks() removes the timing-jitter stutter: when the
        # agent's choose_action makes a frame run long, the real world still
        # draws one consistent step and so now does the imagination, staying
        # perfectly in sync with the display.  each captured frame is one world
        # tick, so this also keeps the imagined motion at true real-world speed.
        gen = imag.get('gen', 0)
        if getattr(self, '_imag_anim_gen', None) != gen:
            self._imag_anim_gen = gen
            # frames advanced in this sweep
            self._imag_anim_pos = 0.0
        # advance by the same number of world ticks the real loop ran this frame
        # (one on a normal frame, more on a heavy catch-up frame), so imagined
        # traps stay in lock-step with the real world's pacing.
        step = getattr(self, '_frame_world_steps', 1)
        self._imag_anim_pos = getattr(self, '_imag_anim_pos', 0.0) + step
        prog = self._imag_anim_pos
        if n > 1:
            # play once, then hold final frame
            prog = min(prog, n - 1)
        else:
            prog = 0.0
        fa = int(prog)
        fb = min(fa + 1, n - 1)
        frac = prog - fa
        frame = frames[fa]
        nframe = frames[fb]

        def lerp(a, b, u):
            return a + (b - a) * u

        # ── mini-map viewport centred on the imagined action ────────────────
        ox, oy = imag['origin']
        # tiles shown across the mini-map
        VIEW = 11
        # mini tile size
        mts = (pw - 20) // VIEW
        map_x = px + 10
        map_y = y + 8
        cx_t = ox - VIEW // 2
        cy_t = oy - VIEW // 2

        def to_px(wx, wy):
            return (map_x + int((wx - cx_t) * mts),
                    map_y + int((wy - cy_t) * mts))

        def in_view(wx, wy, margin=1.0):
            """True only when a world point lies within the mini-map window, so
            off-screen imagined entities are skipped rather than mapped to a
            stray pixel (defence-in-depth alongside the panel clip)."""
            return (cx_t - margin <= wx <= cx_t + VIEW + margin and
                    cy_t - margin <= wy <= cy_t + VIEW + margin)

        # map background + walls
        pygame.draw.rect(self.screen, (18, 20, 30) if not FORMAL_STYLE else (238, 240, 244),
                         pygame.Rect(map_x, map_y, VIEW * mts, VIEW * mts))
        for ty2 in range(cy_t, cy_t + VIEW):
            for tx2 in range(cx_t, cx_t + VIEW):
                if 0 <= tx2 < COLS and 0 <= ty2 < ROWS and self.grid[ty2][tx2] == 1:
                    sx, sy = to_px(tx2, ty2)
                    pygame.draw.rect(self.screen, (50, 54, 70) if not FORMAL_STYLE else (200, 204, 212),
                                     pygame.Rect(sx, sy, mts, mts))

        # ── imagined hazards, interpolated between the two bracketing frames so
        # rotating arms / expanding rings / darts move smoothly ─────────────
        haz_c = (235, 120, 90)
        for ti, tr in enumerate(frame['traps']):
            k = tr['kind']
            # base layer: shade the trap's true lethal-tile footprint (computed
            # by the agent's own mapper).  this makes every trap kind visible
            # with its real danger area, regardless of whether a detailed
            # shape-draw branch exists below.  drawn faintly so the shape draws
            # (arms, rings, projectiles) read clearly on top.
            for (ftx, fty) in tr.get('footprint', []):
                if not in_view(ftx, fty, margin=0):
                    continue
                sx, sy = to_px(ftx, fty)
                cell = pygame.Surface((mts, mts), pygame.SRCALPHA)
                cell.fill((235, 120, 90, 60))
                self.screen.blit(cell, (sx, sy))
            if tr['ox'] is None and not tr.get('footprint'):
                continue
            ntr = nframe['traps'][ti] if ti < len(nframe['traps']) else tr

            def itp(key):
                a = tr.get(key); b = ntr.get(key)
                if a is None or b is None:
                    return a if a is not None else b
                # angles can wrap; interpolate the short way for rotators
                if key == 'angle':
                    d = (b - a + math.pi) % (2 * math.pi) - math.pi
                    return a + d * frac
                return lerp(a, b, frac)

            if k in ('fire_bar', 'ice_beam', 'pendulum_axe') and tr['angle'] is not None and tr['arm_len']:
                pxc = (tr['pivot_x'] if tr['pivot_x'] is not None else tr['ox'])
                pyc = (tr['pivot_y'] if tr['pivot_y'] is not None else tr['oy'])
                if not in_view(pxc, pyc, margin=tr['arm_len'] + 1):
                    continue
                ang = itp('angle')
                arm = tr['arm_len']
                a = to_px(pxc, pyc)
                if k == 'fire_bar':
                    # real fire_bar radiates n_arms arms (1 or 2) at angle+arm*π
                    # from its hub.  drawing a fixed 2 arms turned a one-armed
                    # ("half") spinner into a full bar — the reported mismatch.
                    n_arms = tr.get('n_arms') or 1
                    for armi in range(n_arms):
                        ba = ang + armi * math.pi
                        pygame.draw.line(self.screen, haz_c, a,
                                         to_px(pxc + math.cos(ba) * arm,
                                               pyc + math.sin(ba) * arm), 3)
                elif k == 'ice_beam':
                    # real ice_beam casts two beams at cos(angle)*sign — i.e. the
                    # two beams point in opposite directions (angle and angle+π),
                    # forming a single straight bar through the hub that rotates
                    # (not a v-shaped mirror across the x-axis, which was the
                    # earlier bug that made the imagined beam look wrong).
                    for sign in (1, -1):
                        bx2 = pxc + math.cos(ang) * sign * arm
                        by2 = pyc + math.sin(ang) * sign * arm
                        pygame.draw.line(self.screen, (130, 200, 235), a,
                                         to_px(bx2, by2), 3)
                # pendulum_axe — a single swinging arm
                else:
                    pygame.draw.line(self.screen, haz_c, a,
                                     to_px(pxc + math.cos(ang) * arm,
                                           pyc + math.sin(ang) * arm), 3)
            elif k == 'spore_burst' and tr['burst_r']:
                if not in_view(tr['ox'], tr['oy'], margin=(tr['burst_r'] or 0) + 1):
                    continue
                c = to_px(tr['ox'], tr['oy'])
                rr = itp('burst_r') or tr['burst_r']
                pygame.draw.circle(self.screen, haz_c, c,
                                   max(2, int(rr * mts)), 2)
            elif k == 'ceiling_crusher':
                # a column of width crush_w; lethal while dropping/down.  draw a
                # vertical bar at ox, brighter when it is in its crushing phase.
                cw = tr.get('crush_w') or 1.0
                pyv = tr['py'] if tr['py'] is not None else tr['oy']
                if not in_view(tr['ox'], pyv, margin=cw + 1):
                    continue
                danger = tr.get('state') in ('dropping', 'down')
                col = (235, 120, 90) if danger else (120, 90, 70)
                sx, sy = to_px(tr['ox'] - cw / 2, tr['oy'] - 1)
                w_px = max(2, int(cw * mts))
                h_px = max(2, int(((pyv - tr['oy']) + 2) * mts))
                pygame.draw.rect(self.screen, col,
                                 pygame.Rect(sx, sy, w_px, h_px), 0 if danger else 1)
            elif k == 'frozen_spike_row' and tr.get('spikes'):
                # a row of spikes; lethal once risen.  draw each spike, height
                # scaled by 'rise', brighter when fully up.
                rise = tr.get('rise') or 0.0
                for (sxw, syw) in tr['spikes']:
                    if not in_view(sxw, syw):
                        continue
                    sx, sy = to_px(sxw, syw)
                    col = (170, 235, 255) if rise > 0.5 else (90, 130, 150)
                    h = max(2, int(mts * (0.3 + 0.7 * rise)))
                    pygame.draw.polygon(self.screen, col, [
                        (sx + mts // 2, sy + mts // 2 - h // 2),
                        (sx + 2, sy + mts // 2 + h // 2),
                        (sx + mts - 2, sy + mts // 2 + h // 2)])
            elif k == 'sarcophagus':
                # anchor box + any in-flight projectiles (self.shots).
                if in_view(tr['ox'], tr['oy']):
                    sx, sy = to_px(tr['ox'], tr['oy'])
                    pygame.draw.rect(self.screen, (200, 170, 110),
                                     pygame.Rect(sx + 2, sy + 2, mts - 4, mts - 4), 1)
                for (shx, shy) in (tr.get('shots') or []):
                    if not in_view(shx, shy):
                        continue
                    sx, sy = to_px(shx, shy)
                    pygame.draw.circle(self.screen, (255, 200, 90),
                                       (sx + mts // 2, sy + mts // 2), max(2, mts // 4))
            elif k == 'mummy_wrap':
                # anchor + the homing dart when active.
                if in_view(tr['ox'], tr['oy']):
                    sx, sy = to_px(tr['ox'], tr['oy'])
                    pygame.draw.circle(self.screen, (210, 195, 150),
                                       (sx + mts // 2, sy + mts // 2), max(2, mts // 3), 1)
                if tr.get('active') and tr['px'] is not None:
                    dx2 = itp('px'); dy2 = itp('py')
                    if in_view(dx2, dy2):
                        sx, sy = to_px(dx2, dy2)
                        pygame.draw.circle(self.screen, (235, 215, 160),
                                           (sx + mts // 2, sy + mts // 2), max(2, mts // 3))
            else:
                wx = itp('px') if tr['px'] is not None else tr['ox']
                wy = itp('py') if tr['py'] is not None else tr['oy']
                if wx is None or not in_view(wx, wy):
                    continue
                sx, sy = to_px(wx, wy)
                pygame.draw.circle(self.screen, haz_c, (sx + mts // 2, sy + mts // 2),
                                   max(2, mts // 3))

        # ── activation countdown overlay ────────────────────────────────────
        # for each dormant cyclic trap, show how many ticks until it next fires —
        # the timing the agent's dynamicsmodel learns from watching the world.
        # counts down as the imagined frames advance.  a trap whose period the
        # agent has reliably learned (licensed law) shows a solid green count;
        # one it cannot yet predict (jittered activation) shows a faint amber
        # "~" estimate, so the panel distinguishes learned knowledge from guess.
        learned = imag.get('learned_kinds', set())
        for tr in frame['traps']:
            if tr.get('cd_active', True):
                # already firing — no countdown
                continue
            base_ticks = tr.get('cd_ticks', 0)
            if base_ticks <= 0:
                continue
            ax = tr.get('ox'); ay = tr.get('oy')
            if ax is None or not in_view(ax, ay):
                continue
            # decrement the learned countdown as the rollout's imagined time
            # advances (fa = imagined ticks elapsed in this sweep).
            remaining = int(base_ticks - fa)
            sx, sy = to_px(ax, ay)
            cx2, cy2 = sx + mts // 2, sy + mts // 2
            is_learned = tr['kind'] in learned
            if remaining <= 0:
                # imagined moment of activation — flash a ring.
                pygame.draw.circle(self.screen, (255, 90, 80), (cx2, cy2),
                                   max(4, mts // 2), 2)
                continue
            # countdown ring: arc proportion = fraction of period remaining.
            ring_c = (110, 220, 150) if is_learned else (220, 180, 90)
            r = max(5, mts // 2)
            # background ring
            pygame.draw.circle(self.screen, (60, 64, 78), (cx2, cy2), r, 1)
            # number
            label = (str(remaining) if is_learned else f"~{remaining}")
            t = self.f_sm.render(label, True, ring_c)
            self.screen.blit(t, (cx2 - t.get_width() // 2, cy2 - t.get_height() // 2))

        # imagined enemies (interpolated).  an enemy that has entered its wait
        # phase is at the limit of what the model can predict — its next leg is
        # random — so it is drawn dimmed with a hollow ring + "?" to make the
        # model's honest uncertainty visible, rather than implying a confident
        # prediction of random motion.
        for ei, ev in enumerate(frame['enemies']):
            exr, eyr = ev[0], ev[1]
            unknown = ev[2] if len(ev) > 2 else False
            if ei < len(nframe['enemies']) and not unknown:
                exr = lerp(exr, nframe['enemies'][ei][0], frac)
                eyr = lerp(eyr, nframe['enemies'][ei][1], frac)
            if not in_view(exr, eyr):
                continue
            sx, sy = to_px(exr, eyr)
            cx2, cy2 = sx + mts // 2, sy + mts // 2
            if unknown:
                pygame.draw.circle(self.screen, (120, 70, 120), (cx2, cy2),
                                   # hollow = uncertain
                                   max(2, mts // 3), 1)
                q = self.f_sm.render("?", True, (160, 110, 160))
                self.screen.blit(q, (cx2 - 3, cy2 - 7))
            else:
                pygame.draw.circle(self.screen, (210, 80, 200), (cx2, cy2),
                                   max(2, mts // 3))

        # ── the full predicted forward path, always visible (the future) ─────
        # drawn faintly end-to-end so the panel reads as "here is where this
        # leads", with a brighter played-so-far segment and a gliding head.
        all_pts = [to_px(bx, by) for (bx, by) in (f['body'] for f in frames)]
        all_pts = [(a + mts // 2, b + mts // 2) for (a, b) in all_pts]
        if len(all_pts) >= 2:
            pygame.draw.lines(self.screen, (50, 90, 120), False, all_pts, 2)
            # endpoint marker (where the imagined trajectory ends)
            ex_, ey_ = all_pts[-1]
            pygame.draw.circle(self.screen, (70, 130, 170), (ex_, ey_), 3, 1)
            # brighter segment up to the playhead
            head = all_pts[:fa + 2]
            if len(head) >= 2:
                pygame.draw.lines(self.screen, (90, 200, 255), False, head, 2)

        # gliding imagined body (interpolated between plies → smooth)
        bx = lerp(frame['body'][0], nframe['body'][0], frac)
        by = lerp(frame['body'][1], nframe['body'][1], frac)
        bsx, bsy = to_px(bx, by)
        body_c = (90, 220, 255)
        dframe = imag.get('death_frame', -1)
        if dframe < 0 and imag.get('death_ply', -1) >= 0:
            # fallback if no sub-tick index
            dframe = imag['death_ply']
        if imag['died'] and dframe >= 0 and prog >= dframe:
            # imagined death reached
            body_c = (255, 70, 70)
        pygame.draw.circle(self.screen, body_c, (bsx + mts // 2, bsy + mts // 2),
                           max(3, mts // 2 - 1))

        y = map_y + VIEW * mts + 12

        # ── verdict / status text ───────────────────────────────────────────
        held = (fa >= n - 1)
        ply_txt = self.f_sm.render(
            ("window predicted — settled" if held
             else f"simulating ahead  {fa}/{n - 1}"), True,
            FML["ink_soft"] if FORMAL_STYLE else (140, 150, 180))
        self.screen.blit(ply_txt, (px + 10, y)); y += 16
        if imag['died']:
            vc = (200, 50, 50) if FORMAL_STYLE else (255, 90, 90)
            v = self.f_sm.render(f"FORESEES DEATH: {imag['death_kind']}", True, vc)
            self.screen.blit(v, (px + 10, y)); y += 15
            v2 = self.f_sm.render(f"at imagined ply {imag['death_ply']}", True, vc)
            self.screen.blit(v2, (px + 10, y)); y += 16
            note = self.f_sm.render("→ route rejected, replanning", True,
                                    FML["ink_soft"] if FORMAL_STYLE else (150, 150, 150))
            self.screen.blit(note, (px + 10, y)); y += 16
        else:
            vc = (40, 150, 90) if FORMAL_STYLE else (110, 220, 150)
            v = self.f_sm.render("trajectory survivable", True, vc)
            self.screen.blit(v, (px + 10, y)); y += 16

        # legend
        y += 6
        leg = [((90, 220, 255), "imagined agent"),
               ((235, 120, 90), "imagined hazard"),
               ((255, 70, 70), "foreseen death"),
               ((110, 220, 150), "learned countdown"),
               ((220, 180, 90), "~ est. countdown")]
        for col, lbl in leg:
            pygame.draw.circle(self.screen, col, (px + 14, y + 6), 4)
            t = self.f_sm.render(lbl, True, FML["ink_soft"] if FORMAL_STYLE else (150, 155, 175))
            self.screen.blit(t, (px + 24, y)); y += 15

    def draw_side_panel(self):
        """Right-side panel showing recently reused expectations."""
        # panel starts at right edge of game viewport
        px = W
        pw = SIDE_W
        ph = WIN_H
        # background
        bg_c    = FML["panel_bg"] if FORMAL_STYLE else (8, 8, 14)
        ln_c    = FML["panel_ln"] if FORMAL_STYLE else (35, 32, 55)
        title_c = FML["ink"]      if FORMAL_STYLE else (80, 200, 160)
        sep_c   = FML["panel_ln"] if FORMAL_STYLE else (35, 55, 45)
        pygame.draw.rect(self.screen, bg_c, pygame.Rect(px, 0, pw, ph))
        pygame.draw.line(self.screen, ln_c, (px, 0), (px, ph), 2)

        y = 10
        # title
        title = self.f_sm.render("UNIQUE REUSED EXPECTATIONS", True, title_c)
        self.screen.blit(title, (px + 8, y))
        y += 16
        pygame.draw.line(self.screen, sep_c, (px + 6, y), (px + pw - 6, y), 1)
        y += 6

        if not (self.agent_mode and self.agent):
            hint = self.f_sm.render("[TAB] enable agent", True, FML["ink_soft"] if FORMAL_STYLE else (40, 60, 50))
            self.screen.blit(hint, (px + 8, y + 4))
            return

        # deliberation status (feedback #1): visualise thinking as world time
        if getattr(self.agent, "_pending_ticks", 0) > 0:
            th = self.f_sm.render(
                f"deliberating… plan in {self.agent._pending_ticks} ticks",
                True, (180, 120, 20) if FORMAL_STYLE else (245, 205, 90))
            self.screen.blit(th, (px + 8, y)); y += 16

        log = list(self.agent.memory.reused_log)
        if not log:
            none_txt = self.f_sm.render("none yet", True, FML["ink_soft"] if FORMAL_STYLE else (40, 60, 50))
            self.screen.blit(none_txt, (px + 8, y + 4))
            return

        BAR_W  = pw - 20
        for t_val, label, conf, source in log:
            if y + 36 > ph - 4:
                break

            # source badge colour
            src_col = (60, 190, 120) if source == "mem" else (120, 100, 220)
            src_lbl = "MEM" if source == "mem" else "EEC"
            badge   = self.f_sm.render(src_lbl, True, src_col)
            pygame.draw.rect(self.screen,
                             (*[max(0, c - 140) for c in src_col], 180),
                             pygame.Rect(px + 6, y, badge.get_width() + 6, 13),
                             border_radius=3)
            self.screen.blit(badge, (px + 9, y + 1))

            # sim-time stamp
            t_txt = self.f_sm.render(f"t={t_val}", True, FML["ink_soft"] if FORMAL_STYLE else (55, 55, 75))
            self.screen.blit(t_txt, (px + pw - t_txt.get_width() - 6, y + 1))
            y += 15

            # rule label — wrap across up to 3 lines, sized to actual glyph width
            char_w = self.f_sm.size("M")[0] or 7
            max_chars = max(8, (pw - 16) // char_w)
            lab_col  = FML["ink"] if FORMAL_STYLE else (180, 180, 210)
            lab_col2 = FML["ink_soft"] if FORMAL_STYLE else (140, 140, 175)
            remaining = label
            for li in range(3):
                if not remaining:
                    break
                chunk = remaining[:max_chars]
                remaining = remaining[max_chars:]
                if li == 2 and remaining:
                    # truncate overly long labels
                    chunk = chunk[:-1] + "…"
                    remaining = ""
                seg = self.f_sm.render(chunk, True, lab_col if li == 0 else lab_col2)
                self.screen.blit(seg, (px + 8, y))
                y += 13

            # confidence bar
            bar_fill = int(BAR_W * max(0.0, min(1.0, conf)))
            bar_bg   = pygame.Rect(px + 8, y, BAR_W, 5)
            bar_fg   = pygame.Rect(px + 8, y, bar_fill, 5)
            bar_col  = (int(255 * (1 - conf)), int(200 * conf), 80)
            pygame.draw.rect(self.screen, FML["panel_ln"] if FORMAL_STYLE else (25, 25, 35), bar_bg, border_radius=2)
            pygame.draw.rect(self.screen, bar_col,      bar_fg, border_radius=2)
            conf_txt = self.f_sm.render(f"{conf:.2f}", True, FML["ink_soft"] if FORMAL_STYLE else (90, 90, 110))
            self.screen.blit(conf_txt, (px + BAR_W - conf_txt.get_width() + 8, y - 12))
            y += 9

            # divider
            pygame.draw.line(self.screen, FML["panel_ln"] if FORMAL_STYLE else (22, 22, 32),
                             (px + 6, y + 2), (px + pw - 6, y + 2), 1)
            y += 7

    def _draw_hud_metrics(self, y0):
        """Formal HUD: centre room name, right-side controls, PE agent stats."""
        room = self.cur_room()
        if room:
            rname = RTYPES[room.rtype]["theme"].upper()
            badge = self.f_med.render(rname, True, FML["ink"])
            self.screen.blit(badge, (W//2 - badge.get_width()//2, y0+10))
            tc = self.f_sm.render(
                f"{len(room.straps)+len(room.dtraps)} hazards", True, FML["ink_soft"])
            self.screen.blit(tc, (W//2 - tc.get_width()//2, y0+34))

        if not self.agent_mode:
            ctrl = self.f_sm.render(
                "WASD/Arrows Move   R New Maze   TAB Agent   ESC Quit",
                True, FML["ink_soft"])
            self.screen.blit(ctrl, (W - ctrl.get_width()-8, y0+HUD_H-15))

        if self.agent_mode and self.agent:
            mem = self.agent.memory
            bx_pe = W - 390
            badge_txt = self.f_sm.render("PE AGENT", True, FML["agent"])
            self.screen.blit(badge_txt, (bx_pe, y0+10))
            row1 = self.f_sm.render(
                f"E:{mem.count}  D:{mem.danger_count}  H:{mem.holds_count}    "
                f"Wins:{self._completions}  Fails:{self._fails}",
                True, FML["ink"])
            self.screen.blit(row1, (bx_pe, y0+26))
            row2 = self.f_sm.render(
                f"Sim:{mem.sims_run}  Skip:{mem.sims_skipped}"
                f"  Forms:{mem.expectation_forms}  Rules:{mem.count}"
                f"  Der:{mem.rules_derived}  Tr:{mem.transit_hits}",
                True, FML["ink"])
            self.screen.blit(row2, (bx_pe, y0+38))
            row3 = self.f_sm.render(
                f"EEC:{self.agent.eec_reasoner.chain_dangers_detected}  "
                f"Vic:{mem.vicarious_confirms}  "
                f"Spec:{mem.specialisations}  t={self.agent.sim_time}",
                True, FML["ink_soft"])
            self.screen.blit(row3, (bx_pe, y0+50))
        else:
            hint = self.f_sm.render("[TAB] Enable PE Agent", True, FML["ink_soft"])
            self.screen.blit(hint, (W - hint.get_width()-8, y0+10))

    def draw_hud(self):
        y0=H
        if FORMAL_STYLE:
            pygame.draw.rect(self.screen, FML["panel_bg"], pygame.Rect(0,y0,W,HUD_H))
            pygame.draw.line(self.screen, FML["panel_ln"], (0,y0),(W,y0),1)
            bx=12; by=y0+10
            alive = not self.player.dead
            ac = FML["goal"] if alive else (200,60,60)
            pygame.draw.rect(self.screen, ac, pygame.Rect(bx-1,by-1,150,18),1)
            atxt = self.f_sm.render("ALIVE — ONE-HIT-KILL" if alive else "TERMINATED",
                                    True, ac)
            self.screen.blit(atxt,(bx+4,by+2))
            ex = self.f_sm.render(f"Rooms: {len(self.visited)} / {len(self.rooms)}",
                                  True, FML["ink_soft"])
            self.screen.blit(ex,(bx,by+22))
            # status effects as flat labels
            stx=bx; sty=y0+44
            for eff in self.player.statuses:
                lbl=self.f_sm.render(eff.upper(), True, FML["ink"])
                pygame.draw.rect(self.screen, FML["panel_ln"],
                                 pygame.Rect(stx,sty,lbl.get_width()+8,14),1)
                self.screen.blit(lbl,(stx+4,sty+1))
                stx += lbl.get_width()+14
            self._draw_hud_metrics(y0)
            return
        pygame.draw.rect(self.screen,(10,10,16),pygame.Rect(0,y0,W,HUD_H))
        # accent strip — colour shifts with current room
        room=self.cur_room()
        strip_col=(45,40,65)
        if room:
            th=THEMES[RTYPES[room.rtype]["theme"]]
            strip_col=lerpc((20,18,30),th["acc"],0.35)
        pygame.draw.rect(self.screen,strip_col,pygame.Rect(0,y0,W,3))
        pygame.draw.line(self.screen,(30,28,45),(0,y0+3),(W,y0+3),1)

        # ── status / alive indicator ─────────────────────────────────────────
        bx=12; by=y0+10
        alive_col=(45,185,75)
        pygame.draw.rect(self.screen,(10,30,15),pygame.Rect(bx-1,by-1,130,18))
        pygame.draw.rect(self.screen,alive_col,pygame.Rect(bx-1,by-1,130,18),1)
        alive_txt=self.f_sm.render("ALIVE  —  ONE HIT KILL",True,alive_col)
        self.screen.blit(alive_txt,(bx+4,by+2))
        # rooms explored
        explored=self.f_sm.render(f"Rooms: {len(self.visited)} / {len(self.rooms)}",True,(130,120,160))
        self.screen.blit(explored,(bx,by+22))

        # ── status pills ─────────────────────────────────────────────────────
        stx=bx; sty=y0+44
        for eff,frames in self.player.statuses.items():
            sc=SDEFS[eff]["col"]
            pill_w=len(eff)*7+14
            # pill background
            pygame.draw.rect(self.screen,lerpc(sc,(0,0,0),0.75),
                             pygame.Rect(stx,sty,pill_w,14),border_radius=7)
            pygame.draw.rect(self.screen,sc,
                             pygame.Rect(stx,sty,pill_w,14),1,border_radius=7)
            et=self.f_sm.render(eff.upper(),True,sc)
            self.screen.blit(et,(stx+4,sty+1))
            stx+=pill_w+5

        # ── room info (centre) ───────────────────────────────────────────────
        room=self.cur_room()
        if room:
            th=THEMES[RTYPES[room.rtype]["theme"]]
            rname=RTYPES[room.rtype]["theme"].upper()
            ICONS={"dungeon":"⚔","lava":"🔥","ice":"❄","forest":"🌿","tomb":"💀","void":"✦"}
            icon=ICONS.get(room.rtype,"◈")
            # room name badge
            badge=self.f_med.render(f"{icon}  {rname}  {icon}",True,th["acc"])
            bx2=W//2-badge.get_width()//2
            pygame.draw.rect(self.screen,(*lerpc(th["acc"],(0,0,0),0.85),200),
                             pygame.Rect(bx2-6,y0+8,badge.get_width()+12,badge.get_height()+4),border_radius=4)
            self.screen.blit(badge,(bx2,y0+10))
            # trap count
            tc=self.f_sm.render(f"{len(room.straps)+len(room.dtraps)} traps",True,(130,100,105))
            self.screen.blit(tc,(W//2-tc.get_width()//2,y0+36))

        # ── controls (right) ────────────────────────────────────────────────
        ctrl=self.f_sm.render("WASD/Arrows  Move   R  New Maze   TAB  PE Agent   ESC  Quit",True,(48,52,72))
        self.screen.blit(ctrl,(W-ctrl.get_width()-8,y0+HUD_H-15))

        # ── pe agent panel ───────────────────────────────────────────────────
        if self.agent_mode and self.agent:
            mem = self.agent.memory
            badge_col = (50, 200, 140)
            badge_txt = self.f_sm.render("PE AGENT", True, badge_col)
            bx_pe = W - 390
            pygame.draw.rect(self.screen, (*lerpc(badge_col,(0,0,0),0.85), 200),
                             pygame.Rect(bx_pe-4, y0+8, badge_txt.get_width()+8, badge_txt.get_height()+4),
                             border_radius=3)
            self.screen.blit(badge_txt, (bx_pe, y0+10))
            # row 1: memory counts + outcome totals
            row1 = self.f_sm.render(
                f"E:{mem.count}  D:{mem.danger_count}  H:{mem.holds_count}    "
                f"Wins:{self._completions}  Fails:{self._fails}",
                True, (70, 170, 110))
            self.screen.blit(row1, (bx_pe, y0+26))
            # row 2: simulation counters (wider spacing)
            row2 = self.f_sm.render(
                f"Sim:{mem.sims_run}  Skip:{mem.sims_skipped}"
                f"  Forms:{mem.expectation_forms}"
                f"  Try:{mem.rule_attempts}"
                f"  Rules:{mem.expectations_created - mem.rules_derived}"
                f"  Der:{mem.rules_derived}"
                f"  Tr:{mem.transit_hits}",
                True, (70, 170, 110))
            self.screen.blit(row2, (bx_pe, y0+38))
            # row 3: eec chain + vicarious confirmations + sim time
            row3 = self.f_sm.render(
                f"EEC chain:{self.agent.eec_reasoner.chain_dangers_detected}   "
                f"Vic:{mem.vicarious_confirms}   "
                f"ΔP obs:{mem.causal.observations} drop:{mem.preconds_dropped}   "
                f"Fact:{mem.factored_rules} Soft:{mem.partial_reuses} Spec:{mem.specialisations}   "
                f"t={self.agent.sim_time}",
                True, (80, 210, 170))
            self.screen.blit(row3, (bx_pe, y0+50))
        else:
            hint = self.f_sm.render("[TAB] Enable PE Agent", True, (45, 65, 55))
            self.screen.blit(hint, (W - hint.get_width() - 8, y0+10))
        # ── hazard pulse indicator ───────────────────────────────────────────
        lbl_info = self.hazard_pulse.hud_label()
        if lbl_info:
            lbl_txt, lbl_col = lbl_info
            flash = int(128 + 127 * math.sin(self.tick * 0.18))
            pls = self.f_med.render(f"⚠ {lbl_txt} ⚠", True, lbl_col)
            pls.set_alpha(flash)
            self.screen.blit(pls, (W//2 - pls.get_width()//2, y0 + 50))

        self._minimap()

    def _minimap(self):
        mmw,mmh=170,118; mmx=W-mmw-8; mmy=H-mmh-8
        ms=pygame.Surface((mmw,mmh),pygame.SRCALPHA)
        # dark backdrop with rounded feel
        pygame.draw.rect(ms,(5,5,10,200),(0,0,mmw,mmh),border_radius=4)
        sx=mmw/COLS; sy=mmh/ROWS
        # draw all floor tiles (corridors appear as faint dots)
        for ry in range(0,ROWS,2):
            for rx in range(0,COLS,2):
                if self.grid[ry][rx]==0 and not self.room_of.get((rx,ry)):
                    px2=int(rx*sx); py2=int(ry*sy)
                    pygame.draw.rect(ms,(35,35,50,120),(px2,py2,max(1,int(sx)),max(1,int(sy))))
        for room in self.rooms:
            th=THEMES[RTYPES[room.rtype]["theme"]]
            visited=room in self.visited
            rx=int(room.x*sx); ry=int(room.y*sy)
            rw=max(3,int(room.w*sx)); rh=max(3,int(room.h*sy))
            if visited:
                # filled room with floor colour
                pygame.draw.rect(ms,(*lerpc(th["floor"],(0,0,0),0.2),200),(rx,ry,rw,rh))
                pygame.draw.rect(ms,(*th["acc"],180),(rx,ry,rw,rh),1)
            else:
                # unexplored — just faint outline
                pygame.draw.rect(ms,(*th["acc"],50),(rx,ry,rw,rh),1)
        # exit marker
        ex=int(self.end[0]*sx); ey=int(self.end[1]*sy)
        pygame.draw.circle(ms,(255,215,0),(ex,ey),4)
        pygame.draw.circle(ms,(255,255,180),(ex,ey),2)
        # player dot with direction
        px2=int(self.player.tx*sx); py2=int(self.player.ty*sy)
        pygame.draw.circle(ms,(255,255,255),(px2,py2),4)
        pygame.draw.circle(ms,(80,160,255),(px2,py2),3)
        fx=px2+int(math.cos(self.player.facing)*5)
        fy=py2+int(math.sin(self.player.facing)*5)
        pygame.draw.line(ms,(255,255,255),(px2,py2),(fx,fy),1)
        # border
        pygame.draw.rect(ms,(60,65,100,220),(0,0,mmw,mmh),1,border_radius=4)
        self.screen.blit(ms,(mmx,mmy))
        # title above minimap
        mt=self.f_sm.render("MAP",True,(75,85,110))
        self.screen.blit(mt,(mmx+4,mmy-14))

    def draw_overlay(self):
        if self.state=="playing": return
        is_dead=self.state=="dead"
        is_timeout=self.state=="timeout"
        if FORMAL_STYLE:
            ov=asurf(W,H); ov.fill((244,245,247,210)); self.screen.blit(ov,(0,0))
            pw,ph=420,200
            px2,py2=W//2-pw//2,H//2-ph//2
            border=(190,60,60) if (is_dead or is_timeout) else FML["goal"]
            pygame.draw.rect(self.screen, FML["panel_bg"], pygame.Rect(px2,py2,pw,ph))
            pygame.draw.rect(self.screen, border, pygame.Rect(px2,py2,pw,ph), 2)
            _title = ("TIMED OUT" if is_timeout
                      else "RUN TERMINATED" if is_dead else "EXIT REACHED")
            title=self.f_big.render(_title, True, border)
            self.screen.blit(title,(W//2-title.get_width()//2,py2+22))
            sub=self.f_med.render(
                f"Wins: {self._completions}    Runs failed: {self._fails}",
                True, FML["ink"])
            self.screen.blit(sub,(W//2-sub.get_width()//2,py2+72))
            pygame.draw.line(self.screen, FML["panel_ln"],
                             (px2+20,py2+104),(px2+pw-20,py2+104),1)
            if self.agent_mode:
                secs=max(0,round((90-self._restart_timer)/FPS,1))
                ptxt=f"Auto-restarting in {secs:.0f}s (memory wiped)"
            else:
                ptxt="Press R to restart"
            p=self.f_med.render(ptxt, True, FML["ink_soft"])
            self.screen.blit(p,(W//2-p.get_width()//2,py2+ph-38))
            return
        ov=asurf(W,H)
        ov.fill((0,0,0,185))
        self.screen.blit(ov,(0,0))
        is_dead=self.state=="dead"

        # panel
        pw,ph=420,220
        px2,py2=W//2-pw//2,H//2-ph//2
        panel=asurf(pw,ph)
        _fail = is_dead or is_timeout
        panel.fill(((28,10,10,230) if _fail else (10,20,28,230)))
        panel_border=(180,40,40) if _fail else (50,180,100)
        pygame.draw.rect(panel,(*panel_border,200),(0,0,pw,ph),2,border_radius=8)
        self.screen.blit(panel,(px2,py2))

        # title
        if is_dead:
            title=self.f_big.render("YOU DIED",True,(225,50,50))
            sub=self.f_med.render("The dungeon claimed you.",True,(160,100,100))
        elif is_timeout:
            title=self.f_big.render("TIMED OUT",True,(225,160,40))
            sub=self.f_med.render("Ran out of time to reach the exit.",True,(190,150,90))
        else:
            title=self.f_big.render("ESCAPED!",True,(255,215,40))
            sub=self.f_med.render("You found the exit!",True,(140,200,120))
        self.screen.blit(title,(W//2-title.get_width()//2,py2+18))
        self.screen.blit(sub,(W//2-sub.get_width()//2,py2+60))

        # divider
        pygame.draw.line(self.screen,(*panel_border,120),(px2+20,py2+88),(px2+pw-20,py2+88),1)

        # restart prompt
        if self.agent_mode:
            secs_left = max(0, round((90 - self._restart_timer) / FPS, 1))
            prompt_txt = f"Auto-restarting in {secs_left:.0f}s..."
            prompt_col = (100, 200, 140)
        else:
            prompt_txt = "Press R to play again"
            prompt_col = (120, 130, 160)
        prompt=self.f_med.render(prompt_txt, True, prompt_col)
        self.screen.blit(prompt,(W//2-prompt.get_width()//2,py2+ph-38))

    def _bench_summary(self) -> dict:
        """Aggregate stats for a headless benchmark run (feedback #2)."""
        mem = self.agent_memory
        think = self._think_total + (self.agent.think_ticks_total
                                     if self.agent else 0)
        total = mem.sims_run + mem.sims_skipped
        dyn_answers = self._dyn_total + (self.agent.dynamics.answers
                                         if self.agent else 0)
        laws = sum(1 for r in mem.rules
                   if r.effect.name == "OccupancyLaw")
        return dict(mode=self.mode, ticks=self._bench_tick,
                    completions=self._completions, deaths=self._fails,
                    rules=mem.count, laws=laws, sims_run=mem.sims_run,
                    sims_skipped=mem.sims_skipped,
                    reuse_pct=(100.0 * mem.sims_skipped / total) if total else 0.0,
                    dyn_answers=dyn_answers, think_ticks=think,
                    q_answered=mem.diag_answered,
                    q_nomatch=mem.diag_no_candidate,
                    q_gate=mem.diag_gate_blocked,
                    q_thresh=mem.diag_thresh_blocked,
                    safe_void=mem.diag_safe_voided,
                    danger_void=mem.diag_danger_voided,
                    deaths_predictable=self._deaths_predictable,
                    deaths_unpredictable=self._deaths_unpredictable,
                    death_by_kind=dict(self._death_by_kind))

    def _step_world(self):
        """Advance world logic by exactly one fixed timestep.

        Decoupled from rendering (supervisor feedback #3 / lag fix): the run()
        loop calls this at a FIXED rate via an accumulator, independent of how
        long a frame takes to draw or how long the agent deliberated.  A slow
        frame is caught up by running this several times; a fast machine never
        runs it faster than TICK_HZ.  World time is therefore constant and the
        display can never freeze the simulation, nor the simulation the display.
        """
        self.tick += 1
        self._bench_tick += 1
        if self.state == "playing":
            cur_room_now = self.cur_room()
            if RELOC_ON_REENTRY and cur_room_now is not None:
                if self._prev_room is not None and cur_room_now != self._prev_room:
                    self._relocate_traps(cur_room_now)
            self._prev_room = cur_room_now

            if self.agent_mode:
                self.agent.step(self.straps, self.dtraps, self.enemies,
                                self.hazard_pulse)
                keys = self.agent.keys
            else:
                keys = pygame.key.get_pressed()
            self.player.update(keys, self.grid)
            # each hazard self-seeds (per world seed at construction), so
            # nondeterministic motion is reproducible across agents on a seed.
            for t in self.straps:
                t.update()
            st = self.strap_map.get((self.player.tx, self.player.ty))
            if st: st.check_hit(self.player, self.floors)
            for dt in self.dtraps:
                dt.update(self.player)
                dt.check_hit(self.player)
            # ── roaming enemies ───────────────────────────────────────────
            for e in self.enemies:
                e.update(self.player)
                e.check_hit(self.player)
            # ── hazard pulse ──────────────────────────────────────────────
            self.hazard_pulse.update(self.player, self.grid)
            # ── re-entry trap relocation ──────────────────────────────────
            if self.player.dead:
                self.state = "dead"
            elif math.hypot(self.player.x - self.end[0],
                            self.player.y - self.end[1]) < 0.8:
                self.state = "win"
            elif self.tick >= LIVE_TIMEOUT_TICKS:
                # whole-attempt timeout, mirroring the headless benchmark and the
                # mcts baseline: an attempt gets live_timeout_ticks world ticks to
                # reach the exit; if it has not, the run ends as a timeout (then
                # auto-restarts in agent mode just like a win/death).  without
                # this, a stuck or merely slow agent could run the interactive
                # session forever, whereas every other run mode is time-bounded.
                self.state = "timeout"
        # count outcome on the first tick of each non-playing state
        if self.state != "playing" and not self._counted_outcome:
            self._counted_outcome = True
            if self.state == "win":
                self._completions += 1
            elif self.state == "timeout":
                # a timeout is a non-completion but not a death — keep it out of
                # the death-attribution stats so predictable-death diagnostics
                # are not polluted by runs that simply ran out of time.
                self._fails += 1
            else:
                self._fails += 1
                # attribute the death: predictable killer => simulation bug.
                dk = getattr(self.player, "death_kind", None)
                dp = getattr(self.player, "death_predictable", None)
                if dk is not None:
                    self._death_by_kind[dk] = self._death_by_kind.get(dk, 0) + 1
                if dp is True:
                    self._deaths_predictable += 1
                elif dp is False:
                    self._deaths_unpredictable += 1
                # post-mortem for predictable deaths: was the killer knowable?
                # recorded here (not in agent.step) because the agent's step()
                # is not called again once the world state leaves "playing" —
                # the agent dies after its own step within the same tick.
                if dp is True and self.agent is not None:
                    kill_tile = (self.player.tx, self.player.ty)
                    last_tm = (self.agent._last_obs or {}).get('trap_map', {})
                    known = getattr(self.agent, "_known_static_traps", {})
                    pm = {
                        "kind": dk,
                        "tile": kill_tile,
                        "player_xy": (round(self.player.x, 2),
                                      round(self.player.y, 2)),
                        "in_last_trap_map": kill_tile in last_tm,
                        "trap_map_kind": last_tm.get(kill_tile),
                        "in_static_mem": kill_tile in known,
                        "is_static": dk in STRAP_KINDS,
                    }
                    if not hasattr(self, "_pm_all"):
                        self._pm_all = []
                    self._pm_all.append(pm)
            # every run is an independent trial: win or lose, the next run
            # starts from scratch with empty expectation memory and no
            # learned dynamics laws.  knowledge never carries across runs.
            self._reset_memory_on_restart = True
            # append this finished run to the live session csv (created at
            # launch).  map the world state to the standard outcome label.
            _outcome = ("win" if self.state == "win"
                        else "timeout" if self.state == "timeout"
                        else "death")
            self._write_live_csv_row(_outcome)
        # auto-restart in agent mode after a brief pause on win/dead
        if self.agent_mode and self.state != "playing":
            self._restart_timer += 1
            # ~1.5 s at tick_hz
            if self._restart_timer >= 90:
                self.new_game()
        # track visited rooms
        cur = self.cur_room()
        if cur:
            self.visited.add(cur)
            self.last_room = cur
        # ambient particles advance with world time (skip in headless/formal)
        if self.state == "playing" and not self.headless and not FORMAL_STYLE and not REDUCE_EFFECTS:
            self._update_particles()

    def run(self):
        # ── fixed-timestep loop (lag fix): world logic at a constant tick_hz,
        # rendering as fast as the frame allows.  an accumulator banks elapsed
        # real time and spends it in whole logic ticks; max_catchup caps how
        # many ticks one frame may run so a compute spike can stutter the
        # picture but never snowball the simulation ("spiral of death").
        # world-logic rate (60 hz)
        TICK_HZ     = FPS
        DT          = 1.0 / TICK_HZ
        # most logic ticks per rendered frame
        MAX_CATCHUP = 5
        accumulator = 0.0
        prev = time.perf_counter()

        if self.headless:
            # benchmark mode: no real-time pacing, no rendering — run logic flat out.
            while True:
                self._step_world()
                if self.max_ticks is not None and self._bench_tick >= self.max_ticks:
                    return self._bench_summary()
                self._drain_events()
            # (unreachable)

        while True:
            now = time.perf_counter()
            frame = now - prev
            prev = now
            # clamp a very long frame so we don't try to simulate a huge gap
            if frame > MAX_CATCHUP * DT:
                frame = MAX_CATCHUP * DT
            accumulator += frame

            self._drain_events()

            # run as many fixed logic ticks as real time has accrued
            steps = 0
            while accumulator >= DT and steps < MAX_CATCHUP:
                self._step_world()
                accumulator -= DT
                steps += 1
            # tell the imagination panel how many world ticks advanced this frame
            # so its playback advances by the same amount — keeping the imagined
            # traps in lock-step with the real world's pacing even when a heavy
            # frame runs multiple catch-up ticks (otherwise the imagination would
            # play in slow motion relative to the real traps on slow frames).
            self._frame_world_steps = max(1, steps)
            # render exactly once per frame, regardless of how many (or zero)
            # logic ticks ran.  a slow agent tick just means fewer frames, not
            # a frozen world; a fast machine renders spare frames harmlessly.
            self._render_frame()

            # yield the cpu briefly so we don't busy-spin at 100% when idle
            self.clock.tick(TICK_HZ)

    def _close_live_csv(self):
        """Flush and close the session CSV (rows are already fsync'd)."""
        fh = getattr(self, "_live_csv_fh", None)
        if fh is not None:
            try:
                fh.flush()
                fh.close()
            except (OSError, ValueError):
                pass
            self._live_csv_fh = None
            self._live_csv_writer = None

    def _drain_events(self):
        for ev in pygame.event.get():
            if ev.type == QUIT:
                self._close_live_csv(); pygame.quit(); sys.exit()
            if ev.type == KEYDOWN:
                if ev.key == K_r: self.new_game()
                if ev.key == K_ESCAPE:
                    self._close_live_csv(); pygame.quit(); sys.exit()
                if ev.key == K_TAB: self.agent_mode = not self.agent_mode

    def _render_frame(self):
        if self.headless:
            return
        cam_x, cam_y = self.cam()
        self.screen.fill(FML["bg"] if FORMAL_STYLE else (8,6,14))
        self.draw_world(cam_x,cam_y)
        if not FORMAL_STYLE and not REDUCE_EFFECTS:
            self._draw_particles(cam_x,cam_y)
        for t in self.straps:
            dist_to_player = math.hypot(t.tx - self.player.x, t.ty - self.player.y)
            visible = dist_to_player <= FOG_REVEAL_DIST
            if visible and abs(t.tx-self.player.tx)<22 and abs(t.ty-self.player.ty)<22:
                t.draw(self.screen,cam_x,cam_y,TS)
        for dt in self.dtraps:
            dist_to_player = math.hypot(dt.ox - self.player.x, dt.oy - self.player.y)
            visible = dist_to_player <= FOG_REVEAL_DIST + 1
            if visible and abs(dt.ox-self.player.x)<22 and abs(dt.oy-self.player.y)<22:
                dt.draw(self.screen,cam_x,cam_y,TS)
        # draw roaming enemies (respect fog of war)
        for e in self.enemies:
            e.draw(self.screen, cam_x, cam_y, TS, self.player)
        if VISION_ENABLED and self.agent_mode and self.agent is not None:
            self._draw_vision_outline(cam_x, cam_y)
        self.player.draw(self.screen,cam_x,cam_y,TS,self.f_sm)
        self._draw_agent_plan_overlay(cam_x, cam_y)

        self.draw_hud()
        self.draw_side_panel()
        self.draw_imagination_panel()
        self.draw_overlay()
        pygame.display.flip()


def run_paired_benchmark(n_attempts: int, ticks: int, modes=None,
                         csv_path: str = "maze_comparison.csv",
                         seeds=None) -> str:
    """Paired, capped, crash-safe multi-seed comparison across agent modes.

    Runs exactly `n_attempts` seeds (drawn in order from BENCHMARK_SEEDS unless
    an explicit `seeds` list is given) for each mode in `modes`.  For a single
    mode this is "run this agent for N attempts, then stop"; for several modes
    it is a paired design — every mode faces the SAME maze for a given seed, so
    differences are attributable to the agent, not the environment.

    Crash-/interrupt-safety: one CSV row per (seed, mode) run is written AND
    flushed to disk the instant the run finishes, inside a try/finally, so the
    file is always a complete, valid CSV of every run that finished — even if
    the process is killed, errors out, or you Ctrl-C it partway.  When the
    requested attempt cap is reached the loop ends and the file is closed
    normally with all metrics saved.

    Long/tidy format (one run per row): ready for groupby-by-mode aggregation,
    Wilson intervals on the `win` column, and a cost-vs-success scatter.
    """
    import os, csv, time
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    if modes is None:
        modes = ["avoidant", "sim_only", "popperian", "astar", "random", "mcts"]

    # reproducible seed set: the first n_attempts of the fixed benchmark_seeds
    # array (or a caller-supplied list).  using the shared constant guarantees
    # any other script that seeds the same generator reproduces these mazes.
    if seeds is None:
        if n_attempts > len(BENCHMARK_SEEDS):
            raise ValueError(
                f"requested {n_attempts} attempts but only "
                f"{len(BENCHMARK_SEEDS)} seeds are defined in BENCHMARK_SEEDS")
        seeds = BENCHMARK_SEEDS[:n_attempts]

    fields = ["seed", "mode", "outcome", "win", "death", "timeout",
              "ticks", "decisions", "path_tiles", "optimal_tiles", "path_ratio",
              "sim_steps", "sims_run", "sims_skipped", "reuse_pct",
              "rules", "valid_rules", "think_ticks", "close_calls",
              "death_kind", "death_predictable", "wall_s"]

    total = len(seeds) * len(modes)
    done = 0
    t_all = time.time()
    fh = open(csv_path, "w", newline="", encoding="utf-8")

    # ── save-on-manual-close ────────────────────────────────────────────────
    # the per-run flush()+fsync() below already makes every completed run
    # durable the instant it finishes, so the csv is never lost.  but a plain
    # window/terminal close (sigterm/sighup, or the windows console ctrl_close)
    # kills python without running the `finally`, so the clean "finalised"
    # message and a final flush wouldn't fire.  translate those signals into a
    # normal exception so the `finally` runs and the file is flushed+closed
    # cleanly no matter how the process is asked to stop.
    import signal as _signal

    def _graceful_stop(signum, frame):
        # raising here unwinds into the try/finally, which flushes and closes.
        raise KeyboardInterrupt(f"signal {signum}")

    _prev_handlers = {}
    for _sig_name in ("SIGTERM", "SIGHUP", "SIGBREAK", "SIGINT"):
        _sig = getattr(_signal, _sig_name, None)
        if _sig is None:
            continue
        try:
            _prev_handlers[_sig] = _signal.signal(_sig, _graceful_stop)
        except (ValueError, OSError):
            # not on the main thread, or unsupported on this os — skip.
            pass

    try:
        wr = csv.DictWriter(fh, fieldnames=fields)
        wr.writeheader(); fh.flush()
        for mode in modes:
            for attempt, seed in enumerate(seeds, start=1):
                # seed before world generation so every mode faces an identical
                # maze for this seed.  a fresh game regenerates the world in
                # __init__ → new_game under this seed.
                random.seed(seed)
                g = Game(mode=mode, headless=True, max_ticks=ticks)
                t0 = time.time()
                try:
                    row = g.run_single_trial(ticks)
                except Exception as exc:
                    # never let one bad run abort the batch; log it and move on.
                    row = dict(mode=mode, outcome=f"error:{type(exc).__name__}",
                               win=0, death=0, timeout=0, ticks=0)
                finally:
                    try:
                        pygame.quit()
                    except Exception:
                        pass
                row["seed"] = seed
                row["wall_s"] = round(time.time() - t0, 2)
                # write+flush+fsync as one unit so a stop between writerow and
                # flush can't leave a half-written final row on disk.
                wr.writerow({k: row.get(k, "") for k in fields})
                # durable after every single run
                fh.flush()
                os.fsync(fh.fileno())
                done += 1
                # on a death, append what killed the agent and whether that
                # hazard was predictable (a predictable death is one the forward
                # model should have foreseen; nondeterministic hazards are not).
                death_note = ""
                if row.get('outcome') == 'death':
                    dk = row.get('death_kind') or '?'
                    dp = row.get('death_predictable')
                    pred = ('predictable' if dp in (True, 'True')
                            else 'nondeterministic' if dp in (False, 'False')
                            else '?')
                    death_note = f" killed_by={dk} ({pred})"
                print(f"[{done:>4}/{total}] {mode:<11} attempt "
                      f"{attempt:>3}/{len(seeds)}  seed={seed:<7} "
                      f"{row.get('outcome',''):<10} ticks={row.get('ticks','')} "
                      f"sim_steps={row.get('sim_steps','')} "
                      f"({row['wall_s']}s){death_note}")
    except KeyboardInterrupt:
        # manual stop (ctrl-c, window/terminal close, or os sigterm): every
        # finished run is already saved; report and exit through `finally`.
        print(f"\n[interrupted] stopping early — {done}/{total} completed runs "
              f"already saved to {csv_path}")
    finally:
        # restore any signal handlers we replaced.
        for _sig, _hdlr in _prev_handlers.items():
            try:
                _signal.signal(_sig, _hdlr)
            except (ValueError, OSError):
                pass
        fh.flush()
        try:
            os.fsync(fh.fileno())
        except Exception:
            pass
        fh.close()
        print(f"\nCSV finalised: {done}/{total} runs saved → {csv_path}  "
              f"(elapsed {time.time()-t_all:.0f}s)")
    return csv_path


def run_benchmark(mode: str, ticks: int) -> dict:
    """Headless benchmark of one agent mode (feedback #2: comparison agents).

    Replicates the paper's Table-I methodology in the maze domain: the agent
    runs for a fixed world-time budget, auto-restarting on win/death, and we
    measure completions, deaths, expectation reuse, and deliberation time.
    """
    import os, time
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    g = Game(mode=mode, headless=True, max_ticks=ticks)
    g.agent_mode = True
    t0 = time.time()
    summary = g.run()
    summary['wall_s'] = round(time.time() - t0, 1)
    # per-decision trace → csv (feedback #4: how the agent solves the room)
    try:
        import csv
        fname = f"solve_trace_{mode}.csv"
        with open(fname, "w", newline="", encoding="utf-8") as fh:
            wr = csv.writer(fh)
            wr.writerow(["tick", "mode", "tile_x", "tile_y", "dx", "dy",
                         "source", "sims_used", "plan_latency", "mem_rules",
                         "rule"])
            for d in g.trace:
                wr.writerow([d['tick'], d['mode'], d['tile'][0], d['tile'][1],
                             d['action'][0], d['action'][1], d['source'],
                             d['sims_used'], d['plan_latency'], d['mem_rules'],
                             d['rule']])
        summary['trace_file'] = fname
    except Exception as exc:
        summary['trace_file'] = f"(trace write failed: {exc})"
    pygame.quit()
    return summary


def print_benchmark_table(results: list) -> None:
    hdr = (f"{'agent':<12}{'ticks':>8}{'wins':>6}{'deaths':>8}{'rules':>7}"
           f"{'laws':>6}{'sims':>8}{'reused':>8}{'reuse%':>8}{'dyn':>7}"
           f"{'think':>7}{'wall s':>8}")
    print("\n" + hdr)
    print("-" * len(hdr))
    for r in results:
        print(f"{r['mode']:<12}{r['ticks']:>8}{r['completions']:>6}"
              f"{r['deaths']:>8}{r['rules']:>7}{r['laws']:>6}"
              f"{r['sims_run']:>8}{r['sims_skipped']:>8}"
              f"{r['reuse_pct']:>7.1f}%{r['dyn_answers']:>7}"
              f"{r['think_ticks']:>7}{r['wall_s']:>8}")
    print()
    # ── death-cause diagnostic ───────────────────────────────────────────
    # predictable deaths = the forward model failed to foresee a knowable
    # collision (a simulation/planning bug).  unpredictable = roamer/stochastic
    # trap, which can be a legitimate loss.
    any_pred = any(r.get('deaths_predictable', 0) for r in results)
    print("death cause (predictable death => simulation bug):")
    for r in results:
        pred = r.get('deaths_predictable', 0)
        unpred = r.get('deaths_unpredictable', 0)
        flag = "  <-- BUG: died to predictable hazard" if pred else ""
        print(f"  {r['mode']:<12} predictable={pred:<3} "
              f"unpredictable={unpred:<3}{flag}")
        by_kind = r.get('death_by_kind', {})
        if by_kind:
            parts = ", ".join(f"{k}:{v}" for k, v in sorted(
                by_kind.items(), key=lambda kv: -kv[1]))
            print(f"               by kind: {parts}")
    if not any_pred:
        print("  (no predictable-hazard deaths — sim behaving correctly)")
    print()


if __name__=="__main__":
    _VALID_MODES = ["avoidant", "sim_only", "popperian", "astar", "random", "mcts"]
    # convenience aliases so "pe" maps onto the full mode name.
    _MODE_ALIASES = {"pe": "popperian", "popper": "popperian",
                     "a*": "astar", "astar_search": "astar",
                     "rand": "random", "random_walk": "random",
                     "uct": "mcts", "monte_carlo": "mcts"}

    _args = sys.argv[1:]
    if _args and _args[0] == "--compare":
        # usage:
        # python <file>.py --compare [mode|all] [n_attempts] [ticks] [csv]
        #
        # runs `n_attempts` reproducible seeds (the first n of benchmark_seeds)
        # for the chosen mode (or every mode if 'all'), one csv row per run,
        # flushed+fsynced after each run so the file is always complete even
        # if the process is interrupted partway.
        #
        # defaults: mode=popperian, n_attempts=500, ticks=9000,
        # csv=<mode>_comparison.csv (or maze_comparison.csv for all)
        #
        # examples:
        # python <file>.py --compare popperian 500     # 500 pe runs
        # python <file>.py --compare all 500           # all modes ×500
        # python <file>.py --compare popperian 500 9000 pe500.csv
        _mode  = _MODE_ALIASES.get(_args[1], _args[1]) if len(_args) > 1 else "popperian"
        _n     = int(_args[2]) if len(_args) > 2 else 500
        _ticks = int(_args[3]) if len(_args) > 3 else 9000
        # default output directory for the comparison csv.  an explicit 5th
        # cli argument (a full path or bare filename) overrides this.  falls
        # back to the current working directory if the folder does not exist
        # (e.g. when run on a different machine).
        _OUT_DIR = r"C:/Users/kper2/Downloads"
        if not os.path.isdir(_OUT_DIR):
            _OUT_DIR = os.getcwd()
        if len(_args) > 4:
            _csv = _args[4]
            # a bare filename (no directory part) still goes to _out_dir.
            if not os.path.dirname(_csv):
                _csv = os.path.join(_OUT_DIR, _csv)
        else:
            _name = ("maze_comparison.csv" if _mode == "all"
                     else f"{_mode}_comparison.csv")
            _csv = os.path.join(_OUT_DIR, _name)
        if _mode == "all":
            _modes = _VALID_MODES
        elif _mode in _VALID_MODES:
            _modes = [_mode]
        else:
            print(f"unknown mode {_mode!r}; choose one of: "
                  f"{', '.join(_VALID_MODES)}, or 'all'")
            sys.exit(1)
        if _n > len(BENCHMARK_SEEDS):
            print(f"only {len(BENCHMARK_SEEDS)} seeds defined; capping "
                  f"attempts at {len(BENCHMARK_SEEDS)}")
            _n = len(BENCHMARK_SEEDS)
        print(f"comparison: {_n} attempts × {len(_modes)} mode(s) "
              f"= {_n*len(_modes)} runs, {_ticks} ticks each → {_csv}")
        print(f"seeds: first {_n} of BENCHMARK_SEEDS "
              f"({BENCHMARK_SEEDS[0]}…{BENCHMARK_SEEDS[_n-1]})")
        run_paired_benchmark(_n, _ticks, modes=_modes, csv_path=_csv)
    elif _args and _args[0] == "--bench":
        # usage: python maze_pe_causal_v2.py --bench [mode|all] [ticks]
        # modes: popperian | sim_only | avoidant | astar | random | mcts | all
        _mode  = _args[1] if len(_args) > 1 else "all"
        _mode  = _MODE_ALIASES.get(_mode, _mode)
        _ticks = int(_args[2]) if len(_args) > 2 else 9000
        _modes = (["avoidant", "sim_only", "popperian", "astar", "random", "mcts"]
                  if _mode == "all" else [_mode])
        _results = []
        for _m in _modes:
            print(f"benchmarking {_m} for {_ticks} ticks…")
            _results.append(run_benchmark(_m, _ticks))
        print_benchmark_table(_results)
        for _r in _results:
            print(f"  trace: {_r.get('trace_file')}")
    else:
        Game().run()
