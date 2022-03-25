# TDW BCS Demo

BCS demo of [ThreeDWorld (TDW)](https://github.com/threedworld-mit/tdw)

## Requirements

- A stable Internet connection
- Python 3.6+
- Git

## Setup

1. **Install TDW** `pip3 install tdw` On OS X and Linux, you may need to `sudo pip3 install tdw` On Windows, you may need to `pip3 install tdw --user`
2. **Clone this repo** `git clone https://github.com/alters-mit/tdw_bcs_demo.git`
3. **Change directory to this repo** `cd tdw_bcs_demo`

## Run a controller

To run one of the controllers, `cd tdw_bcs_demo` and `python3 CONTROLLER`

OS X and Linux:

```bash
python3 hello_world.py
```

Windows:

```bash
py -3 hello_world.py
```

## List of controllers

| Controller | Goal |
| --- | --- |
| `hello_world.py` | Print "hello world". |
| `tdw_room.py` | Position the camera so that you can see the box. |
| `use_the_force.py` | Apply a force to a ball in order to knock objects off the table. |
| `use_the_brute_force.py` | Use an automated brute-force method to find a solution to the `UseTheForce` demo. |