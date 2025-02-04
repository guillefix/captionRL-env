from src.envs.envList import *
import numpy as np
import pybullet as p
import pickle as pk

def add_xyz_rpy_controls(env):
    controls = []
    orn = env.instance.default_arm_orn_RPY
    controls.append(env.p.addUserDebugParameter("X", -1, 1, 0))
    controls.append(env.p.addUserDebugParameter("Y", -1, 1, 0.00))
    controls.append(env.p.addUserDebugParameter("Z", -1, 1, 0.2))
    controls.append(env.p.addUserDebugParameter("R", -4, 4, orn[0]))
    controls.append(env.p.addUserDebugParameter("P", -4, 4, orn[1]))
    controls.append(env.p.addUserDebugParameter("Y", -4,4, orn[2]))
    controls.append(env.p.addUserDebugParameter("grip", env.action_space.low[-1], env.action_space.high[-1], 0))
    return controls

def add_joint_controls(env):
    for i, obj in enumerate(env.instance.restJointPositions):
        env.p.addUserDebugParameter(str(i), -2*np.pi, 2*np.pi, obj)


joint_control = False # Toggle this flag to control joints or ABS RPY Space
def main():
    
    env = UR5PlayAbsRPY1Obj()

    from src.envs.descriptions import generate_all_descriptions
    from src.envs.env_params import get_env_params
    env_params = get_env_params()
    all_descriptions = generate_all_descriptions(env_params)[2]
    for _ in range(1000):
        while True:
            d = np.random.choice(all_descriptions)
            if d.lower().split()[0] not in ['turn', 'open', 'close', 'make']:
                break
        print(d)
        env.render(mode='human')
        env.reset(description=d,)

        print([o for o in env.instance.objects])
        if joint_control:
            add_joint_controls(env)
        else:
            controls = add_xyz_rpy_controls(env)

        for i in range(1000000):

            if joint_control:
                poses  = []
                for i in range(len(env.instance.restJointPositions)):
                    poses.append(env.p.readUserDebugParameter(i))
                # Uses a hard reset of the arm joints so that we can quickly debug without worrying about forces
                env.instance.reset_arm_joints(env.instance.arm, poses)

            else:
                action = []
                for control in controls:
                    action.append(env.p.readUserDebugParameter(control))

                state = env.instance.calc_actor_state()
                obs, r, done, info = env.step(np.array(action))


if __name__ == "__main__":
    main()
