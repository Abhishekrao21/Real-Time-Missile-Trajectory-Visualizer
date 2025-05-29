# filepath: /project/test.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# Simulation parameters
mass = 1.0  # mass of missile (kg)
# Initial state
pos = np.array([0.0, 0.0])  # x, y
vel = np.array([50.0, 50.0])  # initial velocity (m/s)

# physical parameters
g = 9.81  # gravity 
drag_coeff = 0.02  # drag coefficient
thrust_mag = 0.0  # thrust magnitude (N)

# Time parameters
dt = 0.02  # time step (s)
t_max = 20.0  # total simulation time (s)

# Prepare figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, 300)
ax.set_ylim(0, 150)
ax.set_xlabel('X distance (m)')
ax.set_ylabel('Y height (m)')
ax.set_title('Real-Time Missile Trajectory Visualizer')

# Sliders for parameters
axcolor = 'lightgoldenrodyellow'
ax_drag = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_thrust = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_gravity = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

s_drag = Slider(ax_drag, 'Drag Coeff', 0.0, 0.1, valinit=drag_coeff)
s_thrust = Slider(ax_thrust, 'Thrust (N)', 0.0, 200.0, valinit=thrust_mag)
s_gravity = Slider(ax_gravity, 'Gravity', 0.1, 20.0, valinit=g)

# Button to reset simulation
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
b_reset = Button(ax_reset, 'Reset', color=axcolor, hovercolor='0.975')

# State history
xs, ys = [], []

# Initialize simulation state
state = {
    'pos': pos.copy(),
    'vel': vel.copy(),
    't': 0.0
}

# Integration and update function
def compute_acceleration(v):
    # Gravity acceleration
    gravity_acc = np.array([0.0, -s_gravity.val])
    # Drag acceleration (opposite velocity)
    speed = np.linalg.norm(v)
    if speed > 0:
        drag_acc = -s_drag.val * speed * v / mass
    else:
        drag_acc = np.zeros(2)
    # Thrust acceleration (along velocity direction)
    if speed > 0:
        thrust_acc = (s_thrust.val / mass) * (v / speed)
    else:
        thrust_acc = np.zeros(2)
    return gravity_acc + drag_acc + thrust_acc


def init():
    line.set_data([], [])
    return line,


def update(frame):
    # Update state by simple Euler integration
    a = compute_acceleration(state['vel'])
    state['vel'] += a * dt
    state['pos'] += state['vel'] * dt
    state['t'] += dt

    # Append to history
    xs.append(state['pos'][0])
    ys.append(state['pos'][1])

    # Stop if missile hits ground or exceeds time
    if state['pos'][1] < 0 or state['t'] >= t_max:
        anim.event_source.stop()

    line.set_data(xs, ys)
    return line,

# Reset function
def reset(event):
    global xs, ys
    xs, ys = [], []
    state['pos'] = pos.copy()
    state['vel'] = vel.copy()
    state['t'] = 0.0
    line.set_data([], [])
    anim.event_source.start()

b_reset.on_clicked(reset)

# Run animation
anim = FuncAnimation(fig, update, frames=int(t_max/dt), init_func=init,
                     blit=True, interval=dt*1000, repeat=False)

plt.show()


