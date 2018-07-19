from atari_irl import utils, policies
import pickle
from arguments import add_atari_args, add_trajectory_args, add_expert_args, tf_context_for_args, env_context_for_args
import argparse


def generate_trajectories(args):
    utils.logger.configure()
    with tf_context_for_args(args):
        with env_context_for_args(args) as context:
            policy = policies.EnvPolicy.load(args.expert_path, context.environments)
            ts = policies.sample_trajectories(
                model=policy.model,
                environments=policy.envs,
                n_trajectories=args.num_trajectories,
                one_hot_code=args.one_hot_code,
                render=args.render
            )

    pickle.dump(ts, open(args.trajectories_file, 'wb'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    add_atari_args(parser)
    add_expert_args(parser)
    add_trajectory_args(parser)

    args = parser.parse_args()
    generate_trajectories(args)