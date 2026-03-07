"""Generate docs/assets/network-map-demo.svg from hardcoded mock data.

Run with:
    uv run python scripts/gen_demo_svg.py

Topology (37 devices, 5 hop rings) is designed to exercise every visual feature:
  - Good links  (LQI >= 80):   most router-to-router links (198, 172, 173, 148, etc.)
  - Warn glow   (LQI < 80):    several battery/distant devices (75, 70, 66, 46, 69, 99)
  - Crit glow   (LQI < 30):    TRADFRI Outlet and Hall Button (LQI 0 — dead/unreachable)
  - 5 hop rings for realistic home-network depth
"""

from pathlib import Path

from zigporter.commands.network_map_svg import render_svg

# ── IEEEs ─────────────────────────────────────────────────────────────────────

COORD = "0x0000000000000000"

# Hop 1 — direct coordinator children
LIVING_PLUG = "0xaabbccddeeff0001"
KITCHEN_PLUG = "0xaabbccddeeff0002"
HALL_DOOR_PLUG = "0xaabbccddeeff0003"
IKEA_OUTLET = "0xaabbccddeeff0004"
HALL_SMOKE = "0xaabbccddeeff0005"
HALL_CLIMATE = "0xaabbccddeeff0006"
MASTER_CLIMATE = "0xaabbccddeeff0007"
TRADFRI_OUTLET = "0xaabbccddeeff0008"
HALL_BUTTON = "0xaabbccddeeff0009"

# Hop 2 — children of Living Room Plug
UPSTAIRS_PLUG = "0xaabbccddeeff0010"
HALL_YALE_PLUG = "0xaabbccddeeff0011"
OFFICE_CLIMATE = "0xaabbccddeeff0012"
BEDROOM_PLUG = "0xaabbccddeeff0013"
LIVING_CLIMATE = "0xaabbccddeeff0014"

# Hop 2 — children of Kitchen Plug
EMIL_PLUG = "0xaabbccddeeff0020"
LINUS_CLIMATE = "0xaabbccddeeff0021"
HALL_MOTION = "0xaabbccddeeff0022"
ATTIC_CLIMATE = "0xaabbccddeeff0023"
OUTSIDE_WOODSHED = "0xaabbccddeeff0024"
EMIL_DOOR_PLUG = "0xaabbccddeeff0025"
COFFEE_PLUG = "0xaabbccddeeff0026"

# Hop 2 — children of Hall Door Plug
SMLIGHT = "0xaabbccddeeff0030"
DOWNSTAIRS_TOILET = "0xaabbccddeeff0031"
LEGO_LIGHTS = "0xaabbccddeeff0032"

# Hop 2 — children of IKEA Outlet
DOWNSTAIRS_LEFT = "0xaabbccddeeff0040"
LIVING_SMOKE = "0xaabbccddeeff0041"

# Hop 3 — children of Upstairs Stairs Plug
OFFICE_SOFFA = "0xaabbccddeeff0050"

# Hop 3 — children of Hall Yale Plug
HALL_COATROOM = "0xaabbccddeeff0051"

# Hop 3 — children of SMLIGHT Repeater
GARAGE_SMART = "0xaabbccddeeff0052"
FERROAMP_PLUG = "0xaabbccddeeff0053"
OUTSIDE_FRONT = "0xaabbccddeeff0054"

# Hop 3 — children of Downstairs Left Plug
DOWNSTAIRS_RIGHT = "0xaabbccddeeff0055"

# Hop 4 — children of Hall Coatroom Light
STORAGE_HEATER = "0xaabbccddeeff0060"

# Hop 4 — children of Garage Smart Plug
GARAGE_CENTER = "0xaabbccddeeff0061"
GARAGE_CLIMATE = "0xaabbccddeeff0062"

# Hop 4 — children of Ferroamp Plug
BILLADDER_PLUG = "0xaabbccddeeff0063"

# Hop 4 — children of Downstairs Right Plug
OUTSIDE_ROBBAN = "0xaabbccddeeff0064"
LIVING_ROOM_CLIMATE2 = "0xaabbccddeeff0065"

# Hop 5 — children of Storage Heater Plug
STORAGE_CLIMATE = "0xaabbccddeeff0070"

# Hop 5 — children of Billadder Plug
ROOM_CLIMATE = "0xaabbccddeeff0071"

# ── Topology ──────────────────────────────────────────────────────────────────
#
# Coordinator                                              hop 0
# ├── Living Room Plug       router  hop 1  LQI 198
# │    ├── Upstairs Stairs Plug  router  hop 2  LQI 198
# │    │    └── Office Soffa Plug       router  hop 3  LQI 121
# │    ├── Hall Yale Plug         router  hop 2  LQI 172
# │    │    └── Hall Coatroom Light     router  hop 3  LQI 172
# │    │         └── Storage Heater Plug  router  hop 4  LQI 46  WEAK
# │    │              └── Storage Climate  end   hop 5  LQI 46  WEAK
# │    ├── Office Climate         end     hop 2  LQI 198
# │    ├── Bedroom Plug            router  hop 2  LQI 173
# │    └── Living Room Climate    end     hop 2  LQI 129
# ├── Kitchen Plug           router  hop 1  LQI 148
# │    ├── Emil Plug              end     hop 2  LQI 75  WEAK
# │    ├── Linus Climate          end     hop 2  LQI 75  WEAK
# │    ├── Hall Motion            end     hop 2  LQI 75  WEAK
# │    ├── Attic Climate          end     hop 2  LQI 75  WEAK
# │    ├── Outside Woodshed Plug  end     hop 2  LQI 75  WEAK
# │    ├── Emil Door Plug         end     hop 2  LQI 75  WEAK
# │    └── Coffee Plug            end     hop 2  LQI 75  WEAK
# ├── Hall Door Plug         router  hop 1  LQI 133
# │    ├── SMLIGHT Repeater       router  hop 2  LQI 99  WEAK
# │    │    ├── Garage Smart Plug    router  hop 3  LQI 112
# │    │    │    ├── Garage Center Plug  end  hop 4  LQI 184
# │    │    │    └── Garage Climate      end  hop 4  LQI 70  WEAK
# │    │    ├── Ferroamp Plug          router  hop 3  LQI 136
# │    │    │    └── Billadder Plug   router  hop 4  LQI 66  WEAK
# │    │    │         └── Room Climate   end  hop 5  LQI 66  WEAK
# │    │    └── Outside Front Climate  end   hop 3  LQI 69  WEAK
# │    ├── Downstairs Toilet Cli  end   hop 2  LQI 115
# │    └── Lego Car Lights        end   hop 2  LQI 70  WEAK
# ├── IKEA Outlet            router  hop 1  LQI 115
# │    ├── Downstairs Left Plug   router  hop 2  LQI 115
# │    │    └── Downstairs Right Plug  router  hop 3  LQI 115
# │    │         ├── Outside Robban Plug  end  hop 4  LQI 115
# │    │         └── Living Room Climate  end  hop 4  LQI 115
# │    └── Living Room Smoke      end   hop 2  LQI 115
# ├── Hall Smoke              end     hop 1  LQI 101
# ├── Hall Climate            end     hop 1  LQI 100
# ├── Master Bedroom Climate  end     hop 1  LQI 122
# ├── TRADFRI Outlet         end     hop 1  LQI 0   CRITICAL
# └── Hall Button            end     hop 1  LQI 0   CRITICAL

nodes = {
    COORD: {"friendlyName": "Coordinator", "type": "Coordinator"},
    # hop 1
    LIVING_PLUG: {"friendlyName": "Living Room Plug", "type": "Router"},
    KITCHEN_PLUG: {"friendlyName": "Kitchen Plug", "type": "Router"},
    HALL_DOOR_PLUG: {"friendlyName": "Hall Door Plug", "type": "Router"},
    IKEA_OUTLET: {"friendlyName": "IKEA Outlet", "type": "Router"},
    HALL_SMOKE: {"friendlyName": "Hall Smoke", "type": "EndDevice"},
    HALL_CLIMATE: {"friendlyName": "Hall Climate", "type": "EndDevice"},
    MASTER_CLIMATE: {"friendlyName": "Master Bedroom Climate", "type": "EndDevice"},
    TRADFRI_OUTLET: {"friendlyName": "TRADFRI Outlet", "type": "EndDevice"},
    HALL_BUTTON: {"friendlyName": "Hall Button", "type": "EndDevice"},
    # hop 2 — Living Room Plug children
    UPSTAIRS_PLUG: {"friendlyName": "Upstairs Stairs Plug", "type": "Router"},
    HALL_YALE_PLUG: {"friendlyName": "Hall Yale Plug", "type": "Router"},
    OFFICE_CLIMATE: {"friendlyName": "Office Climate", "type": "EndDevice"},
    BEDROOM_PLUG: {"friendlyName": "Bedroom Plug", "type": "Router"},
    LIVING_CLIMATE: {"friendlyName": "Living Room Climate", "type": "EndDevice"},
    # hop 2 — Kitchen Plug children
    EMIL_PLUG: {"friendlyName": "Emil Plug", "type": "EndDevice"},
    LINUS_CLIMATE: {"friendlyName": "Linus Climate", "type": "EndDevice"},
    HALL_MOTION: {"friendlyName": "Hall Motion", "type": "EndDevice"},
    ATTIC_CLIMATE: {"friendlyName": "Attic Climate", "type": "EndDevice"},
    OUTSIDE_WOODSHED: {"friendlyName": "Outside Woodshed Plug", "type": "EndDevice"},
    EMIL_DOOR_PLUG: {"friendlyName": "Emil Door Plug", "type": "EndDevice"},
    COFFEE_PLUG: {"friendlyName": "Coffee Plug", "type": "EndDevice"},
    # hop 2 — Hall Door Plug children
    SMLIGHT: {"friendlyName": "SMLIGHT Repeater", "type": "Router"},
    DOWNSTAIRS_TOILET: {"friendlyName": "Downstairs Toilet Cli", "type": "EndDevice"},
    LEGO_LIGHTS: {"friendlyName": "Lego Car Lights", "type": "EndDevice"},
    # hop 2 — IKEA Outlet children
    DOWNSTAIRS_LEFT: {"friendlyName": "Downstairs Left Plug", "type": "Router"},
    LIVING_SMOKE: {"friendlyName": "Living Room Smoke", "type": "EndDevice"},
    # hop 3
    OFFICE_SOFFA: {"friendlyName": "Office Soffa Plug", "type": "Router"},
    HALL_COATROOM: {"friendlyName": "Hall Coatroom Light", "type": "Router"},
    GARAGE_SMART: {"friendlyName": "Garage Smart Plug", "type": "Router"},
    FERROAMP_PLUG: {"friendlyName": "Ferroamp Plug", "type": "Router"},
    OUTSIDE_FRONT: {"friendlyName": "Outside Front Climate", "type": "EndDevice"},
    DOWNSTAIRS_RIGHT: {"friendlyName": "Downstairs Right Plug", "type": "Router"},
    # hop 4
    STORAGE_HEATER: {"friendlyName": "Storage Heater Plug", "type": "Router"},
    GARAGE_CENTER: {"friendlyName": "Garage Center Plug", "type": "EndDevice"},
    GARAGE_CLIMATE: {"friendlyName": "Garage Climate", "type": "EndDevice"},
    BILLADDER_PLUG: {"friendlyName": "Billadder Plug", "type": "Router"},
    OUTSIDE_ROBBAN: {"friendlyName": "Outside Robban Plug", "type": "EndDevice"},
    LIVING_ROOM_CLIMATE2: {"friendlyName": "Living Room Climate 2", "type": "EndDevice"},
    # hop 5
    STORAGE_CLIMATE: {"friendlyName": "Storage Climate", "type": "EndDevice"},
    ROOM_CLIMATE: {"friendlyName": "Room Climate", "type": "EndDevice"},
}

parent_map: dict[str, str | None] = {
    COORD: None,
    # hop 1
    LIVING_PLUG: COORD,
    KITCHEN_PLUG: COORD,
    HALL_DOOR_PLUG: COORD,
    IKEA_OUTLET: COORD,
    HALL_SMOKE: COORD,
    HALL_CLIMATE: COORD,
    MASTER_CLIMATE: COORD,
    TRADFRI_OUTLET: COORD,
    HALL_BUTTON: COORD,
    # hop 2
    UPSTAIRS_PLUG: LIVING_PLUG,
    HALL_YALE_PLUG: LIVING_PLUG,
    OFFICE_CLIMATE: LIVING_PLUG,
    BEDROOM_PLUG: LIVING_PLUG,
    LIVING_CLIMATE: LIVING_PLUG,
    EMIL_PLUG: KITCHEN_PLUG,
    LINUS_CLIMATE: KITCHEN_PLUG,
    HALL_MOTION: KITCHEN_PLUG,
    ATTIC_CLIMATE: KITCHEN_PLUG,
    OUTSIDE_WOODSHED: KITCHEN_PLUG,
    EMIL_DOOR_PLUG: KITCHEN_PLUG,
    COFFEE_PLUG: KITCHEN_PLUG,
    SMLIGHT: HALL_DOOR_PLUG,
    DOWNSTAIRS_TOILET: HALL_DOOR_PLUG,
    LEGO_LIGHTS: HALL_DOOR_PLUG,
    DOWNSTAIRS_LEFT: IKEA_OUTLET,
    LIVING_SMOKE: IKEA_OUTLET,
    # hop 3
    OFFICE_SOFFA: UPSTAIRS_PLUG,
    HALL_COATROOM: HALL_YALE_PLUG,
    GARAGE_SMART: SMLIGHT,
    FERROAMP_PLUG: SMLIGHT,
    OUTSIDE_FRONT: SMLIGHT,
    DOWNSTAIRS_RIGHT: DOWNSTAIRS_LEFT,
    # hop 4
    STORAGE_HEATER: HALL_COATROOM,
    GARAGE_CENTER: GARAGE_SMART,
    GARAGE_CLIMATE: GARAGE_SMART,
    BILLADDER_PLUG: FERROAMP_PLUG,
    OUTSIDE_ROBBAN: DOWNSTAIRS_RIGHT,
    LIVING_ROOM_CLIMATE2: DOWNSTAIRS_RIGHT,
    # hop 5
    STORAGE_CLIMATE: STORAGE_HEATER,
    ROOM_CLIMATE: BILLADDER_PLUG,
}

lqi_map: dict[str, int] = {
    COORD: 255,
    # hop 1
    LIVING_PLUG: 198,
    KITCHEN_PLUG: 148,
    HALL_DOOR_PLUG: 133,
    IKEA_OUTLET: 115,
    HALL_SMOKE: 101,
    HALL_CLIMATE: 100,
    MASTER_CLIMATE: 122,
    TRADFRI_OUTLET: 0,  # CRITICAL
    HALL_BUTTON: 0,  # CRITICAL
    # hop 2 — Living Room Plug branch
    UPSTAIRS_PLUG: 198,
    HALL_YALE_PLUG: 172,
    OFFICE_CLIMATE: 198,
    BEDROOM_PLUG: 173,
    LIVING_CLIMATE: 129,
    # hop 2 — Kitchen Plug branch (all weak — battery devices far from router)
    EMIL_PLUG: 75,  # WEAK
    LINUS_CLIMATE: 75,  # WEAK
    HALL_MOTION: 75,  # WEAK
    ATTIC_CLIMATE: 75,  # WEAK
    OUTSIDE_WOODSHED: 75,  # WEAK
    EMIL_DOOR_PLUG: 75,  # WEAK
    COFFEE_PLUG: 75,  # WEAK
    # hop 2 — Hall Door Plug branch
    SMLIGHT: 99,  # WEAK
    DOWNSTAIRS_TOILET: 115,
    LEGO_LIGHTS: 70,  # WEAK
    # hop 2 — IKEA Outlet branch
    DOWNSTAIRS_LEFT: 115,
    LIVING_SMOKE: 115,
    # hop 3
    OFFICE_SOFFA: 121,
    HALL_COATROOM: 172,
    GARAGE_SMART: 112,
    FERROAMP_PLUG: 136,
    OUTSIDE_FRONT: 69,  # WEAK
    DOWNSTAIRS_RIGHT: 115,
    # hop 4
    STORAGE_HEATER: 46,  # WEAK
    GARAGE_CENTER: 184,
    GARAGE_CLIMATE: 70,  # WEAK
    BILLADDER_PLUG: 66,  # WEAK
    OUTSIDE_ROBBAN: 115,
    LIVING_ROOM_CLIMATE2: 115,
    # hop 5
    STORAGE_CLIMATE: 46,  # WEAK
    ROOM_CLIMATE: 66,  # WEAK
}

depth_map: dict[str, int] = {
    COORD: 0,
    # hop 1
    LIVING_PLUG: 1,
    KITCHEN_PLUG: 1,
    HALL_DOOR_PLUG: 1,
    IKEA_OUTLET: 1,
    HALL_SMOKE: 1,
    HALL_CLIMATE: 1,
    MASTER_CLIMATE: 1,
    TRADFRI_OUTLET: 1,
    HALL_BUTTON: 1,
    # hop 2
    UPSTAIRS_PLUG: 2,
    HALL_YALE_PLUG: 2,
    OFFICE_CLIMATE: 2,
    BEDROOM_PLUG: 2,
    LIVING_CLIMATE: 2,
    EMIL_PLUG: 2,
    LINUS_CLIMATE: 2,
    HALL_MOTION: 2,
    ATTIC_CLIMATE: 2,
    OUTSIDE_WOODSHED: 2,
    EMIL_DOOR_PLUG: 2,
    COFFEE_PLUG: 2,
    SMLIGHT: 2,
    DOWNSTAIRS_TOILET: 2,
    LEGO_LIGHTS: 2,
    DOWNSTAIRS_LEFT: 2,
    LIVING_SMOKE: 2,
    # hop 3
    OFFICE_SOFFA: 3,
    HALL_COATROOM: 3,
    GARAGE_SMART: 3,
    FERROAMP_PLUG: 3,
    OUTSIDE_FRONT: 3,
    DOWNSTAIRS_RIGHT: 3,
    # hop 4
    STORAGE_HEATER: 4,
    GARAGE_CENTER: 4,
    GARAGE_CLIMATE: 4,
    BILLADDER_PLUG: 4,
    OUTSIDE_ROBBAN: 4,
    LIVING_ROOM_CLIMATE2: 4,
    # hop 5
    STORAGE_CLIMATE: 5,
    ROOM_CLIMATE: 5,
}

children: dict[str, list[str]] = {
    COORD: [
        LIVING_PLUG,
        KITCHEN_PLUG,
        HALL_DOOR_PLUG,
        IKEA_OUTLET,
        HALL_SMOKE,
        HALL_CLIMATE,
        MASTER_CLIMATE,
        TRADFRI_OUTLET,
        HALL_BUTTON,
    ],
    # hop 1
    LIVING_PLUG: [UPSTAIRS_PLUG, HALL_YALE_PLUG, OFFICE_CLIMATE, BEDROOM_PLUG, LIVING_CLIMATE],
    KITCHEN_PLUG: [
        EMIL_PLUG,
        LINUS_CLIMATE,
        HALL_MOTION,
        ATTIC_CLIMATE,
        OUTSIDE_WOODSHED,
        EMIL_DOOR_PLUG,
        COFFEE_PLUG,
    ],
    HALL_DOOR_PLUG: [SMLIGHT, DOWNSTAIRS_TOILET, LEGO_LIGHTS],
    IKEA_OUTLET: [DOWNSTAIRS_LEFT, LIVING_SMOKE],
    HALL_SMOKE: [],
    HALL_CLIMATE: [],
    MASTER_CLIMATE: [],
    TRADFRI_OUTLET: [],
    HALL_BUTTON: [],
    # hop 2
    UPSTAIRS_PLUG: [OFFICE_SOFFA],
    HALL_YALE_PLUG: [HALL_COATROOM],
    OFFICE_CLIMATE: [],
    BEDROOM_PLUG: [],
    LIVING_CLIMATE: [],
    EMIL_PLUG: [],
    LINUS_CLIMATE: [],
    HALL_MOTION: [],
    ATTIC_CLIMATE: [],
    OUTSIDE_WOODSHED: [],
    EMIL_DOOR_PLUG: [],
    COFFEE_PLUG: [],
    SMLIGHT: [GARAGE_SMART, FERROAMP_PLUG, OUTSIDE_FRONT],
    DOWNSTAIRS_TOILET: [],
    LEGO_LIGHTS: [],
    DOWNSTAIRS_LEFT: [DOWNSTAIRS_RIGHT],
    LIVING_SMOKE: [],
    # hop 3
    OFFICE_SOFFA: [],
    HALL_COATROOM: [STORAGE_HEATER],
    GARAGE_SMART: [GARAGE_CENTER, GARAGE_CLIMATE],
    FERROAMP_PLUG: [BILLADDER_PLUG],
    OUTSIDE_FRONT: [],
    DOWNSTAIRS_RIGHT: [OUTSIDE_ROBBAN, LIVING_ROOM_CLIMATE2],
    # hop 4
    STORAGE_HEATER: [STORAGE_CLIMATE],
    GARAGE_CENTER: [],
    GARAGE_CLIMATE: [],
    BILLADDER_PLUG: [ROOM_CLIMATE],
    OUTSIDE_ROBBAN: [],
    LIVING_ROOM_CLIMATE2: [],
    # hop 5
    STORAGE_CLIMATE: [],
    ROOM_CLIMATE: [],
}

output_path = Path("docs/assets/network-map-demo.svg")
output_path.parent.mkdir(parents=True, exist_ok=True)

render_svg(
    nodes=nodes,
    parent_map=parent_map,
    lqi_map=lqi_map,
    depth_map=depth_map,
    children=children,
    output_path=output_path,
    warn_lqi=80,
    critical_lqi=30,
)

print(f"SVG written to {output_path}")
